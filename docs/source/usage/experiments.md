# Experiments

An experiment class corresponding to a protocol, and takes, as an input, a list of components. The list of components and the protocol is a step (or experiment) and is represented by an instantiated class.

Currently, a few experiments are available in QEnergy: {py:class}`~qenergy.experiments_dv.BB84Experiment`, {py:class}`~qenergy.experiments_dv.EntanglementBasedExperiment`, {py:class}`~qenergy.experiments_dv.MDIQKDExperiment`, {py:class}`~qenergy.experiments_dv.GHZsharing`, {py:class}`~qenergy.experiments_cv.CVQKDProtocol`, {py:class}`~qenergy.experiments_cv.CKAExperiment`. They all inherit from {py:class}`~qenergy.experiments.Experiment`.

Usually they define a {py:func}`time_skr` method, that returns the time that is required to obtain the objective number of secret bits passed as a parameter. Combined with the {py:func}`~qenergy.experiments.Experiment.total_energy` base method of all experiments, that returns the energy required to run the protocol for a time passed as a parameter, this allows to derive the energy required to run the protocol to achieve a certain objective task.