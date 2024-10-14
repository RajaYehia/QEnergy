# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the influence of detector choice on the energetic cost.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import BB84Experiment

from studies import FIGSIZE_HALF, EXPORT_DIR

dist = [d for d in range(200)]
wavelength = 1550
gigabit = 1e9

##Source
laser = comp.LaserNKTkoheras1550()
mu = 0.1
sourcerate = 80 * 10**6
pcoupling = 0.9

# Detector
detectorsnspd = comp.DetectorSNSPD1550()
detectoringaas = comp.DetectorInGAs1550()

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
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, detectorsnspd, dist, other
)
Experiment02 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, detectoringaas, dist, other
)
Experiment03 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.05, laser, detectoringaas, dist, other
)

tskr = Experiment01.time_skr(gigabit)
tskr2 = Experiment02.time_skr(gigabit)
tskr3 = Experiment03.time_skr(gigabit)

Energysnspd = [Experiment01.total_energy(t) / 1000000 for t in tskr]
Energyingaas = [Experiment02.total_energy(t) / 1000000 for t in tskr2]
Energyingaas2 = [Experiment03.total_energy(t) / 1000000 for t in tskr3]


fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
ax.plot(dist, Energysnspd, label="SNSPDs, QBER = 1\\%")
ax.plot(dist, Energyingaas, label="APDs, QBER = 1\\%")
ax.plot(dist, Energyingaas2, label="APDs, QBER = 5\\%")

# plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")
ax.set_ylim(-100, 4000)
fig.savefig(EXPORT_DIR / "BB84detectstudy.pdf", format="pdf")
plt.show()
