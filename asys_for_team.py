# importしないこと！ This file cannot be imported.
# グループワーク用 for group research in the ALESS lesson.
import math
def tan(deg): return math.tan(math.radians(deg))
def atan(val): return math.degrees(math.atan(val))
def cos(deg): return math.cos(math.radians(deg))
def sin(deg): return math.sin(math.radians(deg))

from sys import argv
from collections import defaultdict
import csv, json
from os import listdir
from dill import dump, load

import numpy as np
from geographiclib.geodesic import Geodesic, GeodesicCapability

from temptest import get_table

# 環境 environment
temp_coord_file = './coord_for_team.json'

# 国立環境研究所環境展望台の大気汚染常時監視データと測定局データ (関東地方分、なければ全国分) を解凍しフォルダ名を以下のように設定しこの位置におく。
# ダウンロードするとzipファイル→txtファイルになるのですべてcsvに置き換えておく。
# Download the Kanto region's data (or data from across Japan) from NIES's website,
# unzip, rename the folders you get and set them in the following location.
# You also have to rename every files in the folders (.txt to .csv)
observatory_dir = '../../Datasets/Observatory/'
pollution_dir = '../../Datasets/Pollution/'

# 観測所データ所在地 The observatory data were taken from:
# https://www.nies.go.jp/igreen/tm_down.html
# 汚染物質データ所在地 The pollutant data were taken from:
# https://tenbou.nies.go.jp/download/

# 距離計算 distance calculation between two points on a world map (GRS80)
def calc_dist(lat_0, lon_0, lat_1, lon_1):
  return Geodesic(6378137, 298.257222101**-1).Inverse(lat_0, lon_0, lat_1, lon_1, GeodesicCapability().DISTANCE)['s12']
  
# 緯度経度及び測定所高度 latitude / longtitude / altitude of observatories
with open(temp_coord_file, 'r') as tc: pre_obj = json.load(tc)
del pre_obj['凡例']
obj = {ky: {'coord':( vl[0]+vl[1]/60, vl[2]+vl[3]/60), 'height': vl[4]} for ky, vl in pre_obj.items()}

def filt(value_partial, value_ent, designation):
  return int(value_partial == designation) + int(designation in value_ent)

# 各汚染物質測定地点の緯度経度、物質測定値 Each observatory's location / pollutant density data
# こちらは会計年度カウントしているので注意 each year's data are stored from Apr. to Mar.
pol = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
obs = defaultdict(lambda: defaultdict(lambda: (None, None)))

# pol[年][物質名][測定局コード] = 測定値, 4-3月
# pol[year][pollutant][observatory code] = pollutant density measured at the observatory in the year
# obs[年][測定局コード] = その年の座標
# obs[year][observatory code] = The observatory's location data in the year

# pol
for csv_name in listdir(pollution_dir):
  if csv_name == '!凡例.txt': continue
  if csv_name[0] == '.': continue
  try:
    with open(pollution_dir+csv_name, 'r', encoding='cp932') as ot: obsfile = [items for items in csv.reader(ot)]
    if filt(obsfile[0][47][:4], obsfile[0][47], '月平均値') >= filt(obsfile[0][59][:4], obsfile[0][59], '月平均値'): average_ind = 47
    else: average_ind = 59
    for item in obsfile[1:]:
      if all(item[average_ind:average_ind+12]): pol[int(csv_name[2:6])][item[3]][int(item[11])] = [float(item[ind]) for ind in range(average_ind, average_ind+12)]
  except UnicodeDecodeError: print('Discarded: ', csv_name)

# 1980-2019
for csv_name in sorted(listdir(observatory_dir)):
  if csv_name == '!凡例.txt': continue
  if csv_name[0] == '.': continue
  with open(observatory_dir+csv_name, 'r', encoding='cp932') as ot: obsfile = [items for items in csv.reader(ot)]
  for item in obsfile[1:]:
    if item[9]: obs[int(csv_name[2:6])][int(item[1])] = \
      (float(item[9])+float(item[10])/60+float(item[11])/3600, float(item[12])+float(item[13])/60+float(item[14])/3600)
    elif obs[int(csv_name[2:6])-1][int(item[1])] != (None, None):
      obs[int(csv_name[2:6])][int(item[1])] = obs[int(csv_name[2:6])-1][int(item[1])]
    else: continue

# UHIIと観測所 UHII-observatory data
# tmp[年][地点名] = 12ヶ月分の平均気温の高度補正済みデータ
# tmp[year][location name] = monthly average temperature data in the year (with altitude effect correction)
# uhi[年][地点名] = その年のuhii12ヶ月分。平均とったら年uhii
# uhi[year][location name] = The year's monthly UHII. Their average is the year's UHII.
# 正規の「年」に基づくデータ保存形式 each year's data are stored from Jan. to Dec. (tmp, uhi)

tmp = defaultdict(lambda: defaultdict(list))
uhi = defaultdict(lambda: defaultdict(list))
pln_set = set(obj.keys())
nua_set = {'久喜', 'つくば', '牛久', '海老名', '八王子'}
ura_set = pln_set - nua_set

# 気温データ収集 (1980-2019) Temperature data collection (1980-2019)
if len(argv) > 1 and argv[1] != 'no-collection' or len(argv) == 1:
  for year in range(1980, 2020):
    for num in range(40, 47):
      for name, dat12 in get_table(num, year):
        for objective in pln_set:
          if name in objective or objective in name:
            tmp[year][objective] = dat12 + obj[objective]['height'] * 5.5e-3
            break
else:
  with open('./data.pkl', 'rb') as f: data = load(f)
  tmp = data['tmp']

def calc_uhii(place, year):
  main_place = tmp[year][place]
  nu_factors = [tmp[year][name] for name in nua_set if bool(list(tmp[year].get(name)))]
  return [sum([main_place[i]-nu_factor[i] for nu_factor in nu_factors])/len(nu_factors) for i in range(12)]
  
for year in range(1980, 2020):
  for place in ura_set:
    try: uhi[year][place] = calc_uhii(place, year)
    except: print(f'Discarded (UHII): {year}, {place}')

pickle_object = {'tmp': tmp, 'uhi': uhi, 'ura_set': ura_set, 'obs': obs, 'obj': obj, 'pol': pol, 'calc_dist': calc_dist}
with open('./data.pkl', 'wb') as f: dump(pickle_object, f)