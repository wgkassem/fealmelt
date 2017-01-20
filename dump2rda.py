"""
This program will read dump files generated by an MD simulation and will calculate the
radial distribution function for Al, Fe, and Al-Fe
"""

import sys
import os
import glob
import numpy as np
from argparse import ArgumentParser
import decimal

class atom:
    def __init__(self,id,type,coords):
        self.id = id
        self.type = type
        self.coords = list(coords)

class dump:
    def __init__(self,ids,types,coords,box):
        self.atoms = []
        for i in range(len(ids)):
            self.atoms.append(atom(ids[i],types[i],coords[i]))
        self.box = list(box)

    def calc_rdf(self,nbins,rmax):
        dr = rmax/nbins
        r = [dr*x for tmp in range(nbins)]
        
        
    

pers = ArgumentParser()
pers.add_argument(fin, help="Filename motif containing wildcard *")
pers.add_argument("--average", help="Number of files to average", type=int, default=1)
pers.add_argument("--dt", help="timestep in ps", type=float, default=1)
pers.add_argument("--out", "-o", help="output file")
pers.add_argument("--bins", "-b", help="number of bins", type=int, default=100)

args = pers.parse_args()

### sort filename list by filename key
iwild = args.fin.find("*")
if iwild == -1:
    print("Warning: ONLY ONE FILE SPECIFIED")
    args.range = [0,1,1]
    keys = [args.fin]
else:    
    flist = glob.glob(args.fin) #list of filenames
    print("... %1.0d files found"%(len(flist)))
    print(iwild+1)
    if iwild+1==len(args.fin): iend = None
    else: iend = s.find(args.fin[iwild+1:])
    keys = [int( s[iwild:iend] ) for s in flist]
    keys.sort()
    flist = sorted(flist, key=lambda s: int( s[iwild:iend] ))

### process
nfiles = len(flist)
ids = [-1]*nfiles
types = [-1]*nfiles
coords = [[NaN,NaN,NaN]]*nfiles
box = []

for fname in flist:
    ff = open(fname)
    natoms = 0
    tdump = -1
    iatom = -1
    while True:
        if iatom == natoms: break
        line = ff.readline().strip().split()
        
        if line[1] == "TIMESTEP":
            tdump = float(ff.readline().strip())*args.dt
            continue
        
        if line[1] == "NUMBER":
            natoms = int(ff.readline().strip())
            continue
        
        if line[1] == "BOX":
            for i in range(3):
                line = ff.readline().strip().split()
                box.append([float(x) for x in line])
            continue
        
        if line[1] == "ATOMS":
            c_id = line.index("id")-2
            c_type = line.index("type")-2
            c_x = line.index("x")-2
            c_y = line.index("y")-2
            c_z = line.index("z")-2
            
            for i in range(natoms):
                line = ff.readline().strip().split()
                ids[i] = int(line[c_id])
                types[i] = int(line[c_type])
                coords[i][0]=float(line[c_x]); coords[i][1]=float(line[c_y])
                coords[i][2]=float(line[c_z])
                iatom += 1

            continue

    print("   +++ read file %s, %i atoms, %f time"%(fname,natoms,tdump))
    d = dump(ids,types,coords,box)
    
                
    
    
