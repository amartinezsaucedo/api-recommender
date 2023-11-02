import os
import requests
import re
from pathlib import Path
import zipfile
from ruamel.yaml import YAML

from backend.recommender.persistence.api import Endpoint

yaml = YAML()

GITHUB_REPO_URL = 'https://api.github.com/repos/APIs-guru/openapi-directory/{action}/{ref}'
APIS_SOURCE_FOLDER_NAME = 'APIs/'
APIS_TARGET_FOLDER_NAME = 'backend/recommender/data/APIs/'
DATASET_COMMIT_FILENAME = 'backend/recommender/data/dataset_info.txt'
DATA_FILENAME = "backend/recommender/data/data.txt"
ERROR_FILENAME = "backend/recommender/data/error.txt"


def extract_oapi_data():
    api_folder_exists = os.path.isdir(APIS_TARGET_FOLDER_NAME)
    if not api_folder_exists:
        download_raw_data()
        print('Dataset downloaded')
    print('Processing APIs')
    apis = generate_list(APIS_TARGET_FOLDER_NAME)
    print('APIs loaded')
    print('Number of APIs: ' + str(len(apis)))
    print('Number of endpoints: ' + str(len(apis)))
    return apis


def download_raw_data(ref='main', target_folder_name=APIS_TARGET_FOLDER_NAME):
    response = requests.get(GITHUB_REPO_URL.format(action='zipball', ref=ref))
    if response.ok:
        filename = get_repo_zip_filename(response.headers)
        commit = get_commit(ref)
        target_folder_filename = create_target_folder(target_folder_name)
        print('Downloading dataset')
        download_zip(filename, response.content)
        print('Unzipping repository')
        unzip_api_folder(filename, target_folder_filename)
        delete_downloaded_zip(filename)
        save_dataset_commit(commit)
    else:
        print('An error occurred when attempting to download Open API documentation')


def get_repo_zip_filename(headers):
    filename = re.findall('filename=(.+)', headers['content-disposition'])[0]
    return os.path.join(os.getcwd(), filename)


def get_commit(ref):
    if ref != 'main':
        return ref
    response = requests.get(GITHUB_REPO_URL.format(action='commits', ref=ref))
    if response.ok:
        return response.json()['sha']


def create_target_folder(target_folder_name):
    target_folder_filename = os.path.join(os.getcwd(), target_folder_name)
    Path(target_folder_filename).mkdir(parents=True, exist_ok=True)
    return target_folder_filename


def download_zip(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)


def unzip_api_folder(filename, target_folder_filename):
    with zipfile.ZipFile(filename) as archive:
        for file_info in archive.infolist():
            is_file = file_info.filename[-1] != '/'
            if APIS_SOURCE_FOLDER_NAME in file_info.filename and is_file:
                file_info.filename = remove_parent_directory(file_info.filename)
                archive.extract(file_info, target_folder_filename)


def remove_parent_directory(filename):
    return ''.join(filename.split('/', 2)[2:])


def delete_downloaded_zip(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def save_dataset_commit(commit):
    with open(DATASET_COMMIT_FILENAME, 'w') as file:
        file.write(commit)


def generate_list(dataset_location):
    apis = []
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for absolute_base, _, files in os.walk(dataset_location):
        for f in files:
            if f in ['swagger.yaml', 'openapi.yaml']:
                base = absolute_base.replace(APIS_TARGET_FOLDER_NAME, '')
                try:
                    with open(os.path.join(absolute_base, f), encoding='utf8') as yaml_file:
                        data = yaml.load(yaml_file)
                    print((base + '/' + f))
                    for api in data['paths'].keys():
                        for methodHTTP in data['paths'][api].keys():
                            if methodHTTP.lower() in accepted_meth:
                                if 'description' in list(data['paths'][api][methodHTTP].keys()):
                                    apis.append(Endpoint(endpoint=f"{base}{api}/{methodHTTP}",
                                                         description=data['paths'][api][methodHTTP]['description']))
                except Exception as e:
                    print('Not processed: ' + base + '/' + f)
                    pass
    return apis
