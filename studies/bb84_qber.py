# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the influence of QBER on the energetic consumption of BB84.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import BB84Experiment

from studies import FIGSIZE_HALF, EXPORT_DIR

dist = [d for d in range(100)]
wavelength = 1550
gigabit = 1e9

##Source
laser = comp.LaserNKTkoheras1550()
mu = 0.1
sourcerate = 80 * 10**6
pcoupling = 0.9

# Detector
detector = comp.DetectorSNSPD1550()

# Other components
other = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]

Experiment01 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, detector, dist, other
)
Experiment02 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.02, laser, detector, dist, other
)
Experiment03 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.04, laser, detector, dist, other
)
Experiment04 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.06, laser, detector, dist, other
)
Experiment05 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.08, laser, detector, dist, other
)
Experiment06 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.1, laser, detector, dist, other
)

tskr = Experiment01.time_skr(gigabit)
tskr2 = Experiment02.time_skr(gigabit)
tskr3 = Experiment03.time_skr(gigabit)
tskr4 = Experiment04.time_skr(gigabit)
tskr5 = Experiment05.time_skr(gigabit)
tskr6 = Experiment06.time_skr(gigabit)


Energyskr = [Experiment01.total_energy(t) / 1000000 for t in tskr]
Energyskr2 = [Experiment02.total_energy(t) / 1000000 for t in tskr2]
Energyskr3 = [Experiment03.total_energy(t) / 1000000 for t in tskr3]
Energyskr4 = [Experiment04.total_energy(t) / 1000000 for t in tskr4]
Energyskr5 = [Experiment05.total_energy(t) / 1000000 for t in tskr5]
Energyskr6 = [Experiment06.total_energy(t) / 1000000 for t in tskr6]


fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
ax.plot(dist, Energyskr, label="1\\%")
ax.plot(dist, Energyskr2, label="2\\%")
ax.plot(dist, Energyskr3, label="4\\%")
ax.plot(dist, Energyskr4, label="6\\%")
ax.plot(dist, Energyskr5, label="8\\%")
ax.plot(dist, Energyskr6, label="10\\%")
# plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left", title="QBER", ncols=2)
ax.set_title("$N_{\\rm target} = 1$ GBit")

fig.savefig(EXPORT_DIR / "BB84QBERstudy.pdf", format="pdf")
plt.show()
