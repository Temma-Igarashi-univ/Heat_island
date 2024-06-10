from matplotlib.pyplot import *
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from collections import defaultdict, deque
from warnings import simplefilter

from constants import UHII, ESTIMATED_POLLUTANT_DENSITY, URBAN_AREA_NAMESET, POLLUTANT_NAMES, UNITS

POLLUTANT_NAMES = sorted(POLLUTANT_NAMES)

def nf(num):
  txt = f'{num:.3e}'.replace('e+00', '').replace('e', '\\times 10^{').replace('+0', '+').replace('-0', '-')
  if '{' in txt: txt += '}'
  return txt

outlier_remover = IsolationForest()
std_scale = StandardScaler()
pca = PCA()

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

simplefilter('ignore', UserWarning)
for year_indic in range(1980, 2020, 5):
  print(f'Processing. ({year_indic}-{year_indic+4})')
  fig, ax = subplots(3, 4)
  fig.set_size_inches(16, 16)
  fig.suptitle(f'{year_indic}-{year_indic+4}', verticalalignment = 'bottom')
  subplots_adjust(wspace=0.3, hspace=1)
  for i in range(3):
    for j in range(4):
      k = i*4+j
      if k == 11: break
      target_pol = POLLUTANT_NAMES[k]
      x = np.array([UHII[year, location, month] for year in range(year_indic, year_indic+5) \
            for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
      y = np.array([ESTIMATED_POLLUTANT_DENSITY[year, target_pol, location, month] for year in range(year_indic, year_indic+5) \
            for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
      x = x[~np.isnan(y)]; y = y[~np.isnan(y)]
      x = x[~np.isinf(y)]; y = y[~np.isinf(y)]
      y = y[~np.isinf(x)]; x = x[~np.isinf(x)]
      xr, xe, yr, ye = [], [], [], []
      try:
        outlier_remover.fit(np.array([x, y]).T)
        remove_or_not = outlier_remover.decision_function(np.array([x, y]).T)
        xr = x[remove_or_not  > -.2]; yr = y[remove_or_not  > -.2]
        xe = x[remove_or_not <= -.2]; ye = y[remove_or_not <= -.2]
      except: pass

      ax[i, j].scatter(xr, yr, marker = '.', label = 'adopted')
      ax[i, j].scatter(xe, ye, marker = '.', label = 'error')
      ax[i, j].set_title(target_pol)
      ax[i, j].set_xlabel('UHII')
      ax[i, j].set_ylabel(f'{target_pol} / $\\mathrm{{{UNITS[target_pol]}}}$')
      try:
        (a, b), rss, _, _, _ = np.polyfit(xr, yr, 1, full = True)
        ax[i, j].plot(x, np.poly1d((a, b))(x), label = f'$y={nf(a)}x+{nf(b)}$', color = '#ff0000')
        ax[i, j].plot([min(x)], [min(y)], label = f'$r={np.corrcoef(xr, yr)[0, 1]: .6f}$\n$\\delta={nf(((rss/sum((x-np.mean(x))**2)/(len(x)-2))**.5)[0])}$ ({len(xr)}/{len(x)} data)', color = '#ffffff')
      except: pass
      ax[i, j].legend(loc = 'upper center', bbox_to_anchor = (.5, -.25), handlelength = .5)
  fig.savefig(f'./graphs/monthly_plot_{year_indic}-{year_indic+4}.png', dpi = 720, pad_inches = .05)
  del fig, ax

  fig, ax = subplots(3, 4)
  fig.set_size_inches(16, 16)
  fig.suptitle(f'{year_indic}-{year_indic+4}', verticalalignment = 'bottom')
  subplots_adjust(wspace=0.3, hspace=1)
  for i in range(3):
    for j in range(4):
      k = i*4+j
      if k == 11: break
      target_pol = POLLUTANT_NAMES[k]
      x = np.array([sum(UHII[year, location])/12 \
            for year in range(year_indic, year_indic+5) for location in URBAN_AREA_NAMESET])
      y = np.array([sum(ESTIMATED_POLLUTANT_DENSITY[year, target_pol, location])/12 \
            for year in range(year_indic, year_indic+5) for location in URBAN_AREA_NAMESET])
      x = x[~np.isnan(y)]; y = y[~np.isnan(y)]
      x = x[~np.isinf(y)]; y = y[~np.isinf(y)]
      y = y[~np.isinf(x)]; x = x[~np.isinf(x)]
      xr, xe, yr, ye = [], [], [], []
      try:
        outlier_remover.fit(np.array([x, y]).T)
        remove_or_not = outlier_remover.decision_function(np.array([x, y]).T)
        xr = x[remove_or_not  > -.1]; yr = y[remove_or_not  > -.1]
        xe = x[remove_or_not <= -.1]; ye = y[remove_or_not <= -.1]
      except: pass

      ax[i, j].scatter(xr, yr, marker = '.', label = 'adopted')
      ax[i, j].scatter(xe, ye, marker = '.', label = 'error')
      ax[i, j].set_title(target_pol)
      ax[i, j].set_xlabel('UHII')
      ax[i, j].set_ylabel(f'{target_pol} / $\\mathrm{{{UNITS[target_pol]}}}$')
      try:
        (a, b), rss, _, _, _ = np.polyfit(xr, yr, 1, full = True)
        ax[i, j].plot(x, np.poly1d((a, b))(x), label = f'$y={nf(a)}x+{nf(b)}$', color = '#ff0000')
        ax[i, j].plot([min(x)], [min(y)], label = f'$r={np.corrcoef(xr, yr)[0, 1]: .6f}$\n$\\delta={nf(((rss/sum((x-np.mean(x))**2)/(len(x)-2))**.5)[0])}$ ({len(xr)}/{len(x)} data)', color = '#ffffff')
      except: pass
      ax[i, j].legend(loc = 'upper center', bbox_to_anchor = (.5, -.25), handlelength = .5)
  fig.savefig(f'./graphs/annual_plot_{year_indic}-{year_indic+4}.png', dpi = 720, pad_inches = .05)
  del fig, ax