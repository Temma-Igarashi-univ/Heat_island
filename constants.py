# variable container
from dill import load

with open('./epd.pkl', 'rb') as f: _EPD = load(f)
with open('./data.pkl', 'rb') as f: data = load(f)
_UHI = data['uhi']
URBAN_AREA_NAMESET = data['ura_set']
POLLUTANT_NAMES = {'NMHC', 'CO', 'NO2', 'PM25', 'THC', 'SP', 'SPM', 'SO2', 'NOX', 'CH4', 'OX', 'NO'}
UNITS = {
  'SO2':'ppm', 'NO':'ppm', 'NO2':'ppm', 'NOX':'ppm',
  'CO':'ppm', 'OX':'ppm', 'NMHC':'ppmC', 'CH4':'ppmC',
  'THC':'ppmC', 'SPM':'mg \\ m^{-3}', 'SP':'mg \\ m^{-3}', 'PM25':'\\mu g \\ m^{-3}', 
}

# numpy-like expression
class EstimatedPollutantDensity:
  """推計された汚染物質濃度を保持するクラス。"""
  # The class which contains estimated pollutant density values.
  def __init__(self, dictionary = None):
    self.epd = _EPD if dictionary is None else dictionary

  def __getitem__(self, item):
    """e = EstimatedPollutantDensity() とすると\n
    e[y] = y年の汚染物質と場所の全データ\n
    e[y, p] = y年の汚染物質pの全場所データ\n
    e[y, p, l] = y年の汚染物質pの場所lにおけるデータ\n
    e[y, p, l, m] = y年の物質pの場所lにおけるデータm月号"""
    # when e = EstimatedPollutantDensity(),
    # e[y] = All estimated pollutant data in the year y
    # e[y, p] = Pollutant p's estimated data in the year y
    # e[y, p, l] = Pollutant p's estimated data at the temperature observatory l in the year y
    # e[y, p, l, m] = Pollutant p's estimated data at the temperature observatory l in m[month]/y[year]

    try: l = len(item)
    except: l = 1
    if l == 1: return self.epd[item]
    if l == 2: return self.epd[item[0]][item[1]]
    if l == 3: return self.epd[item[0]][item[1]][item[2]]
    if l == 4: return self.epd[item[0]][item[1]][item[2]][item[3]]
    else: raise ValueError('You can indicate 4 indices or less.')

ESTIMATED_POLLUTANT_DENSITY = EstimatedPollutantDensity()

class Uhii:
  """UHIIを返すクラス。"""
  # The class which contains UHII data.
  def __init__(self, dictionary = None):
    self.uhii = _UHI if dictionary is None else dictionary
  
  def __getitem__(self, item):
    """u = Uhii() とすると\n
    u[y] = y年のUHIIの場所別全データ\n
    u[y, l] = y年の場所lにおける月別UHII12ヶ月分\n
    u[y, l, m] = y年の場所lにおけるm月のUHII
    """
    # when u = Uhii(),
    # u[y] = All UHII data in the year y
    # u[y, l] = All UHII data at the temperature observatory l in the year y
    # u[y, l, m] = All UHII data at the temperature observatory l in m[month]/y[year]

    try: l = len(item)
    except: l = 1
    if l == 1: return self.uhii[item]
    if l == 2: return self.uhii[item[0]][item[1]]
    if l == 3: return self.uhii[item[0]][item[1]][item[2]]
    else: raise ValueError('You can indicate 3 indices or less.')

UHII = Uhii()