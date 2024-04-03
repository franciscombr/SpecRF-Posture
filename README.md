# SpecRF-Posture


## Description

This repository contains the source code for a data acquisition system developed to facilitate the collection of RF measurements for posture recognition research. The system includes two main components: an antenna position controller and a VNA interface. The antenna position controller, consisting of an Arduino Uno and a stepper motor driver, allows synchronous rotation of the antenna to predefined angular positions. On the other hand, the VNA interface, implemented as a Python class utilizing VISA, enables programmable control over the VNA for parameter selection, frequency sweep range configuration, and measurement data retrieval. The system is operated through a Python script that prompts the user to specify the desired posture and the number of angular sweeps. It then iterates over the specified angles, moving the antenna to each position, triggering the VNA to take measurements, and storing the results in CSV files. This system aims to streamline the data acquisition process for posture recognition experiments, enhancing efficiency and reproducibility.

## Acknowledgments
The work was supported by the European Union’s Horizon Europe Re-search and Innovation Program (Project Converge—Telecommunications and Computer Vision Convergence Tools for Research Infrastructures) under Grant 101094831.

More information regarding this project can be found [here](https://converge-project.eu/).

## Authors
| Description | Test Text     |
|    :----:   |    :----:     |
|Mariana Oliveira | mariana.s.fonseca@inesctec.pt|
|Francisco Ribeiro | francisco.m.ribeiro@inesctec.pt |
|Nuno Paulino | nuno.m.paulino@inesctec.pt |
|Okan Yurduseven | okan.yurduseven@qub.ac.uk |
|Luís Pessoa | luis.m.pessoa@inesctec.pt|

## License
This work is made available under a Creative Commons Attribution-NonCommercial 4.0 International License. You can view additional details on [this page](https://creativecommons.org/licenses/by-nc/4.0/).
