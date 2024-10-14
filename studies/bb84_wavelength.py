# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the influence of wavelength on the enegertic consumption of BB84.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_dv import BB84Experiment

from studies import FIGSIZE_HALF, EXPORT_DIR

dist = [d / 100 for d in range(1000)]
gigabit = 1e9
pcoupling = 0.9
sourcerate = 80 * 10**6
mu = 0.1
QBER = 0.01

##1550nm setup
wavelength1550 = 1550
laser1550 = comp.LaserNKTkoheras1550()
detectorsnspd = comp.DetectorSNSPD1550()
detectorapd = comp.DetectorInGAs1550()

## 780nm setup
wavelength780 = 780
laser780 = comp.LaserMira780Pulsed()
detector780 = comp.DetectorSiAPD780()

# 523nm setup
wavelength523 = 523
laser523 = comp.LaserVerdiC532()
detector523 = comp.Detector523()


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
    sourcerate,
    pcoupling,
    mu,
    wavelength1550,
    QBER,
    laser1550,
    detectorsnspd,
    dist,
    other,
)
Experiment015 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength1550, QBER, laser1550, detectorapd, dist, other
)
Experiment02 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength780, QBER, laser780, detector780, dist, other
)
Experiment03 = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength523, QBER, laser523, detector523, dist, other
)

tskr = Experiment01.time_skr(gigabit)
tskr2 = Experiment02.time_skr(gigabit)
tskr3 = Experiment03.time_skr(gigabit)
tskr4 = Experiment015.time_skr(gigabit)

Energy1550snspd = [Experiment01.total_energy(t) / 1000000 for t in tskr]
Energy1550apd = [Experiment015.total_energy(t) / 1000000 for t in tskr4]
Energy780 = [Experiment02.total_energy(t) / 1000000 for t in tskr2]
Energy523 = [Experiment03.total_energy(t) / 1000000 for t in tskr3]


fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)
ax.plot(dist, Energy1550snspd, label="$\\lambda=1550$nm, SNSPDs")
ax.plot(dist, Energy1550apd, label="$\\lambda=1550$nm, APDs")
ax.plot(dist, Energy780, label="$\\lambda=780$nm, APDs")
ax.plot(dist, Energy523, label="$\\lambda=523$nm, APDs")

plt.yscale("log")
ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.set_title("$N_{\\rm target} = 1$ GBit")
ax.set_ylim(top=10**8)
ax.legend(loc="upper right")
fig.savefig(EXPORT_DIR / "BB84wavelengthstudy.pdf", format="pdf")
plt.show()
