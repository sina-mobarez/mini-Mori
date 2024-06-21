# mini-Mori
powefull and simple search engine through images using nlp and clip(openai) 


# vector db

in this project we use vector db to store images and text and then use nlp to search images and text
we use qdrant as vector db
for run locally use docker image 

docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant

# backend 

for backend we use fastapi to implement some endpoint that accept text and return result 

for run it must install fastapi and other dependency and :

fastapi dev main.py ----- for develop env
and 
fastapi run ---- for production 