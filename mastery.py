import requests
import pandas as pd
import common

api_key = common.api
encryptedPUUID="vl761d25onH3aHL6D1YrYo66jcKXb61Z0Foe5e299ACsT0aCibUl7aIftkMz2KrrPjz45FUVBN0i5g"
mastery_url = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}"+"?api_key=" + api_key

response = requests.get(mastery_url)
data = response.json()

print(data)



