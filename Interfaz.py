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
        

        # -------- toolbar ------------
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
        # ================================ Grafica ===========================================
        plt.style.use('bmh')
        self.fig = plt.Figure(figsize=(5.75, 4.0))
        self.plot = self.fig.add_subplot(1,1,1)
        grafFont = FontProperties()
        grafFont.set_family('serif')   # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [mS]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$V_m\ [mV]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
            
        self.plot.set_title('Potencial de acción de una neurona', fontsize='x-large', fontproperties=grafFont)
        self.fig.tight_layout()
        self.imagenGrafica = FigureCanvasTkAgg(self.fig, master=self.frameGrafica)
        self.imagenGrafica.get_tk_widget().place(x=0,y=0)
        self.herramientasGrafica = NavigationToolbar2Tk(self.imagenGrafica, self.frameGrafica, pack_toolbar=False)
        self.herramientasGrafica.update()
        self.herramientasGrafica.place(x=0, y=400)

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

        self.tiempo3_in.configure(state="disabled", disabledbackground=self.color_3)
        self.tiempo4_in.configure(state="disabled", disabledbackground=self.color_3)
        self.intensidad2_in.configure(state="disabled", disabledbackground=self.color_3)
        


        # contenido de metodos de solucion, los nombres de las variables son lo suficientemente dicientes para saber que es cada cosa.
        self.metodos_lbl =  Label(self.frameMetodos, text='Métodos de solución', font=self.fuente_sec,fg = self.color_negro, bg =self.color_2)

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
    
    def limpiarGrafica(self):
        self.plot.cla()
        grafFont = FontProperties()
        grafFont.set_family('serif')   # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [mS]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$V_m\ [mV]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
            
        self.plot.set_title('Potencial de acción de una neurona', fontsize='x-large', fontproperties=grafFont)
        self.imagenGrafica.draw()
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []

    def actualizarParametros(self):
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
        if pOpcion == 2:
            pTiempo3=float(self.tiempo3.get())
            pTiempo4=float(self.tiempo4.get())
            pIntensidad2=float(self.intensidad2.get())
        return (pVm0,pN0,pM0,pH0,pT,pOpcion,pTiempo1,pTiempo2,pTiempo3,pTiempo4,pIntensidad1,pIntensidad2)


    def llamadoEulerFor(self):
        parametros = self.actualizarParametros()
        t_eFor,V_eFor = EulerFor(*parametros)
        self.eForSet.append((t_eFor,V_eFor))
        self.plot.plot(t_eFor, V_eFor,color=self.color_efor)
        self.imagenGrafica.draw()


    def llamadoEulerBack(self):
        parametros = self.actualizarParametros()
        t_eBack,V_eBack = EulerBack(*parametros)
        self.eBackSet.append((t_eBack,V_eBack))
        self.plot.plot(t_eBack,V_eBack,color=self.color_eback)
        self.imagenGrafica.draw()


    def llamadoEulerMod(self):
        parametros = self.actualizarParametros()
        t_eMod,V_eMod = EulerMod(*parametros)
        self.eModSet.append((t_eMod,V_eMod))
        self.plot.plot(t_eMod, V_eMod, color=self.color_emod)
        self.imagenGrafica.draw()


    def llamadoRK2(self):
        parametros = self.actualizarParametros()
        t_RK2,V_RK2 = RK2(*parametros)
        self.RK2Set.append((t_RK2,V_RK2))
        self.plot.plot(t_RK2, V_RK2, color=self.color_rk2)
        self.imagenGrafica.draw()
    

    def llamadoRK4(self):
        parametros = self.actualizarParametros()
        t_RK4,V_RK4 = RK4(*parametros)
        self.RK4Set.append((t_RK4,V_RK4))
        self.plot.plot(t_RK4, V_RK4, color=self.color_rk4)
        self.imagenGrafica.draw()
    
    def llamadoScipy(self):
        parametros = self.actualizarParametros()
        t_SCIPY,V_SCIPY = SCIPY(*parametros)
        self.scipySet.append((t_SCIPY,V_SCIPY))
        self.plot.plot(t_SCIPY, V_SCIPY, color=self.color_scipy)
        self.imagenGrafica.draw()


    def estadoEntradaCorriente(self):
        ''' Funcion que activa las entradas correspondientes a la opcion de corriente indicacda en la variable opcion, 1 para corriente constante y 2 para corriente variable
        '''
        opt = self.opcion.get()
        if opt == 1:
            self.tiempo3_in.configure(state="disabled")
            self.tiempo4_in.configure(state="disabled")
            self.intensidad2_in.configure(state="disabled")
        elif opt == 2:
            self.tiempo3_in.configure(state="normal")
            self.tiempo4_in.configure(state="normal")
            self.intensidad2_in.configure(state="normal")


    def cerrarAplicacion(self):
        ''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
        '''
        MsgBox =  messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        if MsgBox == 'yes':
            self.ventana.destroy()     
            self.ventana.quit()
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')
    

    def guardarDatos(self):
        ''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
        '''
        ahora = time()
        fecha = dt.datetime.utcfromtimestamp(ahora).strftime("%Y-%m-%d_%H-%M-%S")
        nombreCarpetaDatos = 'Datos_' + fecha
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de guardado de datos")
        if directorioNombre == '':
            return
        directorioDatos = Path(directorioNombre)
        carpetaDatos = directorioDatos.joinpath(str(nombreCarpetaDatos))
        try:

            carpetaDatos.mkdir(parents=True, exist_ok=True)

            for i,val in enumerate(self.eForSet):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.efor').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)

            for i,val in enumerate(self.eBackSet):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.eback').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)

            for i,val in enumerate(self.eModSet):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.emod').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)

            for i,val in enumerate(self.RK2Set):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.rk2').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)

            for i,val in enumerate(self.RK4Set):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.rk4').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)

            for i,val in enumerate(self.scipySet):
                x_data = val[0]
                y_data = val[1]
                x_packed = st.pack('d'*len(x_data),*x_data)
                y_packed = st.pack('d'*len(y_data),*y_data)
                with open(carpetaDatos.joinpath(str(i)+'.scipy').absolute(),'wb') as f_efor:
                    f_efor.write(x_packed)
                    f_efor.write(y_packed)
            
        except:
            pass
        

    def cargarDatos(self):
        ''' Funcion que abre un dialogo para seleccionar un archivo del cual se cargaran los datos de una ejecucion previa en formato double
        '''
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de datos generados")
        if directorioNombre == '':
            return
        directorioDatos = Path(directorioNombre)
        try:
            filesEfor = [f.absolute() for f in directorioDatos.glob('*.efor') if f.is_file()]
            filesEback = [f.absolute() for f in directorioDatos.glob('*.eback') if f.is_file()]
            filesEmod = [f.absolute() for f in directorioDatos.glob('*.emod') if f.is_file()]
            filesRK2 = [f.absolute() for f in directorioDatos.glob('*.rk2') if f.is_file()]
            filesRK4 = [f.absolute() for f in directorioDatos.glob('*.rk4') if f.is_file()]
            filesScipy = [f.absolute() for f in directorioDatos.glob('*.scipy') if f.is_file()]
            
            tmpSetEfor = []
            tmpSetEback = []
            tmpSetEmod = []
            tmpSetRK2 = []
            tmpSetRK4 = []
            tmpSetScipy = []

            for fileEfor in filesEfor:
                with open(fileEfor,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_eFor = np.array(unpacked[:tam])
                    V_eFor = np.array(unpacked[tam:])
                    self.plot.plot(t_eFor,V_eFor,color=self.color_efor)
                    tmpSetEfor.append((t_eFor,V_eFor))
            
            
            for fileEback in filesEback:
                with open(fileEback,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_eBack = np.array(unpacked[:tam])
                    V_eBack = np.array(unpacked[tam:])
                    self.plot.plot(t_eBack,V_eBack, color=self.color_eback)
                    tmpSetEback.append((t_eBack,V_eBack))
            
            for fileEmod in filesEmod:
                with open(fileEmod,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_eMod = np.array(unpacked[:tam])
                    V_eMod = np.array(unpacked[tam:])
                    self.plot.plot(t_eMod,V_eMod, color=self.color_emod)
                    tmpSetEmod.append((t_eMod,V_eMod))
            
            for fileRK2 in filesRK2:
                with open(fileRK2,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_RK2 = np.array(unpacked[:tam])
                    V_RK2 = np.array(unpacked[tam:])
                    self.plot.plot(t_RK2,V_RK2,color=self.color_rk2)
                    tmpSetRK2.append((t_RK2,V_RK2))
            
            for fileRK4 in filesRK4:
                with open(fileRK4,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_RK4 = np.array(unpacked[:tam])
                    V_RK4 = np.array(unpacked[tam:])
                    self.plot.plot(t_RK4,V_RK4, color=self.color_rk4)
                    tmpSetRK4.append((t_RK4,V_RK4))
            
            for fileScipy in filesScipy:
                with open(fileScipy,'rb') as f:
                    data = f.read()
                    unpacked = list(st.unpack('d'*(len(data)//8),data))
                    tam = len(unpacked)//2
                    t_SCIPY = np.array(unpacked[:tam])
                    V_SCIPY = np.array(unpacked[tam:])
                    self.plot.plot(t_SCIPY,V_SCIPY, color=self.color_scipy)
                    tmpSetScipy.append((t_SCIPY,V_SCIPY))
            
            self.eForSet+=tmpSetEfor
            self.eBackSet+=tmpSetEback
            self.eModSet+=tmpSetEmod
            self.RK2Set+=tmpSetRK2
            self.RK4Set+=tmpSetRK4
            self.scipySet+=tmpSetScipy
            self.imagenGrafica.draw()

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
