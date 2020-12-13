##
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.integrate as inte
from scipy.integrate import odeint
from matplotlib import rcParams     # Esto es para modificar el estilo de fuente de los gráficos.


'''=====================================================================================================================
                                        CONDICIONES DEL MODELO MATEMÁTICO
====================================================================================================================='''

# Máximo valor de la conductancia del Na+ por unidad de área
g_Na = 120.0    # [mS/cm^2]

# Máximo valor de la conductancia del K+ por unidad de área
g_K = 36.0      # [mS/cm^2]

# Máximo valor de la conductancia del canal de fuga (L) por unidad de área
g_L = 0.3       # [mS/cm^2]


# Potencial de equilibrio de Nernst de Na+
E_Na = 50.0     # [mV]

# Potencial de equilibrio de Nernst de K+
E_K = -77.0     # [mV]

# Potencial de equilibrio de Nernst del canal de fuga.
E_L = -54.4     # [mV]


# Capacitancia de la membrana por unidad de área
C_M = 1.0       # [µF/cm^2]



# ===============================            CONSTANTES DEL I-ÉSIMO CANAL IÓNICO         ===============================

# β_m(Vm)
def beta_m(Vm):
    return 4.0 * np.exp(-(Vm + 65.0) / 18.0)

# α_h(Vm)
def alpha_h(Vm):
    return 0.07 * np.exp(-(Vm + 65.0) / 20.0)

# β_h(Vm)
def beta_h(Vm):
    return 1.0 / (1.0 + np.exp(-(Vm + 35.0) / 10.0))

# α_n(Vm)
def alpha_n(Vm):
    return (0.01 * (Vm + 55.0)) / (1.0 - np.exp(-(Vm + 55.0) / 10.0))

# β_n(Vm)
def beta_n(Vm):
    return 0.125 * np.exp(-(Vm + 65.0) / 80.0)

# α_m(Vm)
def alpha_m(Vm):
    return (0.1 * (Vm + 40.0)) / (1.0 - np.exp(-(Vm + 40.0) / 10.0))



# ====================================            FACTOR DE TEMPERATURA (Φ)         ====================================

def phi(T):
    '''
    :param T: [°C] Temperatura
    :return: Factor que cuantifica la rapidez de cambios en los canales iónicos debido a la temperatura (T).
    '''
    Q_10 = 3        # Radio de las tasas por un incremento de temperatura de 10 °C
    T_base = 6.3    # Temperatura base [°C]
    return (Q_10) ** ((T - T_base) / 10.0)


#==================================            TIEMPO & CORRIENTE (t & I(t))         ===================================

def tiempo_y_corriente(opcion, t1, t2, t3, t4, I1, I2, resol):
    '''
    :param opcion: * 1: Si la corriente es fija. * 2: Si la corriente es variable.
    :param t1: [mS] Valor inicial del intervalo de tiempo 1.
    :param t2: [mS] Valor final del intervalo de tiempo 1.
    :param t3: [mS] Valor inicialdel intervalo de tiempo 2.
    :param t4: [mS] Valor final del intervalo de tiempo 2.
    :param I1: [mV] Intensidad de corriente del intervalo de tiempo 1.
    :param I2: [mV] Intensidad de corriente del intervalo de tiempo 2.
    :param resol: [mS] Resolución o Step de tiempo para crear el rango.
    :return: Tupla (t,I) -> t: Intervalo de tiempo de simulación. I: Intensidad de corriente durante el tiempo t.
    '''

    # PARTE I - Se crea el arreglo de tiempo

    # Tiempo inicial (T0) y final (Tf) de simulación (graficado)
    t_0 = 0.0  # [mS]
    t_f = (t4 if opcion == 2 else t2) + 50.0  # [mS]

    # Se crea el arreglo de tiempo que va desde To a Tf con pasos de resol
    t = np.arange(t_0, t_f + resol, resol)

    # PARTE II - Corriente (I(t))
    I = np.zeros(len(t))      # Se crea el arreglo que almacena la corriente respecto al tiempo.

    # Intervalo 1
    IInd = np.where((t >= t1) & (t <= t2))      # np.where retorna los t que están en el intervalo 1.
    I[IInd] = I1                                # Para los t hallados por np.where en el arreglo se asigna-

    # Intervalo 2 - Aplica cuando la corriente es variable.
    if opcion==2:
        IInd = np.where((t >= t3) & (t <= t4))
        I[IInd] = I2

    return t, I



#=======================================    ARREGLOS QUE ALMACENAN SOLUCIONES   ========================================
def creacionArreglos(V_m0,n_0,m_0,h_0,t):

    '''
    :param V_m0: Potencial de membrana inicial
    :param n_0: Probabilidad inicial de n
    :param m_0: Probabilidad inicial de m
    :param h_0: Probabilidad inicial de h
    :param t: Arreglo de tiempo de la simulación (tiempo graficado).
    :return: Tupla ( V_m(t), n(t), m(t), h(t) ) -> Arreglos para almacenar potencial de membrana (V_m)
    & prob. de n, m y h respecto al tiempo t. Estos arreglos se inicializan respectivamente con V_m0, n_0, m_0 y h_0
    '''

    # Se crean los arreglos
    Vm_array = np.zeros(len(t))
    n_array = np.zeros(len(t))
    m_array = np.zeros(len(t))
    h_array = np.zeros(len(t))

    # Se inicializan los arreglos.
    Vm_array[0] = V_m0
    n_array[0] = n_0
    m_array[0] = m_0
    h_array[0] = h_0

    return Vm_array, n_array, m_array, h_array



'''=====================================================================================================================
                                                ECUACIONES DIFERENCIALES
====================================================================================================================='''

# PARTE I - ECUACIONES AUXILIARES

# Corriente de Na+  [Ec (2)]
def I_Na(Vm, m, h): return g_Na * (m ** 3) * h * (Vm - E_Na)

# Corriente de K+   [Ec (1)]
def I_K(Vm, n): return g_K * (n ** 4) * (Vm - E_K)

# Corriente de fuga L (Cl- y otros iones)   [Ec (3)]
def I_L(Vm):    return g_L * (Vm - E_L)

#-----------------------------------------------------------------------------------------------------------------------

# PARTE II - ECUACIONES DIFERENCIALES

# Ecuación I - Hallada al despejar la ecuación de corriente I(t).    [Ec (5) y (6)]
def dV_dt(I, Vm, n, m, h):
    return (I - I_L(Vm) - I_K(Vm,n) - I_Na(Vm,m,h)) / (C_M)

# Ecuación II
def dn_dt(phi, Vm, n):
    return phi * (alpha_n(Vm) * (1 - n) - beta_n(Vm) * n)

# Ecuación III
def dm_dt(phi, Vm, m):
    return phi * (alpha_m(Vm) * (1 - m) - beta_m(Vm) * m)

# Ecuación IV
def dh_dt(phi,Vm,h):
    return phi * (alpha_h(Vm) * (1 - h) - beta_h(Vm) * h)



'''=====================================================================================================================
                                        SOLUCIÓN DE SISTEMAS DE ECUACIONES
====================================================================================================================='''

#=============================================    FUNCIONES AUXILIARES   ===============================================

# II. EULER HACIA ATRÁS (BACKWARD)
# Permite convertir el problema en un sistema multivariable para poder resolverlo con fsolve.
# y_i = y_(i-1) + h * F(y_i)    →   0 = y_(i-1) + h * F(y_i) - y_i

def FAux_EulerBack(Aux, I, Vm, n, m, h, phi_val, h_res):
    return [Vm + h_res * dV_dt(I, Aux[0], Aux[1], Aux[2], Aux[3]) - Aux[0],
            n + h_res * dn_dt(phi_val, Aux[0], Aux[1]) - Aux[1],
            m + h_res * dm_dt(phi_val, Aux[0], Aux[2]) - Aux[2],
            h + h_res * dh_dt(phi_val, Aux[0], Aux[3]) - Aux[3]]

# III. EULER MODIFICADO (MOD)
# Permite convertir el problema en un sistema multivariable para poder resolverlo con fsolve.
# y_i = y_(i-1) + h/2 * [F(y_(i-1))+F(y_i)]    →   0 = y_(i-1) + h/2 * [F(y_(i-1))+F(y_i)] - y_i

def FAux_EulerMod(Aux, I, Vm, n, m, h, phi_val, h_res):
    return [Vm + (h_res / 2.0) * (dV_dt(I, Vm, n, m, h) + dV_dt(I, Aux[0], Aux[1], Aux[2], Aux[3])) - Aux[0],
            n + (h_res / 2.0)  * (dn_dt(phi_val, Vm, n) + dn_dt(phi_val, Aux[0], Aux[1])) - Aux[1],
            m + (h_res / 2.0)  * (dm_dt(phi_val, Vm, m) + dm_dt(phi_val, Aux[0], Aux[2])) - Aux[2],
            h + (h_res / 2.0)  * (dh_dt(phi_val, Vm, h) + dh_dt(phi_val, Aux[0], Aux[3])) - Aux[3]]



#==============================================    MÉTODOS NUMÉRICOS   =================================================

# I. EULER FORWARD
# Las ecuaciones fueron formuladas siguiendo el formato y_(i) = y_(i-1)+h[F(y_(i-1))]

def EulerFor(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2,h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion,t1,t2,t3,t4,I1,I2,h_res)
    Vm_EulerFor, n_EulerFor, m_EulerFor, h_EulerFor = creacionArreglos(V_m0,n_0,m_0,h_0, t)

    for iter in range(1, len(t)):

        Vm_EulerFor[iter] = Vm_EulerFor[iter - 1] + h_res * dV_dt(I[iter],
                                                                  Vm_EulerFor[iter - 1],
                                                                  n_EulerFor[iter - 1],
                                                                  m_EulerFor[iter - 1],
                                                                  h_EulerFor[iter - 1])
        n_EulerFor[iter] = n_EulerFor[iter - 1] + h_res * dn_dt(phi_val, Vm_EulerFor[iter - 1], n_EulerFor[iter - 1])
        m_EulerFor[iter] = m_EulerFor[iter - 1] + h_res * dm_dt(phi_val, Vm_EulerFor[iter - 1], m_EulerFor[iter - 1])
        h_EulerFor[iter] = h_EulerFor[iter - 1] + h_res * dh_dt(phi_val, Vm_EulerFor[iter - 1], h_EulerFor[iter - 1])

    return t, Vm_EulerFor



# II. EULER BACKWARD

def EulerBack(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2,h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion,t1,t2,t3,t4,I1,I2,h_res)
    Vm_EulerBack, n_EulerBack, m_EulerBack, h_EulerBack = creacionArreglos(V_m0,n_0,m_0,h_0, t)

    for iter in range(1, len(t)):
        BackRoots = opt.fsolve(FAux_EulerBack, np.array([Vm_EulerBack[iter - 1],
                                                         n_EulerBack[iter - 1],
                                                         m_EulerBack[iter - 1],
                                                         h_EulerBack[iter - 1]]),
                               (I[iter], Vm_EulerBack[iter - 1], n_EulerBack[iter - 1], m_EulerBack[iter - 1],
                                h_EulerBack[iter - 1], phi_val, h_res))

        Vm_EulerBack[iter] = BackRoots[0]
        n_EulerBack[iter] = BackRoots[1]
        m_EulerBack[iter] = BackRoots[2]
        h_EulerBack[iter] = BackRoots[3]

    return t, Vm_EulerBack



# III. EULER MOD

def EulerMod(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2,h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion,t1,t2,t3,t4,I1,I2,h_res)
    Vm_EulerMod, n_EulerMod, m_EulerMod, h_EulerMod = creacionArreglos(V_m0,n_0,m_0,h_0, t)

    for iter in range(1, len(t)):
        ModRoots = opt.fsolve(FAux_EulerMod, np.array([Vm_EulerMod[iter - 1],
                                                       n_EulerMod[iter - 1],
                                                       m_EulerMod[iter - 1],
                                                       h_EulerMod[iter - 1]]),
                              (I[iter], Vm_EulerMod[iter - 1], n_EulerMod[iter - 1],
                               m_EulerMod[iter - 1], h_EulerMod[iter - 1], phi_val, h_res))

        Vm_EulerMod[iter] = ModRoots[0]
        n_EulerMod[iter] = ModRoots[1]
        m_EulerMod[iter] = ModRoots[2]
        h_EulerMod[iter] = ModRoots[3]

    return t, Vm_EulerMod



# IV. RUNGE-KUTTA 2 (RK2)

def RK2(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2,h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion,t1,t2,t3,t4,I1,I2,h_res)
    Vm_RK2, n_RK2, m_RK2, h_RK2 = creacionArreglos(V_m0,n_0,m_0,h_0, t)

    for iter in range(1, len(t)):

        #   * kj1 = Fj(yj_(i-1))                    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k11 = dV_dt(I[iter], Vm_RK2[iter - 1], n_RK2[iter - 1], m_RK2[iter - 1], h_RK2[iter - 1])
        k21 = dn_dt(phi_val, Vm_RK2[iter-1], n_RK2[iter-1])
        k31 = dm_dt(phi_val, Vm_RK2[iter-1], m_RK2[iter-1])
        k41 = dh_dt(phi_val, Vm_RK2[iter-1], h_RK2[iter-1])

        #   * kj2 = Fj(yj_(i - 1) + kj1 * h_res)    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k12 = dV_dt(I[iter],
                    Vm_RK2[iter-1] + h_res * k11,
                    n_RK2[iter-1] + h_res * k21,
                    m_RK2[iter-1] + h_res * k31,
                    h_RK2[iter-1] + h_res * k41)
        k22 = dn_dt(phi_val, Vm_RK2[iter-1] + h_res * k11, n_RK2[iter-1] + h_res * k21)
        k32 = dm_dt(phi_val, Vm_RK2[iter-1] + h_res * k11, m_RK2[iter-1] + h_res * k31)
        k42 = dh_dt(phi_val, Vm_RK2[iter-1] + h_res * k11, h_RK2[iter-1] + h_res * k41)

        #   * yj_(i) = yj_(i-1) + (h/2) * (kj1 + kj2)   |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        Vm_RK2[iter] = Vm_RK2[iter - 1] + (h_res / 2.0) * (k11 + k12)
        n_RK2[iter] = n_RK2[iter - 1] + (h_res / 2.0) * (k21 + k22)
        m_RK2[iter] = m_RK2[iter - 1] + (h_res / 2.0) * (k31 + k32)
        h_RK2[iter] = h_RK2[iter - 1] + (h_res / 2.0) * (k41 + k42)

    return t, Vm_RK2


# V. RUNGE-KUTTA 4 (RK4)

def RK4(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2,h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion,t1,t2,t3,t4,I1,I2,h_res)
    Vm_RK4, n_RK4, m_RK4, h_RK4 = creacionArreglos(V_m0,n_0,m_0,h_0, t)

    for iter in range(1, len(t)):

        #   * kj1 = Fj(yj_(i-1))    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k11 = dV_dt(I[iter], Vm_RK4[iter - 1], n_RK4[iter - 1], m_RK4[iter - 1], h_RK4[iter - 1])
        k21 = dn_dt(phi_val, Vm_RK4[iter - 1], n_RK4[iter - 1])
        k31 = dm_dt(phi_val, Vm_RK4[iter - 1], m_RK4[iter - 1])
        k41 = dh_dt(phi_val, Vm_RK4[iter - 1], h_RK4[iter - 1])

        #   * kj2 = Fj(yj_(i - 1) + 0.5 * h_res * kj1 )    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k12 = dV_dt(I[iter],
                    Vm_RK4[iter - 1] + 0.5 * h_res * k11,
                    n_RK4[iter - 1] + 0.5 * h_res * k21,
                    m_RK4[iter - 1] + 0.5 * h_res * k31,
                    h_RK4[iter - 1] + 0.5 * h_res * k41)
        k22 = dn_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k11, n_RK4[iter - 1] + 0.5 * h_res * k21)
        k32 = dm_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k11, m_RK4[iter - 1] + 0.5 * h_res * k31)
        k42 = dh_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k11, h_RK4[iter - 1] + 0.5 * h_res * k41)

        #   * kj3 = Fj(yj_(i - 1) + 0.5 * h_res * kj2 )    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k13 = dV_dt(I[iter],
                    Vm_RK4[iter - 1] + 0.5 * h_res * k12,
                    n_RK4[iter - 1] + 0.5 * h_res * k22,
                    m_RK4[iter - 1] + 0.5 * h_res * k32,
                    h_RK4[iter - 1] + 0.5 * h_res * k42)
        k23 = dn_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k12, n_RK4[iter - 1] + 0.5 * h_res * k22)
        k33 = dm_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k12, m_RK4[iter - 1] + 0.5 * h_res * k32)
        k43 = dh_dt(phi_val, Vm_RK4[iter - 1] + 0.5 * h_res * k12, h_RK4[iter - 1] + 0.5 * h_res * k42)

        #   * kj4 = Fj(yj_(i - 1) +  h_res * kj3 )    |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        k14 = dV_dt(I[iter],
                    Vm_RK4[iter - 1] + h_res * k13,
                    n_RK4[iter - 1] + h_res * k23,
                    m_RK4[iter - 1] + h_res * k33,
                    h_RK4[iter - 1] + h_res * k43)
        k24 = dn_dt(phi_val, Vm_RK4[iter - 1] + h_res * k13, n_RK4[iter - 1] + h_res * k23)
        k34 = dm_dt(phi_val, Vm_RK4[iter - 1] + h_res * k13, m_RK4[iter - 1] + h_res * k33)
        k44 = dh_dt(phi_val, Vm_RK4[iter - 1] + h_res * k13, h_RK4[iter - 1] + h_res * k43)

        #   * yj_(i) = yj_(i-1) + (h/6) * (kj1 + 2*kj2 + 2*kj3 + kj4)   |   ∀ j ∈ { 1: Vm, 2: n, 3: m, 4: h }
        Vm_RK4[iter] = Vm_RK4[iter - 1] + (h_res / 6.0) * (k11 + 2.0 * k12 + 2.0 * k13 + k14)
        n_RK4[iter] = n_RK4[iter - 1] + (h_res / 6.0) * (k21 + 2.0 * k22 + 2.0 * k23 + k24)
        m_RK4[iter] = m_RK4[iter - 1] + (h_res / 6.0) * (k31 + 2.0 * k32 + 2.0 * k33 + k34)
        h_RK4[iter] = h_RK4[iter - 1] + (h_res / 6.0) * (k41 + 2.0 * k42 + 2.0 * k43 + k44)

    return t, Vm_RK4


# VI. Odeint

def SCIPY(V_m0, n_0, m_0, h_0, T, opcion, t1, t2, t3, t4, I1, I2, h_res=0.01):

    phi_val = phi(T)
    t, I = tiempo_y_corriente(opcion, t1, t2, t3, t4, I1, I2, h_res)

    # ECUACIÓN AUXILIAR I
    def Id(t_ev, t_1=t1, t_2=t2, t_3=t3, t_4=t4, I_1=I1, I_2=I2, op = opcion):

        '''
        :param t: [mS] Tiempo para el cual se quiere averiguar la corriente.
        :return: [mV] Corriente en el tiempo t dado por parámetro.
        '''

        if t_ev >= t_1 and t_ev <= t_2: return I_1
        elif (t_ev >= t_3 and t_ev <= t_4) and (op == 2): return I_2
        else: return 0.0

    # ECUACIÓN AUXILIAR II
    def deriv_ev_ini(X,t_ev):

        '''
        :param X: Arreglo con valores iniciales del potencial de membrana inicial (V_m0) y la probabilidad inicial de
        n, m, h (n_0, m_0 y  h_0 respectivamente.)
        :param t_0: Tiempo evaluado
        :return: Matriz con las ecuaciones diferenciales evaluadas en t_0.
        '''

        dy = np.zeros((4,))
        dy[0] = dV_dt(Id(t_ev),X[0],X[1],X[2],X[3])
        dy[1] = dn_dt(phi_val,X[0],X[1])
        dy[2] = dm_dt(phi_val,X[0],X[2])
        dy[3] = dh_dt(phi_val,X[0],X[3])

        return dy

    # Se implementa la solución del sistema ODE usando la funcion odeint de la librería Scipy.
    Sol_Scipy = odeint(deriv_ev_ini,[V_m0, n_0, m_0, h_0],t)

    # Por como se organizó el sistema, la primera columna (índice 0) corresponde al vector de soluciones Vm.
    Vm_Scipy = Sol_Scipy[:,0]

    return t, Vm_Scipy

## 0. THIS IS ONLY A TEST :V TODO Borrar después de probar

plt.figure()
rcParams['font.family'] = 'serif'   # Define que las fuentes usadas en el gráfico son serifadas.

plt.xlabel(r'$t\ \ [mS]$',fontsize='x-large')       # Título secundario del eje x
plt.ylabel(r'$V_m\ [mV]$ ',fontsize='large')        # Título secundario del eje y
plt.style.use('bmh')

plt.title('Potencial de acción de una neurona', fontsize='x-large')
plt.tight_layout(pad=2.0)

# ESTOS SON LOS VALORES POR DEFECTO QUE UTILICÉ PARA PROBAR QUE ESTA VAINA FUNCIONA.
V_m0 = -65.0;   n_0 = 0.30;     m_0 = 0.05;     h_0 = 0.60
T = 10.0

opcion = 1
t1 = 10.0;      t2 = 50.0;      t3 = 100.0;     t4 = 150.0
I1 = 20.0;                      I2 = -15.0
##
t_eFor,V_eFor = EulerFor(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_eFor,V_eFor,color='red',label="For")
plt.legend()
##
t_eBack,V_eBack = EulerBack(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_eBack,V_eBack,color='#fbb901',label="Back")
plt.legend()

##
t_eMod,V_eMod = EulerMod(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_eMod,V_eMod,color='darkgreen',label="Mod")
plt.legend()

##
t_RK2,V_RK2 = RK2(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_RK2,V_RK2,color='blue',label="RK2")
plt.legend()

##
t_RK4,V_RK4 = RK4(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_RK4,V_RK4,color='purple',label="RK4")
plt.legend()

##
t_Scipy, V_Scipy = SCIPY(V_m0,n_0,m_0,h_0,T,opcion,t1,t2,t3,t4,I1,I2)
plt.plot(t_Scipy,V_Scipy,color='black',label="Scipy")
plt.legend()