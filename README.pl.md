# neurophify

Narzędzie neurophify rysuje graf wiedzy jako mózg w 3D. Narzędzie czyta plik `graph.json` z graphify albo folder notatek Markdown. Narzędzie dzieli węzły na regiony, układa regiony na 2 półkulach oraz pokazuje wzrost grafu w czasie. Plik `CORE.md` zawiera 20 węzłów o największej ważności.

[![ci](https://github.com/maciejszulia/neurophify/actions/workflows/ci.yml/badge.svg)](https://github.com/maciejszulia/neurophify/actions/workflows/ci.yml)

[English version](README.md)

Legenda: słowo „lub” oznacza co najmniej 1 człon. Słowo „albo” oznacza dokładnie 1 człon. Słowo MOŻE oznacza zezwolenie.

## Słownik

| Termin | Definicja | Słowa zakazane dla tego pojęcia |
|---|---|---|
| węzeł | Strona Markdown albo węzeł z pliku `graph.json`. | punkt, element. |
| krawędź | Link, który łączy 2 węzły. | połączenie, relacja. |
| stopień | Liczba krawędzi węzła. | waga. |
| region | Grupa węzłów, którą narzędzie rysuje 1 kolorem na 1 płacie półkuli. | klaster, społeczność. |
| płat | Część powierzchni półkuli, na której leżą węzły 1 regionu. | obszar, plama. |
| most | Krawędź, która łączy węzły z 2 różnych regionów. | łącznik. |
| hub | Węzeł, który należy do 5 % węzłów z największą liczbą krawędzi. | centrum. |
| label propagation | Algorytm, który daje węzłowi region przeważający wśród sąsiadów węzła. | klasteryzacja. |
| układ siłowy | Algorytm, który przyciąga połączone węzły oraz odpycha od siebie każde 2 węzły. | symulacja. |
| czas węzła | Para chwil: pierwsza zmiana węzła (pole `t`) oraz najnowsza zmiana węzła (pole `last`). | data, wiek. |
| ważność | Liczba $w(v)$ ze wzoru w kroku 6 sekcji „Sposób działania”. | priorytet, ranga. |
| konsolidacja | Zapis 20 węzłów o największej ważności w pliku `CORE.md`. | scalanie, merge. |
| składowa spójna | Zbiór węzłów, w którym ścieżka krawędzi łączy każde 2 węzły zbioru, bez krawędzi do węzła spoza zbioru. | grupa, wyspa. |
| modularność | Liczba $Q$ ze wzoru w kroku 7 sekcji „Sposób działania”. | jakość, spójność. |
| folder wyjścia | Folder, do którego narzędzie zapisuje 5 plików wyjścia. | katalog wyników. |
| skill | Folder z plikiem `SKILL.md`, który opisuje agentowi kroki zadania. | wtyczka. |
| image | Szablon kontenera Dockera z Pythonem oraz plikiem `neurophify.py`. | obraz. |

Skróty: 3D oznacza 3 wymiary. HTML, SVG, JSON oraz Markdown oznaczają formaty plików. CI oznacza continuous integration: GitHub Actions uruchamia testy po każdym pushu oraz dla każdego pull requesta.

## Demo

![Dokumentacja SilverBulleta w neurophify: 313 stron na 2 półkulach, kolory według regionów](docs/demo/brain.svg)

Rysunek to plik [`docs/demo/brain.svg`](docs/demo/brain.svg). Źródłem rysunku jest dokumentacja SilverBulleta. Wersja interaktywna 3D działa w GitHub Pages: [maciejszulia.github.io/neurophify/demo/brain.html](https://maciejszulia.github.io/neurophify/demo/brain.html). Kliknij przycisk Play na pasku czasu. Wynik: widok 3D pokazuje wzrost dokumentacji w latach od 2022 do 2026 włącznie. Raporty tekstowe to pliki [`docs/demo/REGIONS.md`](docs/demo/REGIONS.md) oraz [`docs/demo/CORE.md`](docs/demo/CORE.md).

## Wyniki

- Folder `docs/` SilverBulleta: 313 węzłów, 1460 krawędzi, 24 regiony, 8 składowych spójnych, modularność 0,3582. Czas przebiegu: od 0,57 s do 0,64 s włącznie w 5 przebiegach.
- Plik `graph.json` z graphify dla kodu TypeScript: 2731 węzłów, 4386 krawędzi, 24 regiony, 162 składowe spójne, modularność 0,5794. Czas przebiegu: od 1,23 s do 1,45 s włącznie w 5 przebiegach.

Pomiar: 2026-11-15, neurophify w wersji 1.2.0, komenda powłoki `time python3 neurophify.py ...`, komputer ThinkPad T470p z procesorem Intel Core i7-7700HQ, Python w wersji 3.14.8. W czasie pomiaru inna praca obciążała komputer: średnie obciążenie systemu wynosiło 4,8. Liczby składowych spójnych oraz modularność pochodzą z plików `REGIONS.md` tych samych przebiegów. Przebieg dla folderu Markdown zawiera 1 wywołanie `git log` dla całej historii repozytorium SilverBulleta. Dla tego samego wejścia 2 przebiegi zapisują identyczne pliki.

## Szybki start

```bash
git clone https://github.com/maciejszulia/neurophify.git
cd neurophify
python3 neurophify.py --selftest
python3 neurophify.py examples/graph.json
python3 neurophify.py . --title "This repository"
```

Plik `examples/graph.json` to graf wywołań funkcji w skrypcie `neurophify.py`. Węzeł każdej funkcji ma pole `community` oraz pole `time`. Komenda w wierszu 5 rysuje pliki Markdown tego repozytorium. Komendy, które odtwarzają demo z dokumentacji SilverBulleta:

```bash
git clone https://github.com/silverbulletmd/silverbullet.git ../silverbullet
git -C ../silverbullet checkout a0ab7e9d
python3 neurophify.py ../silverbullet/docs --title "SilverBullet docs" --out docs/demo
```

Sklonuj pełną historię repozytorium SilverBulleta. Klon z opcją `--depth 1` ma 1 commit, więc każda strona dostaje czas tego commitu.

Narzędzie wymaga Pythona w wersji 3.11 lub nowszej. Narzędzie używa tylko biblioteki standardowej. Każdy przebieg zapisuje 5 plików w folderze `neurophify-out/`. Opcja `--out FOLDER` zmienia folder wyjścia.

| Plik | Zawartość |
|---|---|
| `brain.html` | Interaktywny widok 3D. Przeciągnij mysz, żeby obrócić mózg. Najedź na węzeł, żeby odczytać nazwę węzła. Kliknij węzeł, żeby przybliżyć kamerę do węzła. Kliknij przycisk Play, żeby zobaczyć wzrost grafu. |
| `brain.svg` | Statyczny rysunek tej samej sceny z tego samego kierunku. |
| `brain.json` | Węzły z pozycjami, regionami oraz czasem węzła, krawędzie, regiony. |
| `REGIONS.md` | Każdy region: liczba węzłów, 5 węzłów centralnych, mosty do innych regionów. Na końcu pliku stoją sekcje „Time” oraz „Graph metrics”. |
| `CORE.md` | 20 węzłów o największej ważności: region, stopień, data najnowszej zmiany, ważność. Dla folderu Markdown każdy wiersz zawiera pierwszy akapit strony. |

Inne wejścia:

```bash
python3 neurophify.py graphify-out/graph.json                       # graf z graphify
python3 neurophify.py notes/ --exclude '_archive' --exclude 'drafts/*' --title "My notes"
python3 neurophify.py --help                                        # opcje oraz kody wyjścia
```

Komenda dla Dockera w folderze z plikiem `graph.json`:

```bash
docker run --rm -v "$PWD:/data" ghcr.io/maciejszulia/neurophify /data/graph.json --out /data/out
```

Workflow `image` publikuje image w GitHub Container Registry po każdym pushu tagu `v*`. Komenda `docker build -t neurophify .` buduje ten sam image lokalnie. Kontener działa z prawami użytkownika root, więc pliki w folderze `out/` należą do użytkownika root. Dodaj opcję `--user "$(id -u):$(id -g)"`, żeby pliki należały do użytkownika, który uruchamia komendę.

Plik `SKILL.md` pozwala użyć repozytorium jako skillu agenta. Utwórz w folderze skilli link do folderu repozytorium. Potem poproś agenta o „/neurophify” albo o „graf 3D”.

## Sposób działania

![Sposób działania neurophify: wejście, regiony, układ 3D, pliki wyjścia](docs/diagrams/how-it-works.pl.svg)

Narzędzie wykonuje każdy krok w tej kolejności:

1. Wczytanie. Narzędzie czyta plik jako `graph.json` z graphify w formacie node-link biblioteki networkx. Lista `nodes` zawiera pola `id`, `label` oraz `community`. Lista `links` albo lista `edges` zawiera pola `source` oraz `target`. Narzędzie czyta folder jako zbiór plików Markdown: każdy plik `.md` to węzeł, każdy link `[[strona]]`, `[[strona|alias]]` oraz `[tekst](plik.md)` to krawędź. Narzędzie pomija linki w blokach kodu, ukryte foldery oraz folder wyjścia.
2. Czas. Narzędzie ustala czas węzła według wejścia:
   - Folder w repozytorium git: narzędzie bierze pierwszy oraz najnowszy commit każdej strony z 1 wywołania `git log`. Jeżeli plik strony ma zmiany bez commitu, to najnowszą zmianą strony jest późniejsza z 2 chwil: najnowszy commit strony albo czas modyfikacji pliku.
   - Folder poza repozytorium git: czas modyfikacji pliku jest pierwszą oraz najnowszą zmianą strony.
   - Plik `graph.json`: węzeł MOŻE mieć pole `time` w formacie ISO 8601 albo w sekundach od epoki Unix.

   Plik `brain.html` pokazuje pasek czasu z przyciskiem Play. Sekcja „Time” w pliku `REGIONS.md` podaje dzień z największą liczbą nowych węzłów oraz liczbę nowych węzłów w każdym miesiącu. Sekcja „Time” podaje też stan każdego regionu w okresie 30 dni, który kończy się w chwili najnowszej zmiany w grafie: „growing”, „active” albo „dormant”.
3. Regiony. Pole `community` w pliku `graph.json` wyznacza regiony. Jeżeli pole `community` nie istnieje, to regiony wyznacza label propagation z ziarnem 42 w co najwyżej 50 iteracjach. Hub przyjmuje region od sąsiadów. Label propagation pomija głos huba. Powód: strona indeksu linkuje do każdego tematu, więc głos strony indeksu połączyłby tematy w 1 region. Legenda zawiera 23 największe regiony. Narzędzie łączy pozostałe regiony w region „other”.
4. Układ. Każda półkula to elipsoida. Środki regionów leżą na powierzchni elipsoidy wzdłuż spirali Fibonacciego. Każdy region zajmuje tyle punktów powierzchni, ile ma węzłów: punkty najbliższe środkowi regionu. Dlatego region tworzy 1 płat. Wewnątrz płata układ siłowy trzyma połączone węzły blisko siebie, a huby kładzie przy środku płata.
5. Wyjście. Plik `brain.html` osadza dane oraz przypina każdy węzeł do pozycji (`fx`, `fy`, `fz`) w bibliotece [3d-force-graph](https://github.com/vasturiano/3d-force-graph) w wersji 1.80.1. Plik `brain.svg` rzutuje te same pozycje z tego samego kierunku kamery. Rozmiar węzła rośnie z liczbą krawędzi. Stałą etykietę ma 10 węzłów z największą liczbą krawędzi.
6. Konsolidacja. Plik `CORE.md` zawiera 20 węzłów o największej ważności. Wzór ważności węzła $v$:

   $$w(v) = \bigl(1 + \deg(v)\bigr) \cdot 2^{-d(v)/30}$$

   Symbol $w(v)$ oznacza ważność węzła $v$, bez jednostki. Symbol $\deg(v)$ oznacza stopień węzła $v$, bez jednostki. Symbol $d(v)$ oznacza czas między najnowszą zmianą węzła $v$ a najnowszą zmianą w grafie. Jednostka symbolu $d(v)$ to dzień. Węzeł bez czasu ma $d(v) = 0$.

   Węzeł traci połowę ważności po każdych 30 dniach bez zmiany. Składnik 1 daje węzłowi bez krawędzi ważność większą niż 0. Przy równej ważności o kolejności decyduje etykieta, potem identyfikator węzła. Dla folderu Markdown każdy wiersz tabeli w pliku `CORE.md` zawiera pierwszy akapit strony: bez frontmattera YAML, nagłówków oraz bloków kodu, co najwyżej 300 znaków. Akapit trafia tylko do pliku `CORE.md`.
7. Metryki grafu. Sekcja „Graph metrics” stoi na końcu pliku `REGIONS.md`. Sekcja podaje liczbę składowych spójnych, liczbę węzłów największej składowej spójnej, liczbę węzłów bez krawędzi oraz modularność podziału na regiony:

   $$Q = \sum_c \left[\frac{L_c}{m} - \left(\frac{D_c}{2m}\right)^2\right]$$

   Symbol $c$ oznacza region. Symbol $L_c$ oznacza liczbę krawędzi wewnątrz regionu $c$. Symbol $D_c$ oznacza sumę stopni węzłów regionu $c$. Symbol $m$ oznacza liczbę krawędzi grafu. Każdy symbol jest liczbą bez jednostki.

   Region „other” to 1 region. Graf bez krawędzi ma $Q = 0$.

## Związek z graphify

Skill graphify buduje graf wiedzy z kodu oraz dokumentów. Skill graphify zapisuje plik `graphify-out/graph.json`. Narzędzie neurophify czyta plik `graphify-out/graph.json` i dodaje trzeci wymiar. Kod graphify nie należy do repozytorium. Narzędzie neurophify działa bez graphify: folder plików Markdown wystarcza.

## Granice

- Regiony z label propagation to heurystyka. Przy innym ziarnie granice regionów przesuwają się.
- Widok 3D w pliku `brain.html` pobiera bibliotekę 3d-force-graph z serwera jsDelivr. Dlatego widok 3D wymaga dostępu do sieci. Pliki `brain.svg`, `REGIONS.md` oraz `CORE.md` działają bez sieci.
- Jeżeli region ma więcej niż 770 węzłów, to narzędzie pomija układ siłowy w tym regionie. Wtedy huby zajmują punkty najbliższe środkowi płata.
- Legenda pokazuje co najwyżej 24 regiony. Region „other” zbiera mniejsze regiony. Region „other” leży na 1 półkuli albo na 2 półkulach: narzędzie wybiera podział, który wyrównuje liczby węzłów na półkulach.
- Narzędzie rysuje krawędzie bez kierunku. Narzędzie pomija typy krawędzi z pliku `graph.json`.
- Tylko pliki `.md` są węzłami. Narzędzie pomija link do strony, której brak w folderze.
- Narzędzie wywołuje `git log` bez opcji `--follow`. Dlatego czas pliku ze zmienioną nazwą zaczyna się od commitu, który zmienił nazwę pliku.
- Ważność w pliku `CORE.md` zależy tylko od stopnia węzła oraz od wieku najnowszej zmiany węzła. Narzędzie pomija treść strony przy liczeniu ważności.
- Image Dockera nie zawiera gita. Dlatego folder Markdown w kontenerze dostaje czas modyfikacji pliku.

## Licencja i autor

Licencja MIT, patrz plik [LICENSE](LICENSE). Autor: Maciej Szulia.

Dane demo: folder `docs/` repozytorium [SilverBullet](https://github.com/silverbulletmd/silverbullet), commit `a0ab7e9d`, odczyt 2026-11-15, licencja MIT, Copyright 2022 Zef Hemel. Folder `docs/demo/` zawiera nazwy stron, linki oraz czasy commitów z folderu `docs/` SilverBulleta. Plik `docs/demo/CORE.md` cytuje pierwszy akapit 20 stron: co najwyżej 300 znaków z każdej strony.
