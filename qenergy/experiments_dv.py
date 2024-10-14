# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import math
from typing import List

from qenergy.components import Component, Fiber, Oven, MotorizedWavePlate, Computer
from qenergy.experiments import Experiment


class DVExperiment(Experiment):
    """Model for an experiment
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `pcoupling` : float
        Coupling in the fiber success probability
    `mu`: float
        Efficiency of the source
    `wavelength`: int
        Wavelength of experiment [nm]
    """

    def __init__(self, sourcerate, pcoupling, mu, wavelength, allcomponent=[]):
        super().__init__()
        self.sourcerate = sourcerate
        self.pcoupling = pcoupling
        self.mu = mu
        self.wavelength = wavelength
        self.fiber = Fiber(self.wavelength)
        self.list_components = allcomponent

    def h(self, p: float) -> float:
        """
        Return the binary entropy of p.

        Args:
            p (float): probability.

        Returns:
            float: binary entropy of p.
        """
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1.")
        if p in (0, 1):
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


class BB84Experiment(DVExperiment):
    """Model for a BB84 experiment
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `pcoupling` : float
        Coupling in the fiber success probability
    `mu`: float
        Efficiency of the source
    `wavelength`: int
        Wavelength of experiment [nm]
    `qber` : float
        Qubit Error Rate
    `source`: Component
        source used from component.py
    `detector`: Component
        detector used from component.py
    `dist`: list
        Range of distances considered [km]
    `othercomponent`: list
        Other components involved in the experiment
    """

    def __init__(
        self,
        sourcerate,
        pcoupling,
        mu,
        wavelength,
        qber,
        source,
        detector,
        dist,
        othercomponent=[],
    ):
        super().__init__(sourcerate, pcoupling, mu, wavelength)
        self.qber = qber
        self.source = source
        self.detector = detector
        self.dist = dist
        self.othercomponent = othercomponent
        self.list_components = [self.source] + [self.detector] + self.othercomponent

    def compute_raw_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [
            self.sourcerate
            * self.mu
            * (self.pcoupling)
            * self.detector.efficiency
            * (10 ** (-self.fiber.attenuation_fiber_db_km * d / 10))
            for d in self.dist
        ]

    def compute_secret_key_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [R * (1 - 2 * self.h(self.qber)) for R in self.compute_raw_rate()]

    def time_skr(self, objective):
        """Time necessary to create 'objective' secret bits"""
        return [objective / R for R in self.compute_secret_key_rate()]


class EntanglementBasedExperiment(DVExperiment):
    """Model for a E91 experiment
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `pcoupling` : float
        Coupling in the fiber success probability
    `mu`: float
        Efficiency of the source
    `wavelength`: int
        Wavelength of experiment [nm]
    `qber` : float
        Qubit Error Rate
    `source`: Component
        source used from component.py
    `detector_alice`: Component
        detector used by Alice from component.py
    `detector_bob`: Component
        detector used by Bob from component.py
    `dist`: list
        Range of distances considered [km]
    `othercomponent`: list
        Other components involved in the experiment
    """

    def __init__(
        self,
        sourcerate: float,
        pcoupling: float,
        mu: float,
        wavelength: float,
        qber: float,
        source: Component,
        detector_alice: Component,
        detector_bob: Component,
        dist: List[float],
        othercomponent: List[Component] = [],
    ):
        super().__init__(sourcerate, pcoupling, mu, wavelength)
        self.qber = qber
        self.source = source
        self.detector_alice = detector_alice
        self.detector_bob = detector_bob
        self.dist = dist
        self.othercomponent = othercomponent
        self.list_components = (
            [self.source]
            + [self.detector_alice]
            + [self.detector_bob]
            + self.othercomponent
        )

    def compute_raw_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [
            self.sourcerate
            * self.mu
            * (self.pcoupling**2)
            * (self.detector_alice.efficiency)
            * (self.detector_bob.efficiency)
            * (10 ** (-self.fiber.attenuation_fiber_db_km * d / 10))
            for d in self.dist
        ]

    def compute_secret_key_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [R * (1 - 2 * self.h(self.qber)) for R in self.compute_raw_rate()]

    def time_skr(self, objective):
        """Time necessary to create 'objective' secret bits"""
        return [objective / R for R in self.compute_secret_key_rate()]


class MDIQKDExperiment(DVExperiment):
    """Model for a MDIQKD experiment with Alice and Bob sending BB84 states to a central station that performs a BSM with efficiency pbsm
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `pcoupling` : float
        Coupling in the fiber success probability
    `mu`: float
        Efficiency of the source
    `wavelength`: int
        Wavelength of experiment [nm]
    `qber` : float
        Qubit Error Rate
    `source_alice`: Component
        source used by Alice from component.py
    `source_bob`: Component
        source used by Bob from component.py
    `detector`: Component
        detector used by the central node from component.py
    `dist`: list
        Range of distances considered [km]
    `othercomponent`: list
        Other components involved in the experiment
    `pbsm`: float
        Probability that the bell state measurement succeeds
    """

    def __init__(
        self,
        sourcerate,
        pcoupling,
        mu,
        wavelength,
        qber,
        source_alice,
        source_bob,
        detector,
        dist,
        pbsm,
        othercomponent=[],
    ):
        super().__init__(sourcerate, pcoupling, mu, wavelength)
        self.qber = qber
        self.source_alice = source_alice
        self.source_bob = source_bob
        self.detector = detector
        self.dist = dist
        self.othercomponent = othercomponent
        self.pbsm = pbsm
        self.list_components = (
            [self.source_alice]
            + [self.source_bob]
            + [self.detector]
            + self.othercomponent
        )

    def compute_raw_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [
            self.sourcerate
            * self.mu
            * self.mu
            * (self.pcoupling**2)
            * (self.detector.efficiency**2)
            * (10 ** (-self.fiber.attenuation_fiber_db_km * d / 10))
            * self.pbsm
            for d in self.dist
        ]

    def compute_secret_key_rate(self):
        """Calculation of the raw rate of the BB84 experiment
        returns an array of raw rates for all the distance considered"""
        return [R * (1 - 2 * self.h(self.qber)) for R in self.compute_raw_rate()]

    def time_skr(self, objective):
        """Time necessary to create 'objective' secret bits"""
        return [objective / R for R in self.compute_secret_key_rate()]

    def raw_time(self, objective):
        """Time necessary to create 'objective' bits"""
        return [objective / R for R in self.compute_raw_rate()]


class GHZsharing(DVExperiment):
    """Model for a GHZ-CKA experiment with a central node sending qubits of a GHZ states to n parties, at equal distance from the source
    Instance of an experiment to estimate its energy

    Parameters
    ----------
    `sourcerate` : float
        Rate of the source [Hz]
    `pcoupling` : float
        Coupling in the fiber success probability
    `mu`: float
        Efficiency of the source
    `wavelength`: int
        Wavelength of experiment [nm]
    `qber` : float
        Qubit Error Rate
    `source_ghz`: Componentsinner
        laser used from component.py
    `n`: int
        Number of parties involved
    `detector`: Component
        detector used by the parties from component.py
    `dist`: int
        Distance between the central party and the others [km]
    `othercomponent`: list
        Other components involved in the experiment
    """

    def __init__(
        self,
        sourcerate,
        pcoupling,
        mu,
        wavelength,
        qber,
        source_ghz,
        n,
        detector,
        dist,
        othercomponent=[],
    ):
        super().__init__(sourcerate, pcoupling, mu, wavelength)
        self.qber = qber
        self.source_ghz = source_ghz
        self.detector = detector
        self.dist = dist
        self.n = n
        self.othercomponent = othercomponent
        self.list_components = self.othercomponent
        for _ in range(n):
            self.list_components.append(detector)
            self.list_components.append(MotorizedWavePlate())
            self.list_components.append(Computer())
        for _ in range(math.ceil(n / 2)):
            self.list_components.append(source_ghz)
            self.list_components.append(Oven())
        for _ in range(math.floor((n - 1) / 2)):
            self.list_components.append(MotorizedWavePlate())

    def raw_time_ghz(self, objective):
        """Time necessary to share and measure 'objective' GHZ states among the n parties"""
        raw = (
            self.sourcerate
            * (self.mu ** (self.n / 2))
            * (self.pcoupling**self.n)
            * (self.detector.efficiency ** (self.n))
            * (10 ** (self.n * (-self.fiber.attenuation_fiber_db_km * self.dist / 10)))
        )
        traw = objective / raw
        return traw
