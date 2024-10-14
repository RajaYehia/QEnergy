# Quickstart

## Studies

The plots presented in the paper can be generated from the scripts in `studies`. The `make all` command regenerates all the plots in the export folder.

## Test your own hardware

One of the goal of QEnergy is for users to investigate the cost of quantum communication protocols with their own hardware. Say for instance, that you have another way of performing the detection, then it is possible to define a new Component:

```{eval-rst}
.. plot:: pyplots/quickstart_hardware.py
    :include-source: true
    :align: center
```