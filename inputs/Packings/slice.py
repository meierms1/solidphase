#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Generate Packed Spheres');
parser.add_argument('dir', help='directory')
parser.add_argument('-z', nargs='*', default=[0.0], type=float, help='Z offset')
args=parser.parse_args()

dir = args.dir

3d = open(dir+"/3d.xyzr")

for z in args.z:
    print(z)
