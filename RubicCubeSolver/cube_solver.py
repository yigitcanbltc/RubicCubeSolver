import kociemba
from collections import Counter

# Küp durumunu dosyadan oku
try:
    with open('current_state.txt', 'r') as f:
        cube_state = f.read().strip()
except FileNotFoundError:
    print("Hata: Küp durumu bulunamadı!")
    exit()

# Küp durumunu kontrol et
counter = Counter(cube_state)

if len(cube_state) == 54 and all(count == 9 for count in counter.values()) and len(counter) == 6:
    try:
        solution = kociemba.solve(cube_state)
        print(solution)  # Sadece çözümü yazdır
    except ValueError as e:
        print(f"Hata: {e}")
else:
    print("Hata: Küp durumu geçersiz!")
