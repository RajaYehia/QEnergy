# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
from qenergy import components as comp

# from cvqkd import *
from qenergy.skr_cv import skr_asymptotic_homodyne_psk, skr_asymptotic_heterodyne_psk
from qenergy.skr_cv import skr_asymptotic_homodyne, skr_asymptotic_heterodyne
from qenergy.skr_cv import skr_asymptotic_cka

from qenergy.experiments import Experiment


################## CV experiments ##################


class CVExperiment(Experiment):
    """
    Model for an experiment in continuous variable QKD
    Instance of an experiment to estimate its energy

    Args:
        eta (float): Efficiency of the detector
        Vel (float): Electronic noise of the detector[SNU]
        beta (float): Information reconciliation efficiency
    """

    def __init__(self, eta, Vel, beta, allcomponent=[]):
        super().__init__()
        self.wavelength = 1550  # The wavelength is constant
        self.eta = eta
        self.Vel = Vel
        self.beta = beta
        self.fiber = comp.Fiber(self.wavelength)
        self.list_components = allcomponent


class CVQKDProtocol(CVExperiment):
    """Model for a CVQKD experiment with any modulation and detection
    Instance of an experiment to estimate its energy

    Args:
        sourcerate (float): Rate of the source [Hz]
        eta (float): Efficiency of the detector
        nu (float): Electronic noise of the detector[SNU]
        beta (float): Information reconciliation efficiency
        source (Component): source used from component.py
        detector (List[Component]): detection setup used, it includes the polarization
        setup (str): name of the detection setup
        xi (float): Excess noise at Alice's side [SNU]
        dist (list): Range of distances considered [km]
        protocol (str): Protocol under implementation, it decides the secret key rate
        othercomponent (List[Component]): Other components involved in the experiment
    """

    def __init__(
        self,
        eta,
        Vel,
        beta,
        sourcerate,
        source,
        detector,
        xi,
        dist,
        protocol,
        othercomponent=[],
    ):
        super().__init__(eta, Vel, beta)
        self.sourcerate = sourcerate
        self.source = source
        self.detector = detector[1:]
        self.setup = detector[0]
        self.xi = xi
        self.dist = dist
        self.othercomponent = othercomponent
        self.protocol = protocol
        self.list_components = self.source + self.detector + self.othercomponent

    def compute_secret_key_rate(self):
        """Calculation of the raw rate of the CVQKD protocol
        returns an array of raw rates for all the distances considered"""

        # Double polarization induces a double rate
        if self.setup.split()[-1] == "2P":
            number_polarizations = 2
        else:
            number_polarizations = 1

        # PSK Homodyne
        if self.protocol == "PSK" and self.setup.split()[0] == "Homodyne":
            number_states = 4
            number_users = None
            skr_formula = skr_asymptotic_homodyne_psk
            va_end = 5
            va_step = 0.01

        # PSK Heterodyne
        elif self.protocol == "PSK":
            number_states = 4
            number_users = None
            skr_formula = skr_asymptotic_heterodyne_psk
            va_end = 5
            va_step = 0.01

        # Gaussian Homodyne
        elif self.setup.split()[0] == "Homodyne":
            number_states = None
            number_users = None
            skr_formula = skr_asymptotic_homodyne
            va_end = 100
            va_step = 1

        # Gaussian Heterodyne (default option)
        else:
            number_states = None
            number_users = None
            skr_formula = skr_asymptotic_heterodyne
            va_end = 100
            va_step = 1

        va_start = 0.1
        vas = np.arange(va_start, va_end, va_step)

        skrates = []
        for distance in self.dist:
            T = 10 ** (-self.fiber.attenuation_fiber_db_km * distance / 10)
            key_rates = [
                skr_formula(
                    va,
                    T,
                    self.xi,
                    self.eta,
                    self.Vel,
                    self.beta,
                    number_states,
                    number_users,
                )
                for va in vas
            ]
            # Return skr as bits per second
            skrates.append(number_polarizations * np.max(key_rates) * self.sourcerate)

        return skrates

    def time_skr(self, objective):
        """Time necessary to create 'objective' secret bits"""
        return [objective / R for R in self.compute_secret_key_rate() if R > 0]


################## CKA experiments ##################


class CKAExperiment(Experiment):
    """Model for an experiment in continuous variable CKA
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `eta`: float
        Efficiency of the detector
    `Vel`: float
        Electronic noise of the detector[SNU]
    `beta`: float
        Information reconciliation efficiency
    `number_users`: int
        No. of users involved in the protocol

    """

    def __init__(self, eta, Vel, beta, number_users, allcomponent=[]):
        super().__init__()
        self.wavelength = 1550  # The wavelength is constant
        self.eta = eta
        self.Vel = Vel
        self.beta = beta
        self.number_users = number_users
        self.fiber = comp.Fiber(self.wavelength)
        self.list_components = allcomponent


class CKAProtocol(CKAExperiment):
    """Model for a CVCKA experiment with any number of users
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `eta`: float
        Efficiency of the detector
    `nu`: float
        Electronic noise of the detector[SNU]
    `beta`: float
        Information reconciliation efficiency
    `number_users`: int
        No. of users involved in the protocol
    `source`: Component
        source used from component.py
    `detector`: Component
        detector used from component.py, it includes the polarization
    `xi`: float
        Excess noise at Alice's side [SNU]
    `dist`: list
        Range of distances considered [km]
    `othercomponent` : list
        Other components involved in the experiment
    """

    def __init__(
        self,
        eta,
        Vel,
        beta,
        number_users,
        sourcerate,
        source,
        detector,
        xi,
        dist,
        othercomponent=[],
    ):
        super().__init__(eta, Vel, beta, number_users)
        self.sourcerate = sourcerate
        self.source = source
        self.detector = detector
        self.xi = xi
        self.dist = dist
        self.othercomponent = othercomponent
        self.list_components = [self.source] + [self.detector] + self.othercomponent

    def compute_secret_key_rate(self):
        """Calculation of the raw rate of the CVCKA protocol
        returns an array of raw rates for all the distances considered"""
        number_states = None

        skr_formula = skr_asymptotic_cka
        va_start, va_end, va_step = (0.1, 7, 0.01)

        vas = np.arange(va_start, va_end, va_step)

        skrates = []
        for distance in self.dist:
            T = 10 ** (-self.fiber.attenuation_fiber_db_km * distance / 10)
            key_rates = [
                skr_formula(
                    va,
                    T,
                    self.xi,
                    self.eta,
                    self.Vel,
                    self.beta,
                    number_states,
                    self.number_users,
                )
                for va in vas
            ]
            # Return skr as bits per second
            skrates.append(np.nanmax(key_rates) * self.sourcerate)

        return skrates

    def time_skr(self, objective):
        """Time necessary to create 'objective' secret bits"""
        return [objective / R for R in self.compute_secret_key_rate()]
