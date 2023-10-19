import sys
import tkinter as tk
from tkinter import Label, PhotoImage, Scale, filedialog, font, messagebox

import numpy as np
from PIL import  Image, ImageFilter, ImageTk

# Variáveis globais    
current_image = None
original_image = None
edited_image = None
rotation_angle = 0
resized_image = None
max_width, max_height = 600, 300

# Funções

# Função para abrir uma imagem
def open_image():
    global current_image, original_image, edited_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        original_image = Image.open(file_path)

        img_array = np.array(original_image)
        img_height, img_width, _ = img_array.shape

        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img_array = np.array(original_image.resize((new_width, new_height)))

            edited_image = Image.fromarray(img_array)
        else:
            edited_image = original_image.copy()

        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image

# Função para girar a imagem
def rotate_image():
    global current_image, edited_image, rotation_angle
    if current_image:
        
        max_width, max_height = 600, 300  
        
        img_array = np.array(edited_image)
        img_height, img_width, _ = img_array.shape

        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img_array = np.array(edited_image.resize((new_width, new_height)))

            edited_image = Image.fromarray(img_array)

        rotation_angle += 90
        if rotation_angle > 360:
            rotation_angle = 0 

        if rotation_angle == 90:
            edited_image = edited_image.transpose(Image.ROTATE_90)
        elif rotation_angle == 180:
            edited_image = edited_image.rotate(rotation_angle, expand=True)
        elif rotation_angle == 270:
            edited_image = edited_image.transpose(Image.ROTATE_270)
        else:
            edited_image = edited_image.transpose(Image.FLIP_TOP_BOTTOM) 

        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image
        update_rotation_label()


# Função para salvar a imagem
def save_image():
    global current_image, edited_image
    if edited_image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                       ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                
                edited_image.save(file_path)
                messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao salvar a imagem: {str(e)}")

# Função para efeito de desfocar imagem
def apply_blur_effect(blur_radius):
    global current_image, edited_image
    if current_image:
        blurred_image = edited_image.filter(
            ImageFilter.GaussianBlur(radius=blur_radius))
        edited_image.paste(blurred_image)
        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image

        
def blur_effect():
    blur_radius = 2
    apply_blur_effect(blur_radius)        


        
def apply_gaussian_effect():
    global current_image, edited_image, original_image
    if current_image:
        try:
            blur_radius = gaussian_radius_slider.get()
            original_image = edited_image.copy() 
            blurred_image = edited_image.filter(
                ImageFilter.GaussianBlur(radius=blur_radius))
            edited_image = blurred_image.copy()
            current_image = ImageTk.PhotoImage(edited_image)
            label.config(image=current_image)
            label.image = current_image
        except ValueError:
            messagebox.showerror(
                "Erro", "Insira um valor válido para o raio do efeito gaussiano.")
def toggle_gaussian_controls():
    global current_image, gaussian_controls_visible

    if current_image:
        if gaussian_controls_visible:
            gaussian_radius_slider.pack_forget()
            apply_gaussian_button.pack_forget()
            # cancel_gaussian_button.pack_forget() 
            gaussian_controls_visible = False
        else:
            gaussian_radius_slider.pack(side="left", padx=5, pady=5)
            apply_gaussian_button.pack(side="left", padx=5, pady=5)
            # cancel_gaussian_button.pack(side="left", padx=5, pady=5)  
            gaussian_controls_visible = True            

# Função para redimensionar a imagem
def resize_image():
    global current_image, edited_image, resized_image
    if current_image:
        for widget in image_resize_frame.winfo_children():
            widget.destroy()

        if resized_image is None:
            current_image = ImageTk.PhotoImage(edited_image)
        else:
            current_image = ImageTk.PhotoImage(resized_image)

        label.config(image=current_image)
        label.image = current_image

        width_label = tk.Label(
            image_resize_frame, text="Largura:", bg=main_window_color)
        width_label.pack(side="left", expand=False)
        width_entry = tk.Entry(image_resize_frame, width=10)
        width_entry.pack(side="left", expand=False)

        height_label = tk.Label(
            image_resize_frame, text="Altura:", bg=main_window_color)
        height_label.pack(side="left", expand=False)
        height_entry = tk.Entry(image_resize_frame, width=10)
        height_entry.pack(side="left", expand=False)

        def apply_resize():
            try:
                new_width = int(width_entry.get())
                new_height = int(height_entry.get())
                global resized_image
                resized_image = edited_image.resize(
                    (new_width, new_height), Image.ANTIALIAS)
                current_image = ImageTk.PhotoImage(resized_image)
                label.config(image=current_image)
                label.image = current_image
            except ValueError:
                messagebox.showerror(
                    "Erro", "Insira valores válidos para largura e altura.")

        # Botão para aplicar o redimensionamento
        apply_button = tk.Button(
            image_resize_frame, text="Aplicar", command=apply_resize, bg=main_window_color)
        apply_button.pack(side="left", fill=tk.NONE)

        # Função para cancelar o redimensionamento
        def cancel_resize():
            label.config(image=current_image)
            label.image = current_image
            width_entry.delete(0, tk.END)
            height_entry.delete(0, tk.END)

            for widget in image_resize_frame.winfo_children():
                widget.destroy()

        # Botão para cancelar o redimensionamento
        cancel_button = tk.Button(
            image_resize_frame, text="Cancelar", command=cancel_resize, bg=main_window_color)
        cancel_button.pack(side="left", fill=tk.NONE)


# Função para converter a imagem para preto e branco
def image_color():
    global current_image, edited_image
    if current_image:
        try:
            edited_image = edited_image.convert('L') 
            current_image = ImageTk.PhotoImage(edited_image)
            label.config(image=current_image)
            label.image = current_image
        except ValueError:
            messagebox.showerror(
                "Erro", "Ocorreu um erro ao converter a imagem para preto e branco.")


# Função para atualizar a rotação da imagem
def update_rotation_label():
    rotation_label.config(text=f"Ângulo de Rotação: {rotation_angle}°")


# Função para remover a imagem
def remove_image():
    global current_image, original_image, edited_image
    label.config(image=None)
    label.image = None
    current_image = None
    original_image = None
    edited_image = None

# Funções efeito gaussiano
gaussian_controls_visible = False

def toggle_gaussian_controls():
    global current_image, gaussian_controls_visible

    if current_image:
        if gaussian_controls_visible:
            gaussian_radius_slider.pack_forget()
            apply_gaussian_button.pack_forget()
            gaussian_controls_visible = False
        else:
            gaussian_radius_slider.pack(side="left", padx=5, pady=5)
            apply_gaussian_button.pack(side="left", padx=5, pady=5)
            gaussian_controls_visible = True

# Função para cancelar as alterações
def cancel_effect():
    global current_image, edited_image, original_image
    if original_image:
        img_array = np.array(original_image)
        img_height, img_width, _ = img_array.shape

        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img_array = np.array(original_image.resize((new_width, new_height)))

        edited_image = Image.fromarray(img_array)
        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image            


# Encerrar o programa
def close():
    main_window.quit()
    sys.exit()

# Interface gráfica
main_window = tk.Tk()

# Cores
main_window_color = "#5f7074"
color_menu = "#cadade"

# Fontes de texto
font_menu_title = font.Font(family="Comic Sans MS", size=16)
font_menu = font.Font(family="Comic Sans MS", size=8)

main_window.title("Editor de Imagens")
logo = PhotoImage(file='src/images/image-editing.png')
main_window.iconphoto(True, logo)
main_window.configure(bg=main_window_color)
main_window.geometry("800x650")

# opções
options_frame = tk.Frame(main_window, bg=color_menu)
options_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

# Menu
menu_frame = tk.Frame(main_window, bg=color_menu)
menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

menu_title = Label(menu_frame, text="Menu", font=font_menu_title)
menu_title.grid(row=0, column=1, padx=10, pady=10)

menu_buttons = [
    ("Carregar\nImagem", open_image),
    ("Remover\nImagem", remove_image),
    ("Girar\nImagem", rotate_image),
    ("Desfocar\nImagem", blur_effect),
    ("Aplicar\nGaussiano", toggle_gaussian_controls),
    ("Tamanho\nImagem", resize_image),
    ("Imagem\nP&B", image_color),
    ("Cancelar\nAlterações", cancel_effect),
    ("Salvar\nImagem", save_image),
    ("Sair", close)
]

for i, (text, command) in enumerate(menu_buttons, start=1):
    button = tk.Button(menu_frame, text=text,
                       command=command, font=font_menu, width=7)

    if text == "Sair":
        button.grid(row=i, column=1, padx=10, pady=50)
    else:
        button.grid(row=i, column=1, padx=5, pady=5)

# Crie um Frame para conter a imagem
image_frame = tk.Frame(main_window)
image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crie uma label para exibir a imagem carregada
label = tk.Label(image_frame, bg=main_window_color)
label.pack(fill=tk.BOTH, expand=True)

# Crie um rótulo para exibir o ângulo de rotação
rotation_label = tk.Label(image_frame, text="",
                          font=font_menu, bg=main_window_color)
rotation_label.pack(side="bottom", fill=tk.BOTH, expand=False)

# Variável global para armazenar a imagem atual
current_image = None
original_image = None
edited_image = None
rotation_angle = 0

# Crie um Frame para ajustar a imagem
image_resize_frame = tk.Frame(main_window, bg=main_window_color)
image_resize_frame.pack(side="bottom", fill=tk.BOTH, expand=False)

# Crie um Frame para ajustar o efeito gaussiano
gaussian_frame = tk.Frame(main_window, bg=main_window_color)
gaussian_frame.pack(side="bottom", fill=tk.BOTH, expand=False)

# Crie um Frame para ajustar o efeito gaussiano
gaussian_radius_slider = Scale(
    gaussian_frame, from_=0, to=10, orient="horizontal", length=200, label="Ajuste Gaussiano", bg=main_window_color)
gaussian_radius_slider.pack_forget()

apply_gaussian_button = tk.Button(
    gaussian_frame, text="Aplicar", command=apply_gaussian_effect, font=font_menu, bg=main_window_color)
apply_gaussian_button.pack_forget() 

main_window.mainloop()
