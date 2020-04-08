# Cowichan-River-Model
A model of nitrate transport in the Cowichan River (Final Project for CIVE-580)

This model was developed by Joseph Martin, Kelsey Shaw, and Andrew Freiburger for the course CIVE 580 - Contaminant Fate and Transport at the University of Victoria.

The model is built around to functions: a Kinematic Wave Function (KWE) which models the velocities in the river and an Advection Dispersion Reaction Function which models the transport and reaction of nitrate in the river.

The code in this repository is a Supplementary Material to the final report submitted on 7 Apr 20.

While the final report has been submitted for the purposes of the course, developement remains on going.

Current issues are:
- Unrealistically large velocities being computed (likely due to improper measurement of flow cross-sections)
- A large range of concentrations - including some large outliers 
- Quasi-instantaneous changes in concentration
