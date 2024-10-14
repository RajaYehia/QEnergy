# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Optional

import numpy as np
from scipy.constants import physical_constants

from qenergy.components.base import ActiveComponent, PassiveComponent


class BeamSplitter(PassiveComponent):
    name = "Beamsplitter"


class PolarizingBeamSplitter(PassiveComponent):
    name = "Polarizing beamsplitter"
    # Contrast of the detector
    # probability that a photon is routed to the wrong port
    meas_flip = 0
    power = 0
    fixed_energy = 0


class Waveplate(PassiveComponent):
    name = "Waveplate"
    meas_flip = 0.05


class MotorizedWavePlate(Waveplate):
    name = "Motorized Waveplate"
    power = 31
    fixed_energy = 60 * 31
    meas_power = 8.3
    fixed_energy_meas = 0.249 * 1e3


class Fiber(PassiveComponent):
    """
    Define a fiber to calculate its photon loss.
    -> set or get db_km/att_distance are used to define the properties of
    the fiber attenuation in distance or in dB/km
    -> Transmission calculate the fiber transmission
    """

    name = "Fiber"
    power = 0
    fixed_energy = 0
    _length: float
    _attenuation_fiber_db_km: float
    _attenuation_distance: float

    def __init__(
        self,
        wavelength: float,
        length: Optional[float] = None,
        dephasing: float = 0.02,
        coupling: float = 0.9,
    ):
        """
        Define a fiber and sets its default attenuation fiber value
        to 0.2dB/km (typical fiber loss in telecommunication fiber)
        """
        super(Fiber, self).__init__()
        # Speed of light in a fiber
        self.light_speed = (
            2 / 3.0 * physical_constants["speed of light in vacuum"][0] / 10**3
        )
        self.dephasing = dephasing  # dephasing rate per km (in Hz)
        self.coupling = coupling  # fiber coupling efficiency

        if length is None:
            self._length = 0
        else:
            self._length = length
        if wavelength == 1550:
            self._attenuation_fiber_db_km = 0.18
        elif wavelength == 780:
            self._attenuation_fiber_db_km = 4
        elif wavelength == 523:
            self._attenuation_fiber_db_km = 30

    @property
    def T(self):
        """Fiber transmission for a given distance"""
        return self.transmission(self._length)

    @property
    def attenuation_fiber_db_km(self):
        """Attenuation of the fiber in dB per km"""
        return self._attenuation_fiber_db_km

    @property
    def attenuation_distance(self):
        """Attenuation length of the fiber in km"""
        return self._attenuation_distance

    @attenuation_fiber_db_km.setter
    def attenuation_fiber_db_km(self, value):
        self._attenuation_fiber_db_km = value
        self._attenuation_distance = self.convert(value)

    @attenuation_distance.setter
    def attenuation_distance(self, value):
        self._attenuation_distance = value
        self._attenuation_fiber_db_km = self.convert(value)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value: float):
        if type(value) not in [int, float]:
            raise ValueError("distance L should be a positive real.")
        if value < 0:
            raise ValueError("distance L should be a positive real.")
        self._length = value

    @staticmethod
    def convert(f):
        return 10 / (np.log(10) * f)

    def transmission(self, distance):
        """Fiber transmission for a given distance"""
        return np.exp(-distance / self.attenuation_distance)


class SwitchClassic(ActiveComponent):
    success = 0.9


class SwitchIntensityModulator(ActiveComponent):
    success = 0.9
    transmission = 0.7  # ~2 dB insertion loss
    speed = 40 * 10**9  # 40 GHz speed on 2x2 intensity modulator switches
    power = 500  # 350W average for the accompanying signal generator + 400W DC bias voltage power
    fixed_energy = 30 * 500
    meas_power = 26
    fixed_energy_meas = 0.78 * 1e3


class Cryostat(ActiveComponent):
    name = "Cryostat"
    power = 3000  # all electronics and compressors included, except computer
    fixed_energy = 72000  # Approximately 24h long setup on initial cooling
    cooling_time = 0  # 1h long cooling needed every 24h, models exist without that


class Computer(ActiveComponent):
    name = "Computer"
    power = 150  # 300W for computer, DAQ, screen and everything included.
    fixed_energy = 60 * power
    meas_power = 100
    fixed_energy_meas = 6 * 1e3


class Oven(ActiveComponent):
    name = "Oven"
    power = 15
    fixed_energy = 10 * 60 * power
    meas_power = 0.9
    fixed_energy_meas = 0.54 * 1e3


class StabilizationTimeBin(ActiveComponent):
    name = "Stabilization setup"
    power = 200
    fixed_energy = 0


class ComputerDSP(ActiveComponent):
    name = "DSP"
    DSP = 0.006  # 6mJ/symbol


class DAC(ActiveComponent):
    name = "Digital2Analog"
    power = 40
    fixed_energy = 0


class MBC(ActiveComponent):
    name = "ModulatorBiasController"
    power = 5.5
    fixed_energy = 30 * power


class ThorlabsPowerMeter(ActiveComponent):
    name = "ThorlabsPowerMeter_CVQKD"
    power = 0.8
    fixed_energy = 0


class ADC(ActiveComponent):
    name = "Analog2Digital"
    power = 30
    fixed_energy = 0
    meas_power = 20


class PolarizationController(ActiveComponent):
    name = "Polarization Controller"
    power = 1.8
    fixed_energy = 0
    meas_power = 0.35


class SwitchCVQKD(ActiveComponent):
    name = "Switch CVQKD"
    power = 0.35
    fixed_energy = 0


class TimeTagger(ActiveComponent):
    name = "Time tagger"
    power = 50  # 50W alone, without computer.
    meas_power = 22
