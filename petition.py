from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
import json
from forms import Step1Form, Step2Form, Step3Form 

app = Flask(__name__)

def init_group_info():
    if not session.get('group_info'):
        session['group_info'] = {}
   
def step_handler(current_page, next_page, form=None):
    init_group_info()
    if request.method == 'GET':
        print(session['group_info'])
        form = form(**(session['group_info']))
        return render_template(current_page, group_info=session['group_info'], form=form)
    else:
        form = form(request.form)
        session['group_info'].update(form.data)
        session['group_info'] = session['group_info']
        return redirect(url_for(next_page))


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new_form")
def new_form():
    session['group_info'] = {}
    return redirect(url_for('step1'))

@app.route("/step1", methods=['GET', 'POST'])
def step1():
    return step_handler("step1.html", 'step2', Step1Form)
    
@app.route("/step2", methods=['GET', 'POST'])
def step2():
   return step_handler("step2.html", 'step3', Step2Form)

@app.route("/step3", methods=['GET', 'POST'])
def step3():
   return  step_handler("step3.html", 'application', Step3Form)

@app.route("/application", methods=['GET', 'POST'])
def application():
    print(session['group_info'])
    with open('application.json', 'a') as outfile:
        json.dump(session['group_info'], outfile)
    session['group_info'] = {}
    return render_template('applied.html')

if __name__ == "__main__":
    # set as part of the config
    SECRET_KEY = 'many random bytes'

    # or set directly on the app
    app.secret_key = 'many random bytes'
    app.run()
