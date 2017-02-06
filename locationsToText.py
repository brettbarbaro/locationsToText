# -*- coding: utf-8 -*-
"""
locationsToText
Created on Monday, September 5, 2016 at 11:54 PM

@author: brett barbaro, ludovic autin


Built from NC_and_Gags_to_pointcloud

Will create a text file with locations and rotations of objects for import into Tomosimu

"""
import numpy as np
import upy
from autopack import transformation
import os
#
helperClass = upy.getHelperClass()
helper = helperClass()
#
##import datetime   # optional for timestamp if desired
##current_time = datetime.datetime.strftime(datetime.datetime.now(), '%H.%M.%S')
#    
#    #def __init__(self):  # if there are no initial values to assign, this def can be omitted
#        #return None
#        

def getLocations(objects): #objects is the string identifying the parent of the sphere objects in C4D
    """Gets the positions of the properly placed locations.
    
    input - the string identifying the parent of the sphere objects in C4D
    output - an array containing the positions of the locations in the parent

    """
    #get_points
    parent = helper.getObject(objects)
    childs = helper.getChilds(parent)
     
    #in C4D position is allpos[c4d.ID_BASEOBJECT_REL_POSITION]
    #C4D is left hand
    #getTranslation in helper return the C4D vector
    #ToVec from helper convert c4D vector to regular vector right handed
    for ch in childs:
        all_pos = [helper.ToVec(helper.getTranslation(ch)) for ch in childs]
        rotations = [helper.getPropertyObject(ch, key='rotation') for ch in childs]

    return [all_pos, rotations]

locations = getLocations("Meshs_ext__1BXR")

# print locations[1][0][0]

pdbs = ['1BXR','1A1S','ENV'] #1BXR','1A1S','1EQR','1GYT','1KYI','1VPX','1W6T','2AWB','2BYU','2GLS','2IDB','3DY4','1BXR','1F1B','1KP8','1QO1','1VRG','1YG6','2BO9','2GHO','2H12','2REC'};
numbers = [0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# 2 possibilities:
#
#  1. make list of proteins first, then index with numbers.
#  2. include protein name for every entry in output.
#  
# option 1 will result in smaller file sizes and be faster
# option 2 will result in a larger, more comprehensible output file
# Currently using option 2. 
# later on, maybe try measuring speed to see if it really makes a difference

#print locations
#print pdbs

output = open("/Users/Brett/FELLOWSHIP/tomosimu_sandbox/workspace/output.txt","w")

for x in range(len(locations[0])):
    matrix = np.ndarray.tolist(locations[1][x][0])
    number=numbers[x]
    output.write(str(
                    pdbs[number] + str(',   ') +
                    str(locations[0][x][0] / 10) + str(', ') + #cellPACK is in Angstrom, but tomosimu is in nm. So this adjustment must be made.
                    str(locations[0][x][1] / 10) + str(', ') + 
                    str(locations[0][x][2] / 10) + str(',   ') +
                    str(matrix[0][0]) + str(',') + 
                    str(matrix[0][1]) + str(',') + 
                    str(matrix[0][2]) + str(',') + 
                    str(matrix[1][0]) + str(',') + 
                    str(matrix[1][1]) + str(',') + 
                    str(matrix[1][2]) + str(',') + 
                    str(matrix[2][0]) + str(',') + 
                    str(matrix[2][1]) + str(',') + 
                    str(matrix[2][2]) + '\n'
                    ))

output.close()

#transformations = mytools.get_transformations("Meshs_ext__DNA_GYRASE")
#print transformations
#
##make_points
#newpoints=[]
#for trans in transformations:
#    newpoints.extend(helper.ApplyMatrix(locations,trans)) #cannot be all put on one line because that only works with append
#
#
#print newpoints
#outfile="/Users/Brett/Dev/CSVTORECIPE/locations"
#np.save(outfile,newpoints)
#np.savetxt(outfile+".txt",newpoints,delimiter=',')
#pointscloud, mesh_pts = helper.PointCloudObject("pts_cloud",vertices=newpoints) 

