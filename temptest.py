from time import sleep
import re
from collections import defaultdict as dd

import numpy as np
import selenium, bs4
import chromedriver_binary
import selenium.webdriver

bs = bs4.BeautifulSoup

url = 'https://www.data.jma.go.jp/stats/etrn/view/monthly_h1.php?prec_no=NN&block_no=00&year=YYYY&month=&day=&view=p2'

def get_table(place, year):
  """
  Parameters
  ----------
  :place: 数値。40-46が順に茨城、栃木、群馬、埼玉、東京、千葉、神奈川に対応。\n
  :year: 年。年度ではない。1980-2019。
  """
  # :place: number. 40(Ibaraki), 41(Tochigi), 42(Gumma), 43(Saitma), 44(Tokyo), 45(Chiba), 46(Kanagawa).
  # :year: number between 1980-2019.

  print(f'Collecting data in {year}')
  valid_url = url.replace('NN', f'{place}').replace('YYYY', f'{year}')
  option = selenium.webdriver.ChromeOptions()
  option.add_argument('--user-agent=MeteorologyStudyDataCollecter (through Google Chrome/selenium, your-mail@address.com)')
  option.add_argument('--headless')
  driver = selenium.webdriver.Chrome(option)
  driver.get(valid_url)
  sleep(2)
  parser = bs(driver.page_source.encode(), 'html.parser')
  driver.close(); driver.quit()
  try:
    items = parser.find_all('tr', {'class':'mtx'})
    itemh = [[str(item).replace('<th>', '').replace('</th>', '') for item in itemholder.find_all('th')[1:]] for itemholder in items][0]
    itemd = [
      [float(re.sub(r"[^\d.]", "", str(item).replace('<td class="data_0_0">', '').replace('</td>', ''))) \
        for item in itemholder.find_all('td')[1:]] \
        for itemholder in items
    ][1:]
    return list(zip(itemh, np.array(itemd).T))
  except:
    print(f'Discarded: (place, year) = ({place}, {year})')
    return []