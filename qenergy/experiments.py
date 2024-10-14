# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Defines the base experiment object.
"""

from typing import List

from qenergy.components import Component


class Experiment:
    """
    Base experiment.

    All experiments have a list of components that can be used to derive the consummed power.
    """

    list_components: List[Component]  #: List of components of the experiment.

    def total_energy(self, time: float) -> float:
        """
        Returns the total energy required to run the experiment for a time t.

        Args:
            time (float): duration of the experiment.

        Returns:
            float: total energy to run the experiment for a time t.
        """
        tot = 0
        for component in self.list_components:
            tot += component.power * time + component.fixed_energy
        return tot

    def total_energy_measured(self, time: float) -> float:
        """
        Returns the total energy to run the experiment for a time t
        based on the measured values of the components.

        Args:
            time (float): duration of the experiment.

        Returns:
            float: total energy to run the experiment for a time t based on the measured values.
        """
        tot = 0
        for component in self.list_components:
            tot += component.total_energy_measured(time)
        return tot

    def power(self) -> float:
        """
        Returns the total power consummed by all the components of the setup.

        Returns:
            float: total consummed power by all the components.
        """
        tot = 0
        for component in self.list_components:
            tot += component.power
        return tot
