# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Study of the power consumption contributions for the different setups (Bb84, E91, MDI, CV).
"""

import matplotlib.pyplot as plt
from qenergy import components as comp

from studies import EXPORT_DIR, BASE_TEXTWIDTH_IN

FONTSIZE = 9.5


def order(input_dict, total_sum):
    other = 0
    elems = []
    powers = []
    for elem, power in input_dict.items():
        if power / total_sum < 0.05:
            other += power
        else:
            elems.append(elem)
            powers.append(power)

    sorted_elems = [x for _, x in sorted(zip(powers, elems), reverse=True)]
    sorted_elems += ["Other"]
    sorted_power = list(sorted(powers, reverse=True)) + [other]
    return sorted_elems, sorted_power
    # return zip(
    #     *dict(
    #         sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    #     ).items()
    # )


cmap = plt.colormaps["tab20c"]
colors_source = [1, 2, 3, 4]
colors_detection = [5, 6, 7, 8]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
    2, 2, figsize=(BASE_TEXTWIDTH_IN, BASE_TEXTWIDTH_IN)
)

# BB84

source = {
    "Laser": comp.LaserNKTkoheras1550.power,
    "Waveplate": comp.MotorizedWavePlate.power,
    "Computer": comp.Computer.power,
    "IM": comp.SwitchIntensityModulator.power,
}
detection = {
    "Detectors": comp.DetectorSNSPD1550.power,
    "Waveplate": comp.MotorizedWavePlate.power,
    "Computer": comp.Computer.power,
    "Time tagger": comp.TimeTagger.power,
}
total_sum = sum(source.values()) + sum(detection.values())

(labels_source, sizes_source) = order(source, total_sum)

(labels_detection, sizes_detection) = order(detection, total_sum)

# explode = [0] * len(sizes_source) + [0.1] * len(sizes_detection)
# hatch = [""] * len(sizes_source) + ["//"] * len(sizes_detection)
colors = cmap(
    colors_source[: len(sizes_source)] + colors_detection[: len(sizes_detection)]
)
sizes = sizes_source + sizes_detection
labels = labels_source + labels_detection
ax1.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    # explode=explode,
    # hatch=hatch,
    startangle=90,
    colors=colors,
    textprops={"fontsize": FONTSIZE},
)

ax1.set_title("BB84", fontsize=11)

# E91

source = {"Laser": comp.LaserMira780Pulsed.power, "Oven": comp.Oven.power}
detection = {
    "Waveplate": 2 * comp.MotorizedWavePlate.power,
    "Computers": 2 * comp.Computer.power,
    "Time taggers": 2 * comp.TimeTagger.power,
    "Detectors": 2 * comp.DetectorSNSPD1550.power,
}

total_sum = sum(source.values()) + sum(detection.values())

(labels_source, sizes_source) = order(source, total_sum)

(labels_detection, sizes_detection) = order(detection, total_sum)

# explode = [0] * len(sizes_source) + [0.1] * len(sizes_detection)
# hatch = [""] * len(sizes_source) + ["//"] * len(sizes_detection)
colors = cmap(
    colors_source[: len(sizes_source)] + colors_detection[: len(sizes_detection)]
)
sizes = sizes_source + sizes_detection
labels = labels_source + labels_detection
ax2.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    # explode=explode,
    # hatch=hatch,
    startangle=90,
    colors=colors,
    textprops={"fontsize": FONTSIZE},
)

ax2.set_title("E91", fontsize=11)

# MDI

source = {
    "Lasers": 2 * comp.LaserNKTkoheras1550.power,
    "Waveplates": 2 * comp.MotorizedWavePlate.power,
    "Computers": 2 * comp.Computer.power,
    "IM": comp.SwitchIntensityModulator.power,
}  # Add intensity modulator ??
detection = {
    "Detectors": comp.DetectorSNSPD1550.power,
    "Time taggecomp.r": comp.TimeTagger.power,
}  # Add detector ?

total_sum = sum(source.values()) + sum(detection.values())

(labels_source, sizes_source) = order(source, total_sum)

(labels_detection, sizes_detection) = order(detection, total_sum)

# explode = [0] * len(sizes_source) + [0.1] * len(sizes_detection)
# hatch = [""] * len(sizes_source) + ["//"] * len(sizes_detection)
colors = cmap(
    colors_source[: len(sizes_source)] + colors_detection[: len(sizes_detection)]
)

sizes = sizes_source + sizes_detection
labels = labels_source + labels_detection
ax3.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    # explode=explode,
    # hatch=hatch,
    startangle=90,
    colors=colors,
    textprops={"fontsize": FONTSIZE},
)

ax3.set_title("MDI", fontsize=11)

# CV-QKD
## Assuming 2Q, 1P

source = {
    "Laser": comp.LaserCVPPCL590.power,
    "MBC": comp.MBC.power,
    "DAC": comp.DAC.power,
    "PM": comp.ThorlabsPowerMeter.power,
    "Computer": comp.Computer.power,
}
detection = {
    "ADC": comp.ADC.power,
    "Laser": comp.LaserCVPPCL590.power,
    "Computer": comp.Computer.power,
    "Switch": comp.SwitchCVQKD.power,
    "PC": comp.PolarizationController.power,
    "BHD": 2 * comp.ThorlabsPDB.power,
}

total_sum = sum(source.values()) + sum(detection.values())


(labels_source, sizes_source) = order(source, total_sum)

(labels_detection, sizes_detection) = order(detection, total_sum)

# explode = [0] * len(sizes_source) + [0.1] * len(sizes_detection)
# hatch = [""] * len(sizes_source) + ["//"] * len(sizes_detection)
colors = cmap(
    colors_source[: len(sizes_source)] + colors_detection[: len(sizes_detection)]
)
sizes = sizes_source + sizes_detection
labels = labels_source + labels_detection
ax4.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    # explode=explode,
    # hatch=hatch,
    startangle=90,
    colors=colors,
    textprops={"fontsize": FONTSIZE},
)

ax4.set_title("CV-QKD", fontsize=11)
plt.show()
fig.tight_layout()
# fig.set_figwidth(BASE_TEXTWIDTH_IN)
fig.savefig(EXPORT_DIR / "piecharts.pdf", format="pdf")
