from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
import json
from forms import Step1Form, Step2Form, Step3Form 
import models 
from sqlalchemy import update


app = Flask(__name__)

GROUP_INFO = 'group_info'
GUEST_KEY = 'guest_id'

class JGuest(object):
    """Class to represent applications in Jinja"""
    def __init__(self, pk, json_string):
        self.pk = pk
        self.__represent(json_string)

    def __represent(self, json_string):
        json_string = json.loads(json_string)
        self.group_name = json_string['group_name']
        self.date_arr = json_string['date_arr']
        self.date_dep = json_string['date_dep']
        self.senior = json_string['senior']
        self.pers_status = json_string['pers_status']
        self.is_ready =  self.__is_ready(json_string)

    def __is_ready(self, json_string):
        for i in json_string:
            if not json_string[i]:
                return "в процессе заполнения"
        return "готово"


class PetitionList(object):
    model = models.Guest
    db_session  = models.session

    def index(self):
        guests = self.db_session.query(self.model).all()
        guests = [JGuest( g.id, g.json_string)  for g in guests]
        return render_template('index.html', guests=guests)

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

    def step_handler(self, current_page, next_page, form=None):
        if request.method == 'GET':
            form = form(**(session[GROUP_INFO]))
            return render_template(current_page, group_info=session[GROUP_INFO], form=form)
        else:
            form = form(request.form)
            session[GROUP_INFO].update(form.data)
            session[GROUP_INFO] = session[GROUP_INFO]
            return redirect(url_for(next_page))

    def applicate(self):
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

        

petitions = PetitionList()

@app.route("/")
def index():
    return petitions.index()

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
