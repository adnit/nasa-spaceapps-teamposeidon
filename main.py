from typing import Union
from fastapi import FastAPI
import csv
import math
import json


sea_level_dict = {}
co2_level_dict = {}
global_temp_dict = {}
 
with open('sea_level.csv', encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
    for rows in csv_reader:
      key = rows['ID']
      sea_level_dict[key] = rows

with open('co2.csv', encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
    for rows in csv_reader:
      key = rows['year']
      co2_level_dict[key] = rows

with open('global_temp.csv', encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
    for rows in csv_reader:
      key = rows['Year']
      global_temp_dict[key] = rows

def get_sealevel_past(year):
  shuma = 0.0
  sasia = 0
  for i in sea_level_dict.keys():
    if int(float(sea_level_dict[i].get(' Year'))) == year:
      shuma += float(sea_level_dict[i].get('StdDevGMSL_noGIA'))
      sasia += 1
  
  return math.floor((shuma/sasia + 38.6) * 100)/100.0

def get_sealevel_future(year):
  yearly_sea_rise = 3.04
  return (get_sealevel_past(2022) + (yearly_sea_rise * (int(year) - 2022)))

def get_co2(year):
  year = '%s' % year
  yearly_co2_rise = 1.8
  if int(year) <= 2021:
    return float(co2_level_dict[year].get('mean'))
  else:
    return float(get_co2(2021) + (yearly_co2_rise * (int(year) - 2021)))

def get_global_temp(year):
  year = '%s' % year
  yearly_temp_rise = 0.11
  if int(year) <= 2016:
    return float(global_temp_dict[year].get('Mean'))
  else:
    return float(get_global_temp(2016) + (yearly_temp_rise * (int(year) - 2016)))


def floor(a):
  return math.floor(a * 100)/100.0

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/sea-level/{year}")
def read_item(year: str, q: Union[str, None] = None):
    if int(year) > 2022:
      sea_level = get_sealevel_future(year)
    else:
      sea_level = get_sealevel_past(2022)
    
    return {"year": year,
     "sea-level": floor(sea_level),
     "co2-level": floor(get_co2(year)),
     "global_temp": floor(get_global_temp(year))}