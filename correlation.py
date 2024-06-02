from matplotlib.pyplot import *
import numpy as np
from collections import defaultdict

from constants import UHII, ESTIMATED_POLLUTANT_DENSITY, URBAN_AREA_NAMESET, POLLUTANT_NAMES, UNITS

POLLUTANT_NAMES = sorted(POLLUTANT_NAMES)

print('\nCORRCOEF from monthly data')
fig, ax = subplots(3, 4)
fig.set_size_inches(16, 9)
subplots_adjust(wspace=0.3, hspace=0.4)
for i in range(3):
  for j in range(4):
    k = i*4+j
    if k == 11: break
    target_pol = POLLUTANT_NAMES[k]
    x = np.array([UHII[year, location, month] for year in range(2015, 2020) \
          for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
    y = np.array([ESTIMATED_POLLUTANT_DENSITY[year, target_pol, location, month] for year in range(2015, 2020) \
          for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
    y = y[x<60];         x = x[x<60]
    x = x[~np.isnan(y)]; y = y[~np.isnan(y)]
    print('CORRCOEFF of ' + f'{target_pol}'.rjust(4) + f': {np.corrcoef(x, y)[0, 1]: .6f}' + f' (from {str(len(x)).zfill(5)} data)')
    
    ax[i, j].scatter(x, y, marker = '.')
    ax[i, j].set_title(target_pol)
    ax[i, j].set_xlabel('UHII')
    ax[i, j].set_ylabel(f'{target_pol} / $\\mathrm{{{UNITS[target_pol]}}}$')
fig.savefig('./monthly_plot.png', dpi = 720, pad_inches = .05)
show()

print('\nCORRCOEF from annual average')
fig, ax = subplots(3, 4)
fig.set_size_inches(16, 9)
subplots_adjust(wspace=0.3, hspace=0.4)
for i in range(3):
  for j in range(4):
    k = i*4+j
    if k == 11: break
    target_pol = POLLUTANT_NAMES[k]
    x = np.array([sum(UHII[year, location])/12 \
          for year in range(2015, 2020) for location in URBAN_AREA_NAMESET])
    y = np.array([sum(ESTIMATED_POLLUTANT_DENSITY[year, target_pol, location])/12 \
          for year in range(2015, 2020) for location in URBAN_AREA_NAMESET])
    y = y[x<60];         x = x[x<60]
    x = x[~np.isnan(y)]; y = y[~np.isnan(y)]
    print('CORRCOEFF of ' + f'{target_pol}'.rjust(4) + f': {np.corrcoef(x, y)[0, 1]: .6f}' + f' (from {str(len(x)).zfill(5)} data)')
    
    ax[i, j].scatter(x, y, marker = '.')
    ax[i, j].set_title(target_pol)
    ax[i, j].set_xlabel('UHII')
    ax[i, j].set_ylabel(f'{target_pol} / $\\mathrm{{{UNITS[target_pol]}}}$')
fig.savefig('./annual_plot.png', dpi = 720, pad_inches = .05)
show()