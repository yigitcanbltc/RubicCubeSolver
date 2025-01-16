import tkinter as tk
import random
import subprocess
import os
import threading
from tkinter import messagebox

root = tk.Tk()
root.title("6 Adet Kare Düzeni")
root.geometry("800x600")  # Ana pencere boyutu
root.resizable(False, False)

# Kare boyutları ve konum düzeni
square_size = 35
padding = 10  # Kareler arasındaki boşluk
positions = [
    (550, 215), (250, 60),  # İlk sıra
    (100, 215), (250, 215),  # İkinci sıra
    (400, 215), (250, 370)  # Üçüncü sıra
]

# Orta kareler için kullanılacak renkler (her biri yalnızca bir kez kullanılacak)
center_colors = ["orange","white","blue","green","red","yellow"]
ordered_center_colors = ["white","green","red","yellow","blue","orange"]
sides = ["B","U","L","F","R","D"]
ordered_sides = ["U","R","F","D","L","B"]
available_colors = ["white", "blue", "red", "green", "orange", "yellow"]

# Kullanıcının tıkladığı renk
selected_color = None
popup_open = None  # Pop-up penceresinin referansı
grid_frames = []  # 3x3 karelerin listesi
ordered_grid_frames = []

# Global değişkenler bölümüne ekleyin
solution_label = None

# Renk paletini oluştur
def create_color_palette():
    global selected_color
    
    # Renkler paletini sol üst köşeye ekle
    for i, color in enumerate(available_colors):
        color_button = tk.Button(root, bg=color, width=4, height=2, command=lambda c=color: set_selected_color(c))
        color_button.place(x=10, y=10 + i * 35)  # Y ekseninde sıralanmış butonlar

# Renk seçildiğinde yapılacak işlem
def set_selected_color(color):
    global selected_color
    selected_color = color

# Kareyi tıklayıp rengini değiştirmek
def change_square_color(event, frame):
    global selected_color
    if selected_color:  # Eğer bir renk seçilmişse
        frame.config(bg=selected_color)

def create_grid(x, y, i):
    """Her bir 3x3 düzenin içeriğini oluşturur."""
    container_frame = tk.Frame(root, bg="white")
    container_frame.place(x=x, y=y)

    # Büyük kareyi içeren frame
    big_frame = tk.Frame(container_frame, width=3 * square_size + 2 * padding, 
                        height=3 * square_size + 2 * padding, bg="white")
    big_frame.pack()

    # 3x3 kare matrisi oluştur
    grid_frames = []
    for row in range(3):
        for col in range(3):
            # Orta kare için özel renk atanır
            if row == 1 and col == 1:
                color = center_colors[i]
                frame = tk.Frame(
                    big_frame,
                    width=square_size,
                    height=square_size,
                    bg=color,
                    highlightbackground="black",
                    highlightthickness=1,
                )
                label = tk.Label(frame, text=sides[i], font=("Arial", 16), bg=center_colors[i])
                label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                color = "lightblue"
                frame = tk.Frame(
                    big_frame,
                    width=square_size,
                    height=square_size,
                    bg=color,
                    highlightbackground="black",
                    highlightthickness=1,
                )
            
            frame.grid(row=row, column=col, padx=5, pady=5)
            frame.pack_propagate(False)
            grid_frames.append(frame)  # Tüm frameleri listeye ekle
            frame.bind("<Button-1>", lambda event, f=frame: change_square_color(event, f))

    return grid_frames

def create_cube_state(all_grid_frames, ordered_colors):
    # Her yüz için ayrı bir string oluştur
    face_states = {
        'U': '',  # Up
        'R': '',  # Right
        'F': '',  # Front
        'D': '',  # Down
        'L': '',  # Left
        'B': ''   # Back
    }
    
    # Yüz indeksleri ile yüz harflerini eşleştir
    face_mapping = {
        1: 'U',  # Üst yüz (ikinci pozisyon)
        4: 'R',  # Sağ yüz (beşinci pozisyon)
        3: 'F',  # Ön yüz (dördüncü pozisyon)
        5: 'D',  # Alt yüz (altıncı pozisyon)
        2: 'L',  # Sol yüz (üçüncü pozisyon)
        0: 'B'   # Arka yüz (birinci pozisyon)
    }
    
    # Her grid için renkleri kontrol et
    for grid_idx, grid_frames in enumerate(all_grid_frames):
        current_face = face_mapping[grid_idx]
        for frame in grid_frames:
            for color in ordered_colors:
                if frame.cget("bg") == color:
                    if color == "white":
                        face_states[current_face] += "U"
                    elif color == "red":
                        face_states[current_face] += "R"
                    elif color == "green":
                        face_states[current_face] += "F"
                    elif color == "yellow":
                        face_states[current_face] += "D"
                    elif color == "blue":
                        face_states[current_face] += "L"
                    elif color == "orange":
                        face_states[current_face] += "B"
                    break
    
    # İstenen sırada birleştir: U R F D L B
    cube_state = (face_states['U'] + face_states['R'] + face_states['F'] + 
                 face_states['D'] + face_states['L'] + face_states['B'])
    
    return cube_state

def load_cube_colors():
    try:
        cube_data = {}
        with open('cube_colors.txt', 'r') as f:
            for line in f:
                square_key, color = line.strip().split(':')
                cube_data[square_key] = color
        return cube_data
    except FileNotFoundError:
        return None

def apply_cube_colors():
    cube_data = load_cube_colors()
    if not cube_data:
        return
    
    # Yüz sırası ve indeks eşleştirmeleri
    face_mapping = {
        'U': 1,  # Üst
        'R': 4,  # Sağ
        'F': 3,  # Ön
        'D': 5,  # Alt
        'L': 2,  # Sol
        'B': 0   # Arka
    }
    
    # Her yüz için renkleri uygula
    for face, pos_idx in face_mapping.items():
        if pos_idx < len(all_grid_frames):
            grid = all_grid_frames[pos_idx]
            for i in range(9):
                square_key = f"{face}{i}"
                if square_key in cube_data:
                    color = cube_data[square_key]
                    grid[i].configure(bg=color)
                    print(f"DEBUG: Setting {square_key} to {color}")

# 6 adet 3x3 kare düzeni oluşturuyoruz
all_grid_frames = []
for i, pos in enumerate(positions):
    x, y = pos
    grid_frames = create_grid(x, y, i)
    all_grid_frames.append(grid_frames)

# Renk paletini oluştur
create_color_palette()

def create_solution_label():
    global solution_label
    solution_label = tk.Label(root, 
                            text="Çözüm Adımları:\nHenüz çözüm yok",
                            font=("Arial", 12),
                            justify=tk.LEFT,
                            width=70,
                            wraplength=500,
                            bg="white",
                            relief="solid",
                            padx=10,
                            pady=10,
                            anchor="w")
    solution_label.place(x=10, y=520)

def run_solver(cube_state):
    global solution_label
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    solver_path = os.path.join(script_dir, 'cube_solver.py')
    
    with open('current_state.txt', 'w') as f:
        f.write(cube_state)
    
    try:
        result = subprocess.run(['python', solver_path], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        solution_text = result.stdout.strip()
        
        if "Hata" not in solution_text:
            # Sadece label'ın metnini güncelle
            solution_label.config(text=f"Çözüm Adımları:\n{solution_text}")
        else:
            messagebox.showerror("Hata", solution_text)
            
    except subprocess.CalledProcessError:
        messagebox.showerror("Hata", "Çözücü çalışırken bir hata oluştu!")

def solve():
    # Küp durumunu al
    cube_state = create_cube_state(all_grid_frames=all_grid_frames, ordered_colors=ordered_center_colors)
    
    # Çözücüyü ayrı bir thread'de çalıştır
    solver_thread = threading.Thread(target=run_solver, args=(cube_state,))
    solver_thread.daemon = True  # Ana uygulama kapandığında thread de kapansın
    solver_thread.start()

# Butonu oluştur
fill_random_button = tk.Button(root, text="Solve", font=("Arial", 12, "bold"), width=10, height=1, command=solve)
fill_random_button.place(x=685, y=5)

def start_color_detection():
    root.withdraw()  # Ana pencereyi gizle
    import subprocess
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    detection_path = os.path.join(script_dir, 'color_detection.py')
    subprocess.run(['python', detection_path])
    root.after(100, lambda: root.deiconify())  # Ana pencereyi tekrar göster
    root.after(200, apply_cube_colors)  # Renkleri yükle

# Soru işareti ikonu ve bilgi penceresi


# Scan Cube butonunu güncelle
scan_cube_button = tk.Button(root, text="Scan Cube", 
                           font=("Arial", 12, "bold"), 
                           width=10, height=1,
                           command=start_color_detection)
scan_cube_button.place(x=685, y=45)

# Ana pencere oluşturulduktan sonra renkleri yükle
root.after(100, apply_cube_colors)

# Ana pencere oluşturulduktan sonra label'ı oluştur (en alt kısma, mainloop'tan önce)
create_solution_label()


root.mainloop()
