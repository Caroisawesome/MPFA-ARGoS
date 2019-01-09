import pdb
import matplotlib.pyplot as plt
import glob
import os.path
import numpy as np
from pylab import *

def sub_gen_coord(max_x,min_x, k):
    x1 = max_x - k/2.0
    y1 = max_y - k/2.0
    coordinates =[]
    for i in range(int(max_x - min_x)/k):
        for j in range(int(max_x - min_x)/k):
            x = x1 -k*i  
            y = y1 -k*j
            coordinates.append([x, y])
    #print coordinates
    return coordinates

arena_width = 81

max_x, max_y = arena_width/2,  arena_width/2;
min_x, min_y = -max_x, -max_y;

gaps = [9]
results=[]
for k in gaps:
  print k
  results.append(sub_gen_coord(max_x, min_x, k))
  

coord_info =open("coord_for_worldFile.xml", "w")
coord_info_text = open("coord.xml", "w")
count =1;
for coords in results:
    for xy in coords:
        coord_info.write("NestPosition_" + str(count) +"=\"" + str(xy[0]) + ", " + str(xy[1])+"\"\n") 
        coord_info_text.write(str(xy[0]) + " " + str(xy[1])+"\n") 
        count += 1  

coord_info_text.close()


# there is only delivering robots
count =0;

total_robot=0

num_Drobot = 5
unit = np.sqrt(2*((gaps[-1]/2.0)**2))
for coords in results[:-1]:
    for xy in coords:
        distance = np.sqrt(xy[0]**2 + xy[1]**2)
        print "distance=", distance
        print "unit=", unit
        print round(distance/unit)
        quantity = num_Drobot*round(distance/unit);
        print "quantity", quantity
        total_robot += quantity
	    
        coord_info.write("<distribute>\n")
        coord_info.write("<position max=\"" + str(xy[0]+0.08*quantity)+ ", " + str(xy[1]+0.08*quantity) + ", 0.0\" method=\"uniform\" min=\"" + str(xy[0])+ ", " + str(xy[1]) + ", 0.0\"/>\n")
        coord_info.write("<orientation mean=\"0, 0, 0\" method=\"gaussian\" std_dev=\"360, 0, 0\"/>\n")
        coord_info.write("<entity max_trials=\"100\" quantity=\""  + str(int(quantity))  +  "\">\n")
        coord_info.write("<foot-bot id=\"D" + str(count)+ "-" + "\"><controller config=\"MPFA\"/></foot-bot>\n")
        coord_info.write("</entity>\n")
        coord_info.write("</distribute>\n\n")
        count += 1  
        
# there are foraging and delivering robots in each region
for xy in results[-1]:
    coord_info.write("<distribute>\n")
    coord_info.write("<position max=\"" + str(xy[0])+ ", " + str(xy[1]) + ", 0.0\" method=\"uniform\" min=\"" + str(xy[0]-0.5)+ ", " + str(xy[1]-0.5) + ", 0.0\"/>\n")
    coord_info.write("<orientation mean=\"0, 0, 0\" method=\"gaussian\" std_dev=\"360, 0, 0\"/>\n")
    coord_info.write("<entity max_trials=\"100\" quantity=\"4\">\n")
    coord_info.write("<foot-bot id=\"F" + str(count)+ "-" + "\"><controller config=\"MPFA\"/></foot-bot>\n")
    coord_info.write("</entity>\n")
    coord_info.write("</distribute>\n\n")
 
    #total_robot += 4
    
    print "nest location =[",xy[0],", ",xy[1], "]"
    distance = np.sqrt(xy[0]**2 + xy[1]**2)
    print "distance=", distance
    print "unit=", unit
    print round(distance/unit)
    quantity = num_Drobot*round(distance/unit);
    print "quantity", quantity
    total_robot += quantity
    
    coord_info.write("<distribute>\n")
    coord_info.write("<position max=\"" + str(xy[0]+0.08*quantity)+ ", " + str(xy[1]+0.08*quantity) + ", 0.0\" method=\"uniform\" min=\"" + str(xy[0])+ ", " + str(xy[1]) + ", 0.0\"/>\n")
    coord_info.write("<orientation mean=\"0, 0, 0\" method=\"gaussian\" std_dev=\"360, 0, 0\"/>\n")
    coord_info.write("<entity max_trials=\"100\" quantity=\""  + str(int(quantity))  +  "\">\n")
    coord_info.write("<foot-bot id=\"D" + str(count)+ "-" + "\"><controller config=\"MPFA\"/></foot-bot>\n")
    coord_info.write("</entity>\n")
    coord_info.write("</distribute>\n\n")
    count += 1  
    
coord_info.close() 

print 'total delivering robot=', total_robot

