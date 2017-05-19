import re
import openpyxl as opx
import json
from shutil import copyfile
import datetime
from docx import Document
from transliterate import translit
import os
from functools import reduce
import datetime 


PERSON_FIELDS = ['brothers', 'sisters', 'children', 'clerics']


class DocxHandler(object):
    person_keys = PERSON_FIELDS


    def __init__(self, json_string):
        self.json_string = json.loads(json_string)
        self.persons = self.__get_persons_only()
        self.doc_name = self.__doc_name()
        copyfile('src/1.docx', self.doc_name)
        self.document = Document(self.doc_name)
        self.__add_autofields_to_json()

    def create_docx(self):
        for k in self.json_string:
            self.__insert_value_in_cell(k)
        self.document.save(self.doc_name)
        return self.doc_name

    def __doc_name(self):
        doc_name = 'out/%s_%s.docx' % ( 
            self.json_string['group_name'], str(datetime.datetime.now()) 
        )
        try: 
            doc_name = translit(doc_name, reversed=True)
        except:
            pass
        return doc_name

    def __insert_value_in_cell(self, key):
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if ('X'+key+'X') in cell.text:
                        cell.text = self.json_string[key]

    def __extract_date(self, dte_str):
        dte = datetime.datetime.strptime(dte_str, '%d %b, %Y')
        return dte

    def __get_persons_only(self):
        return {p:self.json_string[p] for p in self.person_keys}

    def __total_persons(self):
        return reduce((lambda x, y: x + int(self.persons[y])), self.persons, 0)

    def __add_autofields_to_json(self):
        self.json_string['total_persons'] = str(self.__total_persons())
        delta = self.__extract_date(self.json_string['date_dep']) - self.__extract_date(self.json_string['date_arr'])
        self.json_string['nights'] = str(delta.days)
        
