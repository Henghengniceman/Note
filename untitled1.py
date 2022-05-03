# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:50:39 2022

@author: ka1319
"""

from utils_gfat import lidar,lidarQA
import numpy as np
import matplotlib.pyplot as plt
import lidar_processing.lidar_processing.helper_functions as helper_functions
from utils_gfat import lidar_elastic_retrieval
from scipy import integrate
import utils_gfat.lidar_processing.lidar_processing.raman_retrievals as raman_retrievals
import pandas as pd 
import os 
import glob
import xarray as xr

rs_fl ='./Data/kal_1a_Pfp_rs_xf_20180408.nc'
dc_fl='./Data/kal_1a_Pdc_rs_xf_20200520_1702.nc'
ds = lidar.preprocessing(rs_fl=rs_fl,ini_date= '20180408T202100', end_date='20180408T235900')


# ini_date = '20220321T000000.0'
# end_date = '20220321T013000.0'
# ds = ds.sel(time=slice(ini_date, end_date))
aa = ds.signal_387xta.values
