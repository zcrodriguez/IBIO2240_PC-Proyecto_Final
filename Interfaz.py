# imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk ,Image
import tkinter.font as font
from matplotlib import style

# configuracion inicaial de la ventana
ventana = tk.Tk()                # Definimos la ventana con nombre ventana porque es una ventana
ventana.geometry('900x700')      # Tamaño de la ventana
ventana.title('')
ventana.config(cursor="arrow")   # Cursos de flecha
ventana.resizable(False, False)  # Hago que la ventana no sea ajustable en su tamaño
fuente_ppal = font.Font(family='math') # obtengo la fuente que se usara en la interfaz

# algunas funciuones auxiliares
def CerrarAplicacion():
    MsgBox = tk.messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
    if MsgBox == 'yes':
       ventana.destroy()
    else:
        tk.messagebox.showinfo('Retornar','Será retornado a la aplicación')


# Lindo boton rojo de cerrar
tk.Button(master=ventana, text="X",  command = CerrarAplicacion, bg='red', fg = '#ffffff',  width=8, font=fuente_ppal).place(x=0,y=0)

# Frames
frame1 = tk.Frame(master=ventana)
frame1.place(x=550, y=50)
frame1.config(bg="#fff", width=300, height=250, highlightbackground="black", highlightthickness=4)


frame2 = tk.Frame(master=ventana)
frame2.place(x=550, y=350)
frame2.config(bg="#fff", width=300, height=300, highlightbackground="black", highlightthickness=4)

frameGraf = tk.Frame(master=ventana)
frameGraf.place(x=100, y=80)
frameGraf.config(bg="#fff", width=400, height=350, highlightbackground="black", highlightthickness=4)

frame3 = tk.Frame(master=ventana)
frame3.place(x=100, y=450)
frame3.config(bg="#fff", width=400, height=200, highlightbackground="black", highlightthickness=4)



# importar exportar
tk.Button(master=ventana, text="Exportar",  command = CerrarAplicacion, bg='yellow', fg = '#000',  width=10,height=1, font=fuente_ppal).place(x=150, y=20)
tk.Button(master=ventana, text="Importar",  command = CerrarAplicacion, bg='yellow', fg = '#000',  width=10,height=1, font=fuente_ppal).place(x=350, y=20)

# parametros
params_lbl = tk.Label(frame1, text='Parametros', font=fuente_ppal,fg = '#000') 
params_lbl.place(x=100,y=20)

# Opciones de solucion
metodos_lbl = tk.Label(frame2, text='Métodos de solucion', font=fuente_ppal,fg = '#000') 
metodos_lbl.place(x=70,y=20)
tk.Button(master=frame2, text="Euler Adelante",  command = CerrarAplicacion, bg='green', fg = '#ffffff',  width=20,height=1, font=fuente_ppal).place(x=54,y=60)
tk.Button(master=frame2, text="Euler Atras",  command = CerrarAplicacion, bg='green', fg = '#ffffff',  width=20, height=1, font=fuente_ppal).place(x=54,y=120)
tk.Button(master=frame2, text="Runge-Kutta 2",  command = CerrarAplicacion, bg='green', fg = '#ffffff',  width=20, height=1, font=fuente_ppal).place(x=54,y=180)
tk.Button(master=frame2, text="Runge-Kutta 4",  command = CerrarAplicacion, bg='green', fg = '#ffffff',  width=20, height=1, font=fuente_ppal).place(x=54,y=240)

# Corriente
opcion = tk.IntVar()
tk.Radiobutton(master=frame3, text='Corriente fija', value=1, command=CerrarAplicacion, variable=opcion, bg='#A9CCE3',font=('math', 15, 'bold italic')).place(x=30,y=50)
tk.Radiobutton(master=frame3, text='Corriente variable', value=2, command=CerrarAplicacion, variable=opcion, bg='#A9CCE3',font=('math', 15, 'bold italic')).place(x=30,y=80)

# Main loop AKA EL LOOP
ventana.mainloop()