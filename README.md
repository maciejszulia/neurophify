# neurophify

neurophify draws a knowledge graph as a 3D brain: it reads a graphify `graph.json` or a folder of Markdown notes, groups the nodes into regions and lays the regions out on two hemispheres.

[Polska wersja](README.pl.md)

## Demo

![SilverBullet documentation drawn by neurophify: 313 pages on two hemispheres, coloured by region](docs/demo/brain.svg)

The picture is [`docs/demo/brain.svg`](docs/demo/brain.svg), made from the documentation of SilverBullet. The interactive 3D version is [`docs/demo/brain.html`](docs/demo/brain.html): GitHub shows an HTML file as source code, so clone the repository and open the file in a browser. The text report is [`docs/demo/REGIONS.md`](docs/demo/REGIONS.md).

## Results

| Input | Nodes | Edges | Regions | Run time |
|---|---|---|---|---|
| SilverBullet `docs/` folder, Markdown | 313 | 1460 | 24 | 0.40 s to 0.43 s (3 runs) |
| graphify `graph.json` of a TypeScript code base | 2731 | 4386 | 24 | 1.10 s |

Measured on 2026-11-15 with the shell's `time python3 neurophify.py ...` on a ThinkPad T470p (Intel Core i7-7700HQ), Python 3.14.8. Two runs on the same input write byte-identical files.

## Quick start

```bash
git clone https://github.com/maciejszulia/neurophify.git
cd neurophify
python3 neurophify.py --selftest
python3 neurophify.py . --title "This repository"
```

The last command draws the Markdown files of this repository. To rebuild the demo from the SilverBullet documentation:

```bash
git clone --depth 1 https://github.com/silverbulletmd/silverbullet.git ../silverbullet
python3 neurophify.py ../silverbullet/docs --title "SilverBullet docs" --out demo-out
```

The tool needs Python 3.11 or newer and nothing outside the standard library. Each run writes four files to `neurophify-out/` (change it with `--out DIR`):

| File | Content |
|---|---|
| `brain.html` | Interactive 3D view: drag to rotate, scroll to zoom, hover a node to read its name, click a node to fly to it. |
| `brain.svg` | Static picture of the same scene, seen from the same direction. |
| `brain.json` | Nodes with positions and regions, edges, regions. |
| `REGIONS.md` | Each region with its size, its 5 central nodes and its bridges to other regions. |

Other inputs:

```bash
python3 neurophify.py graphify-out/graph.json                       # a graph written by graphify
python3 neurophify.py notes/ --exclude '_archive' --exclude 'drafts/*' --title "My notes"
python3 neurophify.py --help                                        # all options, exit codes
```

`SKILL.md` makes the repository usable as an agent skill: link the folder into your skills directory and ask for "/neurophify" or "3D graph".

## How it works

![How neurophify works: input, regions, 3D layout, output files](docs/diagrams/how-it-works.svg)

1. Load. A file is read as a graphify `graph.json` in the networkx node-link format: `nodes` with `id`, `label` and `community`, and `links` or `edges` with `source` and `target`. A folder is read as Markdown: each `.md` file is a node, and `[[page]]`, `[[page|alias]]` and `[text](file.md)` links are edges. Links inside code blocks, hidden folders and the output folder are skipped.
2. Regions. The `community` field of `graph.json` defines the regions. Without it, label propagation finds them (seed 42, at most 50 iterations); the 5 % of nodes with the most edges take a region but do not vote, so an index page does not pull every topic into one region. The legend keeps the 23 largest regions and merges the rest into "other".
3. Layout. Each hemisphere is an ellipsoid. Region centres lie on its surface along a Fibonacci spiral, and each region takes the surface points nearest its centre, as many as it has nodes, so it forms one patch. Inside the patch a force layout keeps linked nodes close and puts hubs near the centre.
4. Output. `brain.html` embeds the data and pins every node to its position (`fx`, `fy`, `fz`) in [3d-force-graph](https://github.com/vasturiano/3d-force-graph) 1.80.1. `brain.svg` projects the same positions from the same camera direction. Node size grows with the number of edges, and the 10 nodes with the most edges carry a permanent label.

## Relation to graphify

graphify builds a knowledge graph from code and documents and writes `graphify-out/graph.json`. neurophify reads that file and adds the third dimension. The code of graphify is not part of this repository, and neurophify runs without graphify: a folder of Markdown files is enough.

## Limits

- Regions from label propagation are a heuristic: with another seed, region borders move.
- The 3D view in `brain.html` loads 3d-force-graph from jsDelivr and needs a network connection; `brain.svg` and `REGIONS.md` work offline.
- In a region with more than 770 nodes the force layout is skipped and the hubs take the points nearest the centre.
- The legend shows at most 24 regions. "other" collects the smaller ones and can span both hemispheres.
- Edges are drawn without direction; edge types from `graph.json` are not shown.
- Only `.md` files are nodes; a link to a page that does not exist is dropped.

## License and author

MIT, see [LICENSE](LICENSE). Author: Maciej Szulia.

Demo data: the `docs/` folder of [SilverBullet](https://github.com/silverbulletmd/silverbullet) at commit `a0ab7e9d`, read on 2026-11-15, MIT license, Copyright 2022 Zef Hemel. `docs/demo/` holds page names and links derived from that folder.
