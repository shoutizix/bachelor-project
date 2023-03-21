# Bachelor Project

[![License](https://img.shields.io/badge/license-MIT-green)](/LICENSE.md)

## Description

Semester project realized for the [SSA](https://www.epfl.ch/education/educational-initiatives/discovery-learning-program-2/interdisciplinary-projects/epfl-space-situational-awareness-team/) (Space Situational Awareness) association at EPFL.

The purpose of this project is to extract the intensity along the satellite streaks that can be
found in images that were obtained by OMEGACAM on the VLT Survey Telescope. In
this project, we only analyzed the long tracks that were created by high velocity objects,
to try to get an estimation about their rotation. We used Fourier transform to get the
periodicity of the intensity along the tracks. Due to the lack of real data about rotation, we
first had to create fake streaks with sinusoid intensity and different angles. We manually
got the tracks to run the code on them, so ideally this project should be integrated with
[DetectSat](https://github.com/YBouquet/detectsat) so that all the process can be done automatically

## Acknowledgement

The code of DetectSat was originally developped by [Yann Bouquet](https://github.com/YBouquet)

## License

Distributed under the [MIT License](/LICENSE.md)
