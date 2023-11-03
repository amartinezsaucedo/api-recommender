import re
import spacy
import json
import os
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.models import Phrases
from gensim.models.phrases import Phraser

from backend.recommender.persistence.api import Endpoint

LEMMATIZED_APIS_FILE = 'recommender/data/lemmatized_apis.json'
API_INFO_FILE = 'recommender/data/api_info.json'


def get_component_if_both_and_info(data):
    result = []
    api_info = {}
    api_id = 0
    for api, info in data.items():
        for path, description in info.get('endpoints').items():
            api_info[api_id] = [api + path, api, path, description]
            api_id += 1
            result.append(description)
    return result, api_info


def openapi_preprocess(data):
    print("OpenAPI preprocess")
    data = [re.sub('<[^>]*>', '', sent) for sent in data]
    data = [
        re.sub(r'https?://(www\.)?[-a-zA-Z\d@:%._+~#=]{1,256}\.[a-zA-Z\d()]{1,6}\b([-a-zA-Z\d()@:%_+.~#?&/=]*)',
               '', sent) for sent in data]
    return data


def sentences_to_words(sentences):
    print("Convert sentences to words")
    for sentence in sentences:
        yield simple_preprocess(str(sentence), deacc=True)


def remove_stopwords(texts):
    print("Remove stopwords")
    stop_words = stopwords.words('english')
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def generate_bigrams_and_trigrams(data_words):
    print("Generate bigrams and trigrams")
    bigram = Phrases(data_words, min_count=5, threshold=100)
    trigram = Phrases(bigram[data_words], threshold=100)
    bigram_mod = Phraser(bigram)
    trigram_mod = Phraser(trigram)
    return bigram_mod, trigram_mod


def make_trigrams(trigrams, bigrams, texts):
    print("Make trigrams")
    return [trigrams[bigrams[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=None):
    print("Lemmatize words")
    if allowed_postags is None:
        allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        if allowed_postags is not None:
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        else:
            texts_out.append([token.lemma_ for token in doc])
    return texts_out


def transform_oapi_data(endpoints: list[Endpoint]):
    descriptions = [endpoint.description for endpoint in endpoints]
    descriptions = openapi_preprocess(descriptions)
    words = list(sentences_to_words(descriptions))
    bigrams, trigrams = generate_bigrams_and_trigrams(words)
    words_no_stopwords = remove_stopwords(words)
    words_trigrams = make_trigrams(trigrams, bigrams, words_no_stopwords)
    words_lemmatized = lemmatization(words_trigrams)
    lemmatized_apis = []
    for i in range(len(words_lemmatized)):
        if words_lemmatized[i] != [] and not words_lemmatized[i] in lemmatized_apis:
            lemmatized_apis.append(words_lemmatized[i])
            endpoints[i].bow = words_lemmatized[i]
    return endpoints


def load_transformed_data():
    with open(LEMMATIZED_APIS_FILE, 'r') as fp:
        lemmatized_apis = json.load(fp)
    with open(API_INFO_FILE, 'r') as fp:
        api_info = json.load(fp)
    return lemmatized_apis, api_info
