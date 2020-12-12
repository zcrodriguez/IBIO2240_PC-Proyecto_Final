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
# Debido a la dependencia natural de los canales iónicos con la temperatura (Temperatura ∝ Rapidez de los cambios).

# Radio de las tasas por un incremento de temperatura de 10 °C
Q_10 = 3

# Temperatura base
T_base = 6.3    # [°C]

# Factor de temperatura (Φ(T))
def phi(T):
    return (Q_10) ** ((T - T_base) / 10.0)

# Temperatura inresada por usuario
T = 10.0    # [°C]      TODO Conectar este parámetro con interfaz. Lo ingresa el usuario.

# Valor de phi para la temperatura T ingresada por el usuario.
phi_val = phi(T)



# ========================================            CORRIENTE (I(t))         =========================================

# PARTE I - TIEMPO (t)

# Determina si la corriente es fija o variable TODO Traer info desde la interfaz
I_is_var = True

# Intervalo 1   TODO Traer valor inicial y final del intervalo 1 desde la interfaz.
t_i1 = 10.0
t_f1 = 50.0

# Intervalo 2   TODO Traer valor inicial y final del intervalo 2 desde la interfaz.
t_i2 = 100.0
t_f2 = 150.0

# Tiempo inicial (T0) y final (Tf) de simulación (graficado)
t_0 = 0.0   # [mS]
t_f = (t_f2 if I_is_var else t_f1) + 50.0  # [mS]

# Se define un valor para h (Resolución de la respuesta / Step).
h_res = 0.01    # [mS]

# Se crea el arreglo de tiempo que va desde To a Tf con pasos de h
t = np.arange(t_0, t_f + h_res, h_res)

#-----------------------------------------------------------------------------------------------------------------------

# PARTE II - Corriente (I(t))

I_array = np.zeros(len(t))      # Se crea el arreglo que almacena la corriente respecto al tiempo.

I_1 =  9.0     # TODO Traer el valor de corriente del primer intervalo de la interfaz.
I_2 = -9.0     # TODO Traer el valor de corriente del segundo intervalo de la interfaz.

# Intervalo 1
IInd = np.where((t >= t_i1) & (t <= t_f1))          # np.where retorna los t que están en el intervalo 1.
I_array[IInd] = I_1                                 # Para los t hallados por np.where en el arreglo se asigna-

# Intervalo 2 - Aplica cuando la corriente es variable.
if I_is_var:
    IInd = np.where((t >= t_i2) & (t <= t_f2))
    I_array[IInd] = I_2



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

# VALORES INICIALES
# Antes de que el usuario ingrese los valores deseados, deben haber unos valores iniciales 'by default' para
# las incógnitas de tal forma que se pueda ejecutar el modelo.

V_m0 = -65.0    #[mV]   TODO Conectar este parámeto con interfaz. Lo ingresa el usuario.

# Valores de probabilidad: Estimados a partir de gráficos de los papers sugeridos.
m_0 = 0.05      # TODO Conectar este parámeto con interfaz. Lo ingresa el usuario.
n_0 = 0.30      # TODO Conectar este parámeto con interfaz. Lo ingresa el usuario.
h_0 = 0.60      # TODO Conectar este parámeto con interfaz. Lo ingresa el usuario.


#=======================================    ARREGLOS QUE ALMACENAN SOLUCIONES   ========================================

# I. POTENCIAL DE MEMBRANA

# Se crea un arreglo que almacena el V_m de en cada iteración.
Vm_EulerFor = np.zeros(len(t))
Vm_EulerBack = np.zeros(len(t))
Vm_EulerMod = np.zeros(len(t))
Vm_RK2 = np.zeros(len(t))
Vm_RK4 = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → V(t=0) = V_m0.
Vm_EulerFor[0] = V_m0
Vm_EulerBack[0] = V_m0
Vm_EulerMod[0] = V_m0
Vm_RK2[0] = V_m0
Vm_RK4[0] = V_m0

# II. PROBABILIDAD DE n

# Se crea un arreglo que almacena la probabilidad de n en cada iteración.
n_EulerFor = np.zeros(len(t))
n_EulerBack = np.zeros(len(t))
n_EulerMod = np.zeros(len(t))
n_RK2 = np.zeros(len(t))
n_RK4 = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → n(t=0) = n_0.
n_EulerFor[0] = n_0
n_EulerBack[0] = n_0
n_EulerMod[0] = n_0
n_RK2[0] = n_0
n_RK4[0] = n_0

# III. PROBABILIDAD DE m

# Se crea un arreglo que almacena la probabilidad de m en cada iteración.
m_EulerFor = np.zeros(len(t))
m_EulerBack = np.zeros(len(t))
m_EulerMod = np.zeros(len(t))
m_RK2 = np.zeros(len(t))
m_RK4 = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → m(t=0) = m_0.
m_EulerFor[0] = m_0
m_EulerBack[0] = m_0
m_EulerMod[0] = m_0
m_RK2[0] = m_0
m_RK4[0] = m_0

# IV. PROBABILIDAD DE h

# Se crea un arreglo que almacena la probabilidad de h en cada iteración.
h_EulerFor = np.zeros(len(t))
h_EulerBack = np.zeros(len(t))
h_EulerMod = np.zeros(len(t))
h_RK2 = np.zeros(len(t))
h_RK4 = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → h(t=0) = h_0.
h_EulerFor[0] = h_0
h_EulerBack[0] = h_0
h_EulerMod[0] = h_0
h_RK2[0] = h_0
h_RK4[0] = h_0


#=============================================    FUNCIONES AUXILIARES   ===============================================

# EULER HACIA ATRÁS (BACKWARD)
# y_i = y_(i-1) + h * F(y_i)    →   0 = y_(i-1) + h * F(y_i) - y_i

def FAux_EulerBack(Aux, I, Vm, n, m, h, phi_val, h_res):
    return [Vm + h_res * dV_dt(I, Aux[0], Aux[1], Aux[2], Aux[3]) - Aux[0],
            n + h_res * dn_dt(phi_val, Aux[0], Aux[1]) - Aux[1],
            m + h_res * dm_dt(phi_val, Aux[0], Aux[2]) - Aux[2],
            h + h_res * dh_dt(phi_val, Aux[0], Aux[3]) - Aux[3]]

# EULER HACIA ADELANTE (BACKWARD)

def FAux_EulerMod(Aux, I, Vm, n, m, h, phi_val, h_res):
    return [Vm + (h_res / 2.0) * (dV_dt(I, Vm, n, m, h) + dV_dt(I, Aux[0], Aux[1], Aux[2], Aux[3])) - Aux[0],
            n + (h_res / 2.0)  * (dn_dt(phi_val, Vm, n) + dn_dt(phi_val, Aux[0], Aux[1])) - Aux[1],
            m + (h_res / 2.0)  * (dm_dt(phi_val, Vm, m) + dm_dt(phi_val, Aux[0], Aux[2])) - Aux[2],
            h + (h_res / 2.0)  * (dh_dt(phi_val, Vm, h) + dh_dt(phi_val, Aux[0], Aux[3])) - Aux[3]]



#================================================  SOLUCIÓN DEL MODELO =================================================

# Se crea un procedimiento iterativo que recorre por completo el arreglo de tiempo desde
# la segunda posición hasta la última.

# I. EULER FORWARD
# Las ecuaciones fueron formuladas siguiendo el formato y_(i) = y_(i-1)+h[F(y_(i-1))]

for iter in range(1, len(t)):

    Vm_EulerFor[iter] = Vm_EulerFor[iter - 1] + h_res * dV_dt(I_array[iter], Vm_EulerFor[iter - 1],
                                                          n_EulerFor[iter - 1],
                                                          m_EulerFor[iter - 1], h_EulerFor[iter - 1])
    n_EulerFor[iter] = n_EulerFor[iter - 1] + h_res * dn_dt(phi_val, Vm_EulerFor[iter - 1], n_EulerFor[iter - 1])
    m_EulerFor[iter] = m_EulerFor[iter - 1] + h_res * dm_dt(phi_val, Vm_EulerFor[iter - 1], m_EulerFor[iter - 1])
    h_EulerFor[iter] = h_EulerFor[iter - 1] + h_res * dh_dt(phi_val, Vm_EulerFor[iter - 1], h_EulerFor[iter - 1])


# II. EULER BACKWARD

for iter in range(1, len(t)):
    BackRoots = opt.fsolve(FAux_EulerBack, np.array([Vm_EulerBack[iter - 1],
                                                     n_EulerBack[iter - 1],
                                                     m_EulerBack[iter - 1],
                                                     h_EulerBack[iter - 1]]),
                           (I_array[iter], Vm_EulerBack[iter - 1], n_EulerBack[iter - 1], m_EulerBack[iter - 1],
                            h_EulerBack[iter - 1], phi_val, h_res))

    Vm_EulerBack[iter] = BackRoots[0]
    n_EulerBack[iter] = BackRoots[1]
    m_EulerBack[iter] = BackRoots[2]
    h_EulerBack[iter] = BackRoots[3]


# III. EULER MOD
# Las ecuaciones fueron despejadas siguiendo el formato y_(i) = y_(i-1)+h/2*[F(y_(i-1))+F(y_(i))]
    ModRoots = opt.fsolve(FAux_EulerMod, np.array([Vm_EulerMod[iter - 1],
                                                   n_EulerMod[iter - 1],
                                                   m_EulerMod[iter - 1],
                                                   h_EulerMod[iter - 1]]),
                          (I_array[iter], Vm_EulerMod[iter - 1], n_EulerMod[iter - 1],
                           m_EulerMod[iter - 1], h_EulerMod[iter - 1], phi_val, h_res))

    Vm_EulerMod[iter] = ModRoots[0]
    n_EulerMod[iter] = ModRoots[1]
    m_EulerMod[iter] = ModRoots[2]
    h_EulerMod[iter] = ModRoots[3]

# IV. RUNGE-KUTTA 2 (RK2)
# TODO [Caro] Transcribir las ecuaciones que hice en papel.


# V. RUNGE-KUTTA 4 (RK4)



# Gráfico de las soluciones
plt.figure()
plt.plot(t,Vm_EulerFor)
plt.plot(t,Vm_EulerBack)
plt.plot(t,Vm_EulerMod)
