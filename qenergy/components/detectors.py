# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from qenergy.components.base import ActiveComponent

from qenergy.components.lasers import LaserCVPPCL590
from qenergy.components.others import (
    Computer,
    ComputerDSP,
    SwitchCVQKD,
    PolarizationController,
    ADC,
)


class Detector(ActiveComponent):
    name = "Detector"
    efficiency = 1
    require_cryo = False
    multi_photon = False
    dark_count = 0  # in Hz
    time_jitter = 0  # in second


class DetectorSiAPD780(Detector):
    name = "Single-photon avalanche photodiode"
    wavelength = 780
    efficiency = 0.80
    dark_count = 50
    time_jitter = 0.5 * 10**-9
    power = 15
    fixed_energy = 0


class DetectorInGAs1550(Detector):
    name = "Single-photon InGAs detectors"
    wavelength = 1550
    efficiency = 0.25
    dark_count = 400
    time_jitter = 0.5 * 10**-9
    dead_time = 1 * 10**-6
    power = 644
    fixed_energy = 30 * 60 * power
    meas_power = 64
    fixed_energy_meas = 125.7 * 1e3


class DetectorSNSPD780(Detector):
    name = "Superconducting nanowire detector for 780nm"
    efficiency = 0.85
    require_cryo = True
    dark_count = 100
    time_jitter = 20 * 10**-12
    power = 3000
    fixed_energy = 24 * 60 * 60 * 3000


class DetectorSNSPD1550(Detector):
    name = "Superconducting nanowire detector for 1550nm"
    wavelength = 1550
    efficiency = 0.95
    require_cryo = True
    dark_count = 100
    time_jitter = 20 * 10**-12
    power = 3000  # all electronics and compressors included, except computer
    fixed_energy = (
        24 * 60 * 60 * 3000
    )  # Approximately 24h long setup on initial cooling
    meas_power = 2735
    fixed_energy_meas = 117639 * 1e3


class Detector523(Detector):
    name = "Single-photon InGAs detectors"
    wavelength = 523
    efficiency = 0.5
    dark_count = 400
    time_jitter = 0.5 * 10**-9
    dead_time = 1 * 10**-6
    power = 45
    fixed_energy = 0


class ThorlabsPDB(ActiveComponent):
    name = "ThorlabsDetector_CVQKD"
    power = 7.5
    fixed_energy = 0


class RxC(ActiveComponent):
    name = "RxC_Detector"
    power = 0.57
    fixed_energy = 0


class HHI(ActiveComponent):
    name = "HHI_Detector"
    power = 0.61
    fixed_energy = 0


class Koheron(ActiveComponent):
    name = "Koheron_Detector"
    power = 0.13
    fixed_energy = 0


class NeoPhotonics(ActiveComponent):
    name = "NeoPhotonicsPowerMeter"
    power = 1.7
    fixed_energy = 0


class DetectorHomodyne1P(
    ADC,
    LaserCVPPCL590,
    Computer,
    ComputerDSP,  # Receiver
    SwitchCVQKD,
    PolarizationController,
    ThorlabsPDB,
):  # Detection

    name = "Homodyne detector CVQKD"

    power = ADC.power + LaserCVPPCL590.power + Computer.power
    power += SwitchCVQKD.power + PolarizationController.power + ThorlabsPDB.power

    fixed_energy = ADC.fixed_energy + LaserCVPPCL590.fixed_energy
    fixed_energy += Computer.fixed_energy + SwitchCVQKD.fixed_energy
    fixed_energy += PolarizationController.fixed_energy + ThorlabsPDB.fixed_energy

    DSP = ComputerDSP.DSP


class DetectorHomodyne2P(
    ADC,
    LaserCVPPCL590,
    Computer,
    ComputerDSP,  # Receiver
    SwitchCVQKD,
    PolarizationController,
    ThorlabsPDB,
):  # Detection

    name = "Homodyne detector CVQKD, double polarization"

    power = ADC.power + LaserCVPPCL590.power + Computer.power
    power += SwitchCVQKD.power + PolarizationController.power + 2 * ThorlabsPDB.power

    fixed_energy = ADC.fixed_energy + LaserCVPPCL590.fixed_energy
    fixed_energy += Computer.fixed_energy + SwitchCVQKD.fixed_energy
    fixed_energy += PolarizationController.fixed_energy + 2 * ThorlabsPDB.fixed_energy

    DSP = ComputerDSP.DSP


class DetectorHeterodyne1P(
    ADC,
    LaserCVPPCL590,
    Computer,
    ComputerDSP,  # Receiver
    SwitchCVQKD,
    PolarizationController,
    ThorlabsPDB,
):  # Detection

    name = "Heterodyne detector CVQKD"

    power = ADC.power + LaserCVPPCL590.power + Computer.power
    power += SwitchCVQKD.power + PolarizationController.power + 2 * ThorlabsPDB.power

    fixed_energy = ADC.fixed_energy + LaserCVPPCL590.fixed_energy
    fixed_energy += Computer.fixed_energy + SwitchCVQKD.fixed_energy
    fixed_energy += PolarizationController.fixed_energy + 2 * ThorlabsPDB.fixed_energy

    DSP = ComputerDSP.DSP


class DetectorHeterodyne2P(
    ADC,
    LaserCVPPCL590,
    Computer,
    ComputerDSP,  # Receiver
    SwitchCVQKD,
    PolarizationController,
    ThorlabsPDB,
):  # Detection

    name = "Heterodyne detector CVQKD, double polarization"

    power = ADC.power + LaserCVPPCL590.power + Computer.power
    power += SwitchCVQKD.power + PolarizationController.power + 4 * ThorlabsPDB.power

    fixed_energy = ADC.fixed_energy + LaserCVPPCL590.fixed_energy
    fixed_energy += Computer.fixed_energy + SwitchCVQKD.fixed_energy
    fixed_energy += PolarizationController.fixed_energy + 4 * ThorlabsPDB.fixed_energy

    DSP = ComputerDSP.DSP


class DetectorsCVCKA(
    ADC,
    LaserCVPPCL590,
    Computer,
    ComputerDSP,  # Receiver
    SwitchCVQKD,
    PolarizationController,
    ThorlabsPDB,
):

    name = "Detectors CVCKA"

    def power_n_users(self, number_users: int) -> float:
        power = number_users * (LaserCVPPCL590.power + SwitchCVQKD.power)
        power += number_users * (PolarizationController.power + ThorlabsPDB.power)
        power += (number_users // 4) * ADC.power + Computer.power
        return power

    def fixed_energy_n_users(self, number_users: int) -> float:
        fixed_energy = number_users * (
            LaserCVPPCL590.fixed_energy + SwitchCVQKD.fixed_energy
        )
        fixed_energy += number_users * (
            PolarizationController.fixed_energy + ThorlabsPDB.fixed_energy
        )
        fixed_energy += (number_users // 4) * ADC.fixed_energy + Computer.fixed_energy
        return fixed_energy

    def dsp_n_users(self, number_users: int) -> float:
        return number_users * ComputerDSP.DSP
