import numpy as np
import matplotlib.pyplot as plt

from qenergy import components as comp
from qenergy.experiments_dv import BB84Experiment


class MyDetector(comp.Detector):
    name = "My Detector"
    wavelength = 1550
    efficiency = 0.99
    dark_count = 100
    time_jitter = 0.5e-9
    power = 200
    fixed_energy = 0


laser = comp.LaserNKTkoheras1550()
mu = 0.1
sourcerate = 80e6
pcoupling = 0.9
wavelength = 1550
dist = np.arange(0, 100, 1)

other = [
    comp.MotorizedWavePlate(),
    comp.MotorizedWavePlate(),
    comp.Computer(),
    comp.Computer(),
    comp.SwitchIntensityModulator(),
    comp.TimeTagger(),
]

my_experiment = BB84Experiment(
    sourcerate, pcoupling, mu, wavelength, 0.01, laser, MyDetector(), dist, other
)

skr_time = my_experiment.time_skr(1e9)

energy = [my_experiment.total_energy(t) / 1e6 for t in skr_time]

plt.figure()
plt.plot(dist, energy, label="SNSPDs, QBER = 1\\%")

plt.xlabel("Distance [km]")
plt.ylabel("Energy consumption [MJ]")
