import configparser
from abc import ABC, abstractmethod

config = configparser.ConfigParser()
config.read('config.ini')


class configHandler(ABC):
    ui_file = config['FILES']['ui_file']
    data_source = config['FILES']['data_source']

    file_in_mode = config['ARGS']['file_in_mode']
    file_out_mode = config['ARGS']['file_out_mode']
    charset = config['ARGS']['charset']

    main_css = config['STYLES']['stylesheet']
    checkbox_css = config['STYLES']['box_stylesheet']

    sha_key = config['SHA256']['key']

    @abstractmethod
    def do_not_inherit(self):
        pass
