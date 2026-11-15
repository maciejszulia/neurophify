# Regions: SilverBullet docs

313 nodes, 1460 edges, 24 regions. Regions come from the label propagation (seed 42, at most 50 iterations, top 5 % hubs do not vote). 728 edges are bridges between two regions.

| # | Region | Nodes | Hemisphere | Bridge edges |
|---|---|---|---|---|
| 1 | CHANGELOG | 77 | left | 303 |
| 2 | API | 34 | right | 240 |
| 3 | Link | 29 | right | 151 |
| 4 | Object Index | 27 | right | 118 |
| 5 | Object | 19 | left | 114 |
| 6 | Space Style | 18 | right | 62 |
| 7 | Page Picker | 15 | left | 81 |
| 8 | Tag/relation | 13 | right | 46 |
| 9 | Reference/Space Lua and APIs | 8 | left | 54 |
| 10 | Space Lua/Standard Library | 7 | left | 12 |
| 11 | Architecture/Client | 7 | right | 23 |
| 12 | API/widget | 5 | left | 34 |
| 13 | Extensions | 5 | right | 30 |
| 14 | API/auth | 4 | left | 10 |
| 15 | Workbench/Maintenance | 4 | right | 13 |
| 16 | Command | 4 | left | 27 |
| 17 | Plugs/Development/Reference | 3 | right | 13 |
| 18 | Service | 3 | left | 9 |
| 19 | Space Lua/Page Lua | 3 | right | 7 |
| 20 | Page Decorations | 3 | left | 19 |
| 21 | Graph View | 3 | right | 15 |
| 22 | Library/silverbulletmd/Themes/Classic | 3 | left | 0 |
| 23 | View | 3 | right | 35 |
| 24 | other | 16 | both | 40 |

## 1. CHANGELOG

- Nodes: 77; left hemisphere; colour `#3987e5`.
- Central nodes (links inside the region): Reference/SilverBullet Features (28), CHANGELOG (26), Guide/Server Setup (20), Dashboard (19), Space Lua (17).
- Bridges: 303 edges to 22 regions.
  - API: 65 edges, for example API/command -- API; API/crypto -- API; API/markdown -- API.
  - Link: 44 edges, for example CHANGELOG -- API/syntax; Architecture -- Architecture/Editor; CHANGELOG -- Link.
  - Object Index: 37 edges, for example Architecture -- ADR; Reference/Technical Reference -- ADR; Architecture -- ADR/001 Offline-First PWA.
  - Tag/relation: 21 edges, for example CLI -- API/identity; CHANGELOG -- API/index; Account -- Identity.
  - Page Picker: 18 edges, for example CHANGELOG -- API/system; CHANGELOG -- Page Picker; CHANGELOG -- Tag Picker.

## 2. API

- Nodes: 34; right hemisphere; colour `#d95926`.
- Central nodes (links inside the region): API (13), Workbench (10), Repository (10), Library (9), Share (9).
- Bridges: 240 edges to 22 regions.
  - CHANGELOG: 65 edges, for example API -- API/command; API -- API/crypto; API -- API/markdown.
  - Object: 24 edges, for example API -- API/object; API -- API/taskState; API/tag -- API/object.
  - Space Style: 23 edges, for example Library -- ADR/014 Themes as Pages; API -- API/config; Schema -- API/config.
  - Link: 19 edges, for example API -- API/syntax; API/share -- Link; Tool Page -- API/syntax.
  - Object Index: 16 edges, for example Library -- ADR/004 Federation; Workbench/Configuration -- ADR/011 Link Resolution by Name; API -- API/string.

## 3. Link

- Nodes: 29; right hemisphere; colour `#199e70`.
- Central nodes (links inside the region): Markdown (16), Markdown/Extensions (10), Link (8), Reference/Concepts (8), Page (8).
- Bridges: 151 edges to 15 regions.
  - CHANGELOG: 44 edges, for example API/syntax -- CHANGELOG; Architecture/Editor -- Architecture; Link -- CHANGELOG.
  - Page Picker: 26 edges, for example Link -- Aspiring Pages; Page -- Aspiring Pages; Reference/Concepts -- Aspiring Pages.
  - Object: 24 edges, for example Task -- API/object; Markdown/Basics -- API/taskState; Task -- API/taskState.
  - API: 19 edges, for example API/syntax -- API; Link -- API/share; API/syntax -- Tool Page.
  - Object Index: 14 edges, for example Live Preview -- ADR/005 Space Lua; Document -- ADR/007 Core Application Logic on the Client; Link -- ADR/011 Link Resolution by Name.

## 4. Object Index

- Nodes: 27; right hemisphere; colour `#c98500`.
- Central nodes (links inside the region): ADR (16), Zef Hemel (15), ADR/007 Core Application Logic on the Client (12), ADR/003 Indexed Object Graph (11), ADR/001 Offline-First PWA (10).
- Bridges: 118 edges to 18 regions.
  - CHANGELOG: 37 edges, for example ADR -- Architecture; ADR -- Reference/Technical Reference; ADR/001 Offline-First PWA -- Architecture.
  - API: 16 edges, for example ADR/004 Federation -- Library; ADR/011 Link Resolution by Name -- Workbench/Configuration; API/string -- API.
  - Link: 14 edges, for example ADR/005 Space Lua -- Live Preview; ADR/007 Core Application Logic on the Client -- Document; ADR/011 Link Resolution by Name -- Link.
  - Object: 10 edges, for example ADR/003 Indexed Object Graph -- Object; ADR/003 Indexed Object Graph -- Tag; ADR/003 Indexed Object Graph -- Tag/page.
  - Tag/relation: 7 edges, for example ADR/003 Indexed Object Graph -- API/index; ADR/003 Indexed Object Graph -- Tag/relation; Object Index -- API/index.

## 5. Object

- Nodes: 19; left hemisphere; colour `#d55181`.
- Central nodes (links inside the region): Object (12), Guide/Add Structure and Query (12), Tag (11), Frontmatter (7), Attribute (7).
- Bridges: 114 edges to 15 regions.
  - API: 24 edges, for example API/object -- API; API/taskState -- API; API/object -- API/tag.
  - Link: 24 edges, for example API/object -- Task; API/taskState -- Markdown/Basics; API/taskState -- Task.
  - CHANGELOG: 17 edges, for example API/object -- CHANGELOG; API/taskState -- CHANGELOG; Attribute -- Reference/SilverBullet Features.
  - Page Picker: 11 edges, for example Attribute -- Guide/Best Practices; Tag -- Folder; Frontmatter -- Guide/Best Practices.
  - Object Index: 10 edges, for example Object -- ADR/003 Indexed Object Graph; Tag -- ADR/003 Indexed Object Graph; Tag/page -- ADR/003 Indexed Object Graph.

## 6. Space Style

- Nodes: 18; right hemisphere; colour `#0ca30c`.
- Central nodes (links inside the region): Theming (11), Space Style (9), Fonts (8), Theming/Creating a Theme (8), Theming/Variables (7).
- Bridges: 62 edges to 11 regions.
  - API: 23 edges, for example ADR/014 Themes as Pages -- Library; API/config -- API; API/config -- Schema.
  - CHANGELOG: 17 edges, for example API/config -- CHANGELOG; API/theme -- CHANGELOG; Space Style -- CHANGELOG.
  - Link: 5 edges, for example Space Style -- API/syntax; Fonts -- Markdown/Fenced Code Block; Markdown/Admonition -- Markdown/Extensions.
  - Object Index: 5 edges, for example ADR/014 Themes as Pages -- ADR/005 Space Lua; ADR/014 Themes as Pages -- ADR/012 Tooling Lives in Library; ADR/014 Themes as Pages -- Zef Hemel.
  - Object: 3 edges, for example API/config -- Space Lua/Conventions; Tag/meta/theme -- Frontmatter; Tag/meta/theme -- Tag/page.

## 7. Page Picker

- Nodes: 15; left hemisphere; colour `#9085e9`.
- Central nodes (links inside the region): Guide/Finding Content (7), Page Picker (6), Guide/Best Practices (5), Guide/Find and Connect Pages (5), File Tree (4).
- Bridges: 81 edges to 13 regions.
  - Link: 26 edges, for example Aspiring Pages -- Link; Aspiring Pages -- Page; Aspiring Pages -- Reference/Concepts.
  - CHANGELOG: 18 edges, for example API/system -- CHANGELOG; Page Picker -- CHANGELOG; Tag Picker -- CHANGELOG.
  - Object: 11 edges, for example Guide/Best Practices -- Attribute; Folder -- Tag; Guide/Best Practices -- Frontmatter.
  - API: 8 edges, for example API/system -- API; File Tree -- Tool Page; Guide/Best Practices -- Library.
  - Object Index: 6 edges, for example Aspiring Pages -- ADR/011 Link Resolution by Name; API/system -- Guide/When Results Update; Aspiring Pages -- Object Index.

## 8. Tag/relation

- Nodes: 13; right hemisphere; colour `#e66767`.
- Central nodes (links inside the region): Identity (7), At-Mention (7), Tag/relation (6), Authorship (6), Recipient (5).
- Bridges: 46 edges to 10 regions.
  - CHANGELOG: 21 edges, for example API/identity -- CLI; API/index -- CHANGELOG; Identity -- Account.
  - API: 7 edges, for example API/datastore -- API; API/identity -- API; API/index -- API.
  - Object Index: 7 edges, for example API/index -- ADR/003 Indexed Object Graph; Tag/relation -- ADR/003 Indexed Object Graph; API/index -- Object Index.
  - Object: 5 edges, for example API/index -- API/object; Tag/relation -- Object; Tag/identity -- Tag.
  - Link: 1 edges, for example Workbench/Overview -- Document.

## 9. Reference/Space Lua and APIs

- Nodes: 8; left hemisphere; colour `#7eb1ee`.
- Central nodes (links inside the region): Event (5), Reference/Space Lua and APIs (4), Widget (4), Virtual Pages (3), Space Lua/DOM (3).
- Bridges: 54 edges to 18 regions.
  - CHANGELOG: 11 edges, for example Event -- CHANGELOG; Virtual Pages -- CHANGELOG; Completion -- Reference/SilverBullet Features.
  - API: 8 edges, for example API/dom -- API; API/event -- API; Reference/Space Lua and APIs -- API.
  - API/widget: 5 edges, for example API/dom -- API/widget; API/dom -- API/widgets; Widget -- API/icon.
  - Object Index: 3 edges, for example Event -- Object Index; Reference/Space Lua and APIs -- Plugs; Reference/Space Lua and APIs -- Space Lua/Integrated Query.
  - Object: 3 edges, for example Completion -- Frontmatter; Event -- Object; Reference/Space Lua and APIs -- Space Lua/Conventions.

## 10. Space Lua/Standard Library

- Nodes: 7; left hemisphere; colour `#e69372`.
- Central nodes (links inside the region): Space Lua/Standard Library (5), Space Lua/JavaScript Interop (2), API/js (1), API/encoding (1), API/global (1).
- Bridges: 12 edges to 4 regions.
  - API: 6 edges, for example API/encoding -- API; API/global -- API; API/js -- API.
  - CHANGELOG: 2 edges, for example Space Lua/JavaScript Interop -- Space Lua; Space Lua/Standard Library -- Space Lua.
  - Object Index: 2 edges, for example Space Lua/Standard Library -- API/string; Space Lua/Standard Library -- API/table.
  - Reference/Space Lua and APIs: 2 edges, for example Space Lua/JavaScript Interop -- Reference/Space Lua and APIs; Space Lua/Standard Library -- Reference/Space Lua and APIs.

## 11. Architecture/Client

- Nodes: 7; right hemisphere; colour `#6ac0a2`.
- Central nodes (links inside the region): Architecture/Client (6), Architecture/Syscalls (6), Architecture/Datastore (2), Architecture/Plugs (2), Architecture/Services (2).
- Bridges: 23 edges to 7 regions.
  - CHANGELOG: 13 edges, for example Architecture/Client -- Architecture; Architecture/Datastore -- Architecture; Architecture/Events -- Architecture.
  - API: 3 edges, for example Architecture/Space Lua -- API; Architecture/Plugs -- Library; Architecture/Services -- Share.
  - Link: 2 edges, for example Architecture/Client -- Architecture/Editor; Architecture/Syscalls -- Architecture/Editor.
  - Object Index: 2 edges, for example Architecture/Datastore -- Object Index; Architecture/Plugs -- Plugs.
  - Tag/relation: 1 edges, for example Architecture/Datastore -- API/datastore.

## 12. API/widget

- Nodes: 5; left hemisphere; colour `#dcb059`.
- Central nodes (links inside the region): API/widget (4), API/view (2), API/icon (2), API/widgets (1), API/search (1).
- Bridges: 34 edges to 12 regions.
  - API: 9 edges, for example API/icon -- API; API/search -- API; API/view -- API.
  - CHANGELOG: 6 edges, for example API/search -- Search; API/search -- Space Lua; API/view -- CHANGELOG.
  - Reference/Space Lua and APIs: 5 edges, for example API/widget -- API/dom; API/widgets -- API/dom; API/icon -- Widget.
  - Link: 2 edges, for example API/widget -- API/syntax; API/widget -- Live Preview.
  - Object Index: 2 edges, for example API/widget -- Baked Sections; API/widget -- Object Index.

## 13. Extensions

- Nodes: 5; right hemisphere; colour `#e48ead`.
- Central nodes (links inside the region): Page Template (3), Slash Templates (3), Template (3), Extensions (2), API/template (1).
- Bridges: 30 edges to 9 regions.
  - API: 11 edges, for example API/template -- API; Slash Templates -- API/markupBar; Slash Templates -- API/slashCommand.
  - CHANGELOG: 3 edges, for example Page Template -- CHANGELOG; Extensions -- Space Lua; Template -- Space Lua.
  - Object Index: 3 edges, for example Extensions -- Plugs; Template -- Guide/When Results Update; Template -- Space Lua/Integrated Query.
  - Space Style: 3 edges, for example Extensions -- Space Style; Page Template -- Guide/Make it your own; Slash Templates -- Guide/Make it your own.
  - Reference/Space Lua and APIs: 3 edges, for example Extensions -- Reference/Space Lua and APIs; Extensions -- Virtual Pages; Template -- Reference/Space Lua and APIs.

## 14. API/auth

- Nodes: 4; left hemisphere; colour `#61c361`.
- Central nodes (links inside the region): API/auth (3), API/github (2), API/oauth (2), API/sbShare (1).
- Bridges: 10 edges to 2 regions.
  - API: 8 edges, for example API/auth -- API; API/github -- API; API/oauth -- API.
  - CHANGELOG: 2 edges, for example API/auth -- CHANGELOG; API/github -- CHANGELOG.

## 15. Workbench/Maintenance

- Nodes: 4; right hemisphere; colour `#b7b0f1`.
- Central nodes (links inside the region): Workbench/Maintenance (2), Tag/aspiring-page (2), API/space (1), Tag/ambiguous-link (1).
- Bridges: 13 edges to 6 regions.
  - CHANGELOG: 4 edges, for example API/space -- CHANGELOG; API/space -- CLI; Workbench/Maintenance -- CHANGELOG.
  - API: 3 edges, for example API/space -- API; Workbench/Maintenance -- Library; Workbench/Maintenance -- Workbench.
  - Link: 2 edges, for example Tag/ambiguous-link -- Link; Workbench/Maintenance -- Link.
  - Object: 2 edges, for example Tag/ambiguous-link -- Tag; Tag/aspiring-page -- Tag.
  - Object Index: 1 edges, for example Tag/ambiguous-link -- ADR/011 Link Resolution by Name.

## 16. Command

- Nodes: 4; left hemisphere; colour `#ef9c9c`.
- Central nodes (links inside the region): Command (3), Keyboard Shortcuts (3), Command Palette (2), Vim (2).
- Bridges: 27 edges to 13 regions.
  - CHANGELOG: 8 edges, for example Keyboard Shortcuts -- CHANGELOG; Vim -- CHANGELOG; Command -- Local Space.
  - API: 3 edges, for example Command -- Workbench/Configuration; Command Palette -- Workbench/Configuration; Keyboard Shortcuts -- Workbench/Configuration.
  - Link: 2 edges, for example Command Palette -- Guide/My First Markdown Page; Keyboard Shortcuts -- Outlines.
  - Reference/Space Lua and APIs: 2 edges, for example Command -- Reference/Space Lua and APIs; Vim -- Event.
  - API/widget: 2 edges, for example Command -- API/view; Command -- API/widgets.

## 17. Plugs/Development/Reference

- Nodes: 3; right hemisphere; colour `#b0cff5`.
- Central nodes (links inside the region): Plugs/Development/Reference (2), API/asset (1), API/mq (1).
- Bridges: 13 edges to 7 regions.
  - API: 4 edges, for example API/asset -- API; API/mq -- API; Plugs/Development/Reference -- API/slashCommand.
  - CHANGELOG: 3 edges, for example Plugs/Development/Reference -- CHANGELOG; Plugs/Development/Reference -- Reference/Technical Reference; Plugs/Development/Reference -- Space Lua.
  - other: 2 edges, for example Plugs/Development/Reference -- Plugs/Development; Plugs/Development/Reference -- Plugs/Development/Architecture.
  - Reference/Space Lua and APIs: 1 edges, for example Plugs/Development/Reference -- Event.
  - Command: 1 edges, for example Plugs/Development/Reference -- Command.

## 18. Service

- Nodes: 3; left hemisphere; colour `#f0bda8`.
- Central nodes (links inside the region): Service (2), API/service (1), API/capture (1).
- Bridges: 9 edges to 4 regions.
  - API: 3 edges, for example API/capture -- API; API/service -- API; API/service -- API/share.
  - Reference/Space Lua and APIs: 3 edges, for example API/service -- Event; Service -- Event; Service -- Reference/Space Lua and APIs.
  - CHANGELOG: 2 edges, for example API/service -- Workbench/Console; Service -- CHANGELOG.
  - Architecture/Client: 1 edges, for example Service -- Architecture/Services.

## 19. Space Lua/Page Lua

- Nodes: 3; right hemisphere; colour `#a3d8c6`.
- Central nodes (links inside the region): Space Lua/Page Lua (2), API/pageVars (1), Examples/Budget (1).
- Bridges: 7 edges to 5 regions.
  - CHANGELOG: 3 edges, for example Space Lua/Page Lua -- CHANGELOG; Space Lua/Page Lua -- Space Lua; Space Lua/Page Lua -- Workbench/Console.
  - API: 1 edges, for example API/pageVars -- API.
  - Object Index: 1 edges, for example Space Lua/Page Lua -- Guide/When Results Update.
  - Reference/Space Lua and APIs: 1 edges, for example Space Lua/Page Lua -- Reference/Space Lua and APIs.
  - API/widget: 1 edges, for example Space Lua/Page Lua -- API/widget.

## 20. Page Decorations

- Nodes: 3; left hemisphere; colour `#e9ce99`.
- Central nodes (links inside the region): Page Decorations (2), Anything Picker (1), Library/Website/Doc Examples (1).
- Bridges: 19 edges to 10 regions.
  - API: 5 edges, for example Library/Website/Doc Examples -- API/tag; Page Decorations -- API/tag; Anything Picker -- Tool Page.
  - CHANGELOG: 3 edges, for example Anything Picker -- Reference/SilverBullet Features; Page Decorations -- CHANGELOG; Page Decorations -- Publishing.
  - Object: 2 edges, for example Page Decorations -- Frontmatter; Page Decorations -- Tag/page.
  - Page Picker: 2 edges, for example Anything Picker -- Page Picker; Page Decorations -- Page Picker.
  - View: 2 edges, for example Anything Picker -- View; Page Decorations -- View.

## 21. Graph View

- Nodes: 3; right hemisphere; colour `#eeb9cd`.
- Central nodes (links inside the region): Graph View (2), X-Ray (1), Object Graph (1).
- Bridges: 15 edges to 8 regions.
  - CHANGELOG: 4 edges, for example Object Graph -- CHANGELOG; X-Ray -- CHANGELOG; Graph View -- Reference/SilverBullet Features.
  - Object: 4 edges, for example Graph View -- Object; Graph View -- Tag; X-Ray -- Object.
  - Page Picker: 2 edges, for example Graph View -- Aspiring Pages; Graph View -- Guide/Find and Connect Pages.
  - API: 1 edges, for example X-Ray -- API/tag.
  - Object Index: 1 edges, for example Graph View -- ADR/003 Indexed Object Graph.

## 22. Library/silverbulletmd/Themes/Classic

- Nodes: 3; left hemisphere; colour `#9eda9e`.
- Central nodes (links inside the region): Library/silverbulletmd/Themes/Classic (2), Library/silverbulletmd/Themes/Classic/Dark (2), Library/silverbulletmd/Themes/Classic/Light (2).
- Bridges: none.

## 23. View

- Nodes: 3; right hemisphere; colour `#d3cef6`.
- Central nodes (links inside the region): View (2), Linked Mention (2), Linked Tasks (2).
- Bridges: 35 edges to 13 regions.
  - CHANGELOG: 7 edges, for example Linked Mention -- CHANGELOG; View -- CHANGELOG; Linked Mention -- Publishing.
  - Link: 5 edges, for example Linked Mention -- Guide/Knowledge Base; Linked Mention -- Link; Linked Tasks -- Link.
  - Object: 4 edges, for example Linked Mention -- Guide/Task Management; Linked Tasks -- Guide/Task Management; Linked Mention -- Object.
  - Object Index: 3 edges, for example Linked Mention -- ADR/003 Indexed Object Graph; Linked Tasks -- ADR/003 Indexed Object Graph; Linked Mention -- Object Index.
  - Page Picker: 3 edges, for example Linked Mention -- Guide/Find and Connect Pages; Linked Mention -- Guide/Finding Content; View -- Page Picker.

## 24. other

- Nodes: 16; both hemisphere; colour `#6b7280`; merged from 11 smaller regions.
- Central nodes (links inside the region): Markdown/Comment (2), Tag/space-lua (2), Plugs/Development (1), API/codeWidget (1), Space Lua/Integrated Query/Aggregating (1).
- Bridges: 40 edges to 10 regions.
  - CHANGELOG: 13 edges, for example API/codeWidget -- CHANGELOG; Markdown/Comment -- CHANGELOG; Plugs/Development -- CHANGELOG.
  - API: 11 edges, for example API/codeWidget -- API; Plugs/Development -- API; API/codeWidget -- API/tag.
  - Object Index: 4 edges, for example Markdown/Comment -- Object Index; Plugs/Development -- Plugs; Space Lua/Integrated Query/Aggregating -- Space Lua/Integrated Query.
  - Object: 3 edges, for example Markdown/Comment -- Object; Tag/space-lua -- Tag; Tag/space-style -- Tag.
  - Reference/Space Lua and APIs: 3 edges, for example Document Editor -- Reference/Space Lua and APIs; Space Lua/Integrated Query/Aggregating -- Reference/Space Lua and APIs; Space Lua/Integrated Query/Grouping -- Reference/Space Lua and APIs.

## Time

313 of 313 nodes have a time: first node 2022-06-28, last change 2026-11-14. Time comes from the git history of a Markdown folder (outside git: the file modification time) or from the "time" field of graph.json. brain.html replays the growth on a time slider.

- Busiest day: 2026-06-23, 179 new nodes.
- New nodes per month: 2022-06: 1, 2026-06: 179, 2026-08: 17, 2026-09: 27, 2026-10: 37, 2026-11: 52.
- Status covers the 30 days before the last change: growing = new nodes, active = changes only, dormant = no change.

| # | Region | First node | Last change | New in 30 days | Status |
|---|---|---|---|---|---|
| 1 | CHANGELOG | 2022-06-28 | 2026-11-13 | 10 | growing |
| 2 | API | 2026-06-23 | 2026-11-14 | 10 | growing |
| 3 | Link | 2026-06-23 | 2026-11-13 | 3 | growing |
| 4 | Object Index | 2026-06-23 | 2026-11-13 | 3 | growing |
| 5 | Object | 2026-06-23 | 2026-11-13 | 10 | growing |
| 6 | Space Style | 2026-06-23 | 2026-11-13 | 15 | growing |
| 7 | Page Picker | 2026-06-23 | 2026-11-13 | 7 | growing |
| 8 | Tag/relation | 2026-06-23 | 2026-11-09 | 6 | growing |
| 9 | Reference/Space Lua and APIs | 2026-06-23 | 2026-11-13 | 1 | growing |
| 10 | Space Lua/Standard Library | 2026-06-23 | 2026-11-09 | 0 | active |
| 11 | Architecture/Client | 2026-06-23 | 2026-11-03 | 0 | active |
| 12 | API/widget | 2026-06-23 | 2026-11-13 | 0 | active |
| 13 | Extensions | 2026-06-23 | 2026-11-13 | 0 | active |
| 14 | API/auth | 2026-10-20 | 2026-11-13 | 4 | growing |
| 15 | Workbench/Maintenance | 2026-06-23 | 2026-11-09 | 3 | growing |
| 16 | Command | 2026-06-23 | 2026-11-09 | 0 | active |
| 17 | Plugs/Development/Reference | 2026-06-23 | 2026-11-13 | 0 | active |
| 18 | Service | 2026-06-23 | 2026-11-09 | 0 | active |
| 19 | Space Lua/Page Lua | 2026-10-12 | 2026-11-09 | 0 | active |
| 20 | Page Decorations | 2026-06-23 | 2026-11-09 | 1 | growing |
| 21 | Graph View | 2026-06-23 | 2026-11-09 | 1 | growing |
| 22 | Library/silverbulletmd/Themes/Classic | 2026-11-13 | 2026-11-13 | 3 | growing |
| 23 | View | 2026-06-23 | 2026-11-13 | 0 | active |
| 24 | other | 2026-06-23 | 2026-11-13 | 4 | growing |

## Graph metrics

- Connected components: 8, nodes without edges included; the largest has 304 of 313 nodes.
- Nodes without edges: 6.
- Modularity of the regions: Q = 0.3582. $Q = \sum_c \left[\frac{L_c}{m} - \left(\frac{D_c}{2m}\right)^2\right]$, where $L_c$ is the number of edges inside region $c$, $D_c$ the sum of the degrees of its nodes and $m$ the number of edges; "other" counts as 1 region and a graph without edges has Q = 0. Q = 0 means no more edges inside the regions than chance gives a graph with the same degrees.
