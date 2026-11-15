---
name: neurophify
description: Draw a knowledge graph as a 3D brain. Reads graphify-out/graph.json or a folder of Markdown notes and writes brain.html, brain.svg, brain.json, REGIONS.md and CORE.md; with --spin a turning SVG for a README, with --stl an STL model. Use when the user says "/neurophify", "3D graph", "graf 3D", "neurophify", "model 3D do README", or asks to see notes or a graph as a brain.
---

# neurophify

Skill rysuje graf wiedzy jako mózg w 3D. Skrypt `neurophify.py` czyta plik `graph.json` skillu graphify albo folder plików Markdown. Skrypt dzieli węzły na regiony. Skrypt układa regiony na 2 półkulach mózgu.

Dla folderu w repozytorium git skrypt bierze z historii gita pierwszy oraz najnowszy commit każdej strony. Plik `brain.html` pokazuje wzrost grafu na pasku czasu. Plik `CORE.md` zawiera 20 węzłów o największej ważności; dla folderu Markdown plik `CORE.md` zawiera też pierwszy akapit strony każdego z 20 węzłów.

## Słownik

| Termin | Definicja | Słowa zakazane |
|---|---|---|
| węzeł | Strona Markdown albo węzeł z pliku `graph.json`. | punkt, element. |
| krawędź | Link, który łączy 2 węzły. | połączenie, relacja. |
| region | Grupa węzłów, którą skrypt rysuje 1 kolorem na 1 płacie półkuli. | klaster, społeczność. |
| ważność | Liczba, którą skrypt liczy dla węzła z liczby krawędzi węzła oraz z czasu między najnowszą zmianą węzła a najnowszą zmianą w grafie. | priorytet. |
| folder wyjścia | Folder, do którego skrypt zapisuje pliki wyjścia. | katalog wyników. |

## Kroki

Wykonaj każdy krok w tej kolejności:

1. Sprawdź, czy plik `graphify-out/graph.json` istnieje w katalogu roboczym.
   - Jeżeli plik `graphify-out/graph.json` istnieje, to użyj tego pliku jako wejścia.
   - Jeżeli plik `graphify-out/graph.json` nie istnieje, to użyj folderu Markdown z prośby użytkownika.
   - Jeżeli prośba użytkownika nie wskazuje folderu, to użyj katalogu roboczego.
2. Uruchom skrypt `neurophify.py` z folderu tego skillu. Wstaw ścieżkę folderu skillu w miejsce `<skill>`. Komenda dla pliku `graph.json`:

   ```bash
   python3 <skill>/neurophify.py graphify-out/graph.json --out neurophify-out
   ```

   Komenda dla folderu Markdown:

   ```bash
   python3 <skill>/neurophify.py <folder> --out neurophify-out --title "<tytuł>"
   ```

   Opcja `--exclude WZORZEC` pomija pliki i foldery, których ścieżka względna pasuje do wzorca. Użyj tej opcji 1 raz dla każdego wzorca.

   Opcja `--spin` zapisuje dodatkowo plik `brain-spin.svg`: mózg obraca się 1 raz na 12 s. Opcja `--stl` zapisuje dodatkowo plik `brain.stl`: 2 półkule i 40 węzłów o największym stopniu. Użyj obu opcji, gdy użytkownik chce model 3D w README na GitHubie.
3. Sprawdź kod wyjścia skryptu.
   - Kod 0: skrypt zapisał 5 plików oraz 1 plik dla każdej z opcji `--spin` i `--stl`. Wynik: skrypt wypisuje liczbę węzłów, krawędzi i regionów oraz ścieżkę każdego pliku.
   - Kod 2: skrypt wypisuje błąd i wiersz `fix:`. Popraw wejście według wiersza `fix:`. Potem wróć do kroku 2.
4. Przeczytaj tabelę na początku pliku `REGIONS.md`. Tabela podaje regiony od największego. Region „other” stoi zawsze na końcu tabeli.
5. Podaj użytkownikowi każdą informację z listy:
   - Ścieżki 5 plików: `brain.html`, `brain.svg`, `brain.json`, `REGIONS.md`, `CORE.md`.
   - Nazwy 3 największych regionów z pliku `REGIONS.md` oraz liczbę węzłów w każdym z 3 regionów.
   - Uwagę: widok 3D w pliku `brain.html` pobiera bibliotekę 3d-force-graph z serwera jsDelivr.
   - Ścieżkę każdego dodatkowego pliku, jeżeli komenda miała opcję `--spin` lub opcję `--stl`.

## Granice

- Skrypt używa tylko biblioteki standardowej Pythona w wersji 3.11 lub nowszej.
- Plik `brain.html` wymaga dostępu do sieci. Pliki `brain.svg`, `REGIONS.md` oraz `CORE.md` działają bez sieci.
- Legenda ma co najwyżej 24 regiony. Skrypt łączy mniejsze regiony w region „other”.
- Plik `brain-spin.svg` używa animacji SMIL. Blok `stl` w README na GitHubie wymaga przeglądarki z WebGL.
- Komenda `python3 neurophify.py --selftest` sprawdza skrypt w folderze tymczasowym.
