import configparser
from abc import ABC, abstractmethod

config = configparser.ConfigParser()
config.read('config.ini')


class configHandler(ABC):
    main_form_file = config['FILES']['main_form_file']
    add_form_file = config['FILES']['add_form_file']
    data_source = config['FILES']['data_source']
    passwd_source = config['FILES']['passwd_source']

    file_in_mode = config['ARGS']['file_in_mode']
    file_out_mode = config['ARGS']['file_out_mode']
    file_create_mode = config['ARGS']['file_create_mode']
    key_storage = config['ARGS']['key_storage']
    charset = config['ARGS']['charset']

    main_css = config['STYLES']['stylesheet']
    checkbox_css = config['STYLES']['box_stylesheet']

    @abstractmethod
    def do_not_inherit(self):
        pass
