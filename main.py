from typing import Union
from fastapi import FastAPI
import csv
import math
import json


data_dict = {}
 
with open('sea_level.csv', encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
    for rows in csv_reader:
      key = rows['ID']
      data_dict[key] = rows

def get_sealevel_past(year):
  shuma = 0.0
  sasia = 0
  for i in data_dict.keys():
    if int(float(data_dict[i].get(' Year'))) == year:
      shuma += float(data_dict[i].get('StdDevGMSL_noGIA'))
      sasia += 1
  
  return math.floor((shuma/sasia + 38.6) * 100)/100.0

def get_sealevel_future(year):
  yearly_sea_rise = 3.04
  return get_sealevel_past(2022) + (yearly_sea_rise * (year - 2022))

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
     "sea-level": sea_level}