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


we have json file that contain a lot of many info of products,
we can use this command to fetch it and store in db:

python app/process_images.py products.json batch-size

make sure your db is UP.

when u send a text query to this end point:  "/search-images"

it will return a list of images that match the query. like this:

[
    {
        "id": "2073427",
        "score": 0.95
    },
    {
        "id": "2073427",
        "score": 0.92
    }
    // More results...
]

# test 

for test run:

pytest /tests


## front 

for frontend we use vue.js 


## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```


# keyword search 

for this purpose we use meilisearch
for run it by docker use this command:


for load json (products.json) use this command:

python scripts/load_products_to_meilisearch.py path_to_your/products.json
