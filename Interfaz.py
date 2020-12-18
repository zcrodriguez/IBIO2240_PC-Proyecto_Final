# imports
import numpy as np
import matplotlib.pyplot as plt # manipulacion de graficas
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # graficas y toolbar de graficas
from matplotlib.backend_bases import key_press_handler
from matplotlib.font_manager import FontProperties    # Esto es para modificar el estilo de fuente de los gráficos.
import matplotlib
from tkinter import *               # wild card import para evitar llamar tk cada vez

from tkinter import filedialog      # elegir archivos
from tkinter import messagebox      # mensaje de cerrar
from PIL import ImageTk ,Image      # insersion de imagenes
import datetime as dt               # fecha para que la carpeta de datos tenga un nombre bonito
import tkinter.font as font         # mas fuentes
import struct as st
from pathlib import Path
from time import time
from Logica import *                # importo todos los metodos implementados en la logica
# parametros iniciales de matplotlib

matplotlib.use("TkAgg")


class Interfaz:
    ''' Clase que modela toda la interfaz del app, por comodidad y orden se define asi y se llama en la llave main al final del script
    '''

    def __init__(self, ventanta):
        # algunas variables que se usaran a lo largo de la aplicacion
        self.ventana = ventanta
        self.ventana.title('Potencial de accion de la neurona')
        self.fuente_ppal = font.Font(family='math')
        self.fuente_sec = ('math', 15, 'bold italic')
        self.directorioActual = Path(__file__).parent
        # Colores
        self.color_1 = '#2b2c2f'
        self.color_2 = '#615d62'
        self.color_3 = '#414044'
        self.color_4 = '#8e858b'
        self.color_blanco = '#fff'
        self.color_negro = '#000'
        self.color_efor = 'red'
        self.color_eback = '#fbb901'
        self.color_emod = 'darkgreen'
        self.color_rk2 = 'blue'
        self.color_rk4 = 'purple'
        self.color_scipy = 'black'
        # =================== Lista de ejecuciones de cada algoritmo para guardar ==========================
        # guardo tuplas de los listados de x y y de la ejecucion de cada algoritmo mientras no se limpie la grafica
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []
        

        # ================================================= toolbar =================================================
        self.frameHerramientas = Frame(self.ventana, bd=5 , bg=self.color_1)
        # genero los objetos imagen para la toolbox
        abrir_img = Image.open(self.directorioActual.joinpath('Open.png').absolute())
        guardar_img = Image.open(self.directorioActual.joinpath('Save.png').absolute())
        cerrar_img = Image.open(self.directorioActual.joinpath('Close.png').absolute())
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
        # posiciono los botones y el frame de herramientas
        self.abrir_btn.pack(side=LEFT, padx =2,pady=2)
        self.guardar_btn.pack(side=LEFT, padx =2,pady=2)
        self.cerrar_btn.pack(side=RIGHT, padx =2,pady=2)
        self.frameHerramientas.pack(side=TOP,fill=X)

        # =================================================  frame de contenido y subframes =================================================

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
        # ================================ Grafica ===========================================
        plt.style.use('bmh')
        self.fig = plt.Figure(figsize=(5.75, 4.0)) # figura principal
        self.plot = self.fig.add_subplot(1,1,1) # plto principal donde se dibujara todos los datos
        grafFont = FontProperties()
        grafFont.set_family('serif')   # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [mS]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$V_m\ [mV]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
            
        self.plot.set_title('Potencial de acción de una neurona', fontsize='x-large', fontproperties=grafFont) # Titulo Principal
        self.fig.tight_layout()
        self.imagenGrafica = FigureCanvasTkAgg(self.fig, master=self.frameGrafica)  # canvas que dibujara la grafica en la interfaz
        self.imagenGrafica.get_tk_widget().place(x=0,y=0)                           # le asigno su posicion
        self.herramientasGrafica = NavigationToolbar2Tk(self.imagenGrafica, self.frameGrafica, pack_toolbar=False) # creo la barra de herramientas que manipularan la grafica
        self.herramientasGrafica.update()                                                                           # lo añada a la interfaz
        self.herramientasGrafica.place(x=0, y=400)                                                                  # le pongo su lugar

        # boton que se encargara de limpiar las ejecuciones de algoritmos en la grafica
        self.limpiar_btn = Button(master=self.frameGrafica, text="limpiar",  command = self.limpiarGrafica, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.limpiar_btn.place(x=350,y=410)
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
        self.intensidad1 = StringVar()
        self.intensidad2 = StringVar()
        # ================================ Valores Defecto ==================================
        self.opcion.set(1)
        self.Vm_0.set('-65.0')
        self.n0.set('0.30')
        self.m0.set('0.05')
        self.h0.set('0.60')
        self.T.set('10.0')
        self.tiempo1.set('50.0')
        self.tiempo2.set('100.0')
        self.tiempo3.set('150.0')
        self.tiempo4.set('200.0')
        self.intensidad1.set('20.0')
        self.intensidad2.set('-15.0')

        # ================================ Contenido ==================================

        # -----------------------------contenido de corriente--------------------------

        # radio button de corriente constate el cual llama a la funcion que habilita las entradas de datos
        self.corriente_cte = Radiobutton(master=self.frameCorriente, command = self.estadoEntradaCorriente ,text='Corriente constante', value=1,  variable=self.opcion, bg=self.color_2,font=self.fuente_sec)
        self.corriente_cte.place(x=0,y=30)

        
        # radio button de corriente variable el cual llama a la funcion que habilita las entradas de datos adicionales
        self.corriente_var = Radiobutton(master=self.frameCorriente, command = self.estadoEntradaCorriente, text='Corriente variable', value=2,  variable=self.opcion, bg=self.color_2,font=self.fuente_sec)
        self.corriente_var.place(x=0,y=70)

        
        
        # titulo de los parametros de tiempo 
        self.titulo_tiempo =  Label(self.frameCorriente,width=10, text='Tiempo', font=('math', 12, 'bold italic'),fg = self.color_blanco, bg =self.color_2) 
        self.titulo_tiempo.place(x=280,y=10)

        # entradas de tiempo para corriente constante, el separador entre entradas y sus respectivas unidades

        self.tiempo1_in = Entry(master=self.frameCorriente, textvariable=self.tiempo1, width=5, font=self.fuente_sec)
        self.tiempo1_in.place(x=250,y=50)

        self.sep1 =  Label(self.frameCorriente,width=2, text='-', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.sep1.place(x=315,y=50)

        self.tiempo2_in = Entry(master=self.frameCorriente, textvariable=self.tiempo2, width=5, font=self.fuente_sec)
        self.tiempo2_in.place(x=350,y=50)

        self.ms_decor1 =  Label(self.frameCorriente,width=2, text='mS', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ms_decor1.place(x=415,y=50)

        # entradas de tiempo adicionales para corriente variable,  el separador entre entradas y sus respectivas unidades


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

        # intensidad corriente para corriente constante, con borde amarillo y su respectiva etiqueta de unidades
        self.intensidad1_in = Entry(master=self.frameCorriente, textvariable=self.intensidad1, width=5, font=self.fuente_sec, highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intensidad1_in.place(x=470,y=50)

        self.ma_decor1 =  Label(self.frameCorriente,width=2, text='mA', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ma_decor1.place(x=540,y=50)

        # intensidad corriente para corriente variable, con borde amarillo y su respectiva etiqueta de unidades
        self.intensidad2_in = Entry(master=self.frameCorriente, textvariable=self.intensidad2, width=5, font=self.fuente_sec, highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intensidad2_in.place(x=470,y=90)


        self.ma_decor1 =  Label(self.frameCorriente,width=2, text='mA', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ma_decor1.place(x=540,y=90)

        # desactivo las entradas de intesidad variable hasta que se seleccione dicha opcion y le cambio el bg para que se vea cool

        self.tiempo3_in.configure(state="disabled", disabledbackground=self.color_3)
        self.tiempo4_in.configure(state="disabled", disabledbackground=self.color_3)
        self.intensidad2_in.configure(state="disabled", disabledbackground=self.color_3)
        


        # ----------------------------------------------contenido de metodos de solucion ------------------------------------
        # titulo del apartado de metodos de solcion
        self.metodos_lbl =  Label(self.frameMetodos, text='Métodos de solución', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)

        self.metodos_lbl.place(x=35,y=10)

        # boton para el metodo euler for y su respectivo color
        self.metodos_decor1 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_efor) 
        self.metodos_decor1.place(x=20,y=61)

        self.eulerfw_btn = Button(master=self.frameMetodos, text="Euler Adelante",  command = self.llamadoEulerFor, bg=self.color_3, fg = self.color_blanco,  width=20,height=1, font=self.fuente_ppal,border="0")
        self.eulerfw_btn.place(x=45,y=60)

        # boton para el metodo euler back y su respectivo color

        self.metodos_decor2 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_eback) 
        self.metodos_decor2.place(x=20,y=101)

        self.eulerbk_btn = Button(master=self.frameMetodos, text="Euler Atrás",  command = self.llamadoEulerBack, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulerbk_btn.place(x=45,y=100)

        # boton para el metodo euler modificado y su respectivo color
        self.metodos_decor3 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_emod) 
        self.metodos_decor3.place(x=20,y=141)

        self.eulermod_btn = Button(master=self.frameMetodos, text="Euler Mod",  command = self.llamadoEulerMod, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulermod_btn.place(x=45,y=140)

        # boton para el metodo rk2 y su respectivo color
        self.metodos_decor4 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_rk2) 
        self.metodos_decor4.place(x=20,y=181)

        self.rk2_btn = Button(master=self.frameMetodos, text="Runge-Kutta 2",  command = self.llamadoRK2, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk2_btn.place(x=45,y=180)

        # boton para el metodo rk4 y su respectivo color
        self.metodos_decor5 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_rk4) 
        self.metodos_decor5.place(x=20,y=221)

        self.rk4_btn = Button(master=self.frameMetodos, text="Runge-Kutta 4",  command = self.llamadoRK4, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk4_btn.place(x=45,y=220)

        # boton para el metodo scipy y su respectivo color
        self.metodos_decor6 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_scipy) 
        self.metodos_decor6.place(x=20,y=261)

        self.scipy_btn = Button(master=self.frameMetodos, text="Scipy",  command = self.llamadoScipy, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.scipy_btn.place(x=45,y=260)

        # ------------------------------------------------- contenido de parametros -----------------------------------------------
        # titulo del apartadode parametros
        self.metodos_lbl =  Label(self.frameParametros, text='Parámetros', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)

        self.metodos_lbl.place(x=75,y=10)
        # Parámetros
        # etiqueta para el parametro Vm_0 y su respectiva entrada para cambiar el parametro

        self.Vm0_lbl =  Label(self.frameParametros,width=5, text='V'+u"\u2098\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.Vm0_lbl.place(x=30,y=60)

        self.Vm0_in = Entry(master=self.frameParametros, textvariable=self.Vm_0, width=8, font=self.fuente_sec)
        self.Vm0_in.place(x=120,y=60)

        self.Vm0_lbl_units =  Label(self.frameParametros,width=3, text='mV', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2)
        self.Vm0_lbl_units.place(x=220,y=60)
        
        # etiqueta para el parametro n_0 y su respectiva entrada para cambiar el parametro

        self.n0_lbl =  Label(self.frameParametros,width=5, text='n'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.n0_lbl.place(x=30,y=100)

        self.n0_in = Entry(master=self.frameParametros, textvariable=self.n0, width=8, font=self.fuente_sec)
        self.n0_in.place(x=120,y=100)

        # etiqueta para el parametro m_0 y su respectiva entrada para cambiar el parametro
        self.m0_lbl =  Label(self.frameParametros,width=5, text='m'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.m0_lbl.place(x=30,y=140)

        self.m0_in = Entry(master=self.frameParametros, textvariable=self.m0, width=8, font=self.fuente_sec)
        self.m0_in.place(x=120,y=140)


        # etiqueta para el parametro h_0 y su respectiva entrada para cambiar el parametro
        self.h0_lbl =  Label(self.frameParametros,width=5, text='h'+u"\u2080"+":", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.h0_lbl.place(x=30,y=180)

        self.h0_in = Entry(master=self.frameParametros, textvariable=self.h0, width=8, font=self.fuente_sec)
        self.h0_in.place(x=120,y=180)


        # etiqueta para el parametro Temperatura y su respectiva entrada para cambiar el parametro
        self.T_lbl =  Label(self.frameParametros,width=5, text='T:', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1) 
        self.T_lbl.place(x=30,y=220)

        self.T_in = Entry(master=self.frameParametros, textvariable=self.T, width=8, font=self.fuente_sec)
        self.T_in.place(x=120,y=220)

        self.T_lbl_units =  Label(self.frameParametros,width=3, text=u"\N{DEGREE SIGN}C", font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2)
        self.T_lbl_units.place(x=220,y=220)
    
    def limpiarGrafica(self):
        ''' Funcion que limpia las grafica y las listas donde se guardan los datos para los metodos de persistencia
        '''
        self.plot.cla() # lipio toda la grafica, esto elimina incluso los titulos por lo que debo volver a ponerlos despues de esto
        grafFont = FontProperties()
        grafFont.set_family('serif')                                                           # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [mS]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$V_m\ [mV]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
        self.plot.set_title('Potencial de acción de una neurona', fontsize='x-large', fontproperties=grafFont) # titulo principal
        self.imagenGrafica.draw()                                                              # Una vez agregado todo dibujo la grafica en la interfaz
        # vuelvo a poner el valor vacio en las listas que guardan los datos para los metodos de persistencia
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []

    def actualizarParametros(self):
        ''' Metodo que sera llamado cada vez que se desee ejecutar un algoritmo, esto con el fin de siempre tener los parametros actualizados
        '''
        # obtengo los valores de cada entrada de las varibales en la interfaz
        pVm0 = float(self.Vm_0.get())
        pN0 = float(self.n0.get())
        pM0 = float(self.m0.get())
        pH0 = float(self.h0.get())
        pT = float(self.T.get())
        pOpcion = int(self.opcion.get())
        pTiempo1=float(self.tiempo1.get())
        pTiempo2=float(self.tiempo2.get())
        pTiempo3=0
        pTiempo4=0
        pIntensidad1=float(self.intensidad1.get())
        pIntensidad2=0
        # si la opcion es corriente variable entonces obtengo los valores adicionales si no estos permanecen como 0
        if pOpcion == 2:
            pTiempo3=float(self.tiempo3.get())
            pTiempo4=float(self.tiempo4.get())
            pIntensidad2=float(self.intensidad2.get())
        # devuelvo los parametros ordenados
        return (pVm0,pN0,pM0,pH0,pT,pOpcion,pTiempo1,pTiempo2,pTiempo3,pTiempo4,pIntensidad1,pIntensidad2)


    def llamadoEulerFor(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler forward con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_eFor,V_eFor = EulerFor(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.eForSet.append((t_eFor,V_eFor))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_eFor, V_eFor,color=self.color_efor)
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagenGrafica.draw()


    def llamadoEulerBack(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler back con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_eBack,V_eBack = EulerBack(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.eBackSet.append((t_eBack,V_eBack))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_eBack,V_eBack,color=self.color_eback)
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagenGrafica.draw()


    def llamadoEulerMod(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler modificado con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_eMod,V_eMod = EulerMod(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.eModSet.append((t_eMod,V_eMod))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_eMod, V_eMod, color=self.color_emod)
        self.imagenGrafica.draw()


    def llamadoRK2(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo runge-kutta 2 con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_RK2,V_RK2 = RK2(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.RK2Set.append((t_RK2,V_RK2))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_RK2, V_RK2, color=self.color_rk2)
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagenGrafica.draw()
    

    def llamadoRK4(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo runge-kutta 4 con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_RK4,V_RK4 = RK4(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.RK4Set.append((t_RK4,V_RK4))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_RK4, V_RK4, color=self.color_rk4)
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagenGrafica.draw()
    
    def llamadoScipy(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo implementado con scipy con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametros = self.actualizarParametros()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        t_SCIPY,V_SCIPY = SCIPY(*parametros)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        self.scipySet.append((t_SCIPY,V_SCIPY))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        self.plot.plot(t_SCIPY, V_SCIPY, color=self.color_scipy)
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagenGrafica.draw()


    def estadoEntradaCorriente(self):
        ''' Funcion que activa las entradas correspondientes a la opcion de corriente indicacda en la variable opcion, 1 para corriente constante y 2 para corriente variable
        '''
        opt = self.opcion.get() # obtengo el valor de la opcion actual en la interfaz
        # si la opcion es 1 entonces desabilito las entradas adicionales
        if opt == 1:
            self.tiempo3_in.configure(state="disabled")
            self.tiempo4_in.configure(state="disabled")
            self.intensidad2_in.configure(state="disabled")
        # si la opcion es 2 entonces activo las entradas adicionales
        elif opt == 2:
            self.tiempo3_in.configure(state="normal")
            self.tiempo4_in.configure(state="normal")
            self.intensidad2_in.configure(state="normal")


    def cerrarAplicacion(self):
        ''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
        '''
        # creo la caja de mensaje y su valor
        MsgBox =  messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        # si el valor es yes entonces cierro la apliacion
        if MsgBox == 'yes':
            self.ventana.destroy()     
            self.ventana.quit()
        # en caso contrario se notifica el retorono a la aplicacion
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')
    
    def auxGuardar(self, directorio, extencion, listaDatos):
        ''' Metodo auxiliar que ayudara al guardado de archivos, es definido para evitar redundacia en codigo
        '''
         
        # genero un proceso iterativo para leer todas las lineas graficadas en el listado de datos el cual tiene en cada posicion un conjunto (X,Y)
        for i,val in enumerate(listaDatos):
            # obtengo el listado de datos de X 
            x_data = val[0]
            # obtengo el listado de datos deY
            y_data = val[1]
            # las empaqueto en formatodouble
            x_packed = st.pack('d'*len(x_data),*x_data)
            y_packed = st.pack('d'*len(y_data),*y_data)
            # creo el archivo con el nombre i.extencion para hacer la lectura despues de forma facil ejemplo 0.efor
            with open(directorio.joinpath(str(i)+extencion).absolute(),'wb') as f:
                # escribo los datos de X en el archivo
                f.write(x_packed)
                # escribo los datos de Y en el archivo
                f.write(y_packed)
                # Nota: el orden es importante ya que en la lectura se obtendra un set completo por lo que la primera mitad sera X y la segunda mitad sera Y

    def guardarDatos(self):
        ''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
        '''
        ahora = time() # obtengo el timestamp actual
        fecha = dt.datetime.utcfromtimestamp(ahora).strftime("%Y-%m-%d_%H-%M-%S") # genero la fecha actual con el time stamp obtenido previamente
        nombreCarpetaDatos = 'Datos_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha
        # pido el directorio donde se creara la carpeta en la que se guardaran los datos
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de guardado de datos") 
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if directorioNombre == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorioDatos = Path(directorioNombre)
        # se crea el path a la carpeta nueva con el nombre previamente generaro y se manda el comando al sistema para que la cree como carpeta
        carpetaDatos = directorioDatos.joinpath(str(nombreCarpetaDatos))
        carpetaDatos.mkdir(parents=True, exist_ok=True)
        # llamo a la funcion auxiliar con el la carpeta donde se guardaran los datos, la extencion con la que se guardaran y el listado del que leera los datos a guardar
        self.auxGuardar(carpetaDatos,'.efor',self.eForSet)
        self.auxGuardar(carpetaDatos,'.eback',self.eBackSet)
        self.auxGuardar(carpetaDatos,'.emod',self.eModSet)
        self.auxGuardar(carpetaDatos,'.rk2',self.RK2Set)
        self.auxGuardar(carpetaDatos,'.rk4',self.RK4Set)
        self.auxGuardar(carpetaDatos,'.scipy',self.scipySet)
        
    def auxCargar(self, directorio, extencion, color_grafica):
        ''' Metodo auxiliar que ayudara a la carga de archivos, es definido para evitar redundacia en codigo
        retorna una lista con los valores leidos de X y Y de los archivos que encuentre en el path especificado con la extencion especificada
        '''
        # obtengo el nombre de todos los arvhicos con la extencion deseada
        ext = '*'+extencion
        files = [f.absolute() for f in directorio.glob(ext) if f.is_file()]
        tmpSet = [] # variable donde se guardaran los conjuntos
        # proceso iterativo que lee cada archivo
        for tmpF in files:
            with open(tmpF,'rb') as f:
                # leo el contenido del archivo
                data = f.read()
                # desempaqueto el contenido del arvhivo y lo convierto en lista para manipularlo
                unpacked = list(st.unpack('d'*(len(data)//8),data))
                # obtengo la mitad del tamaño para poder partir el array
                tam = len(unpacked)//2
                # genero los valores de X con la mitad de los datos y lo vuelvo un array de numpy
                t = np.array(unpacked[:tam])
                # genero los valores de Y con la segunda mitad de los datos y lo vuelvo un array de numpy
                V = np.array(unpacked[tam:])
                # grafico la linea con el color que debe ir
                self.plot.plot(t,V,color=color_grafica)
                # guardo los valore de X y Y en la lista temporal que se retornara al final de este metodo
                tmpSet.append((t,V))
        # retorno la lista resultante de la lectura de los archivos con la extencion
        return tmpSet


    def cargarDatos(self):
        ''' Funcion que abre un dialogo para seleccionar un archivo del cual se cargaran los datos de una ejecucion previa en formato double
        '''
        # pido el directorio donde se encuentran los datos previamente generados
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de datos generados")
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if directorioNombre == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorioDatos = Path(directorioNombre)
        # se llama a la funcion auxiliar que lee los archivos con la extencion y añade los datos a la grafica
        tmpSetEfor = self.auxCargar(directorioDatos,'.efor', self.color_efor)
        tmpSetEback = self.auxCargar(directorioDatos,'.eback', self.color_eback)
        tmpSetEmod = self.auxCargar(directorioDatos,'.emod', self.color_emod)
        tmpSetRK2 = self.auxCargar(directorioDatos,'.rk2', self.color_rk2)
        tmpSetRK4 = self.auxCargar(directorioDatos,'.rk4',self.color_rk4)
        tmpSetScipy = self.auxCargar(directorioDatos,'.scipy', self.color_scipy)
        # agrego los datos cargados a los existentes en las listas que almacenan estos para la persistencia
        self.eForSet+=tmpSetEfor
        self.eBackSet+=tmpSetEback
        self.eModSet+=tmpSetEmod
        self.RK2Set+=tmpSetRK2
        self.RK4Set+=tmpSetRK4
        self.scipySet+=tmpSetScipy
        # despues de todo lo anterior actualizo el grafico en la interfaz con el metodo draw definido para un canvas
        self.imagenGrafica.draw()


    def iniciar(self):
        ''' Metodo que inicia la interfaz con el main loop, este metodo se define por tener orden en toda la clase y no hacer accesos externos al parametro de ventana
        '''
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
