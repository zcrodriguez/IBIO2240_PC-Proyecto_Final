import numpy as np

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


# Capacitancia de la membrana por unidad de área         ***(PENDIENTE CONFIRMAR, NO APARECE EN EL ENUNCIADO)***
C_M = 1.0 * 10**6       # [F/cm^2]


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

# Radio de las tasas por un incremento de temmpratura de 10 °C
Q_10 = 3

# Temperatura base
T_base = 6.3    # [°C]

# Factor de temperatura: Φ(T)
def phi(T):
    return (Q_10)**((T - T_base) / 10.0)
