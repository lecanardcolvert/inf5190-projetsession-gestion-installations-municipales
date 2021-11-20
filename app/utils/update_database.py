import traceback
import urllib3
import xmltodict
import csv
from io import StringIO

piscine_url = (
    "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e13615"
    "8133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/"
    "piscines.csv"
)
patinoire_url = (
    "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce"
    "1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/"
    "l29-patinoire.xml"
)
glissade_url = (
    "http://www2.ville.montreal.qc.ca/services_citoyens/"
    "pdf_transfert/L29_GLISSADE.xml"
)
http = urllib3.PoolManager()
response = http.request("GET", glissade_url)
response2 = http.request("GET", piscine_url)
response3 = http.request("GET", patinoire_url)
try:
    data = xmltodict.parse(response.data)
    print(data["glissades"]["glissade"][0]["nom"])
    print("------------------------------")
    content = response2.data.decode()
    file = StringIO(content)
    data = csv.reader(file, delimiter=",")
    for row in data:
        print(row[3])
    # content2 = [line.decode("utf-8") for line in response2.data.readlines()]
    print("------------------------------")
    data = xmltodict.parse(response3.data)
    print(data["MAIN"]["arrondissement"][0]["nom_arr"])
except:
    print("Failed to parse xml from response (%s)" % traceback.format_exc())
