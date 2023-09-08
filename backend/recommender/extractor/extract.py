import os
import requests
import re
from pathlib import Path
import zipfile
import pickle
from ruamel.yaml import YAML

yaml = YAML()

GITHUB_REPO_URL = 'https://api.github.com/repos/APIs-guru/openapi-directory/{action}/{ref}'
APIS_SOURCE_FOLDER_NAME = 'APIs/'
APIS_TARGET_FOLDER_NAME = 'backend/recommender/data/APIs/'
DATASET_COMMIT_FILENAME = 'backend/recommender/data/dataset_info.txt'
DATA_FILENAME = "backend/recommender/data/data.txt"
ERROR_FILENAME = "backend/recommender/data/error.txt"


def extract_oapi_data():
    data_file_exists = os.path.isfile(DATA_FILENAME)
    api_folder_exists = os.path.isdir(APIS_TARGET_FOLDER_NAME)
    if data_file_exists:
        data_list = load_list(DATA_FILENAME)
    else:
        if not api_folder_exists:
            download_raw_data()
            print('Dataset downloaded')
        print('Processing APIs')
        data_list = generate_list(DATA_FILENAME, ERROR_FILENAME, APIS_TARGET_FOLDER_NAME)
    print('APIs loaded')
    print('Number of APIs: ' + str(len(data_list)))
    print('Number of endpoints: ' + str(sum(len(api['endpoints'].values()) for api in data_list.values())))
    return data_list


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


def load_list(file):
    with open(file, 'rb') as fp:
        itemlist = pickle.load(fp)
    return itemlist


def generate_list(file, error_file, dataset_location):
    data_list = {}
    unprocessed_data_list = {}
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for base, _, files in os.walk(dataset_location):
        for f in files:
            if f == 'swagger.yaml' or f == 'openapi.yaml':
                API = base.replace(APIS_TARGET_FOLDER_NAME, '')
                try:
                    with open(os.path.join(base, f), encoding='utf8') as yaml_file:
                        data = yaml.load(yaml_file)
                    print((API + '/' + f))
                    data_list[API] = {'description': '', 'endpoints': {}}
                    if 'info' in data and 'description' in data['info']:
                        data_list[API]['description'] = data['info']['description']
                    for api in data['paths'].keys():
                        for methodHTTP in data['paths'][api].keys():
                            if methodHTTP.lower() in accepted_meth:
                                data_list[API]['endpoints'][api + '/' + methodHTTP] = ''
                                if 'description' in list(data['paths'][api][methodHTTP].keys()):
                                    data_list[API]['endpoints'][api + '/' + methodHTTP] = \
                                        data['paths'][api][methodHTTP]['description']
                except Exception as e:
                    print('Not processed: ' + API + '/' + f)
                    unprocessed_data_list[API] = {f, e}
                    pass
    save_list(error_file, unprocessed_data_list)
    save_list(file, data_list)
    return data_list


def save_list(file, itemlist):
    with open(file, 'wb') as fp:
        pickle.dump(itemlist, fp)
