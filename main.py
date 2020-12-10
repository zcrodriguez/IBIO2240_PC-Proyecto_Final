import numpy as np
import matplotlib.pyplot as plt
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

# β_m(V)
def beta_m(V):
    return 4.0 * np.exp(-(V + 65.0) / 18.0)

# α_h(V)
def alpha_h(V):
    return 0.07 * np.exp(-(V + 65.0) / 20.0)

# β_h(V)
def beta_h(V):
    return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))

# α_n(V)
def alpha_n(V):
    return (0.01 * (V + 55.0)) / (1.0 - np.exp(-(V + 55.0) / 10.0))

# β_n(V)
def beta_n(V):
    return 0.125 * np.exp(-(V + 65.0) / 80.0)

# α_m(V)
def alpha_m(V):
    return (0.1 * (V + 40.0)) / (1.0 - np.exp(-(V + 40.0) / 10.0))



# ====================================            FACTOR DE TEMPERATURA (Φ)         ====================================
# Debido a la dependencia natural de los canales iónicos con la temperatura (Temperatura ∝ Rapidez de los cambios).

# Radio de las tasas por un incremento de temperatura de 10 °C
Q_10 = 3

# Temperatura base
T_base = 6.3    # [°C]

# Factor de temperatura (Φ(T))
# TODO Revisar si esto amerita funcion o puede ser una constante, considerando de que T es ingresada por el usuario.
# Si phi se vuelve constante en vez de función (lo cual a lo mejor tiene más sentido) hay que modificar
# las ecuaciones diferenciales.

def phi(T):
    return (Q_10)**((T - T_base) / 10.0)

# Temperatura inresada por usuario
T = 9.7    # [°C]
phi_val = phi(T)


# ========================================            TIEMPO (t)         =========================================
# TODO Verificar que está bien definido. Los tiempos están definidos por los usuarios.
# Tiempo inicial (T0) y final (Tf) de simulación
t_0 = 0.0   # [mS]
t_f = 30.0  # [mS]

# Se define un valor para h (Resolución de la respuesta / Step).
h = 0.01    # [mS]

# Se crea el arreglo de tiempo que va desde To a Tf con pasos de h
t = np.arange(t_0,t_f+h,h)


# ========================================            CORRIENTE (I(t))         =========================================
# TODO Plantear la rutina que permita generar los arreglos de corriente.

# Corriente Continua
# Corriente ingresada por el usuario en el intervalo de tiempo indicado por el usuario en la GUI.

# Corriente Variable
# Corrientes ingresadas por el usuario en los dos (2) intervalos de tiempo indicados por el usuario en la GUI.

# Arreglo mock
I_array = np.zeros(t)

'''=====================================================================================================================
                                                ECUACIONES DIFERENCIALES
====================================================================================================================='''

# PARTE I - ECUACIONES AUXILIARES

# Corriente de Na+  [Ec (2)]
def I_Na(V,m,h):
    return g_Na * (m**3) * h * (V - E_Na)

# Corriente de K+   [Ec (1)]
def I_K(V,n):
    return g_K * (n**4) * (V - E_K)

# Corriente de fuga L (Cl- y otros iones)   [Ec (3)]
def I_L(V):
    return g_L * (V - E_L)

#-----------------------------------------------------------------------------------------------------------------------

# PARTE II - ECUACIONES DIFERENCIALES

# Ecuación I - Hallada al despejar la ecuación de corriente I(t).    [Ec (5) y (6)]
def dV_dt(I, Vm, n, m, h):
    return ( I - I_L(Vm) - I_K(Vm,n) - I_Na(Vm,m,h) ) / ( C_M )

# Ecuación II
def dn_dt(phi,Vm,n):
    return phi* (alpha_n(Vm) * (1 - n) - beta_n(Vm) * n)

# Ecuación III
def dm_dt(phi,Vm,m):
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

V_m0 = -65 #[mV]    Este valor inicial corresponde a V_rest

# Valores de probabilidad: Estimados a partir de gráficos de los papers sugeridos.
m_0 = 0.05
n_0 = 0.30
h_0 = 0.60


#=======================================    ARREGLOS QUE ALMACENAN SOLUCIONES   ========================================

# I. VOLTAJE DE MEMBRANA

# Se crea un arreglo que almacena el V_m de en cada iteración.
Vm_EulerFor = np.zeros(len(t))
#Vm_EulerBack = np.zeros(len(t))
#Vm_EulerMod = np.zeros(len(t))
#Vm_RK2 = np.zeros(len(t))
#Vm_RK4 = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → V(t=0) = V_m0.
Vm_EulerFor[0] = V_m0
#Vm_EulerBack[0] = V_m0
#Vm_EulerMod[0] = V_m0
#Vm_RK2[0] = V_m0
#Vm_RK4[0] = V_m0


# II. PROBABILIDAD DE n

# Se crea un arreglo que almacena el V_m de en cada iteración.
n_EulerFor = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → V(t=0) = V_m0.
n_EulerFor[0] = n_0


# III. PROBABILIDAD DE m

# Se crea un arreglo que almacena el V_m de en cada iteración.
m_EulerFor = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → V(t=0) = V_m0.
m_EulerFor[0] = m_0


# IV. PROBABILIDAD DE h

# Se crea un arreglo que almacena el V_m de en cada iteración.
h_EulerFor = np.zeros(len(t))

# Se asigna el valor de la condicion inicial al primer valor. → V(t=0) = V_m0.
h_EulerFor[0] = m_0



#================================================  SOLUCIÓN DEL MODELO =================================================

# Se crea un procedimiento iterativo que recorre por completo el arreglo de tiempo desde
# la segunda posición hasta la última.
for iter in range(1,len(t)):

    # EULER FORWARD
    Vm_EulerFor[iter] = Vm_EulerFor[iter-1] + h * dV_dt(I_array[iter],Vm_EulerFor[iter-1],n_EulerFor[iter-1],
                                                        m_EulerFor[iter-1],h_EulerFor[iter-1])
    n_EulerFor[iter] = n_EulerFor[iter-1]   + h * dn_dt(phi_val,Vm_EulerFor[iter-1],n_EulerFor[iter-1])
    m_EulerFor[iter] = m_EulerFor[iter-1]   + h * dm_dt(phi_val,Vm_EulerFor[iter-1],m_EulerFor[iter-1])
    h_EulerFor[iter] = h_EulerFor[iter-1]   + h * dh_dt(phi_val,Vm_EulerFor[iter-1],h_EulerFor[iter-1])

    # EULER BACKWARD

    # EULER MOD

    # RUNGE-KUTTA 2 (RK2)
    # TODO [Caro] Transcribir las ecuaciones que hice en papel.

    # RUNGE-KUTTA 4 (RK4)
