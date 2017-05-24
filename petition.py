from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash, send_file
import json
from forms import Step1Form, Step2Form, Step3Form 
import models 
from sqlalchemy import update
from functools import reduce
from create_docx import DocxHandler
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "tatiana": "OVS",
    "artiom": "OVS"
}

GROUP_INFO = 'group_info'
GUEST_KEY = 'guest_id'
PERSON_FIELDS = ['brothers', 'sisters', 'children', 'сlergy']


class JGuest(object):
    """Class to represent petitions in Jinja"""

    person_keys = PERSON_FIELDS
    ready_state = "готово"
    not_ready_state = "в процессе заполнения"

    def __init__(self, pk, json_string):
        self.json_string = json.loads(json_string)
        self.pk = pk
        self.persons = self.__get_persons_only()
        self._represent(json_string)
        

    def _represent(self, json_string):
        self.group_name = self.json_string['group_name']
        self.date_arr = self.json_string['date_arr']
        self.date_dep = self.json_string['date_dep']
        self.senior = self.json_string['senior']
        self.pers_status = self.json_string['guest_information']
        self.total_persons = self.__total_persons()
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
        return reduce((lambda x, y: x + int(self.persons[y])), self.persons, 0)



class PetitionHandler(object):
    model = models.Guest
    db_session  = models.session
    person_keys = PERSON_FIELDS

    def admin(self):
        guests = self.db_session.query(self.model).all()
        guests = [JGuest( g.id, g.json_string)  for g in guests]
        return render_template('admin.html', guests=guests)

    def new_form(self, next_form):
        session[GROUP_INFO] = {}
        session[GUEST_KEY] =  None
        return redirect(url_for(next_form))

    def change_guest(self, pk, next_form):
        session[GUEST_KEY] = pk
        json_string = self.db_session.query(self.model).get(session[GUEST_KEY]).json_string
        info = json.loads(json_string)
        session[GROUP_INFO] = info
        return redirect(url_for(next_form))

    def change_language(self):
        session[GROUP_INFO] = {}
        session[GUEST_KEY] =  None
        session['language'] = None
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            print(request.form['language'])
            session['language'] = request.form['language']
            return redirect(url_for('step1'))

    def create_docx(self, pk):
        json_string = self.db_session.query(self.model).get(pk).json_string
        doc_name = DocxHandler(json_string).create_docx()
        return send_file(doc_name, as_attachment=True)

    def step_handler(self, current_page, next_page, formClass=None):
        if request.method == 'GET':
            form = formClass(**(session[GROUP_INFO]), language=session['language'])
            return render_template(current_page, group_info=session[GROUP_INFO], form=form)
        if request.method == 'POST':
            form_data = {i:request.form[i] for i in request.form if request.form[i]}
            print(form_data)
            form = formClass(**form_data, language=session['language'])
            print(form.validate())
            if form.validate():
                print('ok')
                session[GROUP_INFO].update(dict(form.data))
                session[GROUP_INFO] = session[GROUP_INFO]
                return redirect(url_for(next_page))
            return render_template(current_page, form=form)
            
    def applicate(self):
        self.__fill_empty_persons()
        json_string = json.dumps(session[GROUP_INFO])
        if session.get(GUEST_KEY):
            guest = self.db_session.query(self.model).get(session[GUEST_KEY])
            guest.json_string = json_string
        else:
            guest = self.model(json_string)
            self.db_session.add(guest)
        self.db_session.commit()
        session[GUEST_KEY] = None
        session[GROUP_INFO] = {}
        return render_template('applied.html')

    def __fill_empty_persons(self):
        for p in self.person_keys:
            if not session[GROUP_INFO][p]:
                session[GROUP_INFO][p]='0'

        

petitions = PetitionHandler()

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route("/admin")
@auth.login_required
def admin():
    return petitions.admin()

@app.route("/",  methods=['GET', 'POST'])
def change_language():
    return petitions.change_language()

@app.route('/create_docx/<int:pk>/')
def create_docx(pk):
    return petitions.create_docx(pk=pk)

@app.route('/change_guest/<int:pk>/')
def change_guest(pk):
    return petitions.change_guest(pk=pk, next_form="step1")

@app.route("/new_form")
def new_form():
    return petitions.new_form(next_form="step1")

@app.route("/step1", methods=['GET', 'POST'])
def step1():    
    return petitions.step_handler("step1.html", 'step2', Step1Form)
    
@app.route("/step2", methods=['GET', 'POST'])
def step2():
   return petitions.step_handler("step2.html", 'step3', Step2Form)

@app.route("/step3", methods=['GET', 'POST'])
def step3():
   return  petitions.step_handler("step3.html", 'application', Step3Form)

@app.route("/application", methods=['GET', 'POST'])
def application():
    return  petitions.applicate()

if __name__ == "__main__":
    # set as part of the config
    SECRET_KEY = 'many random bytes'

    # or set directly on the app
    app.secret_key = 'many random bytes'
    app.run()
