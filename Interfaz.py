# imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import rcParams     # Esto es para modificar el estilo de fuente de los gráficos.


import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk ,Image
import tkinter.font as font
from matplotlib import style

# clase principal

class Interfaz:

    def __init__(self, ventanta):
        self.ventana = ventanta
        self.ventana.title('Potencial de accion de la neurona')
        self.fuente_ppal = font.Font(family='math')
        self.fuente_sec = ('math', 15, 'bold italic')
        self.color_1 = '#2b2c2f'
        self.color_2 = '#615d62'
        self.color_3 = '#414044'
        self.color_4 = '#8e858b'
        self.color_blanco = '#fff'
        self.color_negro = '#000'

        # -------- toolbar ------------
        self.frameHerramientas = Frame(self.ventana, bd=5 , bg=self.color_1)
        # genero los objetos imagen para la toolbox
        abrir_img = Image.open('Open.png')
        guardar_img = Image.open('Save.png')
        cerrar_img = Image.open('Close.png')
        abrir_icon = ImageTk.PhotoImage(abrir_img)
        guardar_icon = ImageTk.PhotoImage(guardar_img)
        cerrar_icon = ImageTk.PhotoImage(cerrar_img)
        
        # creo los botones con las imagenes definidas ateriormente
        self.abrir_btn = Button(self.frameHerramientas, image=abrir_icon, command=self.cargarDatos ,border="0",bg=self.color_1)
        self.guardar_btn = Button(self.frameHerramientas, image=guardar_icon, command=self.guardarDatos, border="0",bg=self.color_1)
        self.cerrar_btn = Button(self.frameHerramientas, image=cerrar_icon, command=self.cerrarAplicacion, border="0",bg=self.color_1)

        self.abrir_btn.image = abrir_icon
        self.guardar_btn.image = guardar_icon
        self.cerrar_btn.image = cerrar_icon
        # posiciono los botones y el frame
        self.abrir_btn.pack(side=LEFT, padx =2,pady=2)
        self.guardar_btn.pack(side=LEFT, padx =2,pady=2)
        self.cerrar_btn.pack(side=RIGHT, padx =2,pady=2)
        self.frameHerramientas.pack(side=TOP,fill=X)

        # --------  frame de contenido y subframes ------------

        self.frameContenido = Frame(self.ventana, bd=5 , bg=self.color_4)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameContenido.pack(expand=True, fill=BOTH)
        
        #defino los 2 frames que usara para que la interfaz quede bonita
        # el frame de la izquierda donde ira la grafica y los parametros de corriente
        self.frameLeft = Frame(self.frameContenido, bd=5, width=600 , bg=self.color_4)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameLeft.pack(side=LEFT, fill=Y)
        # el frame de la derecha donde iran los demas parametros y los metodos de solucion
        self.frameRight = Frame(self.frameContenido, bd=5, width=300 , bg=self.color_4)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameRight.pack(side=RIGHT, fill=Y)
        
        # Creo los contenedores de los botones, graficas y demas

        # frame de la grafica
        self.frameGrafica = Frame(self.frameLeft, bd = 5, height=450, width=585 , bg=self.color_2) 
        self.frameGrafica.place(x=0,y=0)
        # frame del apartado para la corriente
        self.frameCorriente = Frame(self.frameLeft, bd = 5, height=150, width=585 , bg=self.color_2)
        self.frameCorriente.place(x=0,y=455)
        # frame de los metodos
        self.frameMetodos = Frame(self.frameRight, bd = 5, height=300, width=285 , bg=self.color_2) 
        self.frameMetodos.place(x=0,y=0)
        # frame del los parametros
        self.frameParametros = Frame(self.frameRight, bd = 5, height=300, width=285 , bg=self.color_2)
        self.frameParametros.place(x=0,y=305)

    	# ================================ Variables para las formulas ================================
        self.fig = None
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
        self.intensidad1 = StringVar()
        self.intensidad2 = StringVar()
        # ================================ Contenido ==================================

        # contenido de corriente

        # radio button de corriente constate el cual llama a la funcion que habilita las entradas de datos
        self.corriente_cte = Radiobutton(master=self.frameCorriente, command = self.estadoEntradaCorriente ,text='Corriente constante', value=1,  variable=self.opcion, bg=self.color_2,font=self.fuente_sec)
        self.corriente_cte.place(x=0,y=30)

        
        # radio button de corriente variable el cual llama a la funcion que habilita las entradas de datos adicionales
        self.corriente_var = Radiobutton(master=self.frameCorriente, command = self.estadoEntradaCorriente, text='Corriente variable', value=2,  variable=self.opcion, bg=self.color_2,font=self.fuente_sec)
        self.corriente_var.place(x=0,y=70)

        
        
        # titulo de los parametros de tiempo 
        self.titulo_tiempo =  Label(self.frameCorriente,width=10, text='Tiempo', font=('math', 12, 'bold italic'),fg = self.color_blanco, bg =self.color_2) 
        self.titulo_tiempo.place(x=280,y=10)

        # entradas de tiempo para corriente constante

        self.tiempo1_in = Entry(master=self.frameCorriente, textvariable=self.tiempo1, width=5, font=self.fuente_sec)
        self.tiempo1_in.place(x=250,y=50)

        self.sep1 =  Label(self.frameCorriente,width=2, text='-', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.sep1.place(x=315,y=50)

        self.tiempo2_in = Entry(master=self.frameCorriente, textvariable=self.tiempo2, width=5, font=self.fuente_sec)
        self.tiempo2_in.place(x=350,y=50)

        self.ms_decor1 =  Label(self.frameCorriente,width=2, text='mS', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ms_decor1.place(x=415,y=50)

        # entradas de tiempo adicionales para corriente variable

        self.tiempo3_in = Entry(master=self.frameCorriente, textvariable=self.tiempo3, width=5, font=self.fuente_sec)
        self.tiempo3_in.place(x=250,y=90)

        self.sep2 =  Label(self.frameCorriente,width=2, text='-', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.sep2.place(x=315,y=90)

        self.tiempo4_in = Entry(master=self.frameCorriente, textvariable=self.tiempo4, width=5, font=self.fuente_sec)
        self.tiempo4_in.place(x=350,y=90)

        self.ms_decor2 =  Label(self.frameCorriente,width=2, text='mS', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ms_decor2.place(x=415,y=90)

        # titulo de las entradas de corriente
        self.titulo_intensidad =  Label(self.frameCorriente,width=10, text='Intensidad', font=('math', 10, 'bold italic'),fg = self.color_blanco, bg =self.color_2)
        self.titulo_intensidad.place(x=460,y=10)

        # intensidad corriente para corriente constante
        self.intensidad1_in = Entry(master=self.frameCorriente, textvariable=self.intensidad1, width=5, font=self.fuente_sec, highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intensidad1_in.place(x=470,y=50)

        self.ma_decor1 =  Label(self.frameCorriente,width=2, text='mA', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ma_decor1.place(x=540,y=50)

        # intensidad corriente para corriente variable
        self.intensidad2_in = Entry(master=self.frameCorriente, textvariable=self.intensidad2, width=5, font=self.fuente_sec, highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intensidad2_in.place(x=470,y=90)


        self.ma_decor1 =  Label(self.frameCorriente,width=2, text='mA', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ma_decor1.place(x=540,y=90)

        # desactivo las entradas hasta que se seleccione un tipo de corriente y le cambio el bg para que se vea cool
        self.tiempo1_in.configure(state="disabled", disabledbackground=self.color_3)
        self.tiempo2_in.configure(state="disabled", disabledbackground=self.color_3)
        self.intensidad1_in.configure(state="disabled", disabledbackground=self.color_3)
        self.tiempo3_in.configure(state="disabled", disabledbackground=self.color_3)
        self.tiempo4_in.configure(state="disabled", disabledbackground=self.color_3)
        self.intensidad2_in.configure(state="disabled", disabledbackground=self.color_3)
        


        # contenido de metodos de solucion, los nombres de las variables son lo suficientemente dicientes para saber que es cada cosa.
        self.metodos_lbl =  Label(self.frameMetodos, text='Métodos de solución', font=self.fuente_sec,fg = self.color_negro, bg =self.color_2)

        self.metodos_lbl.place(x=35,y=10)

        self.eulerfw_btn = Button(master=self.frameMetodos, text="Euler Adelante",  command = self.placeHolderFn, bg=self.color_3, fg = self.color_blanco,  width=20,height=1, font=self.fuente_ppal,border="0")
        self.eulerfw_btn.place(x=45,y=60)

        self.eulerbk_btn = Button(master=self.frameMetodos, text="Euler Atrás",  command = self.placeHolderFn, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulerbk_btn.place(x=45,y=100)

        self.eulermod_btn = Button(master=self.frameMetodos, text="Euler Mod",  command = self.placeHolderFn, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulermod_btn.place(x=45,y=140)

        self.rk2_btn = Button(master=self.frameMetodos, text="Runge-Kutta 2",  command = self.placeHolderFn, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk2_btn.place(x=45,y=180)

        self.rk4_btn = Button(master=self.frameMetodos, text="Runge-Kutta 4",  command = self.placeHolderFn, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk4_btn.place(x=45,y=220)

        # contenido de parametros
        # titulo
        self.metodos_lbl =  Label(self.frameParametros, text='Parámetros', font=self.fuente_sec,fg = self.color_negro, bg =self.color_2)

        self.metodos_lbl.place(x=75,y=10)
        # Parámetros
        # 1

        self.Vm0_lbl =  Label(self.frameParametros,width=5, text='V'+u"\u2098\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        
        self.Vm0_lbl.place(x=30,y=60)

        self.Vm0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=10, font=self.fuente_sec)
        self.Vm0_in.place(x=120,y=60)
        
        # 2

        self.n0_lbl =  Label(self.frameParametros,width=5, text='n'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)

        self.n0_lbl.place(x=30,y=100)

        self.n0_in = Entry(master=self.frameParametros, textvariable=self.n0, width=10, font=self.fuente_sec)
        self.n0_in.place(x=120,y=100)

        #3
        self.m0_lbl =  Label(self.frameParametros,width=5, text='m'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)

        self.m0_lbl.place(x=30,y=140)

        self.m0_in = Entry(master=self.frameParametros, textvariable=self.m0, width=10, font=self.fuente_sec)
        self.m0_in.place(x=120,y=140)


        #4
        self.h0_lbl =  Label(self.frameParametros,width=5, text='h'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)

        self.h0_lbl.place(x=30,y=180)

        self.h0_in = Entry(master=self.frameParametros, textvariable=self.h0, width=10, font=self.fuente_sec)
        self.h0_in.place(x=120,y=180)


        #5
        self.T_lbl =  Label(self.frameParametros,width=5, text='T:', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1) 

        self.T_lbl.place(x=30,y=220)

        self.T_in = Entry(master=self.frameParametros, textvariable=self.T, width=10, font=self.fuente_sec)
        self.T_in.place(x=120,y=220)
        

    def placeHolderFn(self):
        if self.fig is None:
            self.fig = plt.Figure(figsize=(4, 3), dpi=100)
        t = np.arange(0,10, 0.01)
        self.fig.add_subplot(111).plot(t, self.fun(t))     # subplot(filas, columnas, item)
        self.fig.suptitle(self.opcion.get())

        '''
        rcParams['font.family'] = 'serif'   # Define que las fuentes usadas en el gráfico son serifadas.
        plt.xlabel(r'$t\ \ [mS]$',fontsize='x-large')       # Título secundario del eje x
        plt.ylabel(r'$V_m\ [mV]$ ',fontsize='large')        # Título secundario del eje y
        plt.style.use('bmh')
        
        plt.title('Potencial de acción de una neurona', fontsize='x-large')
        plt.tight_layout(pad=2.0)
        '''

        Plot = FigureCanvasTkAgg(self.fig, master=self.frameGrafica)
        Plot.draw()
        toolbar = NavigationToolbar2Tk(Plot, self.frameGrafica, pack_toolbar=False)
        toolbar.update()
        toolbar.place(x=0, y=200 )
        Plot.get_tk_widget().place(x=8,y=8)

    def fun(self, t):
        opt = self.opcion.get()
        if opt == 1:
            return np.sin(t)
        elif opt == 2:
            return np.cos(t)

    def estadoEntradaCorriente(self):
        ''' Funcion que activa las entradas correspondientes a la opcion de corriente indicacda en la variable opcion, 1 para corriente constante y 2 para corriente variable
        '''
        opt = self.opcion.get()
        if opt == 1:
            self.tiempo1_in.configure(state="normal")
            self.tiempo2_in.configure(state="normal")
            self.intensidad1_in.configure(state="normal")
            self.tiempo3_in.configure(state="disabled")
            self.tiempo4_in.configure(state="disabled")
            self.intensidad2_in.configure(state="disabled")
        elif opt == 2:
            self.tiempo1_in.configure(state="normal")
            self.tiempo2_in.configure(state="normal")
            self.intensidad1_in.configure(state="normal")
            self.tiempo3_in.configure(state="normal")
            self.tiempo4_in.configure(state="normal")
            self.intensidad2_in.configure(state="normal")


    def cerrarAplicacion(self):
        ''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
        '''
        MsgBox =  messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        if MsgBox == 'yes':
            self.ventana.destroy()     #FIXME Botón de cierre no funciona.
            self.ventana.quit()
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')
    

    def guardarDatos(self):
        ''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
        '''
        file_name = filedialog.asksaveasfilename()
        try:
            with open(file_name,'wb') as f:
                pass
        except:
            pass
        
    

    def cargarDatos(self):
        ''' Funcion que abre un dialogo para seleccionar un archivo del cual se cargaran los datos de una ejecucion previa en formato double
        '''
        file_name = filedialog.askopenfilename()
        try:
            with open(file_name,'rb') as f:
                pass
        except:
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
