import cv2
import numpy as np

# Kamerayı açma
cap = cv2.VideoCapture(0)

# Kamera açılmadıysa hata mesajı göster
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# Ekran boyutları
width, height = 800, 800
frame_width, frame_height = 120, 120  # Her bir yüzün boyutu

# 3x3 hücreler için
cell_size = 40  # Hücre boyutu (her hücre 40x40 px)

# Yeni 3x3 kare için hücre boyutu (75x75 px)
main_cell_size = 75  # Hücre boyutu (her hücre 75x75 px)

# Yüzlerin konumları (Ekranda her yüzü yerleştireceğimiz x, y koordinatları)
positions = [
    (30, 20),    # F yüzü
    (30, 170),   # R yüzü
    (500, 20),   # L yüzü
    (30, 320),   # U yüzü
    (500, 170),  # D yüzü
    (500, 320)   # B yüzü
]

letter_positions = [
    (79,92),#F
    (79,242),#R
    (549,92),#L
    (79,392),#U
    (549,242),#D
    (549,392)#B
]

center_cell_properties = {
    'F': {'top_left': (70, 60), 'bottom_right': (110, 100), 'color': (0, 255, 0)},   # Yeşil
    'R': {'top_left': (70, 210), 'bottom_right': (110, 250), 'color': (0, 0, 255)},  # Kırmızı
    'U': {'top_left': (70, 360), 'bottom_right': (110, 400), 'color': (255, 255, 255)},  # Beyaz
    'L': {'top_left': (540, 60), 'bottom_right': (580, 100), 'color': (255, 0, 0)},  # Mavi
    'D': {'top_left': (540, 210), 'bottom_right': (580, 250), 'color': (50, 255, 255)}, # Sarı
    'B': {'top_left': (540, 360), 'bottom_right': (580, 400), 'color': (0, 140, 255)}, # Turuncu
}

keys = list(center_cell_properties.keys())
current_index = 0

letters = ['F', 'R', 'L', 'U', 'D', 'B']  # Front, Right, Left, Up, Down, Back

# Yeni 3x3'lük kare için pozisyon (Ekranın merkezi)
center_position = (215, 135)  # Ekranın merkezi, 50 piksel sola ve 100 piksel yukarı alındı

# Capture button position
button_position = (250, 385)
finish_button_position = (250, 430)
button_width = 145
button_height = 40

# Global değişkenler bölümüne ekleyin
cube_colors = {}  # Karelerin renklerini tutacak sözlük

# Global değişkenler bölümüne ekleyin
CUBE_MAIN_COLORS = {
    'green': (0, 255, 0),    # Yeşil (F)
    'red': (0, 0, 255),      # Kırmızı (R)
    'blue': (255, 0, 0),     # Mavi (L)
    'white': (255, 255, 255), # Beyaz (U)
    'yellow': (50, 255, 255), # Sarı (D)
    'orange': (0, 140, 255)   # Turuncu (B)
}

# Global değişkenler bölümüne ekleyin (diğer global değişkenlerle birlikte)
current_letter = 'F'  # Başlangıç yüzü
current_color = (0, 255, 0)  # Başlangıç rengi (yeşil)

# Merkez kare ve komşu kareler için koordinatlar
kare_merkez = (
    center_position[0] + main_cell_size * 1.5,
    center_position[1] + main_cell_size * 1.5
)

# Çevresindeki karelerin merkezleri
komsu_orta_noktalari = {
    "Üst": (kare_merkez[0], kare_merkez[1] - main_cell_size),
    "Alt": (kare_merkez[0], kare_merkez[1] + main_cell_size),
    "Sol": (kare_merkez[0] - main_cell_size, kare_merkez[1]),
    "Sağ": (kare_merkez[0] + main_cell_size, kare_merkez[1]),
    "Sol Üst": (kare_merkez[0] - main_cell_size, kare_merkez[1] - main_cell_size),
    "Sağ Üst": (kare_merkez[0] + main_cell_size, kare_merkez[1] - main_cell_size),
    "Sol Alt": (kare_merkez[0] - main_cell_size, kare_merkez[1] + main_cell_size),
    "Sağ Alt": (kare_merkez[0] + main_cell_size, kare_merkez[1] + main_cell_size),
}

def find_closest_color(bgr_color):
    min_distance = float('inf')
    closest_color = None
    
    # BGR değerlerini ayrı ayrı al
    b, g, r = bgr_color
    
    for color_name, (cb, cg, cr) in CUBE_MAIN_COLORS.items():
        # Öklid mesafesini hesapla
        distance = ((b - cb) ** 2 + (g - cg) ** 2 + (r - cr) ** 2) ** 0.5
        
        if distance < min_distance:
            min_distance = distance
            closest_color = (cb, cg, cr)
    
    return closest_color

# capture_rect_controller fonksiyonunu güncelle
def capture_rect_controller(text, color, should_print=False):
    cv2.rectangle(frame, ((center_position[0]+main_cell_size)+2, (center_position[1]+main_cell_size)+2), 
                  ((center_position[0] + (main_cell_size*2)) - 2, (center_position[1] + (main_cell_size)*2) - 2), 
                  color, -1)
    cv2.putText(frame, text, 
                ((center_position[0] + 1 * main_cell_size)+15, (center_position[1] + 2 * main_cell_size)-15), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    
    if should_print:
        square_mapping = {
            "Üst": f"{current_letter}1",
            "Alt": f"{current_letter}7",
            "Sol": f"{current_letter}3",
            "Sağ": f"{current_letter}5",
            "Sol Üst": f"{current_letter}0",
            "Sağ Üst": f"{current_letter}2",
            "Sol Alt": f"{current_letter}6",
            "Sağ Alt": f"{current_letter}8"
        }
        
        for konum, merkez in komsu_orta_noktalari.items():
            x, y = int(merkez[0]), int(merkez[1])
            bgr_color = frame[y, x]
            # Renk örneklemesi için daha geniş bir alan kullanalım
            bgr_color = get_average_color(frame, x, y, 5)  # 5x5 piksellik alan
            closest_color = find_closest_color(bgr_color)
            square_key = square_mapping[konum]
            cube_colors[square_key] = closest_color

def get_average_color(frame, x, y, size=5):
    """Belirli bir alan içindeki renklerin ortalamasını al"""
    half = size // 2
    roi = frame[y-half:y+half+1, x-half:x+half+1]
    return cv2.mean(roi)[:3]  # BGR değerlerini döndür

# Fare tıklama olayı
def click_event(event, x, y, flags, param):
    global current_index, current_letter, current_color
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_button_pressed(x, y, button_position):  # Capture butonu
            # Önce mevcut yüz için renkleri kaydet
            print(f"\nSeçilen yüz: {current_letter}")
            print(f"Seçilen renk: {current_color}")
            capture_rect_controller(current_letter, current_color, should_print=True)
            
            # Sonra bir sonraki yüze geç
            current_index = (current_index + 1) % len(keys)
            current_letter = keys[current_index]
            current_color = center_cell_properties[current_letter]['color']
        
        elif is_button_pressed(x, y, finish_button_position):  # Finish butonu
            save_cube_colors()  # Renkleri kaydet
            cv2.destroyAllWindows()
            cap.release()
            import subprocess
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(script_dir, 'main.py')
            subprocess.run(['python', main_path])
            exit()

# Tüm karelerin koordinatlarını tutacak sözlük
cube_squares = {}

# Her bir yüz için karelerin koordinatlarını hesapla
faces = ['F', 'R', 'L', 'U', 'D', 'B']
for face_idx, (base_x, base_y) in enumerate(positions):
    face = faces[face_idx]
    # Her bir yüzün 3x3 karelerini hesapla
    for row in range(3):
        for col in range(3):
            # Sol üst köşe koordinatları
            top_left_x = base_x + (col * cell_size)
            top_left_y = base_y + (row * cell_size)
            
            # Sağ alt köşe koordinatları
            bottom_right_x = top_left_x + cell_size
            bottom_right_y = top_left_y + cell_size
            
            # Karenin pozisyon indeksi (0-8)
            square_idx = row * 3 + col
            
            # Sözlüğe ekle
            square_key = f"{face}{square_idx}"  # Örnek: F0, F1, ..., B8
            cube_squares[square_key] = {
                'top_left': (top_left_x, top_left_y),
                'bottom_right': (bottom_right_x, bottom_right_y)
            }

# is_button_pressed fonksiyonunu güncelle
def is_button_pressed(x, y, button_pos):
    if button_pos[0] < x < button_pos[0] + button_width and button_pos[1] < y < button_pos[1] + button_height:
        return True
    return False

def save_cube_colors():
    # Renkleri bir dosyaya kaydet
    with open('cube_colors.txt', 'w') as f:
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            for i in range(9):
                square_key = f"{face}{i}"
                if square_key in cube_colors:
                    color = cube_colors[square_key]
                    color_name = get_color_name(color)
                    print(f"Saving {square_key}: {color_name}")  # Debug için
                    f.write(f"{square_key}:{color_name}\n")

def get_color_name(bgr_color):
    color_map = {
        (0, 255, 0): "green",    # Yeşil (F)
        (0, 0, 255): "red",      # Kırmızı (R)
        (255, 0, 0): "blue",     # Mavi (L)
        (255, 255, 255): "white", # Beyaz (U)
        (50, 255, 255): "yellow", # Sarı (D)
        (0, 140, 255): "orange"   # Turuncu (B)
    }
    
    # HSV renk uzayını kullanalım
    hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    
    # Her renk için HSV değer aralıkları tanımlayalım
    hsv_ranges = {
        "red": [(0, 50, 50), (10, 255, 255)],
        "green": [(45, 50, 50), (75, 255, 255)],
        "blue": [(110, 50, 50), (130, 255, 255)],
        "yellow": [(20, 50, 50), (40, 255, 255)],
        "orange": [(10, 50, 50), (20, 255, 255)],
        "white": [(0, 0, 200), (180, 30, 255)]
    }
    
    for color_name, (lower, upper) in hsv_ranges.items():
        if all(l <= v <= u for l, v, u in zip(lower, hsv_color, upper)):
            return color_name
            
    return "unknown"

# Ana döngü
while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame çekilemedi!")
        break

    # Yüzlerin çizilmesi (6 adet 3x3 hücre)
    for i, (x_offset, y_offset) in enumerate(positions):
        for row in range(3):
            for col in range(3):
                cell_x = x_offset + col * cell_size
                cell_y = y_offset + row * cell_size
                
                # Karenin pozisyon indeksi (0-8)
                square_idx = row * 3 + col
                square_key = f"{faces[i]}{square_idx}"
                
                # Eğer bu kare için kayıtlı bir renk varsa, o rengi kullan
                if square_key in cube_colors:
                    cv2.rectangle(frame, (cell_x, cell_y), 
                                (cell_x + cell_size, cell_y + cell_size), 
                                cube_colors[square_key], -1)
                
                # Karenin çerçevesini çiz
                cv2.rectangle(frame, (cell_x, cell_y), 
                            (cell_x + cell_size, cell_y + cell_size), 
                            (0, 255, 0), 2)

    # Yeni 3x3'lük kareyi ekleyelim (kamera görüntüsü için)
    for row in range(3):
        for col in range(3):
            cell_x = center_position[0] + col * main_cell_size
            cell_y = center_position[1] + row * main_cell_size
            cv2.rectangle(frame, (cell_x, cell_y), (cell_x + main_cell_size, cell_y + main_cell_size), (0, 255, 255), 2)  # Kenarlık çiz

    # Yüzlerin renklerinin çizilmesi
    for letter, properties in center_cell_properties.items():
        top_left = properties['top_left']
        bottom_right = properties['bottom_right']
        color = properties['color']
        cv2.rectangle(frame, top_left, bottom_right, color, -1)  # Yüzleri doldur

    # Harflerin eklenmesi
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2  # Kalınlık burada tanımlandı
    color = (0, 0, 0)  # Siyah
    for (x, y), text in zip(letter_positions, letters):
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)

    # "Capture" butonunun çizilmesi
    cv2.rectangle(frame, button_position, 
                 (button_position[0] + button_width, button_position[1] + button_height), 
                 (255, 0, 0), -1)
    cv2.putText(frame, "Capture", 
                (button_position[0] + 10, button_position[1] + 30), 
                font, font_scale, (255, 255, 255), thickness)

    # "Finish" butonunun çizilmesi
    cv2.rectangle(frame, finish_button_position, 
                 (finish_button_position[0] + button_width, finish_button_position[1] + button_height), 
                 (0, 0, 0), -1)  # Siyah arkaplan
    cv2.putText(frame, "Finish", 
                (finish_button_position[0] + 25, finish_button_position[1] + 30), 
                font, font_scale, (255, 255, 255), thickness)  # Beyaz yazı

    # Mevcut renk ve harfi göster
    capture_rect_controller(current_letter, current_color, should_print=False)
    
    
    

    # Çekilen frame'i ekranda göster
    cv2.imshow('Rubik\'s Cube', frame)
    cv2.setMouseCallback('Rubik\'s Cube', click_event)

    # 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak
cap.release()

# Pencereyi kapat
cv2.destroyAllWindows()
