# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np

# import scipy as sp
# from numba import njit,prange


def G(x) -> float:
    if x == 0:
        return 0
    return (x + 1) * np.log2(x + 1) - x * np.log2(x)


##############################################################################
################### KEY RATE FORMULAE ########################################
##############################################################################


def skr_asymptotic_homodyne(
    Va: float,
    T: float,
    xi: float,
    eta: float,
    Vel: float,
    beta: float,
    _number_states: int,
    _number_users: int,
) -> float:
    return np.clip(
        beta * iab_asymptotic_homodyne(Va, T, xi, eta, Vel)
        - holevo_asymptotic_homodyne(Va, T, xi, eta, Vel),
        0,
        None,
    )


def skr_asymptotic_heterodyne(
    Va: float,
    T: float,
    xi: float,
    eta: float,
    Vel: float,
    beta: float,
    _number_states: int,
    _number_users: int,
) -> float:
    return np.clip(
        beta * iab_asymptotic_heterodyne(Va, T, xi, eta, Vel)
        - holevo_asymptotic_heterodyne(Va, T, xi, eta, Vel),
        0,
        None,
    )


def skr_asymptotic_heterodyne_psk(
    Va: float,
    T: float,
    xi: float,
    eta: float,
    Vel: float,
    beta: float,
    number_states: int,
    _number_users: int,
) -> float:
    return np.clip(
        beta * iab_asymptotic_heterodyne(Va, T, xi, eta, Vel)
        - holevo_asymptotic_heterodyne_psk(Va, T, xi, eta, Vel, number_states),
        0,
        None,
    )


def skr_asymptotic_homodyne_psk(
    Va: float,
    T: float,
    xi: float,
    eta: float,
    Vel: float,
    beta: float,
    number_states: int,
    _number_users: int,
) -> float:
    return np.clip(
        beta * iab_asymptotic_homodyne(Va, T, xi, eta, Vel)
        - holevo_asymptotic_homodyne_psk(Va, T, xi, eta, Vel, number_states),
        0,
        None,
    )


def skr_asymptotic_cka(
    Va: float,
    T,
    xi: float,
    eta: float,
    Vel: float,
    beta: float,
    _number_states: int,
    number_users: int,
) -> float:
    return np.clip(
        beta * iab_asymptotic_cka(Va, T, xi, eta, Vel, number_users)
        - holevo_asymptotic_cka(Va, T, xi, eta, Vel, number_users),
        0,
        None,
    )


##############################################################################
####################### ENTROPIC QUANTITIES ##################################
##############################################################################


def iab_asymptotic_homodyne(
    Va: float, T: float, xi: float, eta: float, Vel: float
) -> float:
    return 0.5 * np.log2(1 + (eta * T * Va) / (1 + Vel + eta * T * xi))


def iab_asymptotic_heterodyne(
    Va: float, T: float, xi: float, eta: float, Vel: float
) -> float:
    return np.log2(1 + (eta * T * Va) / (2 + 2 * Vel + eta * T * xi))


def holevo_asymptotic_homodyne(
    Va: float, T: float, xi: float, eta: float, Vel: float
) -> float:
    chi_hom = (1 + Vel) / eta - 1
    chi_line = 1 / T - 1 + xi
    chi_tot = chi_line + chi_hom / T
    V = Va + 1
    A = V**2 * (1 - 2 * T) + 2 * T + T**2 * (V + chi_line) ** 2
    B = T**2 * (V * chi_line + 1) ** 2
    C = (A * chi_hom + V * np.sqrt(B) + T * (V + chi_line)) / (T * (V + chi_tot))
    D = np.sqrt(B) * (V + np.sqrt(B) * chi_hom) / (T * (V + chi_tot))

    lambda_1 = np.sqrt(0.5 * (A + np.sqrt(A**2 - 4 * B)))
    lambda_2 = np.sqrt(0.5 * (A - np.sqrt(A**2 - 4 * B)))
    lambda_3 = np.sqrt(0.5 * (C + np.sqrt(C**2 - 4 * D)))
    lambda_4 = np.sqrt(0.5 * (C - np.sqrt(C**2 - 4 * D)))

    return (
        G(0.5 * (lambda_1 - 1))
        + G(0.5 * (lambda_2 - 1))
        - G(0.5 * (lambda_3 - 1))
        - G(0.5 * (lambda_4 - 1))
    )


def holevo_asymptotic_heterodyne(
    Va: float, T: float, xi: float, eta: float, Vel: float
) -> float:
    chi_het = (2 - eta + 2 * Vel) / eta
    chi_line = 1 / T - 1 + xi
    chi_tot = chi_line + chi_het / T
    V = Va + 1

    A = V**2 * (1 - 2 * T) + 2 * T + T**2 * (V + chi_line) ** 2
    B = T**2 * (V * chi_line + 1) ** 2
    C = (
        1
        / (T * (V + chi_tot)) ** 2
        * (
            A * chi_het**2
            + B
            + 1
            + 2 * chi_het * (V * np.sqrt(B) + T * (V + chi_line))
            + 2 * T * (V**2 - 1)
        )
    )
    D = (V + np.sqrt(B) * chi_het) ** 2 / (T * (V + chi_tot)) ** 2

    lambda_1 = np.sqrt(0.5 * (A + np.sqrt(A**2 - 4 * B)))
    lambda_2 = np.sqrt(0.5 * (A - np.sqrt(A**2 - 4 * B)))
    lambda_3 = np.sqrt(0.5 * (C + np.sqrt(C**2 - 4 * D)))
    lambda_4 = np.sqrt(0.5 * (C - np.sqrt(C**2 - 4 * D)))

    return (
        G(0.5 * (lambda_1 - 1))
        + G(0.5 * (lambda_2 - 1))
        - G(0.5 * (lambda_3 - 1))
        - G(0.5 * (lambda_4 - 1))
    )


############################################################################################
####################### FUNCTIONS FOR PSK ##################################################
############################################################################################


# @njit
def holevo_asymptotic_heterodyne_psk(
    Va: float, T: float, xi: float, eta: float, Vel: float, number_states: int = 4
) -> float:

    V = 1 + Va
    W = 1 + Va * eta * T + xi * eta * T + Vel

    Z = z_psk(Va, T, xi, eta, Vel, number_states)

    # Build the covariance matrix
    cmatrix = np.diag(np.array([V, V, W, W]))
    cmatrix[0:2, 2:4] = np.diag(np.array([Z, -Z]))
    cmatrix[2:4, 0:2] = np.diag(np.array([Z, -Z]))

    # DetCmatrix = (V*W - Z**2)**2

    # Symplectic eigenvalues
    delta = V**2 + W**2 - 2 * np.abs(Z) ** 2
    nu1 = np.sqrt((delta + np.sqrt(delta**2 - 4 * np.linalg.det(cmatrix))) / 2)
    nu2 = np.sqrt((delta - np.sqrt(delta**2 - 4 * np.linalg.det(cmatrix))) / 2)

    # Conditional symplectic eigenvalue
    nu3 = V - (Z**2) / (W + 1)

    # Mual info from covariance matrix
    # MI = np.log2((1+ V**2 + 2*V)/(1+ nu3**2 + 2*nu3))/2

    g = lambda x: (x + 1) * np.log2(x + 1) - x * np.log2(x) if x != 0 else 0

    # Holevo information
    return g((nu1 - 1) / 2) + g((nu2 - 1) / 2) - g((nu3 - 1) / 2)


# @njit
def holevo_asymptotic_homodyne_psk(
    Va: float, T: float, xi: float, eta: float, Vel: float, number_states: int = 4
) -> float:

    V = 1 + Va
    # Note that calculating W for homodyne distillation is
    # optimized when Bob performs heterodyne detection in PE
    W = 1 + Va * eta * T + xi * eta * T + Vel

    Z = z_psk(Va, T, xi, eta, Vel, number_states)

    # Build the covariance matrix
    cmatrix = np.diag(np.array([V, V, W, W]))
    cmatrix[0:2, 2:4] = np.diag(np.array([Z, -Z]))
    cmatrix[2:4, 0:2] = np.diag(np.array([Z, -Z]))

    # DetCmatrix = (V*W - Z**2)**2

    # Symplectic eigenvalues
    delta = V**2 + W**2 - 2 * np.abs(Z) ** 2
    nu1 = np.sqrt((delta + np.sqrt(delta**2 - 4 * np.linalg.det(cmatrix))) / 2)
    nu2 = np.sqrt((delta - np.sqrt(delta**2 - 4 * np.linalg.det(cmatrix))) / 2)

    # Conditional symplectic eigenvalue
    nu3 = np.sqrt(V * (V - (Z**2) / W))

    g = lambda x: (x + 1) * np.log2(x + 1) - x * np.log2(x) if x != 0 else 0

    # Holevo information
    return g((nu1 - 1) / 2) + g((nu2 - 1) / 2) - g((nu3 - 1) / 2)


# @njit
def z_psk(
    Va: float, T: float, xi: float, eta: float, Vel: float, number_states: int
) -> float:

    amp2 = Va / 2
    theta = 2 * np.pi / number_states

    # Coefficients of the (Schimdt-decomposed) states via a Fourier transform
    nu = [
        np.sum(
            [
                np.exp(-1j * m * k * theta) * np.exp(np.exp(1j * m * theta) * amp2)
                for m in range(number_states)
            ]
        )
        / number_states
        for k in range(number_states)
    ]

    # Clear imaginary residuals
    nu = np.real(nu)

    # Value of Z for a general M-PSK modulation
    ###########################################
    aux1 = np.sum(
        [(nu[k - 1] ** (3 / 2)) / np.sqrt(nu[k]) for k in range(number_states)]
    )
    aux2 = np.sum([(nu[k - 1] ** 2) / nu[k] for k in range(number_states)])

    return np.sqrt(T * eta) * (
        2 * amp2 * np.exp(-amp2) * aux1
        - np.sqrt(2 * xi + Vel / (T * eta))
        * np.sqrt(amp2)
        * np.sqrt(np.exp(-amp2) * aux2 - np.exp(-2 * amp2) * aux1**2)
    )


############################################################################################
####################### FUNCTIONS FOR CKA ##################################################
############################################################################################


def iab_asymptotic_cka(
    Va: float, T: float, xi: float, eta: float, Vel: float, number_users: int
) -> float:

    # NOTICE -- here, Va plays the role of the squeezing!
    mu = np.cosh(Va)

    # Thermal noise
    nth = (1 - eta + Vel) / eta
    omega = 2 * nth + 1

    # Covariance matrix
    x = T * mu + (1 - T) * omega
    y = mu
    z = np.sqrt(T) * np.sqrt(mu**2 - 1)

    # Gamma & Delta
    gamma = (z**2) / (number_users * x) * np.diag([1, -1])
    delt1 = y - (number_users - 1) * (z**2) / (number_users * x)
    delt2 = y - (z**2) / (number_users * x)
    delta = np.diag([delt1, delt2])

    # Conditional covariance matrix
    V_B = delta - gamma @ (np.diag([(delt1 + 1) ** (-1), (delt2 + 1) ** (-1)])) @ gamma

    return (
        np.log2(
            (1 + np.linalg.det(delta) + np.trace(delta))
            / (1 + np.linalg.det(V_B) + np.trace(V_B))
        )
        / 2
    )


def holevo_asymptotic_cka(
    Va: float, T: float, xi: float, eta: float, Vel: float, number_users: int
) -> float:

    # NOTICE -- here, Va plays the role of the squeezing!
    mu = np.cosh(Va)

    # Thermal noise
    nth = (1 - eta + Vel) / eta
    omega = 2 * nth + 1

    # Covariance matrix
    x = T * mu + (1 - T) * omega
    y = mu
    z = np.sqrt(T) * np.sqrt(mu**2 - 1)

    # Holevo Information
    nu = np.sqrt(y * (y - (z**2) / x))

    lam = number_users * omega * mu + T * (
        1 + mu * (number_users - 1 - number_users * omega)
    )
    lam_bar = number_users * omega * mu + T * (
        number_users - 1 - mu * (number_users * omega - 1)
    )
    tau = number_users * omega * (1 - T) + T * (number_users - 1 + mu)
    tau_bar = number_users * omega * (1 - T) + T * (mu * (number_users - 1) + 1)

    nu_n = np.sqrt(lam * lam_bar / (tau * tau_bar))

    return 2 * G((nu - 1) / 2) - G((nu_n - 1) / 2)
