# Components

An experiment, or setup, is described by a protocol, and a list of components.

Any component inherits from the base {py:class}`~qenergy.components.base.Component`. Components are mainly defined, in this work, by a power (representing their instantaneous electrical power consumption), and an initialization energy (corresponding to the integrated power required for the initialization of the device). The measured value can also be saved.

Components will then have several other properties, depending on their type. For instance, {py:class}`~qenergy.components.detectors.Detector` will also include wavelength, efficiency, time jitter and dark counts. While all these parameters are not necessarily taken into account in this first analysis, they may be used in future versions.

In addition to detectors, lasers ({py:class}`~qenergy.components.lasers.Laser`) are defined by their frequency (repetition rate). The {py:class}`~qenergy.components.others.Fiber` is also a special component encompassing the distance dependent losses (also depending on the wavelength).