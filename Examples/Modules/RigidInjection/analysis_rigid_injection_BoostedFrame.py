#!/usr/bin/env python3

# Copyright 2019-2020 Luca Fedeli, Maxence Thevenet, Revathi Jambunathan
#
#
# This file is part of WarpX.
#
# License: BSD-3-Clause-LBNL


'''
Analysis script of a WarpX simulation of rigid injection in a boosted frame.

A Gaussian electron beam starts from -5 microns, propagates rigidly up to
20 microns after which it expands due to emittance only (the focal position is
20 microns). The beam width is measured after ~50 microns, and compared with
the theory (with a 5% error allowed).

The simulation runs in a boosted frame, and the analysis is done in the lab
frame, i.e., on the back-transformed diagnostics.
'''

import numpy as np
import read_raw_data
import yt

yt.funcs.mylog.setLevel(0)

# Read data from back-transformed diagnostics
snapshot = './lab_frame_data/snapshots/snapshot00001'
header   = './lab_frame_data/snapshots/Header'
allrd, info = read_raw_data.read_lab_snapshot(snapshot, header)
z = np.mean( read_raw_data.get_particle_field(snapshot, 'beam', 'z') )
w = np.std ( read_raw_data.get_particle_field(snapshot, 'beam', 'x') )

# initial parameters
z0 = 20.e-6
w0 = 1.e-6
theta0 = np.arcsin(0.1)

# Theoretical beam width after propagation if rigid ON
wth = np.sqrt( w0**2 + (z-z0)**2*theta0**2 )
error_rel = np.abs((w-wth)/wth)
tolerance_rel = 0.03

# Print error and assert small error
print("Beam position: " + str(z))
print("Beam width   : " + str(w))

print("error_rel    : " + str(error_rel))
print("tolerance_rel: " + str(tolerance_rel))

assert( error_rel < tolerance_rel )
