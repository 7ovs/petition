import json
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

class Localizator(object):
    def __init__(self, language='en'):
        self.language = language
        self.localization = self.__extract_localization_dict()
        self.localizated_form_fields =  self.__localizated_form_fields()
        self.__set_titles_as_attrs()
        delattr(self, 'localization')

    def __extract_localization_dict(self):
        """load json localization file as dict to extrcat data by key"""
        with open(dir_path+'/'+'localization.json') as json_data:
            localization = json.load(json_data)
        return localization

    def __set_titles_as_attrs(self):
    	for k, name_by_languages in self.localization['titles'].items():
    		setattr(self, k, name_by_languages[self.language])

    def __localizated_form_fields(self):
        form_fields = self.localization['form_fields']
        localizated_form_fields = {k:name_by_languages[self.language] for k, name_by_languages in form_fields.items()}
        return localizated_form_fields