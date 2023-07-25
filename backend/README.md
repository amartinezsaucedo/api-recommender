# API Recommendation based on Word Embeddings
***
## Available endpoints

### Recommendations `/recommendations`
**GET** Get recommendations based on user query
```
GET /recommendations?query={query}&algorithm={algorithm}&model={model}
```

####     Request parameters

- `query` string **required**
- `algorithm` string **required**
- `model` string **required**

Example
```
GET /recommendations?query=upload%20video&algorithm=fast_text&model=crawl-300d-2M-subword.bin
```
***
### Models `/models`
**GET** Get available word embeddings models
***
### APIs `/apis`
**PATCH** Update APIs definition (forces APIs.guru files to be downloaded and processed again)
