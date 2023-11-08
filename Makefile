install: install_backend install_frontend download_weights

install_backend:
	cd backend && poetry install

install_frontend:
	cd frontend && npm install

run: run_backend run_frontend

run_frontend:
	cd frontend && ng serve

run_backend:
	cd backend && poetry run flask --app recommender/app run

download_weights:
	cd backend/recommender/recommender/pretrained/word2vec && curl -k -LO https://github.com/piskvorky/gensim-data/releases/download/word2vec-google-news-300/word2vec-google-news-300.gz
	cd backend/recommender/recommender/pretrained/word2vec && curl -k -o SO_vectors_200.bin -L https://zenodo.org/records/1199620/files/SO_vectors_200.bin?download=1
	cd backend/recommender/recommender/pretrained/fast_text && curl -k -LO https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip && unzip crawl-300d-2M-subword.zip && rm crawl-300d-2M-subword.zip && rm crawl-300d-2M-subword.vec
