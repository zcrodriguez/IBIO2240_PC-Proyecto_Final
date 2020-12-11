# imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk ,Image
import tkinter.font as font
from matplotlib import style

# clase principal

class Interfaz:

    def __init__(self, ventanta):
        self.ventana = ventanta
        self.ventana.title('Potencial de accion neurona calamar gigante')
        self.fuente_ppal = font.Font(family='math')
        # -------- toolbar ------------
        self.frameHerramientas = Frame(self.ventana, bd=5 , bg='#2b2c2f')
        # genero los objetos imagen para la toolbox
        abrir_img = Image.open('Open.png')
        guardar_img = Image.open('Save.png')
        cerrar_img = Image.open('Close.png')
        abrir_icon = ImageTk.PhotoImage(abrir_img)
        guardar_icon = ImageTk.PhotoImage(guardar_img)
        cerrar_icon = ImageTk.PhotoImage(cerrar_img)
        
        # creo los botones con las imagenes definidas ateriormente
        self.abrir_btn = Button(self.frameHerramientas, image=abrir_icon, command=self.cargarDatos ,border="0",bg='#2b2c2f')
        self.guardar_btn = Button(self.frameHerramientas, image=guardar_icon, command=self.guardarDatos, border="0",bg='#2b2c2f')
        self.cerrar_btn = Button(self.frameHerramientas, image=cerrar_icon, command=self.cerrarAplicacion, border="0",bg='#2b2c2f')

        self.abrir_btn.image = abrir_icon
        self.guardar_btn.image = guardar_icon
        self.cerrar_btn.image = cerrar_icon
        # posiciono los botones y el frame
        self.abrir_btn.pack(side=LEFT, padx =2,pady=2)
        self.guardar_btn.pack(side=LEFT, padx =2,pady=2)
        self.cerrar_btn.pack(side=RIGHT, padx =2,pady=2)
        self.frameHerramientas.pack(side=TOP,fill=X)

        # --------  frame de contenido y subframes ------------

        self.frameContenido = Frame(self.ventana, bd=5 , bg='#8e858b')
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameContenido.pack(expand=True, fill=BOTH)
        
        #defino los 2 frames que usara para que la interfaz quede bonita
        # el frame de la izquierda donde ira la grafica y los parametros de corriente
        self.frameLeft = Frame(self.frameContenido, bd=5, width=600 , bg='#8e858b')
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameLeft.pack(side=LEFT, fill=Y)
        # el frame de la derecha donde iran los demas parametros y los metodos de solucion
        self.frameRight = Frame(self.frameContenido, bd=5, width=300 , bg='#8e858b')
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameRight.pack(side=RIGHT, fill=Y)
        
        # Creo los contenedores de los botones, graficas y demas

        # frame de la grafica
        self.frameGrafica = Frame(self.frameLeft, bd = 5, height=450, width=585 , bg='#615d62') 
        self.frameGrafica.place(x=0,y=0)
        # frame del apartado para la corriente
        self.frameCorriente = Frame(self.frameLeft, bd = 5, height=150, width=585 , bg='#615d62')
        self.frameCorriente.place(x=0,y=455)
        # frame de los metodos
        self.frameMetodos = Frame(self.frameRight, bd = 5, height=300, width=285 , bg='#615d62') 
        self.frameMetodos.place(x=0,y=0)
        # frame del los parametros
        self.frameParametros = Frame(self.frameRight, bd = 5, height=300, width=285 , bg='#615d62')
        self.frameParametros.place(x=0,y=305)

    	# ================================ Variables para las formulas ================================
        self.opcion =  IntVar()
        self.Vm_0 = StringVar()
        self.n0 = StringVar()
        self.m0 = StringVar()
        self.h0 = StringVar()
        self.T = StringVar()
        self.tiempo1 = StringVar()
        self.tiempo2 = StringVar()
        self.tiempo3 = StringVar()
        self.tiempo4 = StringVar()
        self.intencidad1 = StringVar()
        self.intencidad2 = StringVar()
        # ================================ Contenido ==================================

        # contenido de corriente
        self.corriente_cte = Radiobutton(master=self.frameCorriente, text='Corriente constante', value=1, command=self.placeHolderFn, variable=self.opcion, bg='#615d62',font=('math', 15, 'bold italic'))
        self.corriente_cte.place(x=0,y=30)

        

        self.corriente_var = Radiobutton(master=self.frameCorriente, text='Corriente variable', value=2, command=self.placeHolderFn, variable=self.opcion, bg='#615d62',font=('math', 15, 'bold italic'))
        self.corriente_var.place(x=0,y=70)

        
        
        # tiempos 
        self.titulo_tiempo =  Label(self.frameCorriente,width=10, text='Tiempo', font=('math', 12, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.titulo_tiempo.place(x=280,y=10)

        # linea de tiempo 1

        self.tiempo1_in = Entry(master=self.frameCorriente, textvariable=self.tiempo1, width=5, font=('math', 15, 'bold italic'))
        self.tiempo1_in.place(x=250,y=50)

        self.sep1 =  Label(self.frameCorriente,width=2, text='-', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.sep1.place(x=315,y=50)

        self.tiempo2_in = Entry(master=self.frameCorriente, textvariable=self.tiempo2, width=5, font=('math', 15, 'bold italic'))
        self.tiempo2_in.place(x=350,y=50)

        self.ms_decor1 =  Label(self.frameCorriente,width=2, text='mS', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.ms_decor1.place(x=420,y=50)

        # linea de tiempo 2

        self.tiempo3_in = Entry(master=self.frameCorriente, textvariable=self.tiempo3, width=5, font=('math', 15, 'bold italic'))
        self.tiempo3_in.place(x=250,y=90)

        self.sep2 =  Label(self.frameCorriente,width=2, text='-', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.sep2.place(x=315,y=90)

        self.tiempo4_in = Entry(master=self.frameCorriente, textvariable=self.tiempo4, width=5, font=('math', 15, 'bold italic'))
        self.tiempo4_in.place(x=350,y=90)

        self.ms_decor2 =  Label(self.frameCorriente,width=2, text='mS', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.ms_decor2.place(x=420,y=90)

        # intensidad corriente
        self.titulo_intencidad =  Label(self.frameCorriente,width=10, text='Intencidad', font=('math', 10, 'bold italic'),fg = '#fff', bg ='#615d62') 
        self.titulo_intencidad.place(x=460,y=10)

        self.intencidad1_in = Entry(master=self.frameCorriente, textvariable=self.intencidad1, width=5, font=('math', 15, 'bold italic'), highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intencidad1_in.place(x=470,y=50)

        self.intencidad2_in = Entry(master=self.frameCorriente, textvariable=self.intencidad2, width=5, font=('math', 15, 'bold italic'), highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intencidad2_in.place(x=470,y=90)

        

        # contenido de metodos
        self.metodos_lbl =  Label(self.frameMetodos, text='Métodos de solucion', font=('math', 15, 'bold italic'),fg = '#000', bg ='#615d62') 
        self.metodos_lbl.place(x=35,y=10)

        self.eulerfw_btn = Button(master=self.frameMetodos, text="Euler Adelante",  command = self.placeHolderFn, bg='#414044', fg = '#ffffff',  width=20,height=1, font=self.fuente_ppal,border="0")
        self.eulerfw_btn.place(x=45,y=60)

        self.eulerbk_btn = Button(master=self.frameMetodos, text="Euler Atras",  command = self.placeHolderFn, bg='#414044', fg = '#ffffff',  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulerbk_btn.place(x=45,y=100)

        self.eulermod_btn = Button(master=self.frameMetodos, text="Euler mod",  command = self.placeHolderFn, bg='#414044', fg = '#ffffff',  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulermod_btn.place(x=45,y=140)

        self.rk2_btn = Button(master=self.frameMetodos, text="Runge-Kutta 2",  command = self.placeHolderFn, bg='#414044', fg = '#ffffff',  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk2_btn.place(x=45,y=180)

        self.rk4_btn = Button(master=self.frameMetodos, text="Runge-Kutta 4",  command = self.placeHolderFn, bg='#414044', fg = '#ffffff',  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk4_btn.place(x=45,y=220)

        # contenido de parametros
        # titulo
        self.metodos_lbl =  Label(self.frameParametros, text='Parametros', font=('math', 15, 'bold italic'),fg = '#000', bg ='#615d62') 
        self.metodos_lbl.place(x=75,y=10)
        # parametros
        # 1
        self.Vm0_lbl =  Label(self.frameParametros,width=5, text='Vm_0:', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#2b2c2f') 
        self.Vm0_lbl.place(x=30,y=60)

        self.Vm0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=('math', 15, 'bold italic'))
        self.Vm0_in.place(x=120,y=60)
        
        # 2
        self.n0_lbl =  Label(self.frameParametros,width=5, text='n_0:', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#2b2c2f') 
        self.n0_lbl.place(x=30,y=100)

        self.n0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=('math', 15, 'bold italic'))
        self.n0_in.place(x=120,y=100)

        #3
        self.m0_lbl =  Label(self.frameParametros,width=5, text='m_0:', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#2b2c2f') 
        self.m0_lbl.place(x=30,y=140)

        self.m0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=('math', 15, 'bold italic'))
        self.m0_in.place(x=120,y=140)

        #4
        self.h0_lbl =  Label(self.frameParametros,width=5, text='h_0:', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#2b2c2f') 
        self.h0_lbl.place(x=30,y=180)

        self.h0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=('math', 15, 'bold italic'))
        self.h0_in.place(x=120,y=180)

        #5
        self.T_lbl =  Label(self.frameParametros,width=5, text='T:', font=('math', 15, 'bold italic'),fg = '#fff', bg ='#2b2c2f') 
        self.T_lbl.place(x=30,y=180)

        self.T_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=('math', 15, 'bold italic'))
        self.T_in.place(x=120,y=180)
        
    def placeHolderFn(self):
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        t = np.arange(0,10, 0.01)
        fig.add_subplot(111).plot(t, self.fun(t))     # subplot(filas, columnas, item)
        fig.suptitle(self.opcion.get())
        plt.style.use('seaborn-darkgrid')
        plt.close()
        Plot = FigureCanvasTkAgg(fig, master=self.frameGrafica)
        Plot.draw()
        Plot.get_tk_widget().place(x=0,y=0)

    def fun(self, t):
        opt = self.opcion.get()
        if opt == 1:
            return np.sin(t)
        elif opt == 2:
            return np.cos(t)
        elif opt == 3:
            return np.exp(t)
        elif opt == 4:
            return np.log(t)
        elif opt == 5:
            return np.sqrt(t)

    def cerrarAplicacion(self):
        MsgBox =  messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        if MsgBox == 'yes':
            self.ventana.quit()
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')
    

    def guardarDatos(self):
        print('TODO: guardar')
        pass
    

    def cargarDatos(self):
        print('TODO: cargar')
        pass


    def iniciar(self):
        self.ventana.mainloop()




# proceso que inicia la ventana y carga el app proceso que solo se llamara si se ejecuta este archivo y no si se lo importa
if __name__ == '__main__':
    # configuracion inicaial de la ventana
    ventana =  Tk()                  # Definimos la ventana con nombre ventana porque es una ventana
    ventana.geometry('900x700')      # Tamaño de la ventana
    ventana.config(cursor="arrow")   # Cursor de flecha
    ventana.resizable(False, False)  # Hago que la ventana no sea ajustable en su tamaño
    app = Interfaz(ventana)          # Genero el objeto interfaz
    app.iniciar()                    # Main loop AKA EL LOOP
