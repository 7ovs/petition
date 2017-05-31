from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash, send_file
import json
from forms import Step1Form, Step2Form, Step3Form 
import models 
from sqlalchemy import update
from functools import reduce
from create_docx import DocxHandler
from flask_httpauth import HTTPBasicAuth
from localization.localizator import Localizator


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "tatiana": "OVS",
    "artiom": "OVS"
}

GROUP_INFO = 'group_info'
GUEST_KEY = 'guest_id'
PERSON_FIELDS = ['brothers', 'sisters', 'children', 'сlergy']
EMPTY_PERSON_DICT = {"sisters":[], "brothers":[], "сlergy":[], "children":[]}


class PetitionRepresentation(object):
    """Class to represent a petition in Admin"""
    person_keys = PERSON_FIELDS
    ready_state = "готово"
    not_ready_state = "в процессе заполнения"
    representative_fields = ['group_name', 'date_arr', 'date_dep', 'senior']

    def __init__(self, pk, json_string):
        self.json_string = json.loads(json_string)
        self.pk = pk
        self.persons = self.__get_persons_only()
        self.__set_represantation(json_string)
        
    def __set_represantation(self, json_string):
        for i in self.representative_fields:#assign class variables and give them value of json_string
            setattr(self, i, self.json_string.get(i) or "--")
        self.is_ready =  self.__is_ready()

    def __is_ready(self):
        for i in self.json_string:
            if not self.json_string[i]:
                return self.not_ready_state
        #if all person field are 0
        zero_persons = {p:self.persons[p] for p in self.persons if self.persons=='0'}
        if len(zero_persons) == len(self.person_keys):
            return self.not_ready_state
        return self.ready_state

    def __get_persons_only(self):
        return {p:self.json_string[p] for p in self.person_keys}


    def __total_persons(self):
        x = 0
        for i in PERSON_FIELDS:
            x += len(self.persons[i])
        return i


class RequestFormData(object):
    cell_names = ['sisters cell', 'brothers cell', 'сlergy cell', 'children cell']
    persons = EMPTY_PERSON_DICT

    def __init__(self, request):
        session[GROUP_INFO] = session.get(GROUP_INFO) or {"group_name":None}
        self.request = request
        self.post_data = self.__data_for_post_form()

    def save_to_session(self):
        self.__person_fields_to_lists()
        session[GROUP_INFO].update(self.post_data)
        session[GROUP_INFO] = session[GROUP_INFO]

    def __data_for_post_form(self):
        post_data = {k:self.request.form[k] for k in self.request.form if self.request.form[k]}
        post_data.update(self.persons)
        return post_data

    def __person_fields_to_lists(self):
        """fetch person fields and rebuild them as a dict (e.g. {"sisters":[...], "brothers":[...])"""
        for k, v in self.post_data.items():
            if self.__person_cell(k):
                splitted_key = self.__person_key_into_dict(k)
                person_kind = splitted_key['person_kind']
                self.persons[person_kind].append(v)
                print(self.persons)
        self.__delete_person_cell_fields()
        self.post_data.update(self.persons)
        self.persons = {i:[] for i in self.persons}

    def __create_person_keys(self):
        pass       

    def __person_key_into_dict(self, k):
        """split a key into a list and make a dict from this list"""
        key_part_names = ['person_kind', 'no_need', 'number']
        key_into_dict = dict(zip(key_part_names, k.split(' ')))
        return key_into_dict

    def __person_cell(self, k):
        """Check if a key is in persons"""
        for cell_name in self.cell_names:
            if cell_name in k:
                return 1
        return None

    def __delete_person_cell_fields(self):
        self.post_data = {k : v for k, v in self.post_data.items() if not self.__person_cell(k)}


class BaseView(object):
    model = models.Guest
    db_session  = models.session
    person_keys = PERSON_FIELDS
    first_form = 'step1'

    def reset_guest():
        session[GUEST_KEY] = None
        session[GROUP_INFO].clear()


class AdminView(BaseView):
    @classmethod
    def show(cls):
        localizator = Localizator(session.get('language')) if session.get('language') else Localizator('en')
        petitions = cls.db_session.query(cls.model).all()
        petitions = [PetitionRepresentation( p.id, p.json_string)  for p in petitions]
        return render_template('admin.html', petitions=petitions, localizator=localizator)

    @classmethod
    def new_form(cls):
        cls.reset_guest()
        return redirect(url_for(cls.first_form))

    @classmethod
    def change_guest(cls, pk):
        session[GUEST_KEY] = pk
        json_string = cls.db_session.query(cls.model).get(session[GUEST_KEY]).json_string
        info = json.loads(json_string)
        session[GROUP_INFO] = info
        return redirect(url_for(cls.first_form))

    @classmethod
    def create_docx(cls, pk):
        json_string = cls.db_session.query(cls.model).get(pk).json_string
        doc_name = DocxHandler(json_string).create_docx()
        return send_file(doc_name, as_attachment=True)


class ChooseLanguage(BaseView):
    @classmethod
    def show(cls):
        localizator = Localizator(session.get('language')) if session.get('language') else Localizator('en')
        cls.reset_guest()
        session['language'] = None
        if request.method == 'GET':
            return render_template('index.html', localizator=localizator)
        elif request.method == 'POST':
            session['language'] = request.form['language']
            session[GROUP_INFO] = {"group_name":None}
            return redirect(url_for('step1'))


class Application(BaseView):
    @classmethod
    def show(cls):
        localizator = Localizator(session.get('language')) if session.get('language') else Localizator('en')
        json_string = json.dumps(session[GROUP_INFO])
        print(session.get(GUEST_KEY))
        if session.get(GUEST_KEY):
            guest = cls.db_session.query(cls.model).get(session[GUEST_KEY])
            guest.json_string = json_string
        else:
            guest = cls.model(json_string)
            cls.db_session.add(guest)
        cls.db_session.commit()
        cls.reset_guest()
        return render_template('applied.html', localizator=localizator)


class StepView(BaseView):
    @classmethod
    def show(cls, current_page, next_page, formClass=None):
        localizator = Localizator(session.get('language')) if session.get('language') else Localizator('en')
        if not session.get(GROUP_INFO):
            return redirect(url_for('choose_language'))

        elif request.method == 'POST':
            form_data = RequestFormData(request)
            form = formClass(**form_data.post_data, localizator = localizator)
            if form.validate():
                form_data.save_to_session()
                return redirect(url_for(next_page))
            return render_template(
                current_page,
                form=form, 
                localizator=localizator,
                persons = {i:session[GROUP_INFO].get(i) for i in PERSON_FIELDS}
            )

        else:
            form = formClass(**(session[GROUP_INFO]), localizator = localizator)
            return render_template(
                current_page, 
                group_info=session[GROUP_INFO], 
                form=form,  
                localizator=localizator,
                persons = {i:session[GROUP_INFO].get(i) for i in PERSON_FIELDS}
            )


class PetitionHandler(object):

    @classmethod
    def admin(cls):
        return AdminView.show()

    @classmethod
    def new_form(cls):
        return AdminView.new_form()

    @classmethod    
    def change_guest(cls, pk):
       return AdminView.change_guest(pk) 

    @classmethod   
    def create_docx(self, pk):
        return AdminView.create_docx(pk)

    @classmethod    
    def step_handler(cls, **kwargs):
        return StepView.show(**kwargs)

    @classmethod
    def applicate(cls):
        return Application.show()

    @classmethod
    def choose_language(cls):
        return ChooseLanguage.show()


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route("/admin")
@auth.login_required
def admin():
    session['language'] = 'en'
    return PetitionHandler.admin()

@app.route("/",  methods=['GET', 'POST'])
def choose_language():
    session['language'] = 'en'
    return PetitionHandler.choose_language()

@app.route('/create_docx/<int:pk>/')
def create_docx(pk):
    return PetitionHandler.create_docx(pk=pk)

@app.route('/change_guest/<int:pk>/')
def change_guest(pk):
    return PetitionHandler.change_guest(pk=pk)

@app.route("/new_form")
def new_form():
    return PetitionHandler.new_form()

@app.route("/step1", methods=['GET', 'POST'])
def step1():    
    return PetitionHandler.step_handler(current_page = "step1.html", next_page = 'step2', formClass = Step1Form)
    
@app.route("/step2", methods=['GET', 'POST'])
def step2():
   return PetitionHandler.step_handler(current_page = "step2.html", next_page = 'step3', formClass =  Step2Form)

@app.route("/step3", methods=['GET', 'POST'])
def step3():
   return  PetitionHandler.step_handler(current_page = "step3.html", next_page ='application', formClass = Step3Form)

@app.route("/application", methods=['GET', 'POST'])
def application():
    return  PetitionHandler.applicate()

if __name__ == "__main__":
    # set as part of the config
    SECRET_KEY = 'many random bytes'

    # or set directly on the app
    app.secret_key = 'many random bytes'
    app.run()
