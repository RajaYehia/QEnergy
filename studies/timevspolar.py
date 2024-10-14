# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the difference in energetic consumption between time and polarization.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import BB84Experiment

from studies import FIGSIZE_FULL, EXPORT_DIR

dist = [d for d in range(100)]
gigabit = 1e9
pcoupling = 0.9
sourcerate = 80 * 10**6
mu = 0.1
QBER = 0.01

##1550nm setup
wavelength = 1550
laser = comp.LaserNKTkoheras1550()
detector = comp.DetectorSNSPD1550()


# Other components
otherpolar = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]
othertime = [
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.StabilizationTimeBin(),
    comp.TimeTagger(),
]

Experiment01 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, QBER, laser, detector, dist, otherpolar
)
Experiment02 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, QBER, laser, detector, dist, othertime
)


tskr = Experiment01.time_skr(gigabit)
tskr2 = Experiment02.time_skr(gigabit)

Energypolar = [Experiment01.total_energy(t) / 1000000 for t in tskr]
Energytimebin = [Experiment02.total_energy(t) / 1000000 for t in tskr2]


fig, ax = plt.subplots(1, figsize=FIGSIZE_FULL)
plt.plot(dist, Energypolar, label="Polarization encoding")
plt.plot(dist, Energytimebin, label="Time-bin encoding")

# plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")
fig.savefig(EXPORT_DIR / "timebinstudy.pdf", format="pdf")
plt.show()
