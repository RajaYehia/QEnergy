# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the energetic cost of CV-CKA.
"""

import matplotlib.pyplot as plt
from qenergy import components as comp
from qenergy.experiments_cv import CKAProtocol

from studies import FIGSIZE_HALF, EXPORT_DIR


# Parameters of the plot
dist_CKA = [d / 2000 for d in range(1100)]  # Points of the plot
gigabit = 1e9  # Target number of secret bits
MJ = 1e6  # Change of scale to megajoules

# Parameters of the implementation
eta = 0.7  # Detector efficiency
Vel = 0.005  # Electrical noise
beta = 0.95  # Information reconciliation efficiency for CKA
sourcerate = 1e8  # Laser frequency
source = comp.SourceCKA()  # Source (same for all users)
detector = comp.DetectorsCVCKA()  # Detector (depends on the no. of users mod.4)
xi = 0.005  # Excess noise


Nusers = [i for i in range(3, 7)]  # No. of parties involved in the scheme

fig, ax = plt.subplots(1, figsize=FIGSIZE_HALF)

# Loop of the experiments according to the no. of users
for N in Nusers:
    Experiment_CKA = CKAProtocol(
        eta, Vel, beta, N, sourcerate, source, detector, xi, dist_CKA
    )
    tsk_CKA = Experiment_CKA.time_skr(gigabit)
    Energy_CKA = [Experiment_CKA.total_energy(t) / MJ for t in tsk_CKA]
    plt.plot(dist_CKA, Energy_CKA, label=f"{N} users")


ax.set(xlabel="Distance [km]", ylabel="Energy consumption [MJ]")
ax.tick_params(axis="both", which="major")
ax.legend(loc="upper left")
ax.set_title("$N_{\\rm target} = 1$ GBit")
plt.ylim(0, 20)
plt.savefig(EXPORT_DIR / "CVCKAstudy.pdf", format="pdf")
plt.show()
