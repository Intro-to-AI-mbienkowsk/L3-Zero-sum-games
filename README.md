# WSI 2023 LAB3 - Gry o sumie zerowej
### Maksym Bieńkowski

# Zawartość archiwum


## /src/

---
- `constants.py` - stałe, klasa enum opisująca zawartość pola na planszy, dataclass opisujący ruch
- `Player.py` - klasy reprezentujące gracza oraz poszczególne boty
- `TicTacToe.py` - logika gry

## uruchamialne skrypty

---
`runner.py` - GUI napisane w pycharmie, użytkownik może sam zmierzyć się z minimaxowym botem lub obejrzeć rozgrywkę
między botem minimaxowym a losowym. Uruchomienie `python3 -m runner`

`bvb.py` - skrypt przeprowadzający wiele gier między określonymi przez użytkownika botami, bez możliwości podglądu. Służy
do zauważenia szerszych prawidłowości i zwizualizowania wyników (po każdym eksperymencie wyświetlany jest wykres).

#### Flagi:
- `-n` - liczba gier do rozegrania między botami, domyślnie 50
- `-X` - który bot ma grać krzyżykiem, który zaczyna (m lub r oznaczające minimax lub random), domyślnie minimax
- `-O` - analogicznie, który bot ma grać kółkiem, domyślnie random.

Przykład użycia: `python3 -m bvb -n 20 -X m -O m` uruchamia 20 gier minimax vs minimax i wyświetla wykres obrazujący wyniki rozgrywek.

# Krótki opis rozwiązania

---

Zaimplementowałem algorytm minimax z przycinaniem gałęzi metodą alfa-beta. Rozwiązanie szczegółowo opisane w raporcie.