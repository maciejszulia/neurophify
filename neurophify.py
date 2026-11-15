#!/usr/bin/env python3
"""neurophify: draw a knowledge graph as a 3D brain.

Reads a graphify graph.json (networkx node-link format) or a folder of Markdown
files, groups the nodes into regions and lays the regions out on the surface of
two brain hemispheres. Writes five files to the output folder:

  brain.html   interactive 3D view (3d-force-graph from jsDelivr, data embedded)
  brain.svg    static projection of the same scene
  brain.json   nodes with positions and regions, edges, regions
  REGIONS.md   regions, their central nodes, the bridges between regions, graph metrics
  CORE.md      consolidation: the 20 nodes with the largest weight (degree and recency)

Time is the fourth dimension: a node takes its first and last commit from the git
history of a Markdown folder (the file modification time outside git) or the
"time" field of graph.json. brain.html replays the growth on a time slider and
REGIONS.md marks each region growing, active or dormant.

Standard library only, Python 3.11 or newer.
"""
from __future__ import annotations

import argparse
import contextlib
import fnmatch
import html
import io
import json
import math
import os
import posixpath
import random
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from urllib.parse import unquote

VERSION = "1.3.0"
CDN = "https://cdn.jsdelivr.net/npm/3d-force-graph@1.80.1/dist/3d-force-graph.min.js"
MAX_REGIONS = 24          # legend entries, "other" included
TOP_LABELS = 10           # nodes with a permanent label
SEED, LPA_MAX_ITER = 42, 50
SPIN_FRAMES, SPIN_SECONDS = 24, 12   # brain-spin.svg: one turn in 12 s, drawn from 24 key frames
SPIN_PITCH = math.radians(20)        # the turning brain is seen 20 degrees from above
SPIN_EDGES = 120                     # brain-spin.svg: at most 120 edges inside regions, taken from each region in turn
STL_NODES = 40                       # brain.stl: a tetrahedron for each of the 40 nodes with the most edges
HEMI_U, HEMI_V = 12, 6               # brain.stl: hemisphere mesh, 12 steps around, 6 from pole to pole
HEMI_FACETS = 2 * HEMI_U * (HEMI_V - 1)
STL_SHELL = 0.92                     # brain.stl: the hemispheres shrink so the node markers stand out
CORE_SIZE = 20            # nodes in CORE.md
HALF_LIFE = 30            # days: a node loses half its weight per 30 days behind the newest change
PARAGRAPH_CHARS = 300     # longest first paragraph in CORE.md

# Brain geometry, in units of R. Each hemisphere is an ellipsoid with half-axes
# SEMI (x: width, y: height, z: length); the two centres sit at x = -SHIFT and +SHIFT.
R = 300.0
SEMI = (0.42, 0.56, 1.0)
SHIFT = 0.48
CAP_AXIS_Y = 0.25                   # nodes cover a cap around the outer side of each hemisphere
CAP_ANGLE = math.radians(140)       # and leave the medial wall, which faces the other hemisphere, empty
CAMERA = (0.0, 2.4, 1.2)            # view from above and in front, shared by brain.html and brain.svg
GOLDEN = math.pi * (3 - math.sqrt(5))

# Dark-surface categorical hues, 8 slots; regions 9-24 reuse them in two lighter steps.
# Identity does not rest on colour alone: the legend, the tooltip and the position
# of each region on the brain name it too.
BASE_COLORS = ("#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#0ca30c", "#9085e9", "#e66767")
OTHER_COLOR = "#6b7280"
BACKGROUND = "#05070b"
FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, 'DejaVu Sans', sans-serif"


def lighten(color, t):
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{round(c + (255 - c) * t):02x}" for c in (r, g, b))


PALETTE = [lighten(c, t) for t in (0.0, 0.35, 0.6) for c in BASE_COLORS]


class InputError(Exception):
    """A problem with the user's input. The message names the fix."""


def warn(msg):
    print(f"neurophify: {msg}", file=sys.stderr)


def clean(text):
    return " ".join(str(text).split())


# ---------------------------------------------------------------- input A: graph.json

def parse_time(value):
    """Epoch seconds from a number or an ISO 8601 date or datetime (no zone = local time); None if absent, invalid
    or outside the dates that REGIONS.md and CORE.md can print."""
    if value is None or isinstance(value, bool):
        return None
    try:
        t = int(value) if isinstance(value, (int, float)) else int(datetime.fromisoformat(str(value).strip()).timestamp())
        datetime.fromtimestamp(t)
        return t
    except (ValueError, OverflowError, OSError):
        return None


def load_graph_json(path):
    """Return (labels, edges, community or None, community names, {id: (first, last)}) from a node-link graph.json."""
    fix = "  fix: pass graphify-out/graph.json, or a folder of .md files"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise InputError(f"{path} is not valid JSON (line {e.lineno}, column {e.colno}: {e.msg})\n{fix}") from None
    except UnicodeDecodeError:
        raise InputError(f"{path} is not UTF-8 text\n{fix}") from None
    except OSError as e:
        raise InputError(f"cannot read {path}: {e.strerror}\n{fix}") from None
    nodes = data.get("nodes") if isinstance(data, dict) else None
    if not isinstance(nodes, list) or not nodes:
        raise InputError(f'{path} has no "nodes" list\n  fix: pass a graph.json written by graphify '
                         "(networkx node-link format)")
    links = data.get("links", data.get("edges")) or []
    labels, community, names, times, bad_times = {}, {}, {}, {}, 0
    for n in nodes:
        if not isinstance(n, dict) or "id" not in n:
            raise InputError(f'{path}: every node needs an "id" field, found {str(n)[:80]}')
        nid = str(n["id"])
        label = n.get("label")
        labels[nid] = clean(nid if label in (None, "") else label)
        if n.get("community") is not None:
            community[nid] = str(n["community"])
        if n.get("community_name"):
            names[nid] = clean(n["community_name"])
        t = parse_time(n.get("time"))
        if t is not None:
            times[nid] = (t, t)
        elif n.get("time") is not None:
            bad_times += 1
    if bad_times:
        warn(f'{bad_times} "time" values skipped: use ISO 8601 (2026-11-15T19:30) or epoch seconds')
    edges, skipped = set(), 0
    for e in links if isinstance(links, list) else []:
        a, b = (str(e.get("source")), str(e.get("target"))) if isinstance(e, dict) else (None, None)
        if a in labels and b in labels:
            if a != b:
                edges.add((min(a, b), max(a, b)))
        else:
            skipped += 1
    if skipped:
        warn(f"{skipped} edges skipped: unknown node or missing source/target")
    labels = dict(sorted(labels.items()))
    # Regions come from the input only when every node has a community.
    return labels, sorted(edges), (community if len(community) == len(labels) else None), names, times


# ---------------------------------------------------------------- input B: Markdown folder

WIKI_LINK = re.compile(r"\[\[([^\[\]|#]+)[^\[\]]*\]\]")          # [[target]], [[target|alias]], [[target#part]]
MD_LINK = re.compile(r"\]\(\s*(?:<([^>]+)>|([^)\s]+))")          # [text](path.md), [text](<path with spaces.md>)
CODE_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1", re.S | re.M)
CODE_SPAN = re.compile(r"`[^`\n]+`")
FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?^---[ \t]*$", re.S | re.M)
HEADING = re.compile(r"[ \t]{0,3}#{1,6}(?:[ \t]|$)")


def excluded(rel, patterns):
    return any(fnmatch.fnmatch(rel, p) for p in patterns)


def first_paragraph(text):
    """First paragraph of a page without YAML frontmatter, headings and code blocks; at most PARAGRAPH_CHARS characters."""
    text = CODE_FENCE.sub("", FRONTMATTER.sub("", text.lstrip("\ufeff"), count=1))
    for block in re.split(r"\n[ \t]*\n", text):
        para = clean(" ".join(line for line in block.splitlines() if not HEADING.match(line)))
        if para and not all(word.startswith("#") for word in para.split()):  # a line of tags is not a paragraph
            return para if len(para) <= PARAGRAPH_CHARS else para[:PARAGRAPH_CHARS - 1].rstrip() + "…"
    return ""


def resolve_wiki(target, src_dir, ids, by_name):
    t = target.strip()
    if t.lower().endswith(".md"):
        t = t[:-3]
    t = t.strip("/")
    if not t:
        return None
    if t in ids:                                           # page name from the root (SilverBullet)
        return t
    rel = posixpath.normpath(posixpath.join(src_dir, t))   # relative to the linking page
    if rel in ids:
        return rel
    found = by_name.get(t) if "/" not in t else None       # bare file name anywhere (Obsidian)
    return found[0] if found else None


def resolve_md(target, src_dir, ids):
    t = unquote(target.split("#", 1)[0].strip())
    if not t or "://" in t or t.startswith("mailto:") or not t.lower().endswith(".md"):
        return None
    p = t.lstrip("/") if t.startswith("/") else posixpath.join(src_dir, t)
    p = posixpath.normpath(p)[:-3]
    return p if p in ids else None


def parse_git_log(text):
    """{path: (first, last) epoch seconds} from `git log --format=%x00%at --name-only` output."""
    span, t = {}, None
    for line in text.splitlines():
        if line.startswith("\0"):
            t = int(line[1:])
        elif line and t is not None and not line.startswith('"'):  # ponytail: C-quoted names fall back to mtime
            a, b = span.get(line, (t, t))
            span[line] = (min(a, t), max(b, t))
    return span


def file_times(root, files):
    """{node id: (first, last)}: first and last commit of each file under root, else its modification time."""
    span, changed = {}, set()
    git = ["git", "-c", "core.quotePath=false", "-C", root]
    run = lambda *args: subprocess.run(git + list(args), capture_output=True, text=True, encoding="utf-8",
                                       errors="replace", timeout=120)
    try:  # ponytail: one full-history git log; renamed files start at the rename (no --follow)
        out = run("log", "--format=%x00%at", "--name-only", "--relative", "--", ".")
        if out.returncode == 0:
            span = parse_git_log(out.stdout)
            dirty = run("diff", "--name-only", "--relative", "HEAD", "--", ".")
            changed = set(dirty.stdout.splitlines()) if dirty.returncode == 0 else set()
    except (OSError, subprocess.TimeoutExpired):
        pass
    times, missing = {}, 0
    for nid, path in files.items():
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel in span:
            first, last = span[rel]
            if rel in changed:  # saved after its last commit: the save is the last change
                with contextlib.suppress(OSError):
                    last = max(last, int(os.stat(path).st_mtime))
            times[nid] = (first, last)
            continue
        missing += 1
        with contextlib.suppress(OSError):
            m = int(os.stat(path).st_mtime)
            times[nid] = (m, m)
    if span and missing:
        warn(f"{missing} files have no git history; their time is the file modification time")
    return times


def load_folder(root, excludes=(), skip_dir=None):
    """Return (labels, edges, None, {}, times, first paragraphs) for a folder: one node per .md file, one edge per link."""
    root = os.path.abspath(root)
    files = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        dirnames[:] = [d for d in sorted(dirnames)
                       if not d.startswith(".") and os.path.join(dirpath, d) != skip_dir
                       and not excluded(posixpath.join(rel_dir, d), excludes)]
        for name in sorted(filenames):
            if name.startswith(".") or not name.lower().endswith(".md"):
                continue
            rel = posixpath.join(rel_dir, name)
            if not (excluded(rel, excludes) or excluded(rel[:-3], excludes)):
                files[rel[:-3]] = os.path.join(dirpath, name)
    if not files:
        raise InputError(f"no .md files under {root}\n  fix: check the folder and the --exclude patterns")
    by_name = defaultdict(list)
    for nid in sorted(files, key=lambda s: (len(s), s)):
        by_name[posixpath.basename(nid)].append(nid)
    edges, paragraphs = set(), {}
    for nid, path in files.items():
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError as e:
            warn(f"skipped links of {nid}: {e.strerror}")
            continue
        paragraphs[nid] = first_paragraph(text)
        text = CODE_SPAN.sub("", CODE_FENCE.sub("", text))     # link syntax shown as code is not a link
        src_dir = posixpath.dirname(nid)
        targets = {resolve_wiki(m.group(1), src_dir, files, by_name) for m in WIKI_LINK.finditer(text)}
        targets |= {resolve_md(m.group(1) or m.group(2), src_dir, files) for m in MD_LINK.finditer(text)}
        edges |= {(min(nid, t), max(nid, t)) for t in targets if t and t != nid}
    return {nid: nid for nid in sorted(files)}, sorted(edges), None, {}, file_times(root, files), paragraphs


# ---------------------------------------------------------------- regions

def label_propagation(ids, adj, seed=SEED, max_iter=LPA_MAX_ITER):
    """Asynchronous label propagation; ties go to a seeded random choice, so runs repeat.

    Hubs, the top 5 % of nodes by degree (indexes, changelogs), take a label but do not vote:
    their links span every topic and would pull unrelated pages into one region. A node whose
    neighbours are all hubs still follows them.
    ponytail: a heuristic against the one-giant-region failure of plain label propagation;
    upgrade path is modularity optimisation (Louvain or Leiden) if region quality matters more.
    """
    degrees = sorted((len(adj[n]) for n in ids), reverse=True)
    hub = degrees[len(degrees) // 20] if degrees else 0
    rng = random.Random(seed)
    label = {n: n for n in ids}
    order = list(ids)
    for _ in range(max_iter):
        rng.shuffle(order)
        changed = False
        for n in order:
            if not adj[n]:
                continue
            counts = Counter(label[m] for m in adj[n] if len(adj[m]) <= hub) or Counter(label[m] for m in adj[n])
            best = max(counts.values())
            tied = sorted(lab for lab, c in counts.items() if c == best)
            if label[n] not in tied:
                label[n] = rng.choice(tied)
                changed = True
        if not changed:
            break
    return label


def make_regions(ids, adj, labels, community, names):
    if community is None:
        community = label_propagation(ids, adj)
        method = f"label propagation (seed {SEED}, at most {LPA_MAX_ITER} iterations, top 5 % hubs do not vote)"
    else:
        method = "community field of graph.json"
    groups = defaultdict(list)
    for n in ids:
        groups[community[n]].append(n)
    ordered = sorted(groups.values(), key=lambda m: (-len(m), m[0]))
    other, merged = [], 0
    if len(ordered) > MAX_REGIONS:
        merged = len(ordered) - (MAX_REGIONS - 1)
        other = [n for m in ordered[MAX_REGIONS - 1:] for n in m]     # small groups stay next to each other
        ordered = ordered[:MAX_REGIONS - 1]
    regions = []
    for i, members in enumerate(ordered):
        named = Counter(names[n] for n in members if n in names)
        hub = min(members, key=lambda n: (-len(adj[n]), labels[n], n))
        regions.append({"name": named.most_common(1)[0][0] if named else labels[hub],
                        "members": members, "color": PALETTE[i]})
    if other:
        regions.append({"name": "other", "members": other, "color": OTHER_COLOR, "merged": merged})
    return regions, method


# ---------------------------------------------------------------- 3D layout

def unit(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cap_point(frac, j, axis, e1, e2):
    """Direction at area fraction frac of the cap around axis, turned by j golden angles (Fibonacci spiral)."""
    cos_t = 1 - (1 - math.cos(CAP_ANGLE)) * frac
    sin_t = math.sqrt(max(0.0, 1 - cos_t * cos_t))
    phi = j * GOLDEN
    return tuple(cos_t * axis[k] + sin_t * (math.cos(phi) * e1[k] + math.sin(phi) * e2[k]) for k in range(3))


def normalise(pts):
    """Centre 2D points on their mean and scale them to a root-mean-square radius of 1."""
    n = len(pts)
    cx, cy = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    rms = math.sqrt(sum((x - cx) ** 2 + (y - cy) ** 2 for x, y in pts) / n) or 1.0
    return [((x - cx) / rms, (y - cy) / rms) for x, y in pts]


def local_layout(members, adj):
    """Force layout of one region in the plane (Fruchterman-Reingold), normalised. Deterministic."""
    n = len(members)
    index = {m: i for i, m in enumerate(members)}
    edges = [(index[a], index[b]) for a in members for b in adj[a] if b in index and index[a] < index[b]]
    pos = [[math.sqrt((i + 0.5) / n) * math.cos(i * GOLDEN), math.sqrt((i + 0.5) / n) * math.sin(i * GOLDEN)]
           for i in range(n)]                 # sunflower start; members come hubs first, so hubs start inside
    k2 = 1.0 / n
    k = math.sqrt(k2)
    # ponytail: O(n^2) repulsion per iteration. The iteration count keeps pairs x iterations near 1.5e6
    # (about 1 s) and drops to 0 past about 770 nodes, where the sunflower order stays as it is.
    # Upgrade path: a Barnes-Hut quadtree if regions with thousands of nodes matter.
    iters = min(60, 1_500_000 // (n * (n - 1) // 2 or 1))
    iters = iters if iters >= 5 else 0
    t = 0.1
    for _ in range(iters):
        disp = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            px, py = pos[i]
            di = disp[i]
            for j in range(i + 1, n):
                dx, dy = px - pos[j][0], py - pos[j][1]
                f = k2 / (dx * dx + dy * dy + 1e-9)
                di[0] += dx * f
                di[1] += dy * f
                disp[j][0] -= dx * f
                disp[j][1] -= dy * f
        for i, j in edges:
            dx, dy = pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]
            f = math.sqrt(dx * dx + dy * dy) / k
            disp[i][0] -= dx * f
            disp[i][1] -= dy * f
            disp[j][0] += dx * f
            disp[j][1] += dy * f
        for p, d in zip(pos, disp):
            dx, dy = d[0] - p[0], d[1] - p[1]                 # gravity keeps loose nodes near the centre
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                step = min(length, t) / length
                p[0] += dx * step
                p[1] += dy * step
        t = max(t * 0.93, 0.002)
    return normalise(pos)


def fit_patch(members, hc, patch, adj):
    """Put a region's nodes on its patch of surface points, keeping the shape of the force layout."""
    members = sorted(members, key=lambda n: (-len(adj[n]), n))
    c = [sum(p[k] for p in patch) / len(patch) for k in range(3)]
    normal = unit(tuple(c[k] - hc[k] for k in range(3)))
    e1 = unit(cross(normal, (0.0, 1.0, 0.0))) if abs(normal[1]) < 0.99 else (1.0, 0.0, 0.0)
    e2 = cross(normal, e1)
    flat = normalise([(dot([p[k] - c[k] for k in range(3)], e1), dot([p[k] - c[k] for k in range(3)], e2))
                      for p in patch])
    if len(members) > 770:
        # ponytail: past 770 nodes the force layout and the O(n^2) matching are skipped:
        # hubs take the points nearest the centre.
        order = sorted(range(len(patch)), key=lambda i: (flat[i][0] ** 2 + flat[i][1] ** 2, i))
        return {n: patch[i] for n, i in zip(members, order)}
    free, out = list(range(len(patch))), {}
    for n, (x, y) in zip(members, local_layout(members, adj)):   # greedy matching, hubs first
        best = min(free, key=lambda i: ((flat[i][0] - x) ** 2 + (flat[i][1] - y) ** 2, i))
        free.remove(best)
        out[n] = patch[best]
    return out


def layout(regions, adj):
    """Place regions and nodes on two hemispheres; return {node: (x, y, z)}.

    Each hemisphere gets as many evenly spread surface points as it has nodes. Region centres lie
    on the surface; each region takes the free points nearest its centre, as many as it has nodes,
    and its force layout decides which node goes to which point.
    """
    load, parts = [0, 0], []
    for reg in regions:                       # largest first, "other" last; balance the node count
        s, members = (0 if load[0] <= load[1] else 1), reg["members"]
        gap = abs(load[0] - load[1])
        if "merged" in reg and len(members) > gap + 1:     # a large "other" is split over both hemispheres
            half = gap + (len(members) - gap) // 2
            chunks = [(members[:half], s), (members[half:], 1 - s)]
        else:
            chunks = [(members, s)]
        for chunk, side in chunks:
            load[side] += len(chunk)
            parts.append((reg, chunk, side))
    pos = {}
    for s, sign in ((0, -1.0), (1, 1.0)):
        mine = [(reg, chunk) for reg, chunk, side in parts if side == s]
        total = sum(len(chunk) for _, chunk in mine)
        axis = unit((sign, CAP_AXIS_Y, 0.0))
        e1 = unit(cross(axis, (0.0, 0.0, 1.0)))
        e2 = cross(axis, e1)
        hc = (sign * SHIFT * R, 0.0, 0.0)

        def surface(d):
            return tuple(hc[k] + d[k] * SEMI[k] * R for k in range(3))
        done, centres = 0, []
        for j, (reg, chunk) in enumerate(mine):    # each centre sits in a band sized to the region
            centres.append(surface(cap_point((done + len(chunk) / 2) / total, j, axis, e1, e2)))
            done += len(chunk)
            side = ("left", "right")[s]
            if "center" not in reg:
                reg["center"], reg["hemisphere"] = centres[-1], side
            elif reg["hemisphere"] != side:
                reg["hemisphere"] = "both"
        points = [surface(cap_point((i + 0.5) / total, i, axis, e1, e2)) for i in range(total)]
        free, taken = [len(chunk) for _, chunk in mine], [False] * total
        patches = [[] for _ in mine]
        pairs = sorted((sum((p[k] - c[k]) ** 2 for k in range(3)), i, r)
                       for i, p in enumerate(points) for r, c in enumerate(centres))
        for _, i, r in pairs:
            if free[r] and not taken[i]:
                taken[i] = True
                free[r] -= 1
                patches[r].append(points[i])
        for (_, chunk), patch in zip(mine, patches):
            pos.update(fit_patch(chunk, hc, patch, adj))
    return pos


def build_scene(graph, title, source):
    labels, edges, community, names, times = graph
    ids = list(labels)
    adj = {n: [] for n in ids}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for n in ids:
        adj[n].sort()
    regions, method = make_regions(ids, adj, labels, community, names)
    pos = layout(regions, adj)
    region_of = {n: i for i, reg in enumerate(regions) for n in reg["members"]}
    cam = R * 2.8 / math.sqrt(sum(c * c for c in CAMERA))
    return {
        "generator": f"neurophify {VERSION}",
        "title": title,
        "input": source,
        "method": method,
        "camera": [round(c * cam, 1) for c in CAMERA],
        "regions": [{"id": i, "name": reg["name"], "color": reg["color"], "size": len(reg["members"]),
                     "hemisphere": reg["hemisphere"], "center": [round(v, 1) for v in reg["center"]],
                     **({"merged": reg["merged"]} if "merged" in reg else {})}
                    for i, reg in enumerate(regions)],
        "nodes": [{"id": n, "label": labels[n], "region": region_of[n], "degree": len(adj[n]),
                   "x": round(pos[n][0], 1), "y": round(pos[n][1], 1), "z": round(pos[n][2], 1),
                   **({"t": times[n][0], "last": times[n][1]} if n in times else {})} for n in ids],
        "edges": [{"source": a, "target": b} for a, b in edges],
        "top": sorted(ids, key=lambda n: (-len(adj[n]), labels[n], n))[:TOP_LABELS],
    }


# ---------------------------------------------------------------- outputs

def view_transform():
    """Orthographic camera on the CAMERA direction: returns (screen x, screen y down, depth toward viewer)."""
    yaw = -math.atan2(CAMERA[0], CAMERA[2])
    pitch = math.atan2(CAMERA[1], math.hypot(CAMERA[0], CAMERA[2]))
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)

    def view(x, y, z):
        x, z = x * cy + z * sy, -x * sy + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, -y, z
    return view


def node_radius(degree):
    return min(1.6 + 0.9 * math.sqrt(degree), 11.0)


def hemisphere_outlines(view):
    """Projected outline of each hemisphere ellipsoid: [(cx, cy, rx, ry, angle in degrees, half width, half height)]."""
    cols = [view(*(SEMI[k] * R if i == k else 0.0 for i in range(3)))[:2] for k in range(3)]
    sxx = sum(c[0] * c[0] for c in cols)
    syy = sum(c[1] * c[1] for c in cols)
    sxy = sum(c[0] * c[1] for c in cols)
    mid, half = (sxx + syy) / 2, math.sqrt(((sxx - syy) / 2) ** 2 + sxy * sxy)
    angle = math.degrees(0.5 * math.atan2(2 * sxy, sxx - syy))
    rx, ry = math.sqrt(mid + half), math.sqrt(max(mid - half, 0.0))
    out = []
    for sign in (-1.0, 1.0):
        cx, cy, _ = view(sign * SHIFT * R, 0.0, 0.0)
        out.append((cx, cy, rx, ry, angle, math.sqrt(sxx), math.sqrt(syy)))
    return out


def render_svg(scene):
    width, height, legend_w, top, pad = 1200, 800, 290, 92, 28
    esc = html.escape
    nodes, regions = scene["nodes"], scene["regions"]
    view = view_transform()
    pts = {n["id"]: view(n["x"], n["y"], n["z"]) for n in nodes}
    outlines = hemisphere_outlines(view)
    xs = [p[0] for p in pts.values()] + [o[0] + d * o[5] for o in outlines for d in (-1, 1)]
    ys = [p[1] for p in pts.values()] + [o[1] + d * o[6] for o in outlines for d in (-1, 1)]
    zs = [p[2] for p in pts.values()]
    plot_w, plot_h = width - legend_w - 2 * pad, height - top - pad
    bw, bh = (max(xs) - min(xs)) or 1.0, (max(ys) - min(ys)) or 1.0
    s = min(plot_w / bw, plot_h / bh)
    ox = pad + (plot_w - s * bw) / 2 - s * min(xs)
    oy = top + (plot_h - s * bh) / 2 - s * min(ys)
    z0, zspan = min(zs), (max(zs) - min(zs)) or 1.0
    screen = {k: (ox + s * x, oy + s * y, (z - z0) / zspan) for k, (x, y, z) in pts.items()}
    # The far half of each hemisphere is drawn under a translucent cortex, the near half above it.
    centre_z = (view(-SHIFT * R, 0.0, 0.0)[2], view(SHIFT * R, 0.0, 0.0)[2])
    front = {n["id"]: pts[n["id"]][2] >= centre_z[n["x"] >= 0] for n in nodes}
    region_of = {n["id"]: n["region"] for n in nodes}
    paths = defaultdict(list)
    for e in scene["edges"]:
        (x1, y1, d1), (x2, y2, d2) = screen[e["source"]], screen[e["target"]]
        ra, rb = region_of[e["source"]], region_of[e["target"]]
        key = (front[e["source"]] and front[e["target"]], regions[ra]["color"] if ra == rb else "#8b95a5",
               ra != rb, min(3, int((d1 + d2) * 2)))
        paths[key].append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
    title, meta = scene["title"], f'{len(nodes)} nodes, {len(scene["edges"])} edges, {len(regions)} regions'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
           f'font-family="{FONT}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{esc(title)}</title>',
           f'<desc id="desc">{esc(meta)}. Knowledge graph drawn as a 3D brain by neurophify.</desc>',
           f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>']
    for layer in (False, True):
        for (near, color, bridge, bucket), segs in sorted(paths.items()):
            if near == layer:
                opacity = (0.07, 0.12, 0.18, 0.26)[bucket] * (0.7 if bridge else 1.0)
                out.append(f'<path d="{"".join(segs)}" fill="none" stroke="{color}" stroke-opacity="{opacity:.3f}" '
                           'stroke-width="0.8"/>')
        for n in sorted(nodes, key=lambda n: screen[n["id"]][2]):
            if front[n["id"]] == layer:
                x, y, d = screen[n["id"]]
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_radius(n["degree"]):.1f}" '
                           f'fill="{regions[n["region"]]["color"]}" fill-opacity="{0.45 + 0.55 * d:.2f}" '
                           f'stroke="{BACKGROUND}" stroke-width="0.6"/>')
        if not layer:
            for cx, cy, rx, ry, angle, _, _ in outlines:
                x, y = ox + s * cx, oy + s * cy
                out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{s * rx:.1f}" ry="{s * ry:.1f}" '
                           f'transform="rotate({angle:.2f} {x:.1f} {y:.1f})" fill="#0b111b" fill-opacity="0.72" '
                           'stroke="#2a3446" stroke-width="1.5"/>')
    by_id, placed = {n["id"]: n for n in nodes}, []
    for nid in scene["top"]:                  # first free spot: right, left, above, below the node
        x, y, _ = screen[nid]
        r, w = node_radius(by_id[nid]["degree"]) + 4, 7.2 * len(by_id[nid]["label"])
        spots = [(x + r, y + 4), (x - r - w, y + 4), (x - w / 2, y - r - 2), (x - w / 2, y + r + 12)]
        boxes = [(tx, ty - 12, tx + w, ty + 4) for tx, ty in spots]
        fits = [b for b in boxes if b[0] >= 0 and b[2] <= width - legend_w - 8
                and not any(b[0] < p[2] and p[0] < b[2] and b[1] < p[3] and p[1] < b[3] for p in placed)]
        box = (fits or boxes)[0]
        placed.append(box)
        out.append(f'<text x="{box[0]:.1f}" y="{box[3] - 4:.1f}" font-size="13" fill="#f5f7fa" '
                   f'stroke="{BACKGROUND}" stroke-width="3" paint-order="stroke">{esc(by_id[nid]["label"])}</text>')
    out.append(f'<text x="{pad}" y="44" font-size="24" font-weight="600" fill="#f5f7fa">{esc(title)}</text>')
    out.append(f'<text x="{pad}" y="68" font-size="14" fill="#9aa4b2">{esc(meta)}</text>')
    lx = width - legend_w
    out.append(f'<text x="{lx}" y="{top + 4}" font-size="14" font-weight="600" fill="#f5f7fa">Regions</text>')
    for i, reg in enumerate(regions):
        y = top + 28 + i * 22
        name = reg["name"] if len(reg["name"]) <= 27 else reg["name"][:26] + "…"
        out.append(f'<circle cx="{lx + 6}" cy="{y - 4}" r="5" fill="{reg["color"]}"/>')
        out.append(f'<text x="{lx + 18}" y="{y}" font-size="13" fill="#e6e9ef">{esc(name)}</text>')
        out.append(f'<text x="{width - pad}" y="{y}" font-size="13" fill="#9aa4b2" text-anchor="end">{reg["size"]}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def spin_view(angle):
    """View after turning the scene by `angle` around its vertical axis: (screen x, screen y down, depth toward viewer)."""
    cp, sp, ca, sa = math.cos(SPIN_PITCH), math.sin(SPIN_PITCH), math.cos(angle), math.sin(angle)

    def view(x, y, z):
        x, z = x * ca + z * sa, -x * sa + z * ca
        return x, -(y * cp - z * sp), y * sp + z * cp
    return view


def spin_frames(scene, frames=SPIN_FRAMES):
    """Per key frame of one turn around the vertical axis: (screen x, screen y down, depth toward viewer) per node."""
    views = [spin_view(2 * math.pi * f / frames) for f in range(frames)]
    return [[v(n["x"], n["y"], n["z"]) for n in scene["nodes"]] for v in views]


def spin_edges(scene, limit=SPIN_EDGES):
    """Edges of brain-spin.svg: inside 1 region, without the node with the most edges (its fan hides the brain),
    taken from each region in turn so both hemispheres keep their structure."""
    nodes = scene["nodes"]
    if not nodes:
        return []
    hub = min(nodes, key=lambda n: (-n["degree"], n["label"], n["id"]))["id"]
    degree = {n["id"]: n["degree"] for n in nodes}
    region_of = {n["id"]: n["region"] for n in nodes}
    groups = defaultdict(list)
    for e in scene["edges"]:
        if region_of[e["source"]] == region_of[e["target"]] and hub not in (e["source"], e["target"]):
            groups[region_of[e["source"]]].append(e)
    for g in groups.values():
        g.sort(key=lambda e: (-(degree[e["source"]] + degree[e["target"]]), e["source"], e["target"]))
    out, rank = [], 0
    while len(out) < limit and any(rank < len(g) for g in groups.values()):
        out += [groups[r][rank] for r in sorted(groups) if rank < len(groups[r])][:limit - len(out)]
        rank += 1
    return out


def render_spin_svg(scene):
    """brain-spin.svg: the brain turning around its vertical axis, animated with SMIL (no script), for a README."""
    width, height, top = 900, 620, 80
    nodes, regions = scene["nodes"], scene["regions"]
    frames = spin_frames(scene)
    reach = max((math.sqrt(n["x"] ** 2 + n["y"] ** 2 + n["z"] ** 2) for n in nodes), default=1.0) or 1.0
    s = 0.96 * min(width, height - top) / (2 * reach)
    cx0, cy0 = width / 2, top + (height - top) / 2
    index = {n["id"]: i for i, n in enumerate(nodes)}

    def track(i, k):              # coordinate k of node i over the turn, closed back to the first frame
        return [f[i][k] for f in frames] + [frames[0][i][k]]

    def animate(name, values, fmt):
        vals = ";".join(fmt.format(v) for v in values)
        return f'<animate attributeName="{name}" dur="{SPIN_SECONDS}s" repeatCount="indefinite" values="{vals}"/>'

    title, meta = scene["title"], f'{len(nodes)} nodes, {len(regions)} regions. One turn every {SPIN_SECONDS} s.'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
           f'font-family="{FONT}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{html.escape(title)}</title>',
           f'<desc id="desc">{html.escape(meta)} Knowledge graph drawn as a turning 3D brain by neurophify.</desc>',
           f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
           f'<text x="28" y="44" font-size="24" font-weight="600" fill="#f5f7fa">{html.escape(title)}</text>',
           f'<text x="28" y="68" font-size="14" fill="#9aa4b2">{html.escape(meta)}</text>']
    # The outline of each hemisphere turns with the nodes: the projected ellipse of hemisphere_outlines per key frame.
    shapes = [hemisphere_outlines(spin_view(2 * math.pi * f / SPIN_FRAMES)) for f in range(SPIN_FRAMES)]
    for h in (0, 1):
        seq = [o[h] for o in shapes] + [shapes[0][h]]
        turn, prev = [], None
        for q in seq:              # an ellipse turned by 180 degrees is the same ellipse: keep the angle continuous
            a = q[4] if prev is None else q[4] + 180 * round((prev - q[4]) / 180)
            turn.append(a)
            prev = a
        x, y = [cx0 + s * q[0] for q in seq], [cy0 + s * q[1] for q in seq]
        rx, ry = [s * q[2] for q in seq], [s * q[3] for q in seq]
        rotate = ";".join(f"{a:.1f} {px:.0f} {py:.0f}" for a, px, py in zip(turn, x, y))
        out.append(f'<ellipse cx="{x[0]:.0f}" cy="{y[0]:.0f}" rx="{rx[0]:.0f}" ry="{ry[0]:.0f}" '
                   f'transform="rotate({turn[0]:.1f} {x[0]:.0f} {y[0]:.0f})" fill="#0b111b" fill-opacity="0.55" '
                   'stroke="#2a3446" stroke-width="1.5">'
                   + animate("cx", x, "{:.0f}") + animate("cy", y, "{:.0f}")
                   + animate("rx", rx, "{:.0f}") + animate("ry", ry, "{:.0f}")
                   + f'<animateTransform attributeName="transform" type="rotate" dur="{SPIN_SECONDS}s" '
                   f'repeatCount="indefinite" values="{rotate}"/></ellipse>')
    for e in spin_edges(scene):
        a, b = index[e["source"]], index[e["target"]]
        ends = {"x1": [cx0 + s * v for v in track(a, 0)], "y1": [cy0 + s * v for v in track(a, 1)],
                "x2": [cx0 + s * v for v in track(b, 0)], "y2": [cy0 + s * v for v in track(b, 1)]}
        fade = [0.06 + 0.5 * ((za + zb) / 2 + reach) / (2 * reach) for za, zb in zip(track(a, 2), track(b, 2))]
        out.append("<line " + " ".join(f'{k}="{v[0]:.0f}"' for k, v in ends.items())
                   + f' stroke="{regions[nodes[a]["region"]]["color"]}" stroke-opacity="{fade[0]:.2f}" stroke-width="0.8">'
                   + "".join(animate(k, v, "{:.0f}") for k, v in ends.items())
                   + animate("stroke-opacity", fade, "{:.2f}") + "</line>")
    for n in sorted(nodes, key=lambda n: (n["degree"], n["id"])):   # nodes with more edges are drawn on top
        i = index[n["id"]]
        depth = [(z + reach) / (2 * reach) for z in track(i, 2)]
        x, y = [cx0 + s * v for v in track(i, 0)], [cy0 + s * v for v in track(i, 1)]
        r = [node_radius(n["degree"]) * (0.55 + 0.6 * d) for d in depth]
        o = [0.2 + 0.8 * d for d in depth]
        out.append(f'<circle cx="{x[0]:.0f}" cy="{y[0]:.0f}" r="{r[0]:.1f}" opacity="{o[0]:.2f}" '
                   f'fill="{regions[n["region"]]["color"]}">'
                   + animate("cx", x, "{:.0f}") + animate("cy", y, "{:.0f}")
                   + animate("r", r, "{:.1f}") + animate("opacity", o, "{:.2f}") + "</circle>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_stl(scene, top=STL_NODES):
    """brain.stl: ASCII STL of both hemispheres and a tetrahedron for each of the `top` nodes with the most edges.
    The brain's height axis becomes z, so STL viewers show it upright."""
    facets = []

    def add(a, b, c, inside):      # orient the facet so its normal points away from `inside`
        nrm = cross([b[k] - a[k] for k in range(3)], [c[k] - a[k] for k in range(3)])
        if dot(nrm, [(a[k] + b[k] + c[k]) / 3 - inside[k] for k in range(3)]) < 0:
            b, c, nrm = c, b, [-v for v in nrm]
        facets.append((unit(nrm), a, b, c))

    for sign in (-1.0, 1.0):
        centre, axes = (sign * SHIFT * R, 0.0, 0.0), [STL_SHELL * k * R for k in SEMI]

        def p(i, j):
            th, ph = 2 * math.pi * i / HEMI_U, math.pi * j / HEMI_V
            return (centre[0] + axes[0] * math.sin(ph) * math.cos(th), centre[1] + axes[1] * math.cos(ph),
                    centre[2] + axes[2] * math.sin(ph) * math.sin(th))
        for i in range(HEMI_U):
            for j in range(HEMI_V):     # the first and the last band meet at a pole: 1 triangle per step
                if j > 0:
                    add(p(i, j), p(i + 1, j), p(i + 1, j + 1), centre)
                if j < HEMI_V - 1:
                    add(p(i, j), p(i + 1, j + 1), p(i, j + 1), centre)
    corners = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    for n in sorted(scene["nodes"], key=lambda n: (-n["degree"], n["label"], n["id"]))[:top]:
        c, t = (n["x"], n["y"], n["z"]), (4 + 1.5 * math.sqrt(n["degree"])) / math.sqrt(3)
        v = [tuple(c[k] + t * q[k] for k in range(3)) for q in corners]
        for a, b, d in ((0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)):
            add(v[a], v[b], v[d], c)

    def xyz(q):                     # (x, y, z) of the scene -> (x, -z, y) in STL, in units of 10
        return f"{q[0] / 10:.1f} {-q[2] / 10:.1f} {q[1] / 10:.1f}"
    out = ["solid neurophify"]
    for nrm, a, b, c in facets:
        out += [f"facet normal {nrm[0]:.3f} {-nrm[2]:.3f} {nrm[1]:.3f}", "outer loop",
                f"vertex {xyz(a)}", f"vertex {xyz(b)}", f"vertex {xyz(c)}", "endloop", "endfacet"]
    out.append("endsolid neurophify")
    return "\n".join(out) + "\n"


def embed_json(obj):
    """JSON safe inside a <script> element: no '<', '>' or '&' outside escapes."""
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ - neurophify</title>
<style>
html, body { margin: 0; height: 100%; overflow: hidden; background: __BG__; color: #e6e9ef;
  font: 13px/1.45 __FONT__; }
#graph, #labels { position: absolute; inset: 0; }
#labels { pointer-events: none; overflow: hidden; }
.label { position: absolute; white-space: nowrap; font-size: 12px; line-height: 16px;
  color: #f5f7fa; text-shadow: 0 0 3px __BG__, 0 0 3px __BG__; }
#panel { position: absolute; top: 12px; left: 12px; width: 280px; max-height: calc(100% - 110px); overflow: auto;
  background: rgba(9, 12, 18, 0.86); border: 1px solid #252b38; border-radius: 6px; padding: 10px 12px; }
h1 { font-size: 16px; margin: 0 0 2px; }
.meta, .count, #hint { color: #9aa4b2; }
.meta { margin: 0 0 8px; }
ul { list-style: none; margin: 0; padding: 0; }
li { display: flex; align-items: center; gap: 8px; padding: 1px 0; }
.swatch { width: 10px; height: 10px; border-radius: 50%; flex: none; }
.count { margin-left: auto; padding-left: 8px; }
#hint { position: absolute; left: 12px; bottom: 10px; margin: 0; }
#error { color: #ffb4a8; margin: 8px 0 0; }
a { color: #8ab4f8; }
#time { position: absolute; left: 12px; right: 12px; bottom: 34px; display: flex; align-items: center; gap: 10px;
  background: rgba(9, 12, 18, 0.86); border: 1px solid #252b38; border-radius: 6px; padding: 6px 10px; }
#time[hidden] { display: none; }
#time input { flex: 1; min-width: 0; accent-color: #8ab4f8; }
#time output { color: #9aa4b2; white-space: nowrap; font-variant-numeric: tabular-nums; }
button { font: inherit; color: #e6e9ef; background: #1b2130; border: 1px solid #39414f; border-radius: 4px;
  padding: 3px 12px; cursor: pointer; }
</style>
</head>
<body>
<div id="graph"></div>
<div id="labels"></div>
<section id="panel" aria-label="Regions">
<h1>__TITLE__</h1>
<p class="meta">__META__ Text version: <a href="REGIONS.md">REGIONS.md</a>.</p>
<ul id="legend"></ul>
<p id="error" hidden></p>
</section>
<p id="hint">Drag to rotate, scroll to zoom, hover a node to read its name, click a node to fly to it.</p>
<div id="time" hidden><button id="play" type="button">Play</button><label for="when">Time</label>
<input id="when" type="range" min="0" max="0" step="1" value="0"><output id="when-text" for="when"></output></div>
<script id="graph-data" type="application/json">__DATA__</script>
<script src="__CDN__"></script>
<script>
(function () {
  "use strict";
  const data = JSON.parse(document.getElementById("graph-data").textContent);
  const regions = data.regions;
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"})[c]);
  const legend = document.getElementById("legend");
  for (const r of regions) {
    const li = document.createElement("li"), sw = document.createElement("span");
    const name = document.createElement("span"), count = document.createElement("span");
    sw.className = "swatch";
    sw.style.background = r.color;
    name.textContent = r.name;
    count.className = "count";
    count.textContent = r.size;
    li.append(sw, name, count);
    legend.append(li);
  }
  const fail = msg => { const e = document.getElementById("error"); e.textContent = msg; e.hidden = false; };
  if (typeof ForceGraph3D !== "function") {
    fail("The 3D view needs the 3d-force-graph script from cdn.jsdelivr.net. Connect to the network and reload; brain.svg and REGIONS.md work offline.");
    return;
  }
  const nodes = data.nodes.map(n => Object.assign({}, n, {fx: n.x, fy: n.y, fz: n.z}));
  const byId = new Map(nodes.map(n => [n.id, n]));
  const links = data.edges.map(e => {
    const a = byId.get(e.source).region, b = byId.get(e.target).region;
    return {source: e.source, target: e.target, color: a === b ? regions[a].color : "rgba(139, 149, 165, 0.45)"};
  });
  let graph;
  try {
    graph = ForceGraph3D()(document.getElementById("graph"))
      .backgroundColor("__BG__")
      .showNavInfo(false)
      .enableNodeDrag(false)
      .nodeRelSize(3)
      .nodeVal(n => 1 + n.degree)
      .nodeColor(n => regions[n.region].color)
      .nodeOpacity(0.95)
      .nodeLabel(n => "<b>" + esc(n.label) + "</b><br>" + esc(regions[n.region].name) + ", " + n.degree + " links")
      .linkColor("color")
      .linkOpacity(0.22)
      .cooldownTicks(30)
      .onNodeClick(n => {
        const k = 1 + 80 / (Math.hypot(n.x, n.y, n.z) || 1);
        graph.cameraPosition({x: n.x * k, y: n.y * k, z: n.z * k}, n, 1500);
      })
      .graphData({nodes: nodes, links: links});
  } catch (err) {
    fail("The 3D view could not start (" + err.message + "). Open the page in a browser with WebGL enabled.");
    return;
  }
  const c = data.camera;
  graph.cameraPosition({x: c[0], y: c[1], z: c[2]}, {x: 0, y: 0, z: 0}, 0);
  // Time, the fourth dimension: the slider shows the nodes that existed at the chosen moment.
  let now = Infinity;
  const seen = n => n.t === undefined || n.t <= now;
  const times = [...new Set(nodes.filter(n => n.t !== undefined).map(n => n.t))].sort((a, b) => a - b);
  if (times.length > 1) {
    const box = document.getElementById("time"), when = document.getElementById("when");
    const text = document.getElementById("when-text"), play = document.getElementById("play");
    const pad = v => String(v).padStart(2, "0");
    const fmt = t => { const d = new Date(t * 1000); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) + " " + pad(d.getHours()) + ":" + pad(d.getMinutes()); };
    const end = x => byId.get(typeof x === "object" ? x.id : x);
    const update = () => {
      now = times[+when.value];
      graph.nodeVisibility(n => seen(n)).linkVisibility(l => seen(end(l.source)) && seen(end(l.target)));
      text.textContent = fmt(now) + ", " + nodes.filter(seen).length + " of " + nodes.length + " nodes";
    };
    let timer = 0;
    const stop = () => { clearInterval(timer); timer = 0; play.textContent = "Play"; };
    play.addEventListener("click", () => {
      if (timer) return stop();
      if (+when.value >= times.length - 1) when.value = 0;
      play.textContent = "Pause";
      timer = setInterval(() => {
        if (+when.value >= times.length - 1) return stop();
        when.value = +when.value + 1;
        update();
      }, Math.max(16, 8000 / times.length));
      update();
    });
    when.addEventListener("input", () => { stop(); update(); });
    when.max = times.length - 1;
    when.value = times.length - 1;
    box.hidden = false;
    document.getElementById("hint").textContent += " Play the time bar to watch the brain grow.";
    update();
  }
  const layer = document.getElementById("labels");
  const tags = data.top.map(id => {
    const n = byId.get(id), el = document.createElement("div");
    el.className = "label";
    el.textContent = n.label;
    layer.append(el);
    return [n, el, el.offsetWidth, el.offsetHeight];
  });
  const cam = graph.camera();
  (function place() {
    const t = (graph.controls() && graph.controls().target) || {x: 0, y: 0, z: 0};
    const p = cam.position, vx = t.x - p.x, vy = t.y - p.y, vz = t.z - p.z;
    const taken = [];
    for (const [n, el, w, h] of tags) {
      const front = (n.x - p.x) * vx + (n.y - p.y) * vy + (n.z - p.z) * vz > 0 && seen(n);
      el.hidden = !front;
      if (!front) continue;
      const s = graph.graph2ScreenCoords(n.x, n.y, n.z);
      let x = s.x - w / 2, y = s.y - h - 6;
      // a label that would cover an earlier one moves down, one line at a time
      for (let i = 0; i < 6 && taken.some(b => x < b[2] && b[0] < x + w && y < b[3] && b[1] < y + h); i++) y += h;
      taken.push([x, y, x + w, y + h]);
      el.style.left = x + "px";
      el.style.top = y + "px";
    }
    requestAnimationFrame(place);
  })();
  addEventListener("resize", () => graph.width(innerWidth).height(innerHeight));
})();
</script>
</body>
</html>
"""


def render_html(scene):
    meta = f'{len(scene["nodes"])} nodes, {len(scene["edges"])} edges, {len(scene["regions"])} regions.'
    return (HTML.replace("__TITLE__", html.escape(scene["title"])).replace("__META__", html.escape(meta))
            .replace("__BG__", BACKGROUND).replace("__FONT__", FONT).replace("__CDN__", CDN)
            .replace("__DATA__", embed_json(scene)))


def render_regions_md(scene):
    nodes, regions = scene["nodes"], scene["regions"]
    label = {n["id"]: n["label"] for n in nodes}
    degree = {n["id"]: n["degree"] for n in nodes}
    region_of = {n["id"]: n["region"] for n in nodes}
    members = defaultdict(list)
    for n in nodes:
        members[n["region"]].append(n["id"])
    inner, bridges, examples = Counter(), defaultdict(Counter), defaultdict(lambda: defaultdict(list))
    for e in scene["edges"]:
        a, b = e["source"], e["target"]
        ra, rb = region_of[a], region_of[b]
        if ra == rb:
            inner[a] += 1
            inner[b] += 1
            continue
        for x, y, rx, ry in ((a, b, ra, rb), (b, a, rb, ra)):
            bridges[rx][ry] += 1
            if len(examples[rx][ry]) < 3:
                examples[rx][ry].append((x, y))
    cell = lambda s: s.replace("|", "\\|")
    n_bridges = sum(sum(c.values()) for c in bridges.values()) // 2
    lines = [f"# Regions: {scene['title']}", "",
             f"{len(nodes)} nodes, {len(scene['edges'])} edges, {len(regions)} regions. "
             f"Regions come from the {scene['method']}. {n_bridges} edges are bridges between two regions.", "",
             "| # | Region | Nodes | Hemisphere | Bridge edges |", "|---|---|---|---|---|"]
    for i, reg in enumerate(regions):
        lines.append(f"| {i + 1} | {cell(reg['name'])} | {reg['size']} | {reg['hemisphere']} | "
                     f"{sum(bridges[i].values())} |")
    for i, reg in enumerate(regions):
        central = sorted(members[i], key=lambda n: (-inner[n], -degree[n], label[n], n))[:5]
        merged = f"; merged from {reg['merged']} smaller regions" if "merged" in reg else ""
        lines += ["", f"## {i + 1}. {reg['name']}", "",
                  f"- Nodes: {reg['size']}; {reg['hemisphere']} hemisphere; colour `{reg['color']}`{merged}.",
                  "- Central nodes (links inside the region): "
                  + ", ".join(f"{label[n]} ({inner[n]})" for n in central) + "."]
        if not bridges[i]:
            lines.append("- Bridges: none.")
            continue
        lines.append(f"- Bridges: {sum(bridges[i].values())} edges to {len(bridges[i])} regions.")
        for j, count in sorted(bridges[i].items(), key=lambda kv: (-kv[1], kv[0]))[:5]:
            sample = "; ".join(f"{label[x]} -- {label[y]}" for x, y in examples[i][j])
            lines.append(f"  - {regions[j]['name']}: {count} edges, for example {sample}.")
    timed = [n for n in nodes if "t" in n]
    if timed:
        day = lambda t: datetime.fromtimestamp(t).strftime("%Y-%m-%d")
        end = max(n["last"] for n in timed)
        recent = end - 30 * 86400
        busiest, count = max(sorted(Counter(day(n["t"]) for n in timed).items()), key=lambda kv: kv[1])
        months = Counter(day(n["t"])[:7] for n in timed)
        lines += ["", "## Time", "",
                  f"{len(timed)} of {len(nodes)} nodes have a time: first node {day(min(n['t'] for n in timed))}, "
                  f"last change {day(end)}. Time comes from the git history of a Markdown folder (outside git: the file "
                  'modification time) or from the "time" field of graph.json. brain.html replays the growth on a time slider.',
                  "",
                  f"- Busiest day: {busiest}, {count} new nodes.",
                  "- New nodes per month: " + ", ".join(f"{m}: {c}" for m, c in sorted(months.items())) + ".",
                  "- Status covers the 30 days before the last change: growing = new nodes, active = changes only, "
                  "dormant = no change.", "",
                  "| # | Region | First node | Last change | New in 30 days | Status |", "|---|---|---|---|---|---|"]
        for i, reg in enumerate(regions):
            ts = [n for n in timed if n["region"] == i]
            if ts:
                new, last = sum(n["t"] >= recent for n in ts), max(n["last"] for n in ts)
                status = "growing" if new else "active" if last >= recent else "dormant"
                lines.append(f"| {i + 1} | {cell(reg['name'])} | {day(min(n['t'] for n in ts))} | {day(last)} | "
                             f"{new} | {status} |")
    components, largest, isolated, q = graph_metrics(scene)
    lines += ["", "## Graph metrics", "",
              f"- Connected components: {components}, nodes without edges included; the largest has {largest} "
              f"of {len(nodes)} nodes.",
              f"- Nodes without edges: {isolated}.",
              f"- Modularity of the regions: Q = {q:.4f}. "
              r"$Q = \sum_c \left[\frac{L_c}{m} - \left(\frac{D_c}{2m}\right)^2\right]$, where $L_c$ is the number of "
              r"edges inside region $c$, $D_c$ the sum of the degrees of its nodes and $m$ the number of edges; "
              '"other" counts as 1 region and a graph without edges has Q = 0. Q = 0 means no more edges inside '
              "the regions than chance gives a graph with the same degrees."]
    return "\n".join(lines) + "\n"


def graph_metrics(scene):
    """(connected components, nodes in the largest one, nodes without edges, modularity Q of the regions)."""
    parent = {n["id"]: n["id"] for n in scene["nodes"]}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in scene["edges"]:
        parent[find(e["source"])] = find(e["target"])
    sizes = Counter(find(n) for n in parent)
    region = {n["id"]: n["region"] for n in scene["nodes"]}
    inner, degrees, m = Counter(), Counter(), len(scene["edges"])
    for n in scene["nodes"]:
        degrees[n["region"]] += n["degree"]
    for e in scene["edges"]:
        if region[e["source"]] == region[e["target"]]:
            inner[region[e["source"]]] += 1
    q = sum(inner[c] / m - (degrees[c] / (2 * m)) ** 2 for c in degrees) if m else 0.0
    return len(sizes), max(sizes.values()), sum(1 for n in scene["nodes"] if not n["degree"]), q


def core_nodes(scene):
    """[(node, weight)] for the CORE_SIZE heaviest nodes, weight = (1 + degree) * 2^(-d / HALF_LIFE).

    d is the number of days between the last change of the node and the newest change in the graph;
    a node without a time has d = 0. Ties go to the label, then the id.
    """
    end = max((n["last"] for n in scene["nodes"] if "last" in n), default=0)
    weighed = [(n, (1 + n["degree"]) * 2 ** (-(end - n.get("last", end)) / 86400 / HALF_LIFE)) for n in scene["nodes"]]
    return sorted(weighed, key=lambda nw: (-nw[1], nw[0]["label"], nw[0]["id"]))[:CORE_SIZE]


def render_core_md(scene, paragraphs=None):
    """CORE.md, the consolidation: the heaviest nodes; a folder input (paragraphs given) adds each first paragraph."""
    regions, core = scene["regions"], core_nodes(scene)
    lasts = [n["last"] for n in scene["nodes"] if "last" in n]
    day = lambda t: datetime.fromtimestamp(t).strftime("%Y-%m-%d")
    cell = lambda s: s.replace("|", "\\|")
    newest = day(max(lasts)) if lasts else "none: no node has a time"
    lines = [f"# Core: {scene['title']}", "",
             f"The {len(core)} of {len(scene['nodes'])} nodes with the largest weight "
             f"$w(v) = (1 + \\deg(v)) \\cdot 2^{{-d(v)/{HALF_LIFE}}}$. $\\deg(v)$ is the number of edges of node $v$; "
             f"$d(v)$ is the number of days between the last change of $v$ and the newest change in the graph "
             f"({newest}), so a node loses half its weight per {HALF_LIFE} days without a change. "
             "A node without a time has $d(v) = 0$. Ties go to the label, then the id.", "",
             "| # | Node | Region | Degree | Last change | Weight |" + (" First paragraph |" if paragraphs is not None else ""),
             "|---" * (7 if paragraphs is not None else 6) + "|"]
    for i, (n, w) in enumerate(core):
        row = (f"| {i + 1} | {cell(n['label'])} | {cell(regions[n['region']]['name'])} | {n['degree']} | "
               f"{day(n['last']) if 'last' in n else 'unknown'} | {w:.2f} |")
        lines.append(row + (f" {cell(paragraphs.get(n['id'], ''))} |" if paragraphs is not None else ""))
    return "\n".join(lines) + "\n"


def write_outputs(scene, out_dir, paragraphs=None, spin=False, stl=False):
    os.makedirs(out_dir, exist_ok=True)
    files = {"brain.html": render_html(scene), "brain.svg": render_svg(scene),
             "brain.json": json.dumps(scene, ensure_ascii=False, indent=1) + "\n",
             "REGIONS.md": render_regions_md(scene), "CORE.md": render_core_md(scene, paragraphs)}
    if spin:
        files["brain-spin.svg"] = render_spin_svg(scene)
    if stl:
        files["brain.stl"] = render_stl(scene)
    paths = []
    for name, text in files.items():
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        paths.append(path)
    return paths


def default_title(src):
    path = os.path.normpath(os.path.abspath(src))
    if os.path.isdir(path):
        return os.path.basename(path)
    parent = os.path.dirname(path)
    if os.path.basename(parent) == "graphify-out":     # graphify-out/graph.json: name of the project folder
        return os.path.basename(os.path.dirname(parent))
    return os.path.splitext(os.path.basename(path))[0]


def run(src, out_dir="neurophify-out", title=None, excludes=(), spin=False, stl=False):
    if not os.path.exists(src):
        raise InputError(f"input not found: {src}\n  fix: pass graphify-out/graph.json or a folder of .md files")
    name = default_title(src)
    if os.path.isdir(src):
        hint = os.path.join(src, "graphify-out", "graph.json")
        if os.path.isfile(hint):
            warn(f"note: {hint} exists; pass that file to use graphify communities")
        *graph, paragraphs = load_folder(src, excludes, skip_dir=os.path.abspath(out_dir))
    else:
        if excludes:
            warn("--exclude applies to folder input only; ignored")
        graph, paragraphs = load_graph_json(src), None
    scene = build_scene(graph, title or name, name)
    try:
        return write_outputs(scene, out_dir, paragraphs, spin, stl), scene
    except OSError as e:
        raise InputError(f"cannot write to {out_dir}: {e.strerror}\n  fix: choose another folder with --out") from None


# ---------------------------------------------------------------- selftest

def selftest():
    def write(path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def regions_of(scene):
        return {frozenset(n["id"] for n in scene["nodes"] if n["region"] == r["id"]) for r in scene["regions"]}

    checks, warnings = 0, io.StringIO()
    try:
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stderr(warnings):
            # 1. Input A: labels fall back to id, unknown endpoints are dropped, communities are read.
            pa = os.path.join(tmp, "a", "graph.json")
            write(pa, json.dumps({"directed": False, "multigraph": False, "graph": {}, "nodes": [
                {"id": "a", "label": "Alpha", "community": 0}, {"id": "b", "community": 0},
                {"id": "c", "label": "C", "community": 1}, {"id": "d", "label": "D", "community": 1}],
                "links": [{"source": "a", "target": "b"}, {"source": "b", "target": "c"},
                          {"source": "c", "target": "d"}, {"source": "d", "target": "x"}]}))
            labels, edges, community, _, _ = load_graph_json(pa)
            assert labels == {"a": "Alpha", "b": "b", "c": "C", "d": "D"}, f"input A labels: {labels}"
            assert edges == [("a", "b"), ("b", "c"), ("c", "d")], f"input A edges: {edges}"
            assert community == {"a": "0", "b": "0", "c": "1", "d": "1"}, f"input A communities: {community}"
            assert "1 edges skipped" in warnings.getvalue(), "input A: no warning for the edge to a missing node"
            assert regions_of(build_scene(load_graph_json(pa), "t", "a")) == {frozenset("ab"), frozenset("cd")}
            checks += 1
            # 2. Input A with an "edges" key and no community: label propagation splits two 5-cliques.
            pb = os.path.join(tmp, "b.json")
            clique = [{"source": base + i, "target": base + j} for base in (0, 5) for i in range(5) for j in range(i + 1, 5)]
            write(pb, json.dumps({"nodes": [{"id": i} for i in range(10)], "edges": clique + [{"source": 4, "target": 5}]}))
            scene_b = build_scene(load_graph_json(pb), "two cliques", "b")
            assert regions_of(scene_b) == {frozenset("01234"), frozenset("56789")}, f"regions: {regions_of(scene_b)}"
            checks += 1
            # 3. Input B: wiki links, aliases, anchors, Markdown links, code, --exclude, missing pages.
            root = os.path.join(tmp, "notes")
            write(os.path.join(root, "index.md"), "See [[Page One]], [[sub/Deep|deep]] and [[Page One#Part]].\n"
                  "```\n[[Ghost]]\n```\nInline `[[Ghost]]` is code.\n")
            write(os.path.join(root, "Page One.md"), "Back to [[index]]. Missing [[Nowhere]]. [x](https://e.org/a.md)\n")
            write(os.path.join(root, "sub", "Deep.md"), "Up: [one](../Page%20One.md), [two](<../Page One.md>)\n")
            write(os.path.join(root, "Ghost.md"), "No links.\n")
            write(os.path.join(root, "_archive", "Old.md"), "[[index]]\n")
            write(os.path.join(root, "skip-me.md"), "[[index]]\n")
            write(os.path.join(root, ".hidden", "Secret.md"), "[[index]]\n")
            labels, edges, community, _, _, _ = load_folder(root, ["_archive", "skip-*"])
            assert list(labels) == ["Ghost", "Page One", "index", "sub/Deep"], f"input B nodes: {list(labels)}"
            assert edges == [("Page One", "index"), ("Page One", "sub/Deep"), ("index", "sub/Deep")], f"input B edges: {edges}"
            assert community is None
            checks += 1
            # 4. The layout is deterministic; every node and every region centre lies on its hemisphere.
            graph = load_graph_json(pb)
            assert build_scene(graph, "t", "b") == build_scene(graph, "t", "b"), "two runs gave different scenes"
            for n in scene_b["nodes"] + [dict(zip("xyz", r["center"]), id=r["name"]) for r in scene_b["regions"]]:
                hc = (-SHIFT * R if n["x"] < 0 else SHIFT * R, 0.0, 0.0)
                q = math.sqrt(sum(((n[a] - hc[k]) / (SEMI[k] * R)) ** 2 for k, a in enumerate("xyz")))
                assert abs(q - 1) < 0.01, f"{n['id']} lies off the brain surface: {q:.3f}"
            checks += 1
            # 5. Five output files are written.
            out = os.path.join(tmp, "out")
            paths = write_outputs(scene_b, out)
            assert sorted(os.path.basename(p) for p in paths) == ["CORE.md", "REGIONS.md", "brain.html", "brain.json",
                                                                  "brain.svg"]
            assert all(os.path.getsize(p) > 0 for p in paths), "an output file is empty"
            with open(os.path.join(out, "brain.json"), encoding="utf-8") as f:
                assert json.load(f) == scene_b, "brain.json differs from the scene"
            checks += 1
            # 6. brain.html embeds valid JSON, also when a label tries to close the <script> element.
            evil = os.path.join(tmp, "evil.json")
            write(evil, json.dumps({"nodes": [{"id": "x", "label": "</script><b>x & y"}, {"id": "y"}],
                                    "links": [{"source": "x", "target": "y"}]}))
            for scene in (scene_b, build_scene(load_graph_json(evil), "<i>t</i>", "evil")):
                page = render_html(scene)
                m = re.search(r'<script id="graph-data" type="application/json">(.*?)</script>', page, re.S)
                assert m and json.loads(m.group(1)) == scene, "embedded JSON does not match the scene"
                assert page.count("</script>") == 3 and "<i>" not in page, "embedded text escaped its element"
            checks += 1
            # 7. The legend holds at most 24 regions; smaller regions merge into "other".
            pc = os.path.join(tmp, "pairs.json")
            write(pc, json.dumps({"nodes": [{"id": i} for i in range(60)],
                                  "links": [{"source": 2 * i, "target": 2 * i + 1} for i in range(30)]}))
            scene_c = build_scene(load_graph_json(pc), "pairs", "pairs")
            assert len(scene_c["regions"]) == MAX_REGIONS, f"{len(scene_c['regions'])} regions"
            assert scene_c["regions"][-1]["name"] == "other" and scene_c["regions"][-1]["size"] == 14
            left = sum(1 for n in scene_c["nodes"] if n["x"] < 0)
            assert left == 30 and scene_c["regions"][-1]["hemisphere"] == "both", f"unbalanced hemispheres: {left} of 60 left"
            checks += 1
            # 8. Time, the fourth dimension: git log parsing, the "time" field, the Time section of REGIONS.md.
            log = "\x00300\n\nb.md\n\n\x00200\n\na.md\nb.md\n\"q\\\"x.md\"\n\n\x00100\n\na.md\n"
            assert parse_git_log(log) == {"b.md": (200, 300), "a.md": (100, 200)}, f"git log: {parse_git_log(log)}"
            assert parse_time("2026-01-02") == int(datetime(2026, 1, 2).timestamp()) and parse_time(5) == 5
            assert parse_time("soon") is None and parse_time(True) is None and parse_time(float("nan")) is None
            assert parse_time(1e20) is None and parse_time(float("inf")) is None, "a time outside the calendar passed"
            pt = os.path.join(tmp, "timed.json")
            write(pt, json.dumps({"nodes": [{"id": "a", "time": 0}, {"id": "b", "time": 40 * 86400}, {"id": "c"}],
                                  "links": [{"source": "a", "target": "b"}]}))
            scene_t = build_scene(load_graph_json(pt), "timed", "t")
            assert [n.get("t") for n in scene_t["nodes"]] == [0, 40 * 86400, None], f"times: {scene_t['nodes']}"
            md = render_regions_md(scene_t)
            assert "## Time" in md and "| growing |" in md and "## Time" not in render_regions_md(scene_b), md
            checks += 1
            # 9. CORE.md: weight (1 + degree) * 2^(-d/30), d = days behind the newest change (0 without a time);
            #    ties go to the label, then the id. Node ids sort in another order than the labels.
            pk = os.path.join(tmp, "core.json")
            write(pk, json.dumps({"nodes": [
                {"id": "h", "label": "Hub", "time": 0}, {"id": "m", "label": "Mid", "time": 30 * 86400},
                {"id": "z", "label": "New", "time": 60 * 86400}, {"id": "s2", "label": "Same"}, {"id": "s1", "label": "Same"}],
                "links": [{"source": "h", "target": t} for t in ("m", "z", "s1")] + [{"source": "m", "target": "s2"}]}))
            scene_k = build_scene(load_graph_json(pk), "core", "core")
            order = [(n["id"], w) for n, w in core_nodes(scene_k)]
            assert order == [("z", 2.0), ("s1", 2.0), ("s2", 2.0), ("m", 1.5), ("h", 1.0)], f"CORE.md order: {order}"
            rows = re.findall(r"^\| (\d+) \| (.+?) \| .* \| ([\d.]+) \|$", render_core_md(scene_k), re.M)
            assert rows == [("1", "New", "2.00"), ("2", "Same", "2.00"), ("3", "Same", "2.00"), ("4", "Mid", "1.50"),
                            ("5", "Hub", "1.00")], f"CORE.md rows: {rows}"
            assert len(re.findall(r"^\| \d+ \|", render_core_md(scene_c), re.M)) == CORE_SIZE, "CORE.md size"
            checks += 1
            # 10. Graph metrics: two 5-cliques and 1 bridge give m = 21, L = 10 and 10, D = 21 and 21,
            #     Q = 20/21 - 2 * (21/42)^2 = 0.4524; a graph without edges has Q = 0.
            metrics = graph_metrics(scene_b)
            assert metrics[:3] == (1, 10, 0) and abs(metrics[3] - (20 / 21 - 0.5)) < 1e-12, f"metrics: {metrics}"
            assert "Q = 0.4524" in render_regions_md(scene_b), "REGIONS.md has no modularity"
            pe = os.path.join(tmp, "loose.json")
            write(pe, json.dumps({"nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}))
            metrics = graph_metrics(build_scene(load_graph_json(pe), "loose", "loose"))
            assert metrics == (3, 1, 3, 0.0), f"metrics without edges: {metrics}"
            checks += 1
            # 11. CORE.md of a folder: the first paragraph skips frontmatter, headings and code blocks, stops at
            #     300 characters and stays out of brain.html and brain.json.
            notes = os.path.join(tmp, "para")
            write(os.path.join(notes, "a.md"), "---\ntitle: A\n---\n# Title\n\n```\nnot this\n```\n\n## Part\n"
                  "First line\nsecond | line [[b]].\n\nSecond paragraph.\n")
            write(os.path.join(notes, "b.md"), "word " * 100)
            out = os.path.join(tmp, "para-out")
            run(notes, out)
            with open(os.path.join(out, "CORE.md"), encoding="utf-8") as f:
                core = f.read()
            assert "| First line second \\| line [[b]]. |" in core and "not this" not in core, core
            long = first_paragraph("word " * 100)
            assert len(long) <= PARAGRAPH_CHARS and long.endswith("…") and long in core, long
            tags_first = first_paragraph("#guide #meta/page\n\nReal text.")
            assert tags_first == "Real text.", f"a block of tags only is not a paragraph: {tags_first!r}"
            for name in ("brain.html", "brain.json"):
                with open(os.path.join(out, name), encoding="utf-8") as f:
                    assert "First line" not in f.read(), f"the first paragraph leaked into {name}"
            checks += 1
            # 12. brain-spin.svg: one full turn in SPIN_SECONDS; a node in front is larger and more opaque than behind.
            spin = render_spin_svg(scene_b)
            assert spin.count("<circle") == len(scene_b["nodes"]), "brain-spin.svg needs 1 circle per node"
            assert f'dur="{SPIN_SECONDS}s"' in spin and 'repeatCount="indefinite"' in spin, "brain-spin.svg does not loop"
            first = re.search(r"<circle[^>]*>(.*?)</circle>", spin, re.S).group(1)
            radii = [float(v) for v in re.search(r'attributeName="r"[^>]*values="([^"]+)"', first).group(1).split(";")]
            alpha = [float(v) for v in re.search(r'attributeName="opacity"[^>]*values="([^"]+)"', first).group(1).split(";")]
            near, far = radii.index(max(radii)), radii.index(min(radii))
            assert radii[near] > radii[far] and alpha[near] > alpha[far], "depth does not change size and opacity"
            assert len(radii) == SPIN_FRAMES + 1 and radii[0] == radii[-1], "the turn does not close"
            assert len(spin.encode()) <= 500_000, "brain-spin.svg is larger than 500 kB"
            sel = spin_edges(scene_b)
            hub = min(scene_b["nodes"], key=lambda n: (-n["degree"], n["label"], n["id"]))["id"]
            region = {n["id"]: n["region"] for n in scene_b["nodes"]}
            assert sel and len(sel) <= SPIN_EDGES and all(
                region[e["source"]] == region[e["target"]] and hub not in (e["source"], e["target"]) for e in sel), sel
            assert spin.count("<line") == len(sel) == spin.count('attributeName="stroke-opacity"'), "edge fade missing"
            assert spin.count("<ellipse") == 2 and spin.count('type="rotate"') == 2, "hemisphere outlines do not turn"
            checks += 1
            # 13. brain.stl: ASCII STL of both hemispheres and a tetrahedron per top node, at most 100 kB.
            stl = render_stl(scene_b)
            facets = stl.count("facet normal")
            assert stl.startswith("solid neurophify\n") and stl.endswith("endsolid neurophify\n"), "not an ASCII STL solid"
            assert facets == 2 * HEMI_FACETS + 4 * min(STL_NODES, len(scene_b["nodes"])), f"{facets} facets"
            assert stl.count("vertex") == 3 * facets and len(stl.encode()) <= 100_000, "STL vertices or size"
            checks += 1
    except AssertionError as e:
        print(f"selftest: FAILED after {checks} checks: {e}", file=sys.stderr)
        return 1
    print(f"selftest: ok ({checks} checks)")
    return 0


# ---------------------------------------------------------------- CLI

EPILOG = """examples:
  neurophify.py graphify-out/graph.json
  neurophify.py notes/ --exclude '_archive' --exclude 'drafts/*' --title "My notes"
  neurophify.py --selftest

input:
  A file is read as a graphify graph.json (networkx node-link: "nodes" with id, label,
  community; "links" or "edges" with source, target). A folder is read as Markdown:
  each .md file is a node, [[page]], [[page|alias]] and [text](file.md) are edges.
  Hidden folders and the output folder are skipped.

time (the fourth dimension):
  A folder inside a git repository gives each page its first and last commit; outside git,
  the file modification time. A graph.json node may carry "time": ISO 8601 or epoch seconds.

consolidation:
  CORE.md lists the 20 nodes with the largest weight (1 + degree) * 2^(-d/30), where d is the
  number of days between the last change of the node and the newest change in the graph.
  For a folder, each entry adds the first paragraph of the page. REGIONS.md ends with graph
  metrics: connected components, nodes without edges, modularity Q of the regions.

files for a README:
  --spin also writes brain-spin.svg: the brain turning around its vertical axis (SMIL, no script).
  --stl also writes brain.stl: an ASCII STL of both hemispheres and the 40 nodes with the most
  edges. GitHub shows it as an interactive 3D model in a fenced code block marked stl.

exit codes: 0 done, 1 selftest failed, 2 bad usage or unreadable input."""


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="neurophify.py", epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Draw a knowledge graph as a 3D brain: regions on two hemispheres, "
                    "written as brain.html, brain.svg, brain.json, REGIONS.md and CORE.md.")
    parser.add_argument("input", nargs="?", help="graphify graph.json, or a folder of Markdown files")
    parser.add_argument("--out", default="neurophify-out", metavar="DIR", help="output folder (default: neurophify-out)")
    parser.add_argument("--title", metavar="TEXT", help="title of the page and the picture (default: input name)")
    parser.add_argument("--exclude", action="append", default=[], metavar="PATTERN",
                        help="folder input: skip files and folders whose relative path matches "
                             "this fnmatch pattern; repeatable")
    parser.add_argument("--spin", action="store_true", help="also write brain-spin.svg, the brain turning in 3D")
    parser.add_argument("--stl", action="store_true", help="also write brain.stl, a 3D model of the brain")
    parser.add_argument("--selftest", action="store_true", help="run the built-in checks and exit")
    parser.add_argument("--version", action="version", version=f"neurophify {VERSION}")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.input:
        parser.print_help(sys.stderr)
        return 2
    try:
        paths, scene = run(args.input, args.out, args.title, args.exclude, args.spin, args.stl)
    except InputError as e:
        print(f"neurophify: error: {e}", file=sys.stderr)
        return 2
    print(f'neurophify: {len(scene["nodes"])} nodes, {len(scene["edges"])} edges, '
          f'{len(scene["regions"])} regions ({scene["method"]})')
    print("\n".join(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
