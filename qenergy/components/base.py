# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Defines base classes for components.
"""


class Component:
    """
    A generic component.
    """

    name = "component"  #: Name of the component.
    fixed_energy = 0  #: Fixed energy required for setting this object before using it.
    fixed_energy_meas = 0  #: Fixed energy measured in the lab.
    power = 0  #: Power consumed by the component when being used.
    meas_power = 0  #: Power consumption measured in the lab.
    T = 1  #: Photon transmission efficiency of this component (1 - loss of a photon).
    qber = 0  #: single qubit error rate induced by the component..

    def __repr__(self):
        return f"({self.name}: E= {self.fixed_energy}J, P= {self.power}W)"

    def total_energy(self, time: float) -> float:
        """
        Return the total energy spent for a given time.

        Args:
            time (float): time in seconds.

        Returns:
            float: total energy fixed_energy + power*t.
        """
        return self.fixed_energy + time * self.power

    def total_energy_measured(self, time: float) -> float:
        """
        Return the total energy spent for a given time, based on measured power.

        If the measured power is 0, falls back on the datasheet values.

        Args:
            time (float): time in seconds.

        Returns:
            float: total energy fixed_energy_measured + measured_power*t.
        """
        energy = 0
        if self.meas_power == 0:
            energy = self.fixed_energy + time * self.power
        else:
            energy = self.fixed_energy_meas + time * self.meas_power
        return energy


class PassiveComponent(Component):
    """
    Generic passive component.
    """

    name = "passive component"


class ActiveComponent(Component):
    """
    Generic active component.
    """

    name = "active component"
