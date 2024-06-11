from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl
import os

##INICIA ARCHIVOS DE REGISTRO
try: os.mkdir("rdf")
except: None

try: os.mkdir("registros");
except: None

resultado = open ('registros/OntologiasIOT.csv', 'w', encoding='utf-8'); resultado.truncate();
resultado.write ('Vocabulario;Uri;Respuesta;Descargado;Tag;\n')

##CARGA TODOS LOS VOCABULARIOS Y URI'S DE LOV
voc={}
con=0
url = 'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list'
data = requests.get(url)
if data.status_code == 200:
    data = data.json()
    for i in data: voc.update({i["prefix"] : i["uri"]}); con+=1
    print(f'Vocabularios cargados : {con}')
else: print('Error en la uri de Ontologias\nIntentelo de nuevo más tarde')

##CARGA RESPUESTA URI Y CARGA LAS ETIQUETAS
con=0
for i in voc.keys():
    url = "https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/info?vocab="+i
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        tags=data['tags']

        ##FILTRADO POR IOT
        if not "null" in tags:

            ##COMPRUEBA DISPONIBILIDAD WEB
            try:
                req = requests.get(voc[i], timeout=10);
                web = req.status_code
            except: web = 504

            ##DESCARGA RDF
            try:
                response = requests.get(voc[i], timeout=10, headers={'Accept': 'application/rdf+xml'})
                with open("rdf/"+i+".rdf", 'wb') as f: f.write(response.content)               
                descarga="si"; 
            except: descarga="no";
            print(f"{con+1} - {i} - {web} - {descarga}")

            ##REGISTRA DATOS
            text=i+";"+voc[i]+";"+str(web)+";"+descarga+";"
            for e in range(len(tags)):text+=tags[e]+";"
            resultado.write(text+"\n"); con+=1

    else: print('Error en la uri de etiquetas\nIntentelo de nuevo más tarde')

resultado.close()
print(f'Detectadas {con} Ontologias de IoT')
print('Datos guardados en OntologiasIOT.csv')
input("Pulsa enter para finalizar")
