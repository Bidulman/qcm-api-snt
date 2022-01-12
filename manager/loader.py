from config import LOADER

from os import listdir
from json import load


class Loader:

    def __init__(self):
        self.path = LOADER['QCM_FOLDER_PATH']
        self.loaded = []

    def load(self):
        for file in listdir(self.path):
            with open(self.path+file, 'r', encoding='utf-8') as file:
                self.loaded.append(load(file))
        return self.loaded
