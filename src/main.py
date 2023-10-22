import sys
import tkinter as tk
from tkinter import RIDGE, Label, PhotoImage, Scale, filedialog, font, messagebox

import numpy as np
from PIL import Image, ImageFilter, ImageTk

# Variáveis globais
current_image = None
original_image = None
edited_image = None
rotation_angle = 0
resized_image = None
max_width, max_height = 600, 300
gaussian_controls_visible = False

# Funções

# Função para abrir uma imagem

def open_image():
    global current_image, original_image, edited_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Todas as Imagens", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        original_image = Image.open(file_path)

        if original_image.mode == 'L':
            edited_image = original_image.convert('L')
        else:
            img_array = np.array(original_image)
            img_height, img_width, _ = img_array.shape

            if img_width > max_width or img_height > max_height:
                scale = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img_array = np.array(
                    original_image.resize((new_width, new_height)))

                edited_image = Image.fromarray(img_array)
            else:
                edited_image = original_image.copy()

        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image


# Função para remover a imagem
def remove_image():
    global current_image, original_image, edited_image
    label.config(image=None)
    label.image = None
    current_image = None
    original_image = None
    edited_image = None

# Função para girar a imagem


def rotate_image(clockwise=True):
    global current_image, edited_image, rotation_angle
    if current_image:
        max_width, max_height = 600, 300
        img_array = np.array(edited_image)

        if len(img_array.shape) == 2:
            img_height, img_width = img_array.shape
        else:
            img_height, img_width, _ = img_array.shape

        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img_array = np.array(edited_image.resize((new_width, new_height)))

        if clockwise:
            rotation_angle += 90
        else:
            rotation_angle -= 90

        if rotation_angle >= 360:
            rotation_angle = 0
        elif rotation_angle < 0:
            rotation_angle = 270

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


# Função para atualizar a rotação da imagem
def update_rotation_label():
    rotation_label.config(
        text=f"Ângulo de Rotação: {rotation_angle}°", fg=color_font_menu)


# Função para efeito de desfocar imagem
def apply_blur(blur_func):
    global current_image, edited_image
    if current_image:
        blurred_image = edited_image.filter(
            ImageFilter.GaussianBlur(radius=blur_func))
        edited_image.paste(blurred_image)
        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image


def apply_blur_effect():
    filter_func = 1
    apply_blur(filter_func)


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
            messagebox.showerror("Erro no ajuste de desfoque")


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
            image_resize_frame, text="Largura:", bg=main_window_color, fg=color_font_menu)
        width_label.pack(side="left", expand=False)
        width_entry = tk.Entry(image_resize_frame, width=10)
        width_entry.pack(side="left", expand=False)

        height_label = tk.Label(
            image_resize_frame, text="Altura:", bg=main_window_color, fg=color_font_menu)
        height_label.pack(side="left", expand=False)
        height_entry = tk.Entry(image_resize_frame, width=10)
        height_entry.pack(side="left", expand=False)

        def apply_resize():
            try:
                new_width = int(width_entry.get())
                new_height = int(height_entry.get())
                global resized_image
                resized_image = edited_image.resize(
                    (new_width, new_height), Image.LANCZOS)
                current_image = ImageTk.PhotoImage(resized_image)
                label.config(image=current_image)
                label.image = current_image
            except ValueError:
                messagebox.showerror(
                    "Erro", "Insira valores válidos para largura e altura.")

        # Botão para aplicar o redimensionamento
        apply_button = tk.Button(
            image_resize_frame, text="Aplicar", command=apply_resize, bg=main_window_color, fg=color_font_menu)
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
            image_resize_frame, text="Cancelar", command=cancel_resize, bg=main_window_color, fg=color_font_menu)
        cancel_button.pack(side="left", fill=tk.NONE)


# Função para converter a imagem para preto e branco
def image_color_to_pb():
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


def toggle_gaussian_controls():
    global current_image, gaussian_controls_visible

    if current_image:
        if gaussian_controls_visible:
            gaussian_radius_slider.pack_forget()
            apply_gaussian_button.pack_forget()
            gaussian_controls_visible = False
        else:
            gaussian_radius_slider.pack(side="left", padx=5, pady=5)
            apply_gaussian_button.pack(
                side="left", fill="both", padx=5, pady=5)
            gaussian_controls_visible = True

# Função para cancelar as alterações
def cancel_effect():
    global current_image, edited_image, original_image
    if original_image:
        if len(np.array(original_image).shape) == 2:
            img_array = np.array(original_image)
        else:
            img_array = np.array(original_image)
            img_height, img_width, _ = img_array.shape

            if img_width > max_width or img_height > max_height:
                scale = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img_array = np.array(
                    original_image.resize((new_width, new_height)))

        edited_image = Image.fromarray(img_array)
        current_image = ImageTk.PhotoImage(edited_image)
        label.config(image=current_image)
        label.image = current_image

# Função para salvar a imagem
def save_image():
    global current_image, edited_image
    if edited_image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("JPEG files", "*.jpg"),
                       ("PNG files", "*.png"), ("Todos os Arquivos", "*.*")]
        )
        if file_path:
            try:

                edited_image.save(file_path)
                messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao salvar a imagem: {str(e)}")


# Encerrar o programa
def close():
    main_window.quit()
    sys.exit()


# Interface gráfica
main_window = tk.Tk()

# Cores
main_window_color = "#021425"
color_menu = "#1a3242"
color_font_menu = "#99b9d9"
gaussian_color_frame = "#1a3242"

# Fontes de texto
font_menu_title = font.Font(family="Comic Sans MS",
                            size=16, underline=1, weight="bold")
font_menu = font.Font(family="Verdana", size=7)

main_window.title("Editor de Imagens")
logo = PhotoImage(file='src/images/image-editing.png')
main_window.iconphoto(True, logo)
main_window.configure(bg=main_window_color)
main_window.geometry("950x850")

# opções
options_frame = tk.Frame(main_window, bg=color_menu)
options_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

# Menu
menu_frame = tk.Frame(main_window, bg=color_menu)
menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

menu_title = Label(menu_frame, text="Menu",
                   font=font_menu_title, bg=color_menu, fg=color_font_menu)
menu_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


# Icones menu
open_image_icon = Image.open("src/images/adicionar-img.png")
remove_image_icon = Image.open("src/images/remover-img.png")
rotate_image_icon = Image.open("src/images/girar-img.png")
blur_image_icon = Image.open("src/images/desfocar-img.png")
gaussian_image_icon = Image.open("src/images/edicao-img.png")
resize_image_icon = Image.open("src/images/redimensionar-img.png")
image_color_to_pb_icon = Image.open("src/images/preto-branco-img.png")
cancel_image_icon = Image.open("src/images/desfazer-img.png")
save_image_icon = Image.open("src/images/salvar-img.png")
close_icon = Image.open("src/images/sair-img.png")

# Tamanho dos icones menu
open_image_icon = open_image_icon.resize((35, 35))
remove_image_icon = remove_image_icon.resize((35, 35))
rotate_image_icon = rotate_image_icon.resize((35, 35))
blur_image_icon = blur_image_icon.resize((35, 35))
gaussian_image_icon = gaussian_image_icon.resize((35, 35))
resize_image_icon = resize_image_icon.resize((35, 35))
image_color_to_pb_icon = image_color_to_pb_icon.resize((45, 45))
cancel_image_icon = cancel_image_icon.resize((35, 35))
save_image_icon = save_image_icon.resize((35, 35))
close_icon = close_icon.resize((35, 35))

# carrega o icone na tela
open_image_icon_photo = ImageTk.PhotoImage(open_image_icon)
remove_image_icon_photo = ImageTk.PhotoImage(remove_image_icon)
rotate_image_icon_photo = ImageTk.PhotoImage(rotate_image_icon)
blur_image_icon_photo = ImageTk.PhotoImage(blur_image_icon)
gaussian_image_icon_photo = ImageTk.PhotoImage(gaussian_image_icon)
resize_image_icon_photo = ImageTk.PhotoImage(resize_image_icon)
image_color_to_pb_icon_photo = ImageTk.PhotoImage(image_color_to_pb_icon)
cancel_image_icon_photo = ImageTk.PhotoImage(cancel_image_icon)
save_image_icon_photo = ImageTk.PhotoImage(save_image_icon)
close_icon_photo = ImageTk.PhotoImage(close_icon)

# Crie o botão e atribua a imagem como o ícone
menu_title = tk.Button(menu_frame, text="Carregar\nImagem", image=open_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=open_image,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=1, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Remover\nImagem", image=remove_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=remove_image,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=2, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Girar\nImagem", image=rotate_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=rotate_image,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=3, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Desfocar\nImagem", image=blur_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=apply_blur_effect,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=4, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Ajuste Desfoque\nImagem", image=gaussian_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=toggle_gaussian_controls,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=5, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Redimensionar\nImagem", image=resize_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=resize_image,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=6, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Converter para\nPreto e Branco", image=image_color_to_pb_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=image_color_to_pb,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=7, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Cancelar\nAlterações", image=cancel_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=cancel_effect,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=8, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Salvar\nImagem", image=save_image_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=save_image,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=9, column=0, columnspan=2, pady=5)

menu_title = tk.Button(menu_frame, text="Fechar\nEditor", image=close_icon_photo, compound="top",
                       font=font_menu, bg=color_menu, fg=color_font_menu, command=close,
                       relief="flat", highlightthickness=0)
menu_title.grid(row=10, column=0, columnspan=2, pady=30)


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

gaussian_radius_slider = Scale(
    gaussian_frame, from_=0, to=10, orient="horizontal", highlightthickness=0, length=200, label="Deslize para ajustar o desfoque", font=font_menu, bg=main_window_color, fg=color_font_menu)
gaussian_radius_slider.pack(side="left")
gaussian_radius_slider.pack_forget()

apply_gaussian_button = tk.Button(
    gaussian_frame, text="Aplicar", command=apply_gaussian_effect, highlightthickness=0, font=font_menu, bg=main_window_color, fg=color_font_menu)
apply_gaussian_button.pack_forget()

main_window.mainloop()
