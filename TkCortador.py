##Modulo para la ventana
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
##Modulo para el recortador
import pyshorteners as py
##Validacion para enlaces
import requests
##Para hacer dataframe
import pandas as pd
##Para que se pueda copiar el URL
import pyperclip as pyp

##Funcion para reajustar el tamaño de la image
def resize_image(image_path, width, height):
  original_image = Image.open(image_path)
  resized_image = original_image.resize((width, height))
  return ImageTk.PhotoImage(resized_image)

##Funcion para pegar texto
def paste_to_entry(event=None):
    clipboard_text = root.clipboard_get()
    URL_LARGO.delete(0, tk.END)
    URL_LARGO.insert(0, clipboard_text)

##Creacion de la ventana
root=tk.Tk()
root.geometry("1000x500+30+30")
root.resizable(False, False)
root.title("Recortador de URL")

canva1=tk.Canvas(root, width=1000, height=500)
canva1.pack(fill="both", expand=True)

resized_bg=resize_image("BocchiTheRock1.jpg",1000,500)
canva1.create_image(0,0,image=resized_bg, anchor=tk.NW)


##Labels de Textos
label_url_largo=tk.Label(root, text="URL",
                         width=10, height=3,
                         relief="solid",
                         font=("Courier", 14) 
                        )
label_url_largo_1=canva1.create_window(200,200,
                                     anchor=tk.CENTER,
                                     window=label_url_largo
                                    )
##Ingresar Datos para que se pueda pegar el texto
URL_LARGO=tk.Entry(root,
                   textvariable=tk.StringVar(),
                   width=50,
                   font=("Courier",17),
                   bd=1,
                   relief="solid"
                  )
URL_LARGO_1=canva1.create_window(630,200,
                                 anchor=tk.CENTER,
                                 window=URL_LARGO
                                 )
URL_LARGO.bind(paste_to_entry)

##Boton para convertir URL largo a URL corto
def mostrar_aviso(titulo, mensaje, mensaje1):
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("500x250+50+50")
    nueva_ventana.resizable(False, False)

    texto = tk.Label(nueva_ventana, text=mensaje, justify=tk.CENTER,  wraplength=400)
    texto.pack()

    texto1 = tk.Label(nueva_ventana, text=mensaje1, justify=tk.CENTER,  wraplength=400)
    texto1.pack()

    ButtonBack=tk.Button(nueva_ventana, text="Volver",
                         command=nueva_ventana.destroy)
    ButtonBack.pack()

##Funcion para vaidad enlaces URL con Seguridad
def validar_enlace_http_Seguridad():
  enlace = URL_LARGO.get()
  try:
        response = requests.get(enlace)
        response.raise_for_status() 
        s = py.Shortener()
        url_acortado = s.tinyurl.short(enlace)
        
        ##Para copiar eb url_acortado en la memoria
        pyp.copy(url_acortado)

        mensaje = f"El enlace {enlace} es válido. Código de respuesta: {response.status_code}"
        mostrar_aviso("Aviso", mensaje, url_acortado)

        URL_LARGO.delete(0, tk.END)

  except requests.exceptions.RequestException as e:
        mensaje = f"Error al acceder al enlace {enlace}: {e}"
        mensaje1 = "No se pudo acortar en URL"
        mostrar_aviso("Aviso", mensaje, mensaje1)
        URL_LARGO.delete(0, tk.END)

  except py.ShorteningErrorException as e:
        mensaje = f"Error al acortar la URL {enlace}: {e}"
        mensaje1 = "No se pudo acortar en URL"
        mostrar_aviso("Aviso", mensaje, mensaje1)
        URL_LARGO.delete(0, tk.END)
        
##Funcion para ver el historial de los URL acortados
def History():
  nueva_ventana = tk.Toplevel(root)
  nueva_ventana.title()
  nueva_ventana.geometry("500x300+100+100")
  nueva_ventana.resizable(False, False)

  ##Crear tree
  tree=ttk.Treeview(nueva_ventana, columns=("URL", "URL Acortado"), show="headings")
  ##Agregar headings al tree
  tree.heading("URL", text="URL")
  tree.heading("URL Acortado", text="URL Acortado")
  tree.pack(padx=10, pady=10)
  
  ButtonBack=tk.Button(nueva_ventana, text="Volver",
                         command=nueva_ventana.destroy)
  ButtonBack.pack()
  

button1 = tk.Button(root, text="Acortar",
                    command=validar_enlace_http_Seguridad,
                    padx=10, pady=5, width=15, height=2)
button2 = tk.Button(root, text="Historial",
                    command=History,
                    padx=10, pady=5, width=15, height=2)

def borrar_contenido(): URL_LARGO.delete(0, tk.END)
button3 = tk.Button(root, text="Borrar",
                    command=borrar_contenido,
                    padx=10, pady=5, width=15, height=2)

x_spacing=150
canva1.create_window(200, 300, anchor=tk.W, window=button1)
canva1.create_window(200 + button1.winfo_reqwidth() + x_spacing, 300, anchor=tk.W, window=button2)
canva1.create_window(200 + 2 * (button1.winfo_reqwidth() + x_spacing), 300, anchor=tk.W, window=button3)

root.mainloop()


