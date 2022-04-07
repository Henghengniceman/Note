---
tags: features, cool, updated
---
# Work flow of KASCAL (Karlsruhe Scanning Aerosol LiDAR)
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
The most common used elastic retrieved is klett - fernald method. 
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
beta_part = lidar_elastic_retrieval.klett(rcs , height, beta_mol, 
                                          lr_mol,lr_aer, ymin, ymax)
```
```
    Klett - Fernald,  F.  G.:, Appl. Opt., 23, 652–653, 1984
    Parameters
    ----------
    rcs: numpy.ndarray
        range corrected lidar signal (rsc = p(z)*z^2)
    height: numpy.ndarray
        height above ground
    beta_mol: numpy.ndarray   
        backscatter coefficient of molecule     
    lr_mol: numpy.ndarray
        lidar ratio of molecule
    lr_aer: float/int sr
        lidar ratio of aerosol
    ymin: float/int m
        reference height (low limit) 
    ymax: float/int m
        reference height (height limit)
    Output:
        particle_beta: numpy.ndarray
```
### 4.2 Raman retrieval method
- Lidar equation
$$
P\left(R, \lambda_{R}\right)=\frac{C \times \beta\left(R, \lambda_{L}, \lambda_{R}\right)}{R^{2}} \exp \left[-\int_{0}^{R}\left[a\left(\lambda_{L}, r\right)+a\left(\lambda_{R}, r\right)\right] d r\right]
$$
$$
\beta\left(R, \lambda_{L}, \lambda_{R}\right)=N_{R}(R) \frac{d \sigma\left(\lambda_{L}, \lambda_{R}, \pi\right)}{d \Omega}
$$
- Retrieve extinction coefficient 
$$
a_{p}\left(\lambda_{L}, R\right)=\frac{\frac{d}{d r}\left[\ln \frac{N_{R}(R)}{R^{2} P(R)}\right]-a_{m o l}\left(\lambda_{L}, R\right)-a_{m o l}\left(\lambda_{L}, R\right)}{1+\left(\frac{\lambda_{L}}{\lambda_{R}}\right)^{k}}
$$
- Retrieve backscatter coefficient
$$
\beta_{\text {aer }}\left(\lambda_{L}, R\right)=-\beta_{\text {mol }}\left(\lambda_{L}, R\right)+\left[\beta_{\text {aer }}\left(\lambda_{L}, R_{\text {ref }}\right)+\beta_{\text {mol }}\left(\lambda_{L}, R_{r e f}\right)\right] \times \frac{P\left(\lambda_{R}, R_{r e f}\right) P\left(\lambda_{L}, R\right) N_{R}(R)}{P\left(\lambda_{L}, R_{\text {ref }}\right) P\left(\lambda_{R}, R\right) N_{R}\left(R_{r e f}\right)} \times \\
\frac{\exp \left\{-\int_{R_{r e f}}^{R}\left[a_{a e r}\left(\lambda_{R}, r\right)+a_{m o l}\left(\lambda_{R}, r\right)\right] d r\right\}}{\exp \left\{-\int_{R_{r e f}}^{R}\left[a_{a e r}\left(\lambda_{L}, r\right)+a_{m o l}\left(\lambda_{L}, r\right)\right] d r\right\}}
$$
The reference can be find below:
{%pdf https://henghengniceman.github.io/files/Ansman-1992.pdf %}
#### Code
- Extinction coefficient
```python=
import utils_gfat.lidar_processing.lidar_processing.raman_retrievals as raman_retrievals
AeroAlpha = raman_retrievals.raman_extinction(signal, dz, emission_wavelength, 
                                                raman_wavelength, angstrom_aerosol, 
                                                temperature, pressure,window_size,
                                                order)

```
```
Calculates the aerosol extinction coefficient based on pre-processed Raman signals and molecular profiles.

    The derivative is calculated using a Savitzky-Golay filter.

    Parameters
    ----------
    signal : (M,) array
       The range_corrected molecular signal. Should be 1D array of size M.
    dz : float
       Altitude step, used in the derivative [m]
    emission_wavelength, raman_wavelength : float
       The emission and detection wavelengths [nm]
    angstrom_aerosol : float
       The aerosol Angstrom exponent.
    temperature : (M,) array
       Atmospheric temperature profile, same shape as the lidar signal [Kelvin]
    pressure : (M,) array
       Atmospheric pressure profile, same shape as the lidar signal [Pa]
    window_size : int
       the length of the smoothing window. Must be an odd integer number.
    order : int
       The order of the polynomial used in the filtering.
       Must be less then `window_size` - 1.

    Returns
    -------
    alpha_aer : arrays
       The aerosol extinction coefficient [m-1]
       
    Notes
    -----
    The aerosol extinction coefficient is given by the formula:
    
    .. math::
       \alpha_{aer}(R,\lambda_0) = \frac{\frac{d}{dR}ln[\frac{N_{Ra}(R)}
       {S(R,\lambda_{Ra})}] - \alpha_{mol}(R,\lambda_0) - \alpha_{mol}(R,\lambda_{Ra})}
       {[1 + (\frac{\lambda_0}{\lambda_{Ra}})^{\alpha(R)}]}

    References
    ----------
    Ansmann, A. et al. Independent measurement of extinction and backscatter profiles
    in cirrus clouds by using a combined Raman elastic-backscatter lidar.
    Applied Optics Vol. 31, Issue 33, pp. 7113-7131 (1992)    
    """
```
- Backscatter coefficient
```python=
import utils_gfat.lidar_processing.lidar_processing.raman_retrievals as raman_retrievals
BetaRaman = raman_retrievals.raman_backscatter(signal_raman,signal_emission,
                                    reference_idx, dz, backscatter_molecules,
                                    alpha_aerosol_emission, emission_wavelength,
                                    raman_wavelength, angstrom_aerosol, pressure,
                                    temperature, beta_aer_ref=0)

```
```
Calculates the aerosol backscatter coefficient based on:
    * Preprocessed elastic & raman signals.
    * The retrieved aerosol extinction coefficient.

    Parameters
    ----------
    signal_raman : (M,) array
       The range-corrected Raman signal. Should be 1D array of size M.
    signal_emission : (M, ) array
        The range-corrected elastic signal (at the emission wavelength). Should be 1D array of size M.
    reference_idx : int
        It is the index of the reference altitude to find into arrays the quantity (for example the signal) at the
        reference altitude.
    dz : float
        Altitude step, used in the integrals calculations [m]
    alpha_aerosol_emission, alpha_aer_raman : (M,) array
        The aerosol extinction coefficient at each point of the signal profile for emission and raman wavelength.
    alpha_molecular_emission, alpha_mol_raman : (M,) array
        The molecular extinction coefficient at each point of the signal profile for emission and raman wavelength.
    backscatter_molecules : (M, ) array
        The altitude range depended backscatter coefficient from molecules. Units -> [m-1]
    alpha_molecular_emission, alpha_mol_raman : (M,) array
       The molecular extinction coefficient at each point of the signal profile for emission and raman wavelength.
    pressure : (M, ) array
        Atmosphere pressure profile, same as shape as the lidar signal [Pa]
    temperature : (M, ) array
        Atmosphere temperature profile, same as shape as the lidar signal [K]
    beta_aer_ref : float
        The molecular backscatter coefficient at reference altitude.


    Returns
    -------
    backscatter_raman_aer : arrays
        The aerosol  backscatter coefficient [m-1]

    References
    ----------
    Ansmann, A. et al. Independent measurement of extinction and backscatter profiles
    in cirrus clouds by using a combined Raman elastic-backscatter lidar.
    Applied Optics Vol. 31, Issue 33, pp. 7113-7131 (1992)
    
```
## 5: Quality Assurance
### 5.1 Telescope cover test
```python=
from utils_gfat import lidarQA
lidarQA.telecover('20220221')
```
```
    telecover
    Inputs:
    - date_str: date ('yyyymmdd') (str)
    - zmin: minimum altitude we use as base for our rayleigh fit (float)
    - zmax: max altitude we use as base for our rayleigh fit (float)
    - savefig: it determines if we will save our plots (True) or not (False) (bool)
    - level_1a_dn: folder where telecover files are located.
    - rayleigh_fit_dn: folder where we want to save our figures.
    Outputs:
    - ascii files
    - figures
```
### 5.2 Rayleigh fitting 
```python=
from utils_gfat import lidarQA
lidarQA.rayleigh_fit(**kwargs)
```
```
  Thought for measurements taken in a given day. No more than one day should
    be processed

    Parameters
    ----------
    kwargs: dict, all optional
        rs_fl: str
            wildcard list of lidar raw signal level 1a files (*.nc)
        dc_fl: str
            wildcard list of lidar dark current signal level 1a files (*.nc)
        date_str: str
            date in format yyyymmdd
        hour_ini: str
            hh, hhmm, hhmmss
        hour_end: str
            hh, hhmm, hhmmss
        duration: int, float
            duration in minutes for RF
        lidar_name: str
            lidar name (VELETA, MULHACEN)
        meas_type: str
            measurement type (RS, OT, ...)
        channels: str
            if we want all of them we put 'all' (str),
            if we only want some of them we put a list (ex.: 0,1,3,8) (comma separated)
        z_min: int, float
            minimum altitude we use as base for our rayleigh fit
        z_max: int, float
            maximum altitude we use as base for our rayleigh fit
        smooth_range: int, float
            range resolution window for smoothing profiles
        range_min: int, float
            minimum range
        range_max: int, float
            maximum range
        meteo: str
            identifier for hydrostatic (P, T) data source (ecmwf (default), user, lidar, grawmet)
        pressure_prf: array
            pressure profile
        temperature_prf: array
            temperature profile
        data_dn: str
            absolute path for data directory: "data_dn"/LIDAR/1a
        level_1a_dn: str
            level 1a data directory
        ecmwf_dn: str
            ecmwf data directory (ecmwf_dn/yyyy/)
        output_dn: str
            directory to store rayleigh fit results
        save_fig: bool
            save RF figures in png format
        save_earlinet bool
            save earlinet files in ascii format
        verbose: str
            level of message to print ('debug','info','warning','error','critical')
    Returns
    -------
```
### 5.3 Depolarization calibration
```python=
from utils_gfat import lidarQA
lidarQA.depolarization_cal(**kwargs)
```
```
 Calibration of Depolarization based on Delta90-calibration method

    Parameters
    ----------
    kwargs
        p45_fn: str
            file name for P45 measurement (netcdf)
        n45_fn: str
            file name for N45 measurement (netcdf)
        rs_fn: str
            file name for RS complementary measurement (netcdf)
        dc_fn: str
            filename of lidar dark current signal level 1a files (*.nc)
        cal_height_an: tuple, list (2-el)
            height range for averaging calibrations for analog signals
        cal_height_pc: tuple, list (2-el)
            height range for averaging calibrations for photoncounting signals
        pbs_orientation_parameter: int
            polarising beam splitter orientation parameter, y [Freudenthaler, 2016, sec3.3]
            y = -1: reflected = parallel
            y = +1: reflected = perpendicular
        cal_type: str
            type of calibration: rotator (rot), polarizer (pol)
        channels: str ('all'), list()
            list of channels to process
            if we want all of them we put 'all' (str),
            if we only want some of them we put a list (ex.: [0,1,3,8]) (list)
        range_min: int, float
            minimum range
        range_max: int, float
            maximum range
        alpha: float
            rotational misalignment of the polarizing plane of the laser light respect to the incident plane of the PBS
        epsilon: float
            misalignment angle of the rotator
        ghk_tpl_fn: str
            ghk file template for running GHK
        output_dn: str
            directory to store depolarization calibration results

    Returns
    -------
```
## 6. Molecular scatter profile
- Code
```python=
import lidar_processing.lidar_processing.helper_functions as helper_functions
from utils_gfat import lidarQA
for i, _height in enumerate(height):
    sa = helper_functions.standard_atmosphere(_height)
    pressure_prf[i] = sa[0]
    temperature_prf[i] = sa[1]
molp = lidarQA.molecular_properties(355,pressure_prf,temperature_prf,height)
```
```
 Molecular Attenuated  Backscatter: beta_mol_att = beta_mol * Transmittance**2

    Parameters
    ----------
    wavelength: int, float
        wavelength of our desired beta molecular attenuated
    pressure: array
        pressure profile
    temperature: array
        temperature profile
    heights: array
        heights profile

    Returns
    -------
    beta_molecular_att: array
        molecular attenuated backscatter profile
```
