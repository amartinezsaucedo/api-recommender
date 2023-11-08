# API Recommendation based on Word Embeddings
***
## Available endpoints

### Recommendations `/recommendations`
**GET** Get `k` recommendations based on user query
```
GET /recommendations?query={query}&algorithm={algorithm}&model={model}&k={k}
```

####     Request parameters

- `query` string **required**
- `algorithm` string **required**
- `model` string **required**
- `k` int **required**

Example
```
GET /recommendations?query=upload%20video&algorithm=fast_text&model=crawl-300d-2M-subword.bin&k=5
```
***
### Models `/models`
**GET** Get available word embeddings models
***
### Dataset information `/dataset`
**PATCH** Update APIs definition (forces APIs.guru files to be downloaded and processed again)

**GET** Get dataset metadata
***
### Tasks `/tasks?task_id={task_id}`
**GET** Get available word embeddings models

####     Request parameters

- `task_id` string **required**
