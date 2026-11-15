# neurophify

neurophify draws a knowledge graph as a 3D brain: it reads a graphify `graph.json` or a folder of Markdown notes, groups the nodes into regions, lays the regions out on two hemispheres, replays their growth over time and keeps the 20 most important nodes in `CORE.md`.

[![ci](https://github.com/maciejszulia/neurophify/actions/workflows/ci.yml/badge.svg)](https://github.com/maciejszulia/neurophify/actions/workflows/ci.yml)

[Polska wersja](README.pl.md)

## Demo

![A 3D brain made from the SilverBullet documentation turns once every 12 seconds: 313 pages in 24 colour-coded regions on two hemispheres](docs/demo/brain-spin.svg)

[Open the interactive 3D model on GitHub Pages](https://maciejszulia.github.io/neurophify/demo/brain.html): drag to rotate, scroll to zoom, press Play on the time bar to watch the documentation grow from its first page in 2022 to 313 pages.

The animation is [`docs/demo/brain-spin.svg`](docs/demo/brain-spin.svg), written with `--spin` from the documentation of SilverBullet; the static picture of the same scene is [`docs/demo/brain.svg`](docs/demo/brain.svg). The text reports are [`docs/demo/REGIONS.md`](docs/demo/REGIONS.md) (regions, time, graph metrics) and [`docs/demo/CORE.md`](docs/demo/CORE.md) (the 20 pages with the largest weight).

## 3D model in this README

GitHub renders the block below as an interactive 3D model: drag to rotate it. It shows both hemispheres and the 40 pages with the most links as small tetrahedra. The file is [`docs/demo/brain.stl`](docs/demo/brain.stl), written with `--stl`.

```stl
solid neurophify
facet normal 0.336 -0.038 0.941
outer loop
vertex -14.4 -0.0 15.5
vertex -9.4 -6.9 13.4
vertex -8.6 -0.0 13.4
endloop
endfacet
facet normal 0.797 -0.090 0.598
outer loop
vertex -8.6 -0.0 13.4
vertex -9.4 -6.9 13.4
vertex -5.7 -12.0 7.7
endloop
endfacet
facet normal 0.797 -0.090 0.598
outer loop
vertex -8.6 -0.0 13.4
vertex -5.7 -12.0 7.7
vertex -4.4 -0.0 7.7
endloop
endfacet
facet normal 0.974 -0.110 0.196
outer loop
vertex -4.4 -0.0 7.7
vertex -5.7 -12.0 7.7
vertex -4.4 -13.8 0.0
endloop
endfacet
facet normal 0.974 -0.110 0.196
outer loop
vertex -4.4 -0.0 7.7
vertex -4.4 -13.8 0.0
vertex -2.8 -0.0 0.0
endloop
endfacet
facet normal 0.974 -0.110 -0.196
outer loop
vertex -2.8 -0.0 0.0
vertex -4.4 -13.8 0.0
vertex -5.7 -12.0 -7.7
endloop
endfacet
facet normal 0.974 -0.110 -0.196
outer loop
vertex -2.8 -0.0 0.0
vertex -5.7 -12.0 -7.7
vertex -4.4 -0.0 -7.7
endloop
endfacet
facet normal 0.797 -0.090 -0.598
outer loop
vertex -4.4 -0.0 -7.7
vertex -5.7 -12.0 -7.7
vertex -9.4 -6.9 -13.4
endloop
endfacet
facet normal 0.797 -0.090 -0.598
outer loop
vertex -4.4 -0.0 -7.7
vertex -9.4 -6.9 -13.4
vertex -8.6 -0.0 -13.4
endloop
endfacet
facet normal 0.336 -0.038 -0.941
outer loop
vertex -8.6 -0.0 -13.4
vertex -9.4 -6.9 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal 0.252 -0.106 0.962
outer loop
vertex -14.4 -0.0 15.5
vertex -11.5 -12.0 13.4
vertex -9.4 -6.9 13.4
endloop
endfacet
facet normal 0.670 -0.282 0.687
outer loop
vertex -9.4 -6.9 13.4
vertex -11.5 -12.0 13.4
vertex -9.4 -20.7 7.7
endloop
endfacet
facet normal 0.670 -0.282 0.687
outer loop
vertex -9.4 -6.9 13.4
vertex -9.4 -20.7 7.7
vertex -5.7 -12.0 7.7
endloop
endfacet
facet normal 0.894 -0.375 0.245
outer loop
vertex -5.7 -12.0 7.7
vertex -9.4 -20.7 7.7
vertex -8.6 -23.9 0.0
endloop
endfacet
facet normal 0.894 -0.375 0.245
outer loop
vertex -5.7 -12.0 7.7
vertex -8.6 -23.9 0.0
vertex -4.4 -13.8 0.0
endloop
endfacet
facet normal 0.894 -0.375 -0.245
outer loop
vertex -4.4 -13.8 0.0
vertex -8.6 -23.9 0.0
vertex -9.4 -20.7 -7.7
endloop
endfacet
facet normal 0.894 -0.375 -0.245
outer loop
vertex -4.4 -13.8 0.0
vertex -9.4 -20.7 -7.7
vertex -5.7 -12.0 -7.7
endloop
endfacet
facet normal 0.670 -0.282 -0.687
outer loop
vertex -5.7 -12.0 -7.7
vertex -9.4 -20.7 -7.7
vertex -11.5 -12.0 -13.4
endloop
endfacet
facet normal 0.670 -0.282 -0.687
outer loop
vertex -5.7 -12.0 -7.7
vertex -11.5 -12.0 -13.4
vertex -9.4 -6.9 -13.4
endloop
endfacet
facet normal 0.252 -0.106 -0.962
outer loop
vertex -9.4 -6.9 -13.4
vertex -11.5 -12.0 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal 0.094 -0.148 0.985
outer loop
vertex -14.4 -0.0 15.5
vertex -14.4 -13.8 13.4
vertex -11.5 -12.0 13.4
endloop
endfacet
facet normal 0.298 -0.466 0.833
outer loop
vertex -11.5 -12.0 13.4
vertex -14.4 -13.8 13.4
vertex -14.4 -23.9 7.7
endloop
endfacet
facet normal 0.298 -0.466 0.833
outer loop
vertex -11.5 -12.0 13.4
vertex -14.4 -23.9 7.7
vertex -9.4 -20.7 7.7
endloop
endfacet
facet normal 0.499 -0.782 0.374
outer loop
vertex -9.4 -20.7 7.7
vertex -14.4 -23.9 7.7
vertex -14.4 -27.6 0.0
endloop
endfacet
facet normal 0.499 -0.782 0.374
outer loop
vertex -9.4 -20.7 7.7
vertex -14.4 -27.6 0.0
vertex -8.6 -23.9 0.0
endloop
endfacet
facet normal 0.499 -0.782 -0.374
outer loop
vertex -8.6 -23.9 0.0
vertex -14.4 -27.6 0.0
vertex -14.4 -23.9 -7.7
endloop
endfacet
facet normal 0.499 -0.782 -0.374
outer loop
vertex -8.6 -23.9 0.0
vertex -14.4 -23.9 -7.7
vertex -9.4 -20.7 -7.7
endloop
endfacet
facet normal 0.298 -0.466 -0.833
outer loop
vertex -9.4 -20.7 -7.7
vertex -14.4 -23.9 -7.7
vertex -14.4 -13.8 -13.4
endloop
endfacet
facet normal 0.298 -0.466 -0.833
outer loop
vertex -9.4 -20.7 -7.7
vertex -14.4 -13.8 -13.4
vertex -11.5 -12.0 -13.4
endloop
endfacet
facet normal 0.094 -0.148 -0.985
outer loop
vertex -11.5 -12.0 -13.4
vertex -14.4 -13.8 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.094 -0.148 0.985
outer loop
vertex -14.4 -0.0 15.5
vertex -17.3 -12.0 13.4
vertex -14.4 -13.8 13.4
endloop
endfacet
facet normal -0.298 -0.466 0.833
outer loop
vertex -14.4 -13.8 13.4
vertex -17.3 -12.0 13.4
vertex -19.4 -20.7 7.7
endloop
endfacet
facet normal -0.298 -0.466 0.833
outer loop
vertex -14.4 -13.8 13.4
vertex -19.4 -20.7 7.7
vertex -14.4 -23.9 7.7
endloop
endfacet
facet normal -0.499 -0.782 0.374
outer loop
vertex -14.4 -23.9 7.7
vertex -19.4 -20.7 7.7
vertex -20.2 -23.9 0.0
endloop
endfacet
facet normal -0.499 -0.782 0.374
outer loop
vertex -14.4 -23.9 7.7
vertex -20.2 -23.9 0.0
vertex -14.4 -27.6 0.0
endloop
endfacet
facet normal -0.499 -0.782 -0.374
outer loop
vertex -14.4 -27.6 0.0
vertex -20.2 -23.9 0.0
vertex -19.4 -20.7 -7.7
endloop
endfacet
facet normal -0.499 -0.782 -0.374
outer loop
vertex -14.4 -27.6 0.0
vertex -19.4 -20.7 -7.7
vertex -14.4 -23.9 -7.7
endloop
endfacet
facet normal -0.298 -0.466 -0.833
outer loop
vertex -14.4 -23.9 -7.7
vertex -19.4 -20.7 -7.7
vertex -17.3 -12.0 -13.4
endloop
endfacet
facet normal -0.298 -0.466 -0.833
outer loop
vertex -14.4 -23.9 -7.7
vertex -17.3 -12.0 -13.4
vertex -14.4 -13.8 -13.4
endloop
endfacet
facet normal -0.094 -0.148 -0.985
outer loop
vertex -14.4 -13.8 -13.4
vertex -17.3 -12.0 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.252 -0.106 0.962
outer loop
vertex -14.4 -0.0 15.5
vertex -19.4 -6.9 13.4
vertex -17.3 -12.0 13.4
endloop
endfacet
facet normal -0.670 -0.282 0.687
outer loop
vertex -17.3 -12.0 13.4
vertex -19.4 -6.9 13.4
vertex -23.1 -12.0 7.7
endloop
endfacet
facet normal -0.670 -0.282 0.687
outer loop
vertex -17.3 -12.0 13.4
vertex -23.1 -12.0 7.7
vertex -19.4 -20.7 7.7
endloop
endfacet
facet normal -0.894 -0.375 0.245
outer loop
vertex -19.4 -20.7 7.7
vertex -23.1 -12.0 7.7
vertex -24.4 -13.8 0.0
endloop
endfacet
facet normal -0.894 -0.375 0.245
outer loop
vertex -19.4 -20.7 7.7
vertex -24.4 -13.8 0.0
vertex -20.2 -23.9 0.0
endloop
endfacet
facet normal -0.894 -0.375 -0.245
outer loop
vertex -20.2 -23.9 0.0
vertex -24.4 -13.8 0.0
vertex -23.1 -12.0 -7.7
endloop
endfacet
facet normal -0.894 -0.375 -0.245
outer loop
vertex -20.2 -23.9 0.0
vertex -23.1 -12.0 -7.7
vertex -19.4 -20.7 -7.7
endloop
endfacet
facet normal -0.670 -0.282 -0.687
outer loop
vertex -19.4 -20.7 -7.7
vertex -23.1 -12.0 -7.7
vertex -19.4 -6.9 -13.4
endloop
endfacet
facet normal -0.670 -0.282 -0.687
outer loop
vertex -19.4 -20.7 -7.7
vertex -19.4 -6.9 -13.4
vertex -17.3 -12.0 -13.4
endloop
endfacet
facet normal -0.252 -0.106 -0.962
outer loop
vertex -17.3 -12.0 -13.4
vertex -19.4 -6.9 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.336 -0.038 0.941
outer loop
vertex -14.4 -0.0 15.5
vertex -20.2 -0.0 13.4
vertex -19.4 -6.9 13.4
endloop
endfacet
facet normal -0.797 -0.090 0.598
outer loop
vertex -19.4 -6.9 13.4
vertex -20.2 -0.0 13.4
vertex -24.4 -0.0 7.7
endloop
endfacet
facet normal -0.797 -0.090 0.598
outer loop
vertex -19.4 -6.9 13.4
vertex -24.4 -0.0 7.7
vertex -23.1 -12.0 7.7
endloop
endfacet
facet normal -0.974 -0.110 0.196
outer loop
vertex -23.1 -12.0 7.7
vertex -24.4 -0.0 7.7
vertex -26.0 -0.0 0.0
endloop
endfacet
facet normal -0.974 -0.110 0.196
outer loop
vertex -23.1 -12.0 7.7
vertex -26.0 -0.0 0.0
vertex -24.4 -13.8 0.0
endloop
endfacet
facet normal -0.974 -0.110 -0.196
outer loop
vertex -24.4 -13.8 0.0
vertex -26.0 -0.0 0.0
vertex -24.4 -0.0 -7.7
endloop
endfacet
facet normal -0.974 -0.110 -0.196
outer loop
vertex -24.4 -13.8 0.0
vertex -24.4 -0.0 -7.7
vertex -23.1 -12.0 -7.7
endloop
endfacet
facet normal -0.797 -0.090 -0.598
outer loop
vertex -23.1 -12.0 -7.7
vertex -24.4 -0.0 -7.7
vertex -20.2 -0.0 -13.4
endloop
endfacet
facet normal -0.797 -0.090 -0.598
outer loop
vertex -23.1 -12.0 -7.7
vertex -20.2 -0.0 -13.4
vertex -19.4 -6.9 -13.4
endloop
endfacet
facet normal -0.336 -0.038 -0.941
outer loop
vertex -19.4 -6.9 -13.4
vertex -20.2 -0.0 -13.4
vertex -14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.336 0.038 0.941
outer loop
vertex -14.4 -0.0 15.5
vertex -19.4 6.9 13.4
vertex -20.2 -0.0 13.4
endloop
endfacet
facet normal -0.797 0.090 0.598
outer loop
vertex -20.2 -0.0 13.4
vertex -19.4 6.9 13.4
vertex -23.1 12.0 7.7
endloop
endfacet
facet normal -0.797 0.090 0.598
outer loop
vertex -20.2 -0.0 13.4
vertex -23.1 12.0 7.7
vertex -24.4 -0.0 7.7
endloop
endfacet
facet normal -0.974 0.110 0.196
outer loop
vertex -24.4 -0.0 7.7
vertex -23.1 12.0 7.7
vertex -24.4 13.8 0.0
endloop
endfacet
facet normal -0.974 0.110 0.196
outer loop
vertex -24.4 -0.0 7.7
vertex -24.4 13.8 0.0
vertex -26.0 -0.0 0.0
endloop
endfacet
facet normal -0.974 0.110 -0.196
outer loop
vertex -26.0 -0.0 0.0
vertex -24.4 13.8 0.0
vertex -23.1 12.0 -7.7
endloop
endfacet
facet normal -0.974 0.110 -0.196
outer loop
vertex -26.0 -0.0 0.0
vertex -23.1 12.0 -7.7
vertex -24.4 -0.0 -7.7
endloop
endfacet
facet normal -0.797 0.090 -0.598
outer loop
vertex -24.4 -0.0 -7.7
vertex -23.1 12.0 -7.7
vertex -19.4 6.9 -13.4
endloop
endfacet
facet normal -0.797 0.090 -0.598
outer loop
vertex -24.4 -0.0 -7.7
vertex -19.4 6.9 -13.4
vertex -20.2 -0.0 -13.4
endloop
endfacet
facet normal -0.336 0.038 -0.941
outer loop
vertex -20.2 -0.0 -13.4
vertex -19.4 6.9 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal -0.252 0.106 0.962
outer loop
vertex -14.4 -0.0 15.5
vertex -17.3 12.0 13.4
vertex -19.4 6.9 13.4
endloop
endfacet
facet normal -0.670 0.282 0.687
outer loop
vertex -19.4 6.9 13.4
vertex -17.3 12.0 13.4
vertex -19.4 20.7 7.7
endloop
endfacet
facet normal -0.670 0.282 0.687
outer loop
vertex -19.4 6.9 13.4
vertex -19.4 20.7 7.7
vertex -23.1 12.0 7.7
endloop
endfacet
facet normal -0.894 0.375 0.245
outer loop
vertex -23.1 12.0 7.7
vertex -19.4 20.7 7.7
vertex -20.2 23.9 0.0
endloop
endfacet
facet normal -0.894 0.375 0.245
outer loop
vertex -23.1 12.0 7.7
vertex -20.2 23.9 0.0
vertex -24.4 13.8 0.0
endloop
endfacet
facet normal -0.894 0.375 -0.245
outer loop
vertex -24.4 13.8 0.0
vertex -20.2 23.9 0.0
vertex -19.4 20.7 -7.7
endloop
endfacet
facet normal -0.894 0.375 -0.245
outer loop
vertex -24.4 13.8 0.0
vertex -19.4 20.7 -7.7
vertex -23.1 12.0 -7.7
endloop
endfacet
facet normal -0.670 0.282 -0.687
outer loop
vertex -23.1 12.0 -7.7
vertex -19.4 20.7 -7.7
vertex -17.3 12.0 -13.4
endloop
endfacet
facet normal -0.670 0.282 -0.687
outer loop
vertex -23.1 12.0 -7.7
vertex -17.3 12.0 -13.4
vertex -19.4 6.9 -13.4
endloop
endfacet
facet normal -0.252 0.106 -0.962
outer loop
vertex -19.4 6.9 -13.4
vertex -17.3 12.0 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal -0.094 0.148 0.985
outer loop
vertex -14.4 -0.0 15.5
vertex -14.4 13.8 13.4
vertex -17.3 12.0 13.4
endloop
endfacet
facet normal -0.298 0.466 0.833
outer loop
vertex -17.3 12.0 13.4
vertex -14.4 13.8 13.4
vertex -14.4 23.9 7.7
endloop
endfacet
facet normal -0.298 0.466 0.833
outer loop
vertex -17.3 12.0 13.4
vertex -14.4 23.9 7.7
vertex -19.4 20.7 7.7
endloop
endfacet
facet normal -0.499 0.782 0.374
outer loop
vertex -19.4 20.7 7.7
vertex -14.4 23.9 7.7
vertex -14.4 27.6 0.0
endloop
endfacet
facet normal -0.499 0.782 0.374
outer loop
vertex -19.4 20.7 7.7
vertex -14.4 27.6 0.0
vertex -20.2 23.9 0.0
endloop
endfacet
facet normal -0.499 0.782 -0.374
outer loop
vertex -20.2 23.9 0.0
vertex -14.4 27.6 0.0
vertex -14.4 23.9 -7.7
endloop
endfacet
facet normal -0.499 0.782 -0.374
outer loop
vertex -20.2 23.9 0.0
vertex -14.4 23.9 -7.7
vertex -19.4 20.7 -7.7
endloop
endfacet
facet normal -0.298 0.466 -0.833
outer loop
vertex -19.4 20.7 -7.7
vertex -14.4 23.9 -7.7
vertex -14.4 13.8 -13.4
endloop
endfacet
facet normal -0.298 0.466 -0.833
outer loop
vertex -19.4 20.7 -7.7
vertex -14.4 13.8 -13.4
vertex -17.3 12.0 -13.4
endloop
endfacet
facet normal -0.094 0.148 -0.985
outer loop
vertex -17.3 12.0 -13.4
vertex -14.4 13.8 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal 0.094 0.148 0.985
outer loop
vertex -14.4 -0.0 15.5
vertex -11.5 12.0 13.4
vertex -14.4 13.8 13.4
endloop
endfacet
facet normal 0.298 0.466 0.833
outer loop
vertex -14.4 13.8 13.4
vertex -11.5 12.0 13.4
vertex -9.4 20.7 7.7
endloop
endfacet
facet normal 0.298 0.466 0.833
outer loop
vertex -14.4 13.8 13.4
vertex -9.4 20.7 7.7
vertex -14.4 23.9 7.7
endloop
endfacet
facet normal 0.499 0.782 0.374
outer loop
vertex -14.4 23.9 7.7
vertex -9.4 20.7 7.7
vertex -8.6 23.9 0.0
endloop
endfacet
facet normal 0.499 0.782 0.374
outer loop
vertex -14.4 23.9 7.7
vertex -8.6 23.9 0.0
vertex -14.4 27.6 0.0
endloop
endfacet
facet normal 0.499 0.782 -0.374
outer loop
vertex -14.4 27.6 0.0
vertex -8.6 23.9 0.0
vertex -9.4 20.7 -7.7
endloop
endfacet
facet normal 0.499 0.782 -0.374
outer loop
vertex -14.4 27.6 0.0
vertex -9.4 20.7 -7.7
vertex -14.4 23.9 -7.7
endloop
endfacet
facet normal 0.298 0.466 -0.833
outer loop
vertex -14.4 23.9 -7.7
vertex -9.4 20.7 -7.7
vertex -11.5 12.0 -13.4
endloop
endfacet
facet normal 0.298 0.466 -0.833
outer loop
vertex -14.4 23.9 -7.7
vertex -11.5 12.0 -13.4
vertex -14.4 13.8 -13.4
endloop
endfacet
facet normal 0.094 0.148 -0.985
outer loop
vertex -14.4 13.8 -13.4
vertex -11.5 12.0 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal 0.252 0.106 0.962
outer loop
vertex -14.4 -0.0 15.5
vertex -9.4 6.9 13.4
vertex -11.5 12.0 13.4
endloop
endfacet
facet normal 0.670 0.282 0.687
outer loop
vertex -11.5 12.0 13.4
vertex -9.4 6.9 13.4
vertex -5.7 12.0 7.7
endloop
endfacet
facet normal 0.670 0.282 0.687
outer loop
vertex -11.5 12.0 13.4
vertex -5.7 12.0 7.7
vertex -9.4 20.7 7.7
endloop
endfacet
facet normal 0.894 0.375 0.245
outer loop
vertex -9.4 20.7 7.7
vertex -5.7 12.0 7.7
vertex -4.4 13.8 0.0
endloop
endfacet
facet normal 0.894 0.375 0.245
outer loop
vertex -9.4 20.7 7.7
vertex -4.4 13.8 0.0
vertex -8.6 23.9 0.0
endloop
endfacet
facet normal 0.894 0.375 -0.245
outer loop
vertex -8.6 23.9 0.0
vertex -4.4 13.8 0.0
vertex -5.7 12.0 -7.7
endloop
endfacet
facet normal 0.894 0.375 -0.245
outer loop
vertex -8.6 23.9 0.0
vertex -5.7 12.0 -7.7
vertex -9.4 20.7 -7.7
endloop
endfacet
facet normal 0.670 0.282 -0.687
outer loop
vertex -9.4 20.7 -7.7
vertex -5.7 12.0 -7.7
vertex -9.4 6.9 -13.4
endloop
endfacet
facet normal 0.670 0.282 -0.687
outer loop
vertex -9.4 20.7 -7.7
vertex -9.4 6.9 -13.4
vertex -11.5 12.0 -13.4
endloop
endfacet
facet normal 0.252 0.106 -0.962
outer loop
vertex -11.5 12.0 -13.4
vertex -9.4 6.9 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal 0.336 0.038 0.941
outer loop
vertex -14.4 -0.0 15.5
vertex -8.6 0.0 13.4
vertex -9.4 6.9 13.4
endloop
endfacet
facet normal 0.797 0.090 0.598
outer loop
vertex -9.4 6.9 13.4
vertex -8.6 0.0 13.4
vertex -4.4 0.0 7.7
endloop
endfacet
facet normal 0.797 0.090 0.598
outer loop
vertex -9.4 6.9 13.4
vertex -4.4 0.0 7.7
vertex -5.7 12.0 7.7
endloop
endfacet
facet normal 0.974 0.110 0.196
outer loop
vertex -5.7 12.0 7.7
vertex -4.4 0.0 7.7
vertex -2.8 0.0 0.0
endloop
endfacet
facet normal 0.974 0.110 0.196
outer loop
vertex -5.7 12.0 7.7
vertex -2.8 0.0 0.0
vertex -4.4 13.8 0.0
endloop
endfacet
facet normal 0.974 0.110 -0.196
outer loop
vertex -4.4 13.8 0.0
vertex -2.8 0.0 0.0
vertex -4.4 0.0 -7.7
endloop
endfacet
facet normal 0.974 0.110 -0.196
outer loop
vertex -4.4 13.8 0.0
vertex -4.4 0.0 -7.7
vertex -5.7 12.0 -7.7
endloop
endfacet
facet normal 0.797 0.090 -0.598
outer loop
vertex -5.7 12.0 -7.7
vertex -4.4 0.0 -7.7
vertex -8.6 0.0 -13.4
endloop
endfacet
facet normal 0.797 0.090 -0.598
outer loop
vertex -5.7 12.0 -7.7
vertex -8.6 0.0 -13.4
vertex -9.4 6.9 -13.4
endloop
endfacet
facet normal 0.336 0.038 -0.941
outer loop
vertex -9.4 6.9 -13.4
vertex -8.6 0.0 -13.4
vertex -14.4 0.0 -15.5
endloop
endfacet
facet normal 0.336 -0.038 0.941
outer loop
vertex 14.4 -0.0 15.5
vertex 19.4 -6.9 13.4
vertex 20.2 -0.0 13.4
endloop
endfacet
facet normal 0.797 -0.090 0.598
outer loop
vertex 20.2 -0.0 13.4
vertex 19.4 -6.9 13.4
vertex 23.1 -12.0 7.7
endloop
endfacet
facet normal 0.797 -0.090 0.598
outer loop
vertex 20.2 -0.0 13.4
vertex 23.1 -12.0 7.7
vertex 24.4 -0.0 7.7
endloop
endfacet
facet normal 0.974 -0.110 0.196
outer loop
vertex 24.4 -0.0 7.7
vertex 23.1 -12.0 7.7
vertex 24.4 -13.8 0.0
endloop
endfacet
facet normal 0.974 -0.110 0.196
outer loop
vertex 24.4 -0.0 7.7
vertex 24.4 -13.8 0.0
vertex 26.0 -0.0 0.0
endloop
endfacet
facet normal 0.974 -0.110 -0.196
outer loop
vertex 26.0 -0.0 0.0
vertex 24.4 -13.8 0.0
vertex 23.1 -12.0 -7.7
endloop
endfacet
facet normal 0.974 -0.110 -0.196
outer loop
vertex 26.0 -0.0 0.0
vertex 23.1 -12.0 -7.7
vertex 24.4 -0.0 -7.7
endloop
endfacet
facet normal 0.797 -0.090 -0.598
outer loop
vertex 24.4 -0.0 -7.7
vertex 23.1 -12.0 -7.7
vertex 19.4 -6.9 -13.4
endloop
endfacet
facet normal 0.797 -0.090 -0.598
outer loop
vertex 24.4 -0.0 -7.7
vertex 19.4 -6.9 -13.4
vertex 20.2 -0.0 -13.4
endloop
endfacet
facet normal 0.336 -0.038 -0.941
outer loop
vertex 20.2 -0.0 -13.4
vertex 19.4 -6.9 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal 0.252 -0.106 0.962
outer loop
vertex 14.4 -0.0 15.5
vertex 17.3 -12.0 13.4
vertex 19.4 -6.9 13.4
endloop
endfacet
facet normal 0.670 -0.282 0.687
outer loop
vertex 19.4 -6.9 13.4
vertex 17.3 -12.0 13.4
vertex 19.4 -20.7 7.7
endloop
endfacet
facet normal 0.670 -0.282 0.687
outer loop
vertex 19.4 -6.9 13.4
vertex 19.4 -20.7 7.7
vertex 23.1 -12.0 7.7
endloop
endfacet
facet normal 0.894 -0.375 0.245
outer loop
vertex 23.1 -12.0 7.7
vertex 19.4 -20.7 7.7
vertex 20.2 -23.9 0.0
endloop
endfacet
facet normal 0.894 -0.375 0.245
outer loop
vertex 23.1 -12.0 7.7
vertex 20.2 -23.9 0.0
vertex 24.4 -13.8 0.0
endloop
endfacet
facet normal 0.894 -0.375 -0.245
outer loop
vertex 24.4 -13.8 0.0
vertex 20.2 -23.9 0.0
vertex 19.4 -20.7 -7.7
endloop
endfacet
facet normal 0.894 -0.375 -0.245
outer loop
vertex 24.4 -13.8 0.0
vertex 19.4 -20.7 -7.7
vertex 23.1 -12.0 -7.7
endloop
endfacet
facet normal 0.670 -0.282 -0.687
outer loop
vertex 23.1 -12.0 -7.7
vertex 19.4 -20.7 -7.7
vertex 17.3 -12.0 -13.4
endloop
endfacet
facet normal 0.670 -0.282 -0.687
outer loop
vertex 23.1 -12.0 -7.7
vertex 17.3 -12.0 -13.4
vertex 19.4 -6.9 -13.4
endloop
endfacet
facet normal 0.252 -0.106 -0.962
outer loop
vertex 19.4 -6.9 -13.4
vertex 17.3 -12.0 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal 0.094 -0.148 0.985
outer loop
vertex 14.4 -0.0 15.5
vertex 14.4 -13.8 13.4
vertex 17.3 -12.0 13.4
endloop
endfacet
facet normal 0.298 -0.466 0.833
outer loop
vertex 17.3 -12.0 13.4
vertex 14.4 -13.8 13.4
vertex 14.4 -23.9 7.7
endloop
endfacet
facet normal 0.298 -0.466 0.833
outer loop
vertex 17.3 -12.0 13.4
vertex 14.4 -23.9 7.7
vertex 19.4 -20.7 7.7
endloop
endfacet
facet normal 0.499 -0.782 0.374
outer loop
vertex 19.4 -20.7 7.7
vertex 14.4 -23.9 7.7
vertex 14.4 -27.6 0.0
endloop
endfacet
facet normal 0.499 -0.782 0.374
outer loop
vertex 19.4 -20.7 7.7
vertex 14.4 -27.6 0.0
vertex 20.2 -23.9 0.0
endloop
endfacet
facet normal 0.499 -0.782 -0.374
outer loop
vertex 20.2 -23.9 0.0
vertex 14.4 -27.6 0.0
vertex 14.4 -23.9 -7.7
endloop
endfacet
facet normal 0.499 -0.782 -0.374
outer loop
vertex 20.2 -23.9 0.0
vertex 14.4 -23.9 -7.7
vertex 19.4 -20.7 -7.7
endloop
endfacet
facet normal 0.298 -0.466 -0.833
outer loop
vertex 19.4 -20.7 -7.7
vertex 14.4 -23.9 -7.7
vertex 14.4 -13.8 -13.4
endloop
endfacet
facet normal 0.298 -0.466 -0.833
outer loop
vertex 19.4 -20.7 -7.7
vertex 14.4 -13.8 -13.4
vertex 17.3 -12.0 -13.4
endloop
endfacet
facet normal 0.094 -0.148 -0.985
outer loop
vertex 17.3 -12.0 -13.4
vertex 14.4 -13.8 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.094 -0.148 0.985
outer loop
vertex 14.4 -0.0 15.5
vertex 11.5 -12.0 13.4
vertex 14.4 -13.8 13.4
endloop
endfacet
facet normal -0.298 -0.466 0.833
outer loop
vertex 14.4 -13.8 13.4
vertex 11.5 -12.0 13.4
vertex 9.4 -20.7 7.7
endloop
endfacet
facet normal -0.298 -0.466 0.833
outer loop
vertex 14.4 -13.8 13.4
vertex 9.4 -20.7 7.7
vertex 14.4 -23.9 7.7
endloop
endfacet
facet normal -0.499 -0.782 0.374
outer loop
vertex 14.4 -23.9 7.7
vertex 9.4 -20.7 7.7
vertex 8.6 -23.9 0.0
endloop
endfacet
facet normal -0.499 -0.782 0.374
outer loop
vertex 14.4 -23.9 7.7
vertex 8.6 -23.9 0.0
vertex 14.4 -27.6 0.0
endloop
endfacet
facet normal -0.499 -0.782 -0.374
outer loop
vertex 14.4 -27.6 0.0
vertex 8.6 -23.9 0.0
vertex 9.4 -20.7 -7.7
endloop
endfacet
facet normal -0.499 -0.782 -0.374
outer loop
vertex 14.4 -27.6 0.0
vertex 9.4 -20.7 -7.7
vertex 14.4 -23.9 -7.7
endloop
endfacet
facet normal -0.298 -0.466 -0.833
outer loop
vertex 14.4 -23.9 -7.7
vertex 9.4 -20.7 -7.7
vertex 11.5 -12.0 -13.4
endloop
endfacet
facet normal -0.298 -0.466 -0.833
outer loop
vertex 14.4 -23.9 -7.7
vertex 11.5 -12.0 -13.4
vertex 14.4 -13.8 -13.4
endloop
endfacet
facet normal -0.094 -0.148 -0.985
outer loop
vertex 14.4 -13.8 -13.4
vertex 11.5 -12.0 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.252 -0.106 0.962
outer loop
vertex 14.4 -0.0 15.5
vertex 9.4 -6.9 13.4
vertex 11.5 -12.0 13.4
endloop
endfacet
facet normal -0.670 -0.282 0.687
outer loop
vertex 11.5 -12.0 13.4
vertex 9.4 -6.9 13.4
vertex 5.7 -12.0 7.7
endloop
endfacet
facet normal -0.670 -0.282 0.687
outer loop
vertex 11.5 -12.0 13.4
vertex 5.7 -12.0 7.7
vertex 9.4 -20.7 7.7
endloop
endfacet
facet normal -0.894 -0.375 0.245
outer loop
vertex 9.4 -20.7 7.7
vertex 5.7 -12.0 7.7
vertex 4.4 -13.8 0.0
endloop
endfacet
facet normal -0.894 -0.375 0.245
outer loop
vertex 9.4 -20.7 7.7
vertex 4.4 -13.8 0.0
vertex 8.6 -23.9 0.0
endloop
endfacet
facet normal -0.894 -0.375 -0.245
outer loop
vertex 8.6 -23.9 0.0
vertex 4.4 -13.8 0.0
vertex 5.7 -12.0 -7.7
endloop
endfacet
facet normal -0.894 -0.375 -0.245
outer loop
vertex 8.6 -23.9 0.0
vertex 5.7 -12.0 -7.7
vertex 9.4 -20.7 -7.7
endloop
endfacet
facet normal -0.670 -0.282 -0.687
outer loop
vertex 9.4 -20.7 -7.7
vertex 5.7 -12.0 -7.7
vertex 9.4 -6.9 -13.4
endloop
endfacet
facet normal -0.670 -0.282 -0.687
outer loop
vertex 9.4 -20.7 -7.7
vertex 9.4 -6.9 -13.4
vertex 11.5 -12.0 -13.4
endloop
endfacet
facet normal -0.252 -0.106 -0.962
outer loop
vertex 11.5 -12.0 -13.4
vertex 9.4 -6.9 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.336 -0.038 0.941
outer loop
vertex 14.4 -0.0 15.5
vertex 8.6 -0.0 13.4
vertex 9.4 -6.9 13.4
endloop
endfacet
facet normal -0.797 -0.090 0.598
outer loop
vertex 9.4 -6.9 13.4
vertex 8.6 -0.0 13.4
vertex 4.4 -0.0 7.7
endloop
endfacet
facet normal -0.797 -0.090 0.598
outer loop
vertex 9.4 -6.9 13.4
vertex 4.4 -0.0 7.7
vertex 5.7 -12.0 7.7
endloop
endfacet
facet normal -0.974 -0.110 0.196
outer loop
vertex 5.7 -12.0 7.7
vertex 4.4 -0.0 7.7
vertex 2.8 -0.0 0.0
endloop
endfacet
facet normal -0.974 -0.110 0.196
outer loop
vertex 5.7 -12.0 7.7
vertex 2.8 -0.0 0.0
vertex 4.4 -13.8 0.0
endloop
endfacet
facet normal -0.974 -0.110 -0.196
outer loop
vertex 4.4 -13.8 0.0
vertex 2.8 -0.0 0.0
vertex 4.4 -0.0 -7.7
endloop
endfacet
facet normal -0.974 -0.110 -0.196
outer loop
vertex 4.4 -13.8 0.0
vertex 4.4 -0.0 -7.7
vertex 5.7 -12.0 -7.7
endloop
endfacet
facet normal -0.797 -0.090 -0.598
outer loop
vertex 5.7 -12.0 -7.7
vertex 4.4 -0.0 -7.7
vertex 8.6 -0.0 -13.4
endloop
endfacet
facet normal -0.797 -0.090 -0.598
outer loop
vertex 5.7 -12.0 -7.7
vertex 8.6 -0.0 -13.4
vertex 9.4 -6.9 -13.4
endloop
endfacet
facet normal -0.336 -0.038 -0.941
outer loop
vertex 9.4 -6.9 -13.4
vertex 8.6 -0.0 -13.4
vertex 14.4 -0.0 -15.5
endloop
endfacet
facet normal -0.336 0.038 0.941
outer loop
vertex 14.4 -0.0 15.5
vertex 9.4 6.9 13.4
vertex 8.6 -0.0 13.4
endloop
endfacet
facet normal -0.797 0.090 0.598
outer loop
vertex 8.6 -0.0 13.4
vertex 9.4 6.9 13.4
vertex 5.7 12.0 7.7
endloop
endfacet
facet normal -0.797 0.090 0.598
outer loop
vertex 8.6 -0.0 13.4
vertex 5.7 12.0 7.7
vertex 4.4 -0.0 7.7
endloop
endfacet
facet normal -0.974 0.110 0.196
outer loop
vertex 4.4 -0.0 7.7
vertex 5.7 12.0 7.7
vertex 4.4 13.8 0.0
endloop
endfacet
facet normal -0.974 0.110 0.196
outer loop
vertex 4.4 -0.0 7.7
vertex 4.4 13.8 0.0
vertex 2.8 -0.0 0.0
endloop
endfacet
facet normal -0.974 0.110 -0.196
outer loop
vertex 2.8 -0.0 0.0
vertex 4.4 13.8 0.0
vertex 5.7 12.0 -7.7
endloop
endfacet
facet normal -0.974 0.110 -0.196
outer loop
vertex 2.8 -0.0 0.0
vertex 5.7 12.0 -7.7
vertex 4.4 -0.0 -7.7
endloop
endfacet
facet normal -0.797 0.090 -0.598
outer loop
vertex 4.4 -0.0 -7.7
vertex 5.7 12.0 -7.7
vertex 9.4 6.9 -13.4
endloop
endfacet
facet normal -0.797 0.090 -0.598
outer loop
vertex 4.4 -0.0 -7.7
vertex 9.4 6.9 -13.4
vertex 8.6 -0.0 -13.4
endloop
endfacet
facet normal -0.336 0.038 -0.941
outer loop
vertex 8.6 -0.0 -13.4
vertex 9.4 6.9 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal -0.252 0.106 0.962
outer loop
vertex 14.4 -0.0 15.5
vertex 11.5 12.0 13.4
vertex 9.4 6.9 13.4
endloop
endfacet
facet normal -0.670 0.282 0.687
outer loop
vertex 9.4 6.9 13.4
vertex 11.5 12.0 13.4
vertex 9.4 20.7 7.7
endloop
endfacet
facet normal -0.670 0.282 0.687
outer loop
vertex 9.4 6.9 13.4
vertex 9.4 20.7 7.7
vertex 5.7 12.0 7.7
endloop
endfacet
facet normal -0.894 0.375 0.245
outer loop
vertex 5.7 12.0 7.7
vertex 9.4 20.7 7.7
vertex 8.6 23.9 0.0
endloop
endfacet
facet normal -0.894 0.375 0.245
outer loop
vertex 5.7 12.0 7.7
vertex 8.6 23.9 0.0
vertex 4.4 13.8 0.0
endloop
endfacet
facet normal -0.894 0.375 -0.245
outer loop
vertex 4.4 13.8 0.0
vertex 8.6 23.9 0.0
vertex 9.4 20.7 -7.7
endloop
endfacet
facet normal -0.894 0.375 -0.245
outer loop
vertex 4.4 13.8 0.0
vertex 9.4 20.7 -7.7
vertex 5.7 12.0 -7.7
endloop
endfacet
facet normal -0.670 0.282 -0.687
outer loop
vertex 5.7 12.0 -7.7
vertex 9.4 20.7 -7.7
vertex 11.5 12.0 -13.4
endloop
endfacet
facet normal -0.670 0.282 -0.687
outer loop
vertex 5.7 12.0 -7.7
vertex 11.5 12.0 -13.4
vertex 9.4 6.9 -13.4
endloop
endfacet
facet normal -0.252 0.106 -0.962
outer loop
vertex 9.4 6.9 -13.4
vertex 11.5 12.0 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal -0.094 0.148 0.985
outer loop
vertex 14.4 -0.0 15.5
vertex 14.4 13.8 13.4
vertex 11.5 12.0 13.4
endloop
endfacet
facet normal -0.298 0.466 0.833
outer loop
vertex 11.5 12.0 13.4
vertex 14.4 13.8 13.4
vertex 14.4 23.9 7.7
endloop
endfacet
facet normal -0.298 0.466 0.833
outer loop
vertex 11.5 12.0 13.4
vertex 14.4 23.9 7.7
vertex 9.4 20.7 7.7
endloop
endfacet
facet normal -0.499 0.782 0.374
outer loop
vertex 9.4 20.7 7.7
vertex 14.4 23.9 7.7
vertex 14.4 27.6 0.0
endloop
endfacet
facet normal -0.499 0.782 0.374
outer loop
vertex 9.4 20.7 7.7
vertex 14.4 27.6 0.0
vertex 8.6 23.9 0.0
endloop
endfacet
facet normal -0.499 0.782 -0.374
outer loop
vertex 8.6 23.9 0.0
vertex 14.4 27.6 0.0
vertex 14.4 23.9 -7.7
endloop
endfacet
facet normal -0.499 0.782 -0.374
outer loop
vertex 8.6 23.9 0.0
vertex 14.4 23.9 -7.7
vertex 9.4 20.7 -7.7
endloop
endfacet
facet normal -0.298 0.466 -0.833
outer loop
vertex 9.4 20.7 -7.7
vertex 14.4 23.9 -7.7
vertex 14.4 13.8 -13.4
endloop
endfacet
facet normal -0.298 0.466 -0.833
outer loop
vertex 9.4 20.7 -7.7
vertex 14.4 13.8 -13.4
vertex 11.5 12.0 -13.4
endloop
endfacet
facet normal -0.094 0.148 -0.985
outer loop
vertex 11.5 12.0 -13.4
vertex 14.4 13.8 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal 0.094 0.148 0.985
outer loop
vertex 14.4 -0.0 15.5
vertex 17.3 12.0 13.4
vertex 14.4 13.8 13.4
endloop
endfacet
facet normal 0.298 0.466 0.833
outer loop
vertex 14.4 13.8 13.4
vertex 17.3 12.0 13.4
vertex 19.4 20.7 7.7
endloop
endfacet
facet normal 0.298 0.466 0.833
outer loop
vertex 14.4 13.8 13.4
vertex 19.4 20.7 7.7
vertex 14.4 23.9 7.7
endloop
endfacet
facet normal 0.499 0.782 0.374
outer loop
vertex 14.4 23.9 7.7
vertex 19.4 20.7 7.7
vertex 20.2 23.9 0.0
endloop
endfacet
facet normal 0.499 0.782 0.374
outer loop
vertex 14.4 23.9 7.7
vertex 20.2 23.9 0.0
vertex 14.4 27.6 0.0
endloop
endfacet
facet normal 0.499 0.782 -0.374
outer loop
vertex 14.4 27.6 0.0
vertex 20.2 23.9 0.0
vertex 19.4 20.7 -7.7
endloop
endfacet
facet normal 0.499 0.782 -0.374
outer loop
vertex 14.4 27.6 0.0
vertex 19.4 20.7 -7.7
vertex 14.4 23.9 -7.7
endloop
endfacet
facet normal 0.298 0.466 -0.833
outer loop
vertex 14.4 23.9 -7.7
vertex 19.4 20.7 -7.7
vertex 17.3 12.0 -13.4
endloop
endfacet
facet normal 0.298 0.466 -0.833
outer loop
vertex 14.4 23.9 -7.7
vertex 17.3 12.0 -13.4
vertex 14.4 13.8 -13.4
endloop
endfacet
facet normal 0.094 0.148 -0.985
outer loop
vertex 14.4 13.8 -13.4
vertex 17.3 12.0 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal 0.252 0.106 0.962
outer loop
vertex 14.4 -0.0 15.5
vertex 19.4 6.9 13.4
vertex 17.3 12.0 13.4
endloop
endfacet
facet normal 0.670 0.282 0.687
outer loop
vertex 17.3 12.0 13.4
vertex 19.4 6.9 13.4
vertex 23.1 12.0 7.7
endloop
endfacet
facet normal 0.670 0.282 0.687
outer loop
vertex 17.3 12.0 13.4
vertex 23.1 12.0 7.7
vertex 19.4 20.7 7.7
endloop
endfacet
facet normal 0.894 0.375 0.245
outer loop
vertex 19.4 20.7 7.7
vertex 23.1 12.0 7.7
vertex 24.4 13.8 0.0
endloop
endfacet
facet normal 0.894 0.375 0.245
outer loop
vertex 19.4 20.7 7.7
vertex 24.4 13.8 0.0
vertex 20.2 23.9 0.0
endloop
endfacet
facet normal 0.894 0.375 -0.245
outer loop
vertex 20.2 23.9 0.0
vertex 24.4 13.8 0.0
vertex 23.1 12.0 -7.7
endloop
endfacet
facet normal 0.894 0.375 -0.245
outer loop
vertex 20.2 23.9 0.0
vertex 23.1 12.0 -7.7
vertex 19.4 20.7 -7.7
endloop
endfacet
facet normal 0.670 0.282 -0.687
outer loop
vertex 19.4 20.7 -7.7
vertex 23.1 12.0 -7.7
vertex 19.4 6.9 -13.4
endloop
endfacet
facet normal 0.670 0.282 -0.687
outer loop
vertex 19.4 20.7 -7.7
vertex 19.4 6.9 -13.4
vertex 17.3 12.0 -13.4
endloop
endfacet
facet normal 0.252 0.106 -0.962
outer loop
vertex 17.3 12.0 -13.4
vertex 19.4 6.9 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal 0.336 0.038 0.941
outer loop
vertex 14.4 -0.0 15.5
vertex 20.2 0.0 13.4
vertex 19.4 6.9 13.4
endloop
endfacet
facet normal 0.797 0.090 0.598
outer loop
vertex 19.4 6.9 13.4
vertex 20.2 0.0 13.4
vertex 24.4 0.0 7.7
endloop
endfacet
facet normal 0.797 0.090 0.598
outer loop
vertex 19.4 6.9 13.4
vertex 24.4 0.0 7.7
vertex 23.1 12.0 7.7
endloop
endfacet
facet normal 0.974 0.110 0.196
outer loop
vertex 23.1 12.0 7.7
vertex 24.4 0.0 7.7
vertex 26.0 0.0 0.0
endloop
endfacet
facet normal 0.974 0.110 0.196
outer loop
vertex 23.1 12.0 7.7
vertex 26.0 0.0 0.0
vertex 24.4 13.8 0.0
endloop
endfacet
facet normal 0.974 0.110 -0.196
outer loop
vertex 24.4 13.8 0.0
vertex 26.0 0.0 0.0
vertex 24.4 0.0 -7.7
endloop
endfacet
facet normal 0.974 0.110 -0.196
outer loop
vertex 24.4 13.8 0.0
vertex 24.4 0.0 -7.7
vertex 23.1 12.0 -7.7
endloop
endfacet
facet normal 0.797 0.090 -0.598
outer loop
vertex 23.1 12.0 -7.7
vertex 24.4 0.0 -7.7
vertex 20.2 0.0 -13.4
endloop
endfacet
facet normal 0.797 0.090 -0.598
outer loop
vertex 23.1 12.0 -7.7
vertex 20.2 0.0 -13.4
vertex 19.4 6.9 -13.4
endloop
endfacet
facet normal 0.336 0.038 -0.941
outer loop
vertex 19.4 6.9 -13.4
vertex 20.2 0.0 -13.4
vertex 14.4 0.0 -15.5
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -8.5 2.6 -14.3
vertex -8.5 4.9 -16.5
vertex -10.7 4.9 -14.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -8.5 2.6 -14.3
vertex -10.7 2.6 -16.5
vertex -8.5 4.9 -16.5
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -8.5 2.6 -14.3
vertex -10.7 4.9 -14.3
vertex -10.7 2.6 -16.5
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -8.5 4.9 -16.5
vertex -10.7 2.6 -16.5
vertex -10.7 4.9 -14.3
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -25.2 -8.0 5.3
vertex -25.2 -6.1 3.3
vertex -27.2 -6.1 5.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -25.2 -8.0 5.3
vertex -27.2 -8.0 3.3
vertex -25.2 -6.1 3.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -25.2 -8.0 5.3
vertex -27.2 -6.1 5.3
vertex -27.2 -8.0 3.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -25.2 -6.1 3.3
vertex -27.2 -8.0 3.3
vertex -27.2 -6.1 5.3
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -24.1 -15.7 -2.6
vertex -24.1 -13.8 -4.5
vertex -26.0 -13.8 -2.6
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -24.1 -15.7 -2.6
vertex -26.0 -15.7 -4.5
vertex -24.1 -13.8 -4.5
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -24.1 -15.7 -2.6
vertex -26.0 -13.8 -2.6
vertex -26.0 -15.7 -4.5
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -24.1 -13.8 -4.5
vertex -26.0 -15.7 -4.5
vertex -26.0 -13.8 -2.6
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 23.6 -8.7 -11.0
vertex 23.6 -6.9 -12.8
vertex 21.8 -6.9 -11.0
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 23.6 -8.7 -11.0
vertex 21.8 -8.7 -12.8
vertex 23.6 -6.9 -12.8
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 23.6 -8.7 -11.0
vertex 21.8 -6.9 -11.0
vertex 21.8 -8.7 -12.8
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 23.6 -6.9 -12.8
vertex 21.8 -8.7 -12.8
vertex 21.8 -6.9 -11.0
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -18.1 22.3 -8.2
vertex -18.1 23.8 -9.7
vertex -19.6 23.8 -8.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -18.1 22.3 -8.2
vertex -19.6 22.3 -9.7
vertex -18.1 23.8 -9.7
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -18.1 22.3 -8.2
vertex -19.6 23.8 -8.2
vertex -19.6 22.3 -9.7
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -18.1 23.8 -9.7
vertex -19.6 22.3 -9.7
vertex -19.6 23.8 -8.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -20.6 22.4 -4.8
vertex -20.6 23.8 -6.2
vertex -22.0 23.8 -4.8
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -20.6 22.4 -4.8
vertex -22.0 22.4 -6.2
vertex -20.6 23.8 -6.2
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -20.6 22.4 -4.8
vertex -22.0 23.8 -4.8
vertex -22.0 22.4 -6.2
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -20.6 23.8 -6.2
vertex -22.0 22.4 -6.2
vertex -22.0 23.8 -4.8
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 27.6 -0.7 3.1
vertex 27.6 0.7 1.6
vertex 26.2 0.7 3.1
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 27.6 -0.7 3.1
vertex 26.2 -0.7 1.6
vertex 27.6 0.7 1.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 27.6 -0.7 3.1
vertex 26.2 0.7 3.1
vertex 26.2 -0.7 1.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 27.6 0.7 1.6
vertex 26.2 -0.7 1.6
vertex 26.2 0.7 3.1
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 26.3 1.9 -6.7
vertex 26.3 3.3 -8.1
vertex 24.9 3.3 -6.7
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 26.3 1.9 -6.7
vertex 24.9 1.9 -8.1
vertex 26.3 3.3 -8.1
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 26.3 1.9 -6.7
vertex 24.9 3.3 -6.7
vertex 24.9 1.9 -8.1
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 26.3 3.3 -8.1
vertex 24.9 1.9 -8.1
vertex 24.9 3.3 -6.7
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 27.0 -4.1 -4.3
vertex 27.0 -2.7 -5.7
vertex 25.7 -2.7 -4.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 27.0 -4.1 -4.3
vertex 25.7 -4.1 -5.7
vertex 27.0 -2.7 -5.7
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 27.0 -4.1 -4.3
vertex 25.7 -2.7 -4.3
vertex 25.7 -4.1 -5.7
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 27.0 -2.7 -5.7
vertex 25.7 -4.1 -5.7
vertex 25.7 -2.7 -4.3
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 19.7 -26.2 -5.6
vertex 19.7 -24.9 -7.0
vertex 18.3 -24.9 -5.6
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 19.7 -26.2 -5.6
vertex 18.3 -26.2 -7.0
vertex 19.7 -24.9 -7.0
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 19.7 -26.2 -5.6
vertex 18.3 -24.9 -5.6
vertex 18.3 -26.2 -7.0
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 19.7 -24.9 -7.0
vertex 18.3 -26.2 -7.0
vertex 18.3 -24.9 -5.6
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -8.7 23.8 7.7
vertex -8.7 25.2 6.3
vertex -10.1 25.2 7.7
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -8.7 23.8 7.7
vertex -10.1 23.8 6.3
vertex -8.7 25.2 6.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -8.7 23.8 7.7
vertex -10.1 25.2 7.7
vertex -10.1 23.8 6.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -8.7 25.2 6.3
vertex -10.1 23.8 6.3
vertex -10.1 25.2 7.7
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 14.6 26.3 8.0
vertex 14.6 27.7 6.7
vertex 13.3 27.7 8.0
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 14.6 26.3 8.0
vertex 13.3 26.3 6.7
vertex 14.6 27.7 6.7
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 14.6 26.3 8.0
vertex 13.3 27.7 8.0
vertex 13.3 26.3 6.7
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 14.6 27.7 6.7
vertex 13.3 26.3 6.7
vertex 13.3 27.7 8.0
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -25.6 -0.7 6.5
vertex -25.6 0.7 5.1
vertex -26.9 0.7 6.5
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -25.6 -0.7 6.5
vertex -26.9 -0.7 5.1
vertex -25.6 0.7 5.1
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -25.6 -0.7 6.5
vertex -26.9 0.7 6.5
vertex -26.9 -0.7 5.1
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -25.6 0.7 5.1
vertex -26.9 -0.7 5.1
vertex -26.9 0.7 6.5
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -21.0 2.0 14.3
vertex -21.0 3.3 13.0
vertex -22.3 3.3 14.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -21.0 2.0 14.3
vertex -22.3 2.0 13.0
vertex -21.0 3.3 13.0
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -21.0 2.0 14.3
vertex -22.3 3.3 14.3
vertex -22.3 2.0 13.0
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -21.0 3.3 13.0
vertex -22.3 2.0 13.0
vertex -22.3 3.3 14.3
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -16.4 -29.9 0.2
vertex -16.4 -28.6 -1.1
vertex -17.8 -28.6 0.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -16.4 -29.9 0.2
vertex -17.8 -29.9 -1.1
vertex -16.4 -28.6 -1.1
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -16.4 -29.9 0.2
vertex -17.8 -28.6 0.2
vertex -17.8 -29.9 -1.1
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -16.4 -28.6 -1.1
vertex -17.8 -29.9 -1.1
vertex -17.8 -28.6 0.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 17.7 26.0 -6.2
vertex 17.7 27.3 -7.6
vertex 16.4 27.3 -6.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 17.7 26.0 -6.2
vertex 16.4 26.0 -7.6
vertex 17.7 27.3 -7.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 17.7 26.0 -6.2
vertex 16.4 27.3 -6.2
vertex 16.4 26.0 -7.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 17.7 27.3 -7.6
vertex 16.4 26.0 -7.6
vertex 16.4 27.3 -6.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 27.3 3.7 -2.2
vertex 27.3 5.0 -3.5
vertex 26.0 5.0 -2.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 27.3 3.7 -2.2
vertex 26.0 3.7 -3.5
vertex 27.3 5.0 -3.5
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 27.3 3.7 -2.2
vertex 26.0 5.0 -2.2
vertex 26.0 3.7 -3.5
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 27.3 5.0 -3.5
vertex 26.0 3.7 -3.5
vertex 26.0 5.0 -2.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -22.3 11.2 -9.8
vertex -22.3 12.4 -11.1
vertex -23.6 12.4 -9.8
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -22.3 11.2 -9.8
vertex -23.6 11.2 -11.1
vertex -22.3 12.4 -11.1
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -22.3 11.2 -9.8
vertex -23.6 12.4 -9.8
vertex -23.6 11.2 -11.1
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -22.3 12.4 -11.1
vertex -23.6 11.2 -11.1
vertex -23.6 12.4 -9.8
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -7.4 -13.4 13.2
vertex -7.4 -12.1 12.0
vertex -8.7 -12.1 13.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -7.4 -13.4 13.2
vertex -8.7 -13.4 12.0
vertex -7.4 -12.1 12.0
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -7.4 -13.4 13.2
vertex -8.7 -12.1 13.2
vertex -8.7 -13.4 12.0
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -7.4 -12.1 12.0
vertex -8.7 -13.4 12.0
vertex -8.7 -12.1 13.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -14.3 -29.3 5.4
vertex -14.3 -28.1 4.2
vertex -15.6 -28.1 5.4
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -14.3 -29.3 5.4
vertex -15.6 -29.3 4.2
vertex -14.3 -28.1 4.2
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -14.3 -29.3 5.4
vertex -15.6 -28.1 5.4
vertex -15.6 -29.3 4.2
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -14.3 -28.1 4.2
vertex -15.6 -29.3 4.2
vertex -15.6 -28.1 5.4
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -23.6 3.8 10.9
vertex -23.6 5.0 9.6
vertex -24.8 5.0 10.9
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -23.6 3.8 10.9
vertex -24.8 3.8 9.6
vertex -23.6 5.0 9.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -23.6 3.8 10.9
vertex -24.8 5.0 10.9
vertex -24.8 3.8 9.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -23.6 5.0 9.6
vertex -24.8 3.8 9.6
vertex -24.8 5.0 10.9
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 20.7 17.0 11.9
vertex 20.7 18.2 10.7
vertex 19.5 18.2 11.9
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 20.7 17.0 11.9
vertex 19.5 17.0 10.7
vertex 20.7 18.2 10.7
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 20.7 17.0 11.9
vertex 19.5 18.2 11.9
vertex 19.5 17.0 10.7
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 20.7 18.2 10.7
vertex 19.5 17.0 10.7
vertex 19.5 18.2 11.9
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 21.8 -21.5 -7.3
vertex 21.8 -20.2 -8.6
vertex 20.6 -20.2 -7.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 21.8 -21.5 -7.3
vertex 20.6 -21.5 -8.6
vertex 21.8 -20.2 -8.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 21.8 -21.5 -7.3
vertex 20.6 -20.2 -7.3
vertex 20.6 -21.5 -8.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 21.8 -20.2 -8.6
vertex 20.6 -21.5 -8.6
vertex 20.6 -20.2 -7.3
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 19.7 -28.4 -0.1
vertex 19.7 -27.2 -1.3
vertex 18.5 -27.2 -0.1
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 19.7 -28.4 -0.1
vertex 18.5 -28.4 -1.3
vertex 19.7 -27.2 -1.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 19.7 -28.4 -0.1
vertex 18.5 -27.2 -0.1
vertex 18.5 -28.4 -1.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 19.7 -27.2 -1.3
vertex 18.5 -28.4 -1.3
vertex 18.5 -27.2 -0.1
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -25.6 -8.3 -3.1
vertex -25.6 -7.1 -4.3
vertex -26.9 -7.1 -3.1
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -25.6 -8.3 -3.1
vertex -26.9 -8.3 -4.3
vertex -25.6 -7.1 -4.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -25.6 -8.3 -3.1
vertex -26.9 -7.1 -3.1
vertex -26.9 -8.3 -4.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -25.6 -7.1 -4.3
vertex -26.9 -8.3 -4.3
vertex -26.9 -7.1 -3.1
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -22.6 -4.0 12.5
vertex -22.6 -2.8 11.3
vertex -23.8 -2.8 12.5
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -22.6 -4.0 12.5
vertex -23.8 -4.0 11.3
vertex -22.6 -2.8 11.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -22.6 -4.0 12.5
vertex -23.8 -2.8 12.5
vertex -23.8 -4.0 11.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -22.6 -2.8 11.3
vertex -23.8 -4.0 11.3
vertex -23.8 -2.8 12.5
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 27.3 6.0 1.8
vertex 27.3 7.2 0.5
vertex 26.0 7.2 1.8
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 27.3 6.0 1.8
vertex 26.0 6.0 0.5
vertex 27.3 7.2 0.5
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 27.3 6.0 1.8
vertex 26.0 7.2 1.8
vertex 26.0 6.0 0.5
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 27.3 7.2 0.5
vertex 26.0 6.0 0.5
vertex 26.0 7.2 1.8
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -26.3 -2.3 -0.6
vertex -26.3 -1.0 -1.8
vertex -27.6 -1.0 -0.6
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -26.3 -2.3 -0.6
vertex -27.6 -2.3 -1.8
vertex -26.3 -1.0 -1.8
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -26.3 -2.3 -0.6
vertex -27.6 -1.0 -0.6
vertex -27.6 -2.3 -1.8
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -26.3 -1.0 -1.8
vertex -27.6 -2.3 -1.8
vertex -27.6 -1.0 -0.6
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 11.3 24.1 8.8
vertex 11.3 25.3 7.6
vertex 10.1 25.3 8.8
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 11.3 24.1 8.8
vertex 10.1 24.1 7.6
vertex 11.3 25.3 7.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 11.3 24.1 8.8
vertex 10.1 25.3 8.8
vertex 10.1 24.1 7.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 11.3 25.3 7.6
vertex 10.1 24.1 7.6
vertex 10.1 25.3 8.8
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 24.9 -2.6 -9.7
vertex 24.9 -1.4 -11.0
vertex 23.7 -1.4 -9.7
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 24.9 -2.6 -9.7
vertex 23.7 -2.6 -11.0
vertex 24.9 -1.4 -11.0
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 24.9 -2.6 -9.7
vertex 23.7 -1.4 -9.7
vertex 23.7 -2.6 -11.0
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 24.9 -1.4 -11.0
vertex 23.7 -2.6 -11.0
vertex 23.7 -1.4 -9.7
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 9.8 22.9 -7.2
vertex 9.8 24.1 -8.4
vertex 8.6 24.1 -7.2
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 9.8 22.9 -7.2
vertex 8.6 22.9 -8.4
vertex 9.8 24.1 -8.4
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 9.8 22.9 -7.2
vertex 8.6 24.1 -7.2
vertex 8.6 22.9 -8.4
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 9.8 24.1 -8.4
vertex 8.6 22.9 -8.4
vertex 8.6 24.1 -7.2
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 25.2 9.8 -7.4
vertex 25.2 11.0 -8.6
vertex 24.0 11.0 -7.4
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 25.2 9.8 -7.4
vertex 24.0 9.8 -8.6
vertex 25.2 11.0 -8.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 25.2 9.8 -7.4
vertex 24.0 11.0 -7.4
vertex 24.0 9.8 -8.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 25.2 11.0 -8.6
vertex 24.0 9.8 -8.6
vertex 24.0 11.0 -7.4
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 17.3 -29.9 2.7
vertex 17.3 -28.7 1.5
vertex 16.1 -28.7 2.7
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 17.3 -29.9 2.7
vertex 16.1 -29.9 1.5
vertex 17.3 -28.7 1.5
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 17.3 -29.9 2.7
vertex 16.1 -28.7 2.7
vertex 16.1 -29.9 1.5
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 17.3 -28.7 1.5
vertex 16.1 -29.9 1.5
vertex 16.1 -28.7 2.7
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -8.9 -7.9 15.5
vertex -8.9 -6.7 14.3
vertex -10.1 -6.7 15.5
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -8.9 -7.9 15.5
vertex -10.1 -7.9 14.3
vertex -8.9 -6.7 14.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -8.9 -7.9 15.5
vertex -10.1 -6.7 15.5
vertex -10.1 -7.9 14.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -8.9 -6.7 14.3
vertex -10.1 -7.9 14.3
vertex -10.1 -6.7 15.5
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 17.9 26.6 6.6
vertex 17.9 27.7 5.4
vertex 16.7 27.7 6.6
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 17.9 26.6 6.6
vertex 16.7 26.6 5.4
vertex 17.9 27.7 5.4
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 17.9 26.6 6.6
vertex 16.7 27.7 6.6
vertex 16.7 26.6 5.4
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 17.9 27.7 5.4
vertex 16.7 26.6 5.4
vertex 16.7 27.7 6.6
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 25.7 -2.2 9.5
vertex 25.7 -1.0 8.3
vertex 24.5 -1.0 9.5
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 25.7 -2.2 9.5
vertex 24.5 -2.2 8.3
vertex 25.7 -1.0 8.3
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 25.7 -2.2 9.5
vertex 24.5 -1.0 9.5
vertex 24.5 -2.2 8.3
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 25.7 -1.0 8.3
vertex 24.5 -2.2 8.3
vertex 24.5 -1.0 9.5
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -6.2 -3.7 13.8
vertex -6.2 -2.5 12.6
vertex -7.3 -2.5 13.8
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -6.2 -3.7 13.8
vertex -7.3 -3.7 12.6
vertex -6.2 -2.5 12.6
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -6.2 -3.7 13.8
vertex -7.3 -2.5 13.8
vertex -7.3 -3.7 12.6
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -6.2 -2.5 12.6
vertex -7.3 -3.7 12.6
vertex -7.3 -2.5 13.8
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -26.2 3.1 2.4
vertex -26.2 4.3 1.2
vertex -27.4 4.3 2.4
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -26.2 3.1 2.4
vertex -27.4 3.1 1.2
vertex -26.2 4.3 1.2
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -26.2 3.1 2.4
vertex -27.4 4.3 2.4
vertex -27.4 3.1 1.2
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -26.2 4.3 1.2
vertex -27.4 3.1 1.2
vertex -27.4 4.3 2.4
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex -20.4 17.2 -9.7
vertex -20.4 18.4 -10.8
vertex -21.6 18.4 -9.7
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex -20.4 17.2 -9.7
vertex -21.6 17.2 -10.8
vertex -20.4 18.4 -10.8
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex -20.4 17.2 -9.7
vertex -21.6 18.4 -9.7
vertex -21.6 17.2 -10.8
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex -20.4 18.4 -10.8
vertex -21.6 17.2 -10.8
vertex -21.6 18.4 -9.7
endloop
endfacet
facet normal 0.577 0.577 0.577
outer loop
vertex 15.8 22.5 11.3
vertex 15.8 23.6 10.1
vertex 14.6 23.6 11.3
endloop
endfacet
facet normal 0.577 -0.577 -0.577
outer loop
vertex 15.8 22.5 11.3
vertex 14.6 22.5 10.1
vertex 15.8 23.6 10.1
endloop
endfacet
facet normal -0.577 -0.577 0.577
outer loop
vertex 15.8 22.5 11.3
vertex 14.6 23.6 11.3
vertex 14.6 22.5 10.1
endloop
endfacet
facet normal -0.577 0.577 -0.577
outer loop
vertex 15.8 23.6 10.1
vertex 14.6 22.5 10.1
vertex 14.6 23.6 11.3
endloop
endfacet
endsolid neurophify
```

## Results

| Input | Nodes | Edges | Regions | Connected components | Modularity Q | Run time |
|---|---|---|---|---|---|---|
| SilverBullet `docs/` folder, Markdown | 313 | 1460 | 24 | 8 | 0.3582 | 0.57 s to 0.64 s (5 runs) |
| graphify `graph.json` of a TypeScript code base | 2731 | 4386 | 24 | 162 | 0.5794 | 1.23 s to 1.45 s (5 runs) |

Measured on 2026-11-15 with neurophify 1.2.0 and the shell's `time python3 neurophify.py ...` on a ThinkPad T470p (Intel Core i7-7700HQ, load average 4.8 from other work), Python 3.14.8. The components and Q come from `REGIONS.md` of the same runs. The Markdown run includes one `git log` over the whole history of the SilverBullet repository. Two runs on the same input write byte-identical files.

## Quick start

```bash
git clone https://github.com/maciejszulia/neurophify.git
cd neurophify
python3 neurophify.py --selftest
python3 neurophify.py examples/graph.json
python3 neurophify.py . --title "This repository"
```

`examples/graph.json` is the call graph of `neurophify.py`, with a community and a time for each function. The last command draws the Markdown files of this repository. To rebuild the demo from the SilverBullet documentation:

```bash
git clone https://github.com/silverbulletmd/silverbullet.git ../silverbullet
git -C ../silverbullet checkout a0ab7e9d
python3 neurophify.py ../silverbullet/docs --title "SilverBullet docs" --out docs/demo --spin --stl
```

Clone the whole history: in a clone made with `--depth 1` every page has the time of the one commit.

The tool needs Python 3.11 or newer and nothing outside the standard library. Each run writes five files to `neurophify-out/` (change it with `--out DIR`):

| File | Content |
|---|---|
| `brain.html` | Interactive 3D view: drag to rotate, scroll to zoom, hover a node to read its name, click a node to fly to it, play the time bar to watch the graph grow. |
| `brain.svg` | Static picture of the same scene, seen from the same direction. |
| `brain.json` | Nodes with positions, regions and times, edges, regions. |
| `REGIONS.md` | Each region with its size, its 5 central nodes and its bridges to other regions; the Time section; graph metrics. |
| `CORE.md` | The 20 nodes with the largest weight: region, degree, last change, weight and, for a Markdown folder, the first paragraph of the page. |

Two options add files for a README. `--spin` writes `brain-spin.svg`: the brain turns once every 12 seconds, animated with SMIL and no script (313 kB for 313 nodes). `--stl` writes `brain.stl`: an ASCII STL model of both hemispheres and the 40 nodes with the most edges (51 kB), which GitHub renders in a fenced code block marked `stl`.

Other inputs:

```bash
python3 neurophify.py graphify-out/graph.json                       # a graph written by graphify
python3 neurophify.py notes/ --exclude '_archive' --exclude 'drafts/*' --title "My notes"
python3 neurophify.py --help                                        # all options, exit codes
```

With Docker, from the folder that holds `graph.json`:

```bash
docker run --rm -v "$PWD:/data" ghcr.io/maciejszulia/neurophify /data/graph.json --out /data/out
```

The `image` workflow publishes the image to the GitHub Container Registry when a `v*` tag is pushed; `docker build -t neurophify .` builds the same image locally. The container runs as root, so the files in `out/` belong to root; add `--user "$(id -u):$(id -g)"` to keep them yours.

`SKILL.md` makes the repository usable as an agent skill: link the folder into your skills directory and ask for "/neurophify" or "3D graph".

## How it works

![How neurophify works: input, regions, 3D layout, output files](docs/diagrams/how-it-works.svg)

1. Load. A file is read as a graphify `graph.json` in the networkx node-link format: `nodes` with `id`, `label` and `community`, and `links` or `edges` with `source` and `target`. A folder is read as Markdown: each `.md` file is a node, and `[[page]]`, `[[page|alias]]` and `[text](file.md)` links are edges. Links inside code blocks, hidden folders and the output folder are skipped.
2. Time. In a folder inside a git repository each page takes its first and last commit from one `git log`; a page with uncommitted changes takes the later of its last commit and its modification time as its last change. Outside git, the file modification time is both. A `graph.json` node may carry `"time"` as ISO 8601 or epoch seconds. `brain.html` shows a time bar with a Play button, and the Time section of `REGIONS.md` names the busiest day, the new nodes per month and, for the 30 days before the last change, each region as growing, active or dormant.
3. Regions. The `community` field of `graph.json` defines the regions. Without it, label propagation finds them (seed 42, at most 50 iterations); the 5 % of nodes with the most edges take a region but do not vote, so an index page does not pull every topic into one region. The legend keeps the 23 largest regions and merges the rest into "other".
4. Layout. Each hemisphere is an ellipsoid. Region centres lie on its surface along a Fibonacci spiral, and each region takes the surface points nearest its centre, as many as it has nodes, so it forms one patch. Inside the patch a force layout keeps linked nodes close and puts hubs near the centre.
5. Output. `brain.html` embeds the data and pins every node to its position (`fx`, `fy`, `fz`) in [3d-force-graph](https://github.com/vasturiano/3d-force-graph) 1.80.1. `brain.svg` projects the same positions from the same camera direction. Node size grows with the number of edges, and the 10 nodes with the most edges carry a permanent label.
6. Consolidation. `CORE.md` lists the 20 nodes with the largest weight

   $$w(v) = \bigl(1 + \deg(v)\bigr) \cdot 2^{-d(v)/30}$$

   where $\deg(v)$ is the number of edges of node $v$ and $d(v)$ is the number of days between the last change of $v$ and the newest change in the graph; a node without a time has $d(v) = 0$. A node loses half its weight for every 30 days without a change, and the 1 keeps a node without edges in the ranking. Ties go to the label, then the id. For a Markdown folder each entry adds the first paragraph of the page, without YAML frontmatter, headings and code blocks, at most 300 characters; the paragraph stays out of `brain.html` and `brain.json`.
7. Graph metrics. `REGIONS.md` ends with the number of connected components, the size of the largest one, the number of nodes without edges and the modularity of the regions

   $$Q = \sum_c \left[\frac{L_c}{m} - \left(\frac{D_c}{2m}\right)^2\right]$$

   where $L_c$ is the number of edges inside region $c$, $D_c$ is the sum of the degrees of the nodes of region $c$ and $m$ is the number of edges. "other" counts as one region, and a graph without edges has $Q = 0$.

## Relation to graphify

graphify builds a knowledge graph from code and documents and writes `graphify-out/graph.json`. neurophify reads that file and adds the third dimension. The code of graphify is not part of this repository, and neurophify runs without graphify: a folder of Markdown files is enough.

## Limits

- Regions from label propagation are a heuristic: with another seed, region borders move.
- The 3D view in `brain.html` loads 3d-force-graph from jsDelivr and needs a network connection; `brain.svg`, `REGIONS.md` and `CORE.md` work offline.
- In a region with more than 770 nodes the force layout is skipped and the hubs take the points nearest the centre.
- The legend shows at most 24 regions. "other" collects the smaller ones and can span both hemispheres.
- Edges are drawn without direction; edge types from `graph.json` are not shown.
- Only `.md` files are nodes; a link to a page that does not exist is dropped.
- A renamed file starts its time at the rename, because `git log` runs without `--follow`.
- The weight in `CORE.md` counts edges and the age of the last change; it does not read the text of a page.
- The Docker image has no git, so a Markdown folder takes the file modification time.

## License and author

MIT, see [LICENSE](LICENSE). Author: Maciej Szulia.

Demo data: the `docs/` folder of [SilverBullet](https://github.com/silverbulletmd/silverbullet) at commit `a0ab7e9d`, read on 2026-11-15, MIT license, Copyright 2022 Zef Hemel. `docs/demo/` holds page names, links and commit times derived from that folder, and `docs/demo/CORE.md` quotes the first paragraph of 20 pages, at most 300 characters each.
