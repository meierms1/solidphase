#!/usr/bin/env python3
import sys
import os
import openmc
settings = openmc.Settings()
settings.verbosity = 10
from numpy import *
import pylab
import argparse
import simba
import uuid
import datetime

parser = argparse.ArgumentParser(description='Generate Packed Spheres');
parser.add_argument('--radius', default=0.0075, type=float, help='Radius')
parser.add_argument('--pf', default=0.3, type=float, help='Packing Factor')
parser.add_argument('--seed', default=1, type=int, help='Randomization seed')
args=parser.parse_args()

geometry_prob_lo = [0.0, 0.0, 0.0]
geometry_prob_hi = [0.08, 0.05, 0.05]


db = simba.open()
table = db.addTable('Packings')
ct = datetime.datetime.now()

record = dict()
record['HASH'] = str(uuid.uuid4())
file_name = str(ct.timestamp())
record['DIR'] = "Packings/" + file_name
record['Time'] = str(ct)
os.mkdir("../" + record['DIR'])
record['radius'] = args.radius
record['packing_factor'] = args.pf
record['geometry_prob_lo'] = str(geometry_prob_lo)
record['geometry_prob_hi'] = str(geometry_prob_hi)
record['input'] = ''.join(open('pack.py','r').readlines())
record['args'] = str(args)
record['seed'] = args.seed
table.update(record)


radius = args.radius
packing_factor = args.pf

min_x = openmc.XPlane(x0=geometry_prob_lo[0], boundary_type='reflective')
max_x = openmc.XPlane(x0=geometry_prob_hi[0], boundary_type='reflective')
min_y = openmc.YPlane(y0=geometry_prob_lo[1], boundary_type='reflective')
max_y = openmc.YPlane(y0=geometry_prob_hi[1], boundary_type='reflective')
min_z = openmc.ZPlane(z0=geometry_prob_lo[2], boundary_type='reflective')
max_z = openmc.ZPlane(z0=geometry_prob_hi[2], boundary_type='reflective')
region = +min_x & -max_x & +min_y & -max_y  & +min_z & -max_z

print("radius",radius)
print(geometry_prob_lo,geometry_prob_hi)
print("packing factor",packing_factor)
print("folder name: " + file_name )
result = openmc.model.pack_spheres(radius, region, pf=packing_factor,seed=args.seed)
print(len(result),"spheres")
print(result)


circ = linspace(0,2*pi)
f2d = open("../" + record['DIR'] + "/2d_z0.000.xyzr".format(packing_factor),"w")
f3d = open("../" + record['DIR'] + "/3d.xyzr".format(packing_factor),"w")
fig = pylab.figure()
ax=fig.add_subplot()
ax.set_aspect(1)
vol_sph = 0.0
for x0 in result:
    x = x0[0]
    y = x0[1]
    z = x0[2]
    f3d.write("{} {} {} {}\n".format(x,y,z,radius));

    if abs(z) > radius: continue
    
    reff = sqrt(abs(radius**2 - z**2))

    vol_sph = vol_sph + pi*reff**2
    
    f2d.write("{} {} {} {}\n".format(x,y,z,reff))

    ax.plot(x+reff*cos(circ),y+reff*sin(circ))

fig.savefig("../" + record['DIR']+"/thumbnail.png")
f2d.close()
f3d.close()


vol = (geometry_prob_hi[1]-geometry_prob_lo[1])*(geometry_prob_hi[0]-geometry_prob_lo[0])

vol_frac = vol_sph / vol
print(vol_frac)
record['vol_frac'] = vol_frac


table.update(record)
