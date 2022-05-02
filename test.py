# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:28:54 2022

@author: ka1319
"""

from utils_gfat import lidar,lidarQA
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
# rs_fl = '../VELETA/1a/2022/02/22/vlt_1a_Prs_rs_xf_20220222.nc'
# dc_fl='../VELETA/1a/2022/02/22/vlt_1a_Pdc_rs_xf_20220221_2300.nc',
# lidarQA.rayleigh_fit(rs_fl=rs_fl, hour_ini='0000',hour_end='0030',
#                       lidar_name='VELETA',z_min=3000,z_max=4000,output_dn=None)
# lidarQA.telecover('20220221',input_directory='./Data/',output_directory='./Figure/')

# p45_fn = './Data/kal_1a_Pdp-P45_rs_xf_20200821_0025.nc'
# n45_fn = './Data/kal_1a_Pdp-N45_rs_xf_20200821_0025.nc'
# rs_fn =  './Data/kal_1a_Prs_rs_xf_20180408.nc'
# dc_fn = './Data/kal_1a_Pdc_rs_xf_20200520_1702.nc'

# lidarQA.depolarization_cal(p45_fn=p45_fn,rs_fn=rs_fn,n45_fn=n45_fn,dc_fn=dc_fn,alpha=0,
#                             epsilon=8.3,output_dn= '.\\Figure\\')

rs_fl ='./Data/kal_1a_Pfp_rs_xf_20180407.nc'
dc_fl='./Data/kal_1a_Pdc_rs_xf_20200520_1702.nc'
lidarQA.rayleigh_fit(rs_fl=rs_fl,dc_fl=dc_fl,hour_ini='0200',hour_end='0300',
                      lidar_name='KASCAL',z_min=5000,z_max=10000,
                      output_dn= '.\\Figure\\')