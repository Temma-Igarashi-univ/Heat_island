from multiprocessing import Pool, set_start_method
from dill import dump, load
import numpy as np
from collections import defaultdict
from geographiclib.geodesic import Geodesic, GeodesicCapability
from warnings import catch_warnings

with open ('./data.pkl', 'rb') as f: values = load(f)
ura_set, obj, obs, calc_dist, pol = values['ura_set'], values['obj'], values['obs'], values['calc_dist'], values['pol']

def predict_density(year, pol_name):
  """汚染物質濃度算定。ここで会計年度基準を通常年基準に直す。"""
  # Estimation of the pollutant density at the temperature measurement observatories.
  # Return value is a list of calculated density values from Jan. to Dec.
  ret = dict()
  for place in ura_set:
    la, lo = obj[place]['coord']
    deno = np.zeros(12)
    nume = np.zeros(12)
    for k, v in obs[year-1].items():
      vla, vlo = v
      if not pol[year-1][pol_name][k] or any([item is None for item in {la, lo, vla, vlo}]): continue
      for mon in range(9, 12):
        nume[mon-9] += (calc_dist(la, lo, vla, vlo) / 10000)**-1 * pol[year-1][pol_name][k][mon]
        deno[mon-9] += (calc_dist(la, lo, vla, vlo) / 10000)**-1
    for k, v in obs[year].items():
      vla, vlo = v
      if not pol[year][pol_name][k] or any([item is None for item in {la, lo, vla, vlo}]): continue
      for mon in range(9):
        nume[mon+3] += (calc_dist(la, lo, vla, vlo) / 10000)**-1 * pol[year][pol_name][k][mon]
        deno[mon+3] += (calc_dist(la, lo, vla, vlo) / 10000)**-1
    ret[place] = nume / deno
  print('*', end =  '', flush = True)
  return ret

pol_names = {'NMHC', 'CO', 'NO2', 'PM25', 'THC', 'SP', 'SPM', 'SO2', 'NOX', 'CH4', 'OX', 'NO'}

def multi_epd_calculator(year):
  return year, {pol_name: predict_density(year, pol_name) for pol_name in pol_names}

# 対応地点の汚染物質濃度推定 Pollutant density estimation at the correspondent points
# epd[年][汚染物質][地点名] = その年の汚染物質データ
# epd[year][pollutant][location] = The year's pollutant density data
if __name__ == '__main__':
  set_start_method('fork')
  with catch_warnings(action = 'ignore', category = RuntimeWarning):
    with Pool(40) as p: val = p.map(multi_epd_calculator, range(1980, 2020))
  epd = {k: v for k, v in val}
  with open('./epd.pkl', 'wb') as f: dump(epd, f)