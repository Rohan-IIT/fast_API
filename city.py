from fastapi import FastAPI, Path
from pydantic import BaseModel
import requests

app = FastAPI()

@app.get('/')
def index():
    return{'message': 'FastAPI test'}

db = []

class City(BaseModel):
    name: str
    timezone: str

# p = requests.get('http://api.weatherstack.com/current?access_key=f536d0223f2c50e88790a3efcbb2600d&query=Chicago')
# print(p.json())

    
@app.get('/cities/')
def get_cities():
    results = []
    print("result => ", results)
    for city in db:

        p = f'http://api.weatherstack.com/current?access_key=f536d0223f2c50e88790a3efcbb2600d&query={city["timezone"]}'
        response = requests.get(p)
        weather_API = response.json()

        l = weather_API.get("current", {}).get("temperature")
  
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = r.json()['datetime']
        results.append({'query':city['name'],'timezone':city['timezone'], 'temperature': l ,'current_time':current_time})
        print("result => ", results)
    return results

@app.get('/cities/{city_id}/')
def get_city(city_id: int):
    return db[city_id-1]

@app.post('/cities/')
def add_city(city:City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}/')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}