# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:59:58 2024

@author: 12434
"""

import nazca as nd
import numpy as np
import nazca.geometries as geom
from nazca.interconnects import Interconnect
#import nazca.demofab as demo



nd.clear_all()


nd.add_layer2xsection(xsection='Wg', layer=1, accuracy=0.001) # Define the layer, the accuracy = 1nm
#nd.add_layer2xsection(xsection='Wg', layer=2, accuracy=0.001)
wgw = 0.5
mark1 = nd.Polygon(layer = 1, points = geom.box(25,60))
end1 = nd.Polygon(layer = 1, points = geom.box(2, wgw))   #Non-gc design end
message = 'X'
Lm_x = 5000
Lm_y = 5000
st_x = -2300
st_y = -950
nd.text(text=message, height=80, layer=1, align='cc').put(st_x, st_y)
nd.text(text=message, height=80, layer=1, align='cc').put(st_x + Lm_x, st_y)
nd.text(text=message, height=80, layer=1, align='cc').put(st_x, Lm_y + st_y)
nd.text(text=message, height=80, layer=1, align='cc').put(st_x + Lm_x, st_y + Lm_y)

# load a gds file and read as a module
with nd.Cell(name='gc') as gc:
    # load GDS BB
    gc = nd.load_gds(
        filename='merged_output.gds',
        cellname='MERGED',
        
        )
    gc.put()

with nd.Cell(name='tgc') as tgc:
    # load GDS BB
    tgc = nd.load_gds(
        filename='tgc.gds',
        cellname='MERGED',
        
        )
    gc.put()
    


with nd.Cell(name='rr') as rr:
    # load GDS BB
    rr = nd.load_gds(
        filename='rr_m.gds',
        cellname='MERGED',
        
        )
    rr.put()
    
with nd.Cell(name = 'tp07') as tp07:
    tp07 = nd.load_gds(
        filename = 'tp07.gds',
        cellname = 'MERGED'
        )
    tp07.put()
    
with nd.Cell(name = 'tp10') as tp10:
    tp10 = nd.load_gds(
        filename = 'tp10.gds',
        cellname = 'MERGED'
        )
    tp10.put()

with nd.Cell(name = 'tp13') as tp13:
    tp13 = nd.load_gds(
        filename = 'tp13.gds',
        cellname = 'MERGED'
        )
    tp13.put()

with nd.Cell(name = 'tp05') as tp05:
    tp05 = nd.load_gds(
        filename = 'tp05.gds',
        cellname = 'MERGED'
        )
    tp05.put()

with nd.Cell(name = 'tp15') as tp15:
    tp15 = nd.load_gds(
        filename = 'tp15.gds',
        cellname = 'MERGED',
        )
    tp15.put()


with nd.Cell(name = 'nf12') as nf12:
    nf12 = nd.load_gds(
        filename = 'nf_12.gds',
        cellname = 'MERGED',
        )
    nf12.put()

with nd.Cell(name = 'nf20') as nf20:
    nf20 = nd.load_gds(
        filename = 'nf_20.gds',
        cellname = 'MERGED',
        )
    nf20.put()









gc_offset_large = 40
gc_offset_small = 19.75


ic_offset_factor_large = 18
ic_offset_factor_small = 10
ic_offset_factor_smallest = 4

N = 12
wgw = 0.5 # Define the width of the waveguide
lattice_wgl = 1000
input_wgl = 100
input_wgl_long = 6000

# Define the part for nanowire emission 
emission_wgl = 260

#Define the taper offset
tp_l = 10
tp_r = 25

tp_offset_l = tp_l + tp_r
tp_offset_s = tp_l + tp_r - 15


monitor_wgl = 100
monitor_offset_x = -1000

# sinebend waveguide 
ic = Interconnect(width=wgw, radius=30.0)
ic_dis = 250

gap_l1 = 0.38
gap_l2 = 0.35
gap_s = 0.1


#RR
rr_r = 100
rr_g = 0.6
rr_w = 0.5
rr_l = 250
input_r_l = 70
input_r_s = 40
input_r_ss = 28

ic2_l = Interconnect(width = wgw, radius = input_r_l)
ic2_s = Interconnect(width = wgw, radius = input_r_s)
ic2_ss = Interconnect(width = wgw, radius = input_r_ss)

interface_num = int(N/2)

X_num = 4  # With or without different compoents such as 780 notch filter
x_g_dis = 1700  # Define the distance between different groups in x-direction
Y_num = 5   # With different m value of the mode size conversion taper


#Define the size of the notch filter for 780nm
nf12_input = 12/2
nf20_input = 20/2



tp_offset = tp_offset_l
      
for j in range(Y_num):
    for k in range(X_num):
        # if k <=1:
        #     y1 = -wgw-gap_s + j* 350
        #     ic_offset_factor = ic_offset_factor_large
        #     gc_offset = gc_offset_large
        #     ic2 = ic2_l
        #     input_r = input_r_l
        #     #tp_offset = tp_offset_l
        
        if k<=1:
            y1 = -wgw - gap_s + j*250 + 480
            ic_offset_factor = ic_offset_factor_small
            gc_offset = gc_offset_small
            ic2 = ic2_s
            input_r = input_r_s
            #tp_offset = tp_offset_s
        else:
            y1 = -wgw - gap_s - j*250 + 280
            ic_offset_factor = ic_offset_factor_smallest
            #gc_offset = gc_offset_small
            
            ic2 = ic2_ss
            input_r = input_r_ss
            
            
        if k <= 1:
            x1 = k*x_g_dis
        else:
            x1 = (k-2)*x_g_dis
        
        
        
        
        
        
        
       
        
        
        

        # s1 = demo.shallow.strt(10, width = wgw).put(rr_x + rr_l/2, y1-400 - rr_r - rr_g)
        # s2 = demo.shallow.strt(10, width = wgw).put(rr_x + rr_l/2, y1-400 - rr_r - rr_g -2*input_r)
        # demo.shallow.ubend_p2p(pin1=s1, pin2=s2, width = wgw, radius = input_r).put()
        
        
        for i in range(N):
            
            
            
            if i <= interface_num - 1:
                y1 += wgw + gap_s*(i%2 == 0) + gap_l1*(i%2 == 1)
                nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
                ic.sinebend(offset= +ic_offset_factor*(i - interface_num), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1)
                
                
                # if k <=1:
                #     gc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
                # elif k<=3:
                #     tgc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
                if k <=1:
                    tgc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
                    
                
                else:
                    end1.put(ic_dis + x1 + 1, y1+ic_offset_factor*(i-interface_num))
                    
                
                
                if i == interface_num - 1:
                    ty_offset = 50 * (k>= 2) + 12 * ((k-1)%2 == 0)
                    if (k-1)%2 == 0:
                        nf12.put(emission_wgl + x1 + nf12_input - ty_offset, y1-2*input_r )
                    #if k == 2:
                        # nf20.put(emission_wgl + x1 + nf20_input, y1-2*input_r)
                        # Add notch filter or not
                    monitor_offset_y = - (interface_num+1)* (ic_offset_factor + max(gap_l1, gap_l2))
                    
                    
                    nd.strt(input_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl + x1, y1)
                    nd.strt(input_wgl + lattice_wgl + emission_wgl - ty_offset
                            , width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl + x1, y1-2*input_r)
                    ic2.bend(angle = 180, xs = 'Wg', arrow = False, ).put(-lattice_wgl - input_wgl + x1, y1, 180)
                    if j == 0:
                        tp07.put(emission_wgl + tp_offset + x1 + nf12_input*2*((k-1)%2 == 0) - ty_offset , y1-2*input_r)
                    if j == 1:
                        tp10.put(emission_wgl + tp_offset + x1 + nf12_input*2*((k-1)%2 == 0) - ty_offset, y1-2*input_r)
                    if j == 2:
                        tp13.put(emission_wgl + tp_offset + x1 + nf12_input*2*((k-1)%2 == 0) - ty_offset, y1-2*input_r)
                    if j == 3:
                        tp05.put(emission_wgl + tp_offset + x1 + nf12_input*2*((k-1)%2 == 0) - ty_offset, y1-2*input_r)
                    if j == 4:
                        tp15.put(emission_wgl + tp_offset + x1 + nf12_input*2*((k-1)%2 == 0) - ty_offset, y1-2*input_r)
                    
                    
                
                
            else:
                y1 += wgw + gap_l2*(i%2 == 0) + gap_s*(i%2 == 1)
                nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
                ic.sinebend(offset= -ic_offset_factor*(interface_num-i -1), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1)
                # if k<=1:
                #     gc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 ))
                # elif k<=3: 
                #     tgc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 ))
                if k <=1:
                    tgc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 ))
                else:
                    end1.put(ic_dis + x1 + 1, y1-ic_offset_factor*(-1-i+interface_num))
    

for j in range(Y_num):
    ic_offset_factor = ic_offset_factor_small
    dis_cer = 800
    q_e = 0.5
    nf_shift = 20
    y1 = (5)*350 + 200*j -wgw - gap_s
    x1 = 1*x_g_dis
    if j == 0:
        nd.strt(input_wgl_long*1.0 - dis_cer, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1 , y1-120)
        mark1.put(-lattice_wgl - input_wgl_long*q_e -tp_offset +300+ x1, y1 - 165) 
    for i in range(N):
        if i <= interface_num -1:
            y1 += wgw + gap_s*(i%2 == 0) + gap_l1*(i%2 == 1)
            nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
            ic.sinebend(offset= +ic_offset_factor*(i - interface_num), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1)
            tgc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
            if i == interface_num - 1:
                nd.strt(input_wgl_long*q_e, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long*q_e + x1, y1)
                #nf12.put(-lattice_wgl + x1 - nf12_input - input_wgl_long + nf_shift, y1)
                if j == 0:
                    tp05.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 1:
                    tp07.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 2:
                    tp10.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 3:
                    tp13.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 4:
                    tp15.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
        
        else:
            y1 += wgw + gap_l2*(i%2 == 0) + gap_s*(i%2 == 1)
            nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
            ic.sinebend(offset= -ic_offset_factor*(interface_num-i -1), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1) 
            tgc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 ))
        
# for j in range(Y_num):
#     nf_shift = 20
#     y1 = 5*(350 + 200) + 200*j -wgw - gap_s
#     x1 = 2*x_g_dis
#     if j == 0:
#         nd.strt(input_wgl_long*1.8, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long -tp_offset -100+ x1, y1-90)
#         mark1.put(-lattice_wgl - input_wgl_long -tp_offset +300+ x1, y1 - 135)
#         mark1.put(-lattice_wgl - input_wgl_long -tp_offset +330+ x1, y1 - 135)
        
#     for i in range(N):
#         if i <= interface_num -1:
#             y1 += wgw + gap_s*(i%2 == 0) + gap_l1*(i%2 == 1)
#             nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
#             ic.sinebend(offset= +ic_offset_factor*(i - interface_num), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1)
#             tgc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
#             if i == interface_num - 1:
#                 nd.strt(input_wgl_long, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long + x1, y1)
#                 nf12.put(-lattice_wgl + x1 - nf_shift, y1)
#                 if j == 0:
#                     tp05.put(-lattice_wgl - input_wgl_long -tp_offset + x1, y1, 180)
#                 if j == 1:
#                     tp07.put(-lattice_wgl - input_wgl_long -tp_offset + x1, y1, 180)
#                 if j == 2:
#                     tp10.put(-lattice_wgl - input_wgl_long -tp_offset + x1, y1, 180)
#                 if j == 3:
#                     tp13.put(-lattice_wgl - input_wgl_long -tp_offset + x1, y1, 180)
#                 if j == 4:
#                     tp15.put(-lattice_wgl - input_wgl_long -tp_offset + x1, y1, 180)
        
#         else:
#             y1 += wgw + gap_l2*(i%2 == 0) + gap_s*(i%2 == 1)
#             nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
#             ic.sinebend(offset= -ic_offset_factor*(interface_num-i -1), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1) 
#             tgc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 ))
             
for j in range(Y_num):
    q_e = 0.5
    dis_cer = 800
    ic_offset_factor = ic_offset_factor_smallest
    nf_shift = 20
    y1 = 5*(350 + 200) + 100*j -wgw - gap_s
    x1 = 1*x_g_dis
    if j == 0:
        nd.strt(input_wgl_long*1.0 - dis_cer, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1 , y1-90)
        mark1.put(-lattice_wgl - input_wgl_long*q_e -tp_offset +300+ x1 , y1 - 135)
        mark1.put(-lattice_wgl - input_wgl_long*q_e -tp_offset +330+ x1, y1 - 135)
        # mark1.put(-lattice_wgl - input_wgl_long*q_e -tp_offset +360+ x1+dis_cer, y1 - 135)
        
    for i in range(N):
        if i <= interface_num -1:
            y1 += wgw + gap_s*(i%2 == 0) + gap_l1*(i%2 == 1)
            nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
            ic.sinebend(offset= +ic_offset_factor*(i - interface_num), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1)
            #tgc.put(ic_dis + gc_offset + x1, y1 + ic_offset_factor * ( i - interface_num ))
            end1.put(ic_dis+1+x1, y1+ic_offset_factor * (i - interface_num))
            if i == interface_num - 1:
                nd.strt(input_wgl_long*q_e, width = wgw, xs = 'Wg').put(-lattice_wgl - input_wgl_long*q_e + x1, y1)
                nf12.put(-lattice_wgl + x1 - nf_shift, y1)
                if j == 0:
                    tp05.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 1:
                    tp07.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 2:
                    tp10.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 3:
                    tp13.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
                if j == 4:
                    tp15.put(-lattice_wgl - input_wgl_long*q_e -tp_offset + x1, y1, 180)
        
        else:
            y1 += wgw + gap_l2*(i%2 == 0) + gap_s*(i%2 == 1)
            nd.strt(lattice_wgl, width = wgw, xs = 'Wg').put(-lattice_wgl + x1, y1)
            ic.sinebend(offset= -ic_offset_factor*(interface_num-i -1), distance=ic_dis, xs='Wg', arrow=False).put(x1, y1) 
            #tgc.put(ic_dis + gc_offset + x1, y1 - ic_offset_factor * (interface_num - i - 1 )) 
            end1.put(ic_dis+1+x1, y1-ic_offset_factor*(interface_num - i -1))



   


nd.export_gds(filename = 'HQ10.gds')