---
tags: features, cool, updated
---
# Retrieve method (KASCAL - Karlsruhe Scanning Aerosol LiDAR)
>[name=Hengheng Zhang][time=Wenday, April 06, 2022 14:00 PM] [color=#907bf7] E-mail : <hengheng.zhang@kit.edu>
### Table of Contents 
[TOC]

## 1 : Move the raw data into lidar sever folder. (one lidar computer, run automatically)
Bat file path: `C:\DataAnalysisTool\lidar_transfer_manager\bin`
```shell
$ C:\Users\user\anaconda3\Scripts\activate.bat && python c:\DataAnalysisTool\lidar_transfer_manager\python\lidar_transfer_manager.py -l kascal # full path 
```
```
Parameters
----------
C:\Users\user\anaconda3\Scripts\activate.bat  # Anaconda path
C:\DataAnalysisTool\lidar_transfer_manager\python\lidar_transfer_manager.py # python code path
-m : str # measurement type, [OPTIONAL] [example: 'RS', 'DP', 'TC', 'FP', 'ZS', 'AS'], required=False
-l : str # nickname of lidar, [OPTIONAL] [example: 'kal']
-i : str # initial_date, [OPTIONAL] [example: '20180408'], if None, the date will be yesterday 
-e : str # final_date, [OPTIONAL] [example: '20180408'], if None, the date will be today 
```
## 2 : Convert raw bin data into netcdf file. (one lidar computer, run automatically)
Bat file path: `C:\DataAnalysisTool`
```shell
$ C:\Users\user\anaconda3\Scripts\activate.bat && python c:\DataAnalysisTool\lidar_raw2l1\lidar_raw2l1.py -l KASCAL -i 20220320 -e 20220401 -t RS -w True -y c:\DataAnalysisTool\lidar_raw2l1\config\config_kascal.yaml # full path 
```
```
Parameters
----------
C:\Users\user\anaconda3\Scripts\activate.bat  # Anaconda path
C:\DataAnalysisTool\lidar_raw2l1\lidar_raw2l1.py # python code path
-l : str # nickname of lidar, [example: 'kal']
-i : str # initial_date, [OPTIONAL], [example: '20180408'], if None, the date will be yesterday 
-e : str # final_date, [OPTIONAL], [example: '20180408'], if None, the date will be today 
-t : str # measurement type, [example: 'RS', 'DP', 'TC', 'FP', 'ZS', 'AS'], required=False
-c : str # [OPTIONAL], Lidar Config Prod Ini File [see /[code]/raw2l1_v2/raw2l1/conf/config_prod_MULHACEN.ini].
-x: [OPTIONAL] Lidar Initial Raw Letter
-y: [OPTIONAL] Yaml File with Configuration Information: python interpreter, raw2l1 package, logging directory, data directory. [DEFAULT: config/config_server.yaml].
-w: [OPTIONAL] Overwrite 1a netcdf file if exists.
-d: [OPTIONAL] Full Path for data directory
```
## 3: Lidar data pre-processing
```python=
from utils_gfat import lidar,lidarQA
ds = lidar.preprocessing(rs_fl='../KASCAL/1a/2018/04/07/kal_1a_Pfp_rs_xf_20180407.nc',
                         ini_date = '20180407T210000',end_date = '20180407T230000',
                         percentage_required = 20)

```

```
    Preprocessing lidar signals including: dead time, dark measurement,
    background, and bin shift.

    Parameters
    ----------
    rs_fl: str
        Wildcard List of lidar files (i.e, '/drives/c/*.nc') (str)....
    dc_fl: str
        Wildcard List of DC lidar files (i.e, '/drives/c/*.nc') (str)....
    ini_date: str
        yyyymmddThhmmss
    end_date: str
        yyyymmddThhmmss
    ini_range: int, float
        min range [m]
    end_range: int, float
        max range [m]
    bg_window: tuple
        range window limits to calculate background
    percentage_required: int, float
        percentage of the time period required to continue the process. Default 80%
    channels: str, list(str)
        list of channel number (e.g., [0, 1, 5]) or 'all' to load all of them
    bin_zero_fn: str
        bin zero file
    dead_time_fn: str
        dead time file
    data_dn: str
        full path of directory of data where bin zero file should be
    darkcurrent_flag: bool
        active/desactive the dark-current correction.
    deadtime_flag: bool
        active/desactive the dead time correction.
    zerobin_flag: bool
        active/desactive the zero-bin and trigger delay corrections.
    merge_flag: bool
        active/desactive the merge of polarizing components.

    Returns
    -------
    ps_ds: xarray.Dataset
        dataset with pre-processed signal

```
## 4: Lidar retrieval
### 4.1 Elastic retrieval method
The most common used elastic retrieved is Kettle - fernald method. 
- Lidar eqaution
$$
P(r)=C_{0}  \frac{\beta_{a e r}(r)+\beta_{m o l}(r)}{r^{2}} \exp \left(-2 \int_{0}^{r}\left[\alpha_{a e r}(r)+\alpha_{m o l}(r)\right] d r\right) 
$$
- Fernald retrieval method (forward)
$$
\beta\left(r\right)=\frac{\operatorname{X}\left(\mathrm{r}\right) * \exp \left\{2 *\left(S_{a}-S_{m}\right) * \int_{0}^{r} \beta_{m o l}\left(r^{\prime}\right) d r^{\prime}\right\}}{C_0+2 * S_{a} * \int_{0}^{r}\left[\operatorname{X}\left(r^{\prime}\right) * \exp \left\{2 *\left(S_{a}-S_{m}\right) * \int_{0}^{r^{\prime}} \beta_{m o l}\left(r^{\prime \prime}\right) d r^{\prime \prime}\right\}\right] d r^{\prime}} 
$$
and  (backward)
$$
\beta\left(r\right)=\frac{\operatorname{X}\left(\mathrm{r}\right) * \exp \left\{2 *\left(S_{a}-S_{m}\right) * \int_{r}^{r_{r e f}} \beta_{m o l}\left(r^{\prime}\right) d r^{\prime}\right\}}{\frac{X\left(r\right)}{\beta_{\operatorname{aer}}\left(r_{\text {ref }}\right)+ \beta_{\operatorname{mol}}\left(r_{\text {ref }}\right)}+2 * S_{a} * \int_{r}^{r_{r e f}}\left[\operatorname{X}\left(r^{\prime}\right) * \exp \left\{2 *\left(S_{a}-S_{m}\right) * \int_{r^{\prime}}^{r_{r e f}^{\prime}} \beta_{m o l}\left(r^{\prime \prime}\right) d r^{\prime \prime}\right\}\right] d r^{\prime}}
$$
The reference can be find below:
{%pdf https://henghengniceman.github.io/publications/Fernald-1984.pdf %}
#### Code
```python=
from utils_gfat import lidar_elastic_retrieval
beta_part = lidar_elastic_retrieval.klett(rcs_355xpp.values , height, molbeta, 
lr_mol,lr_aer = lr_aer, ymin = 14000, ymax = 16000)
```
```
- Klett clásico verificado con Fernald,  F.  G.:, Appl. Opt., 23, 652–653, 1984
Input:
    rcs: numpy.ndarray
    height: numpy.ndarray
    beta_mol: numpy.ndarray        
    lr_mol: numpy.ndarray
    lr_aer: float/int sr
    ymin: float/int m
    ymax: float/int m
Output:
    particle_beta: numpy.ndarray
```




