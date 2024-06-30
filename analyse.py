from matplotlib.pyplot import *
import numpy as np
from scipy.stats import pearsonr
from sklearn.ensemble import IsolationForest
from collections import defaultdict, deque
from warnings import simplefilter

from constants import UHII, ESTIMATED_POLLUTANT_DENSITY, URBAN_AREA_NAMESET, POLLUTANT_NAMES, UNITS

POLLUTANT_NAMES = sorted(POLLUTANT_NAMES)

def nf(num):
  txt = f'{num:.3e}'.replace('e+00', '').replace('e', '\\times 10^{').replace('+0', '').replace('-0', '-')
  if txt[-3:] == '^{1': txt = txt[:-3]
  if '{' in txt: txt += '}'
  return txt

outlier_remover = IsolationForest()

rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 20
rcParams['mathtext.fontset'] = 'stix'

simplefilter('ignore', UserWarning)

for pol_index in range(12):
  target = POLLUTANT_NAMES[pol_index]
  print(f'Target: {target}')
  # 月別 monthly
  fig, ax = subplots(3, 3)
  fig.set_size_inches(16, 20)
  fig.suptitle(f'{target}: monthly')
  subplots_adjust(top = .93, bottom = .2, wspace=0.3, hspace=1.3)
  for i in range(3):
    for j in range(3):
      if i == j == 2:
        x = np.array([ESTIMATED_POLLUTANT_DENSITY[year, target, location, month] for year in range(1980, 2020) \
              for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
        y = np.array([UHII[year, location, month] for year in range(1980, 2020) \
              for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
        ax[i, j].set_title('1980-2019 (all)')
      else:
        k = i*3+j
        year_indic = 1980+15*i+5*j
        x = np.array([ESTIMATED_POLLUTANT_DENSITY[year, target, location, month] for year in range(year_indic, year_indic+5) \
              for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
        y = np.array([UHII[year, location, month] for year in range(year_indic, year_indic+5) \
              for location in URBAN_AREA_NAMESET for month in range(len(UHII[year, location]))])
        ax[i, j].set_title(f'{year_indic}-{year_indic+4}')
      y = y[~np.isnan(x)]; x = x[~np.isnan(x)]
      y = y[~np.isinf(x)]; x = x[~np.isinf(x)]
      x = x[~np.isinf(y)]; y = y[~np.isinf(y)]
      xr, xe, yr, ye = [], [], [], []
      try:
        outlier_remover.fit(np.array([x, y]).T)
        remove_or_not = outlier_remover.decision_function(np.array([x, y]).T)
        yr = y[remove_or_not  > -.2]; xr = x[remove_or_not  > -.2]
        ye = y[remove_or_not <= -.2]; xe = x[remove_or_not <= -.2]
      except: pass

      ax[i, j].scatter(xr, yr, marker = '.', label = 'adopted')
      ax[i, j].scatter(xe, ye, marker = '.', label = 'error')
      ax[i, j].set_xlabel(f'{target} / $\\mathrm{{{UNITS[target]}}}$')
      ax[i, j].set_ylabel('UHII')
      try:
        (a, b), rss, _, _, _ = np.polyfit(xr, yr, 1, full = True)
        corr, p = pearsonr(xr, yr)
        print(f'{corr:.5f}m'.replace('0.', '.'))
        ax[i, j].plot(x, np.poly1d((a, b))(x), label = f'$y={nf(a)}x+{nf(b)}$'.replace('+-', '-'), color = '#ff0000')
        ax[i, j].plot([min(x)], [min(y)], label = f'$r={corr:.6f}$\n$p={p:.4f}$ ({len(xr)}/{len(x)} data)', color = '#ffffff')
      except: pass
      ax[i, j].legend(loc = 'upper center', bbox_to_anchor = (.5, -.25), handlelength = .5)
  fig.savefig(f'./graphs/monthly_plot_{target}.png', dpi = 720, pad_inches = .05)
  close()
  del fig, ax

  # 年別 yearly
  fig, ax = subplots(3, 3)
  fig.set_size_inches(16, 20)
  fig.suptitle(f'{target}: yearly')
  subplots_adjust(top = .93, bottom = .2, wspace=0.3, hspace=1.3)
  for i in range(3):
    for j in range(3):
      if i == j == 2:
        x = np.array([sum(ESTIMATED_POLLUTANT_DENSITY[year, target, location])/12 \
            for year in range(1980, 2020) for location in URBAN_AREA_NAMESET])
        y = np.array([sum(UHII[year, location])/12 \
            for year in range(1980, 2020) for location in URBAN_AREA_NAMESET])
        ax[i, j].set_title('1980-2019 (all)')
      else:
        k = i*3+j
        year_indic = 1980+15*i+5*j
        x = np.array([sum(ESTIMATED_POLLUTANT_DENSITY[year, target, location])/12 \
            for year in range(year_indic, year_indic+5) for location in URBAN_AREA_NAMESET])
        y = np.array([sum(UHII[year, location])/12 \
            for year in range(year_indic, year_indic+5) for location in URBAN_AREA_NAMESET])
        ax[i, j].set_title(f'{year_indic}-{year_indic+4}')
      y = y[~np.isnan(x)]; x = x[~np.isnan(x)]
      y = y[~np.isinf(x)]; x = x[~np.isinf(x)]
      x = x[~np.isinf(y)]; y = y[~np.isinf(y)]
      xr, xe, yr, ye = [], [], [], []
      try:
        outlier_remover.fit(np.array([x, y]).T)
        remove_or_not = outlier_remover.decision_function(np.array([x, y]).T)
        yr = y[remove_or_not  > -.1]; xr = x[remove_or_not  > -.1]
        ye = y[remove_or_not <= -.1]; xe = x[remove_or_not <= -.1]
      except: pass

      ax[i, j].scatter(xr, yr, marker = '.', label = 'adopted')
      ax[i, j].scatter(xe, ye, marker = '.', label = 'error')
      ax[i, j].set_xlabel(f'{target} / $\\mathrm{{{UNITS[target]}}}$')
      ax[i, j].set_ylabel('UHII')
      try:
        (a, b), rss, _, _, _ = np.polyfit(xr, yr, 1, full = True)
        corr, p = pearsonr(xr, yr)
        print(f'{corr:.5f}y'.replace('0.', '.'))
        ax[i, j].plot(x, np.poly1d((a, b))(x), label = f'$y={nf(a)}x+{nf(b)}$'.replace('+-', '-'), color = '#ff0000')
        ax[i, j].plot([min(x)], [min(y)], label = f'$r={corr:.6f}$\n$p={p:.4f}$ ({len(xr)}/{len(x)} data)', color = '#ffffff')
      except: pass
      ax[i, j].legend(loc = 'upper center', bbox_to_anchor = (.5, -.25), handlelength = .5)
  fig.savefig(f'./graphs/yearly_plot_{target}.png', dpi = 720, pad_inches = .05)
  close()
  del fig, ax