# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Defines laser components.
"""

import math

from qenergy.components.base import ActiveComponent
from qenergy.components.others import MBC, DAC, ThorlabsPowerMeter, Computer


class Laser(ActiveComponent):
    name = "Laser"
    frequency = 80 * 10**6  # in Hz
    power = 10

    @property
    def init_time(self):
        return math.ceil(10**9 / self.frequency)  # in ns


class LaserVerdiC532(Laser):
    name = "Verdi C-Series"
    wavelength = 532  # 532 nm
    power = 360  # 1200W plus water cooling
    fixed_energy = 360 * 30 * 60
    meas_power = None


class LaserVerdiV532(Laser):
    name = "Verdi V-Series"
    wavelength = 532  # 532 nm
    power = 900  # 1200W plus water cooling
    fixed_energy = power * 30 * 60
    meas_power = 480
    fixed_energy_meas = 864 * 1e3


class LaserDLC780(Laser):
    name = "DLC TA pro"
    wavelength = 780
    power = 70
    fixed_energy = 0
    meas_power = None


class LaserD2547P1550(Laser):
    name = "D2547P"
    wavelength = 1550
    power = 3
    fixed_energy = 0


class LaserNKTkoheras1550(Laser):
    name = "NKT Koheras Basik X15"
    wavelength = 1550
    power = 4
    fixed_energy = 30 * power
    meas_power = 4.2
    fixed_energy_meas = 0.126 * 1e3


class LaserMira780Pulsed(Laser):
    name = "Mira HP F"
    wavelength = 780  # 780 nm
    power = 1800
    fixed_energy = 60 * 30 * power


class LaserSCW1550Pulsed(Laser):
    name = "SCW 1532-500R"
    wavelength = 1550  # 1550 nm
    power = 2.4
    fixed_energy = 0


class LaserCVPPCL590(Laser):
    name = "PurePhotonics_PPCL590"
    wavelength = 1550  # 1550 nm
    frequency = 1e8  # This can be actually raised to 1 GHz if necessary
    power = 2
    fixed_energy = 30 * power  # 30 s startup time, times 2 W of power


class LaserCVNKT(Laser):
    name = "Koheras_NKT"
    wavelength = 1550  # 1550 nm
    frequency = 1e8  # This can be actually raised to 1 GHz if necessary
    power = 4.5
    fixed_energy = 120 * power


class SourceCV(LaserCVPPCL590, MBC, DAC, ThorlabsPowerMeter, Computer):

    name = "CVQKD source"

    power = (
        LaserCVPPCL590.power
        + MBC.power
        + DAC.power
        + ThorlabsPowerMeter.power
        + Computer.power
    )

    fixed_energy = LaserCVPPCL590.fixed_energy + MBC.fixed_energy
    fixed_energy += (
        DAC.fixed_energy + ThorlabsPowerMeter.fixed_energy + Computer.fixed_energy
    )


class SourceCKA(LaserCVPPCL590, MBC, DAC, ThorlabsPowerMeter):

    name = "CVCKA source"

    def power_n_users(self, number_users: int) -> float:
        return number_users * (
            LaserCVPPCL590.power + MBC.power + DAC.power + ThorlabsPowerMeter.power
        )

    def fixed_energy_n_users(self, number_users: int) -> float:
        fixed_energy = number_users * (LaserCVPPCL590.fixed_energy + MBC.fixed_energy)
        fixed_energy += number_users * (
            DAC.fixed_energy + ThorlabsPowerMeter.fixed_energy
        )
        return fixed_energy
