import wtforms.form as form
import wtforms.fields as fields
from wtforms import validators, widgets
import json

class LocalizatedForm(form.Form):
    """add localization to standart WTForm with json doc"""
    def __init__(self, localizator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.localizator = localizator
        self.__localizate_fields()

    def __localizate_fields(self):
        for f in self:
            f.label =  self.localizator.localizated_form_fields[f.name]
            f.header =  self.localizator.localizated_form_fields[f.name]

class Step1Form(LocalizatedForm):
    group_name = fields.StringField(
    	validators=[validators.Length(min=2, max=25)]
    )
    senior = fields.StringField( 
    	validators=[validators.Length(min=2, max=25)]
    )
    # responsible = fields.StringField(
    # 	#validators=[validators.input_required()], 
    # )
    phone =  fields.StringField(
    	#validators=[validators.input_required()], 
    )
    arr_aim = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    languages = fields.StringField(
    	validators=[validators.Length(min=2, max=25)]
    )
    guest_information = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    # follow =  fields.StringField(
    # 	#validators=[validators.input_required()], 
    # )
    email =  fields.StringField(
    	#validators=[validators.input_required()], 
    )



class Step2Form(LocalizatedForm):
    date_arr = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    time_arr =  fields.StringField()
    date_dep = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    time_dep = fields.StringField()
    brothers = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    sisters = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    children = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    сlergy = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    tours = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    transport = fields.StringField(
    	#validators=[validators.input_required()], 
    )


class Step3Form(LocalizatedForm):
    # meal = fields.StringField(
    # 	#validators=[validators.input_required()], 
    # )

    breakfast = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    breakfast_persons = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    breakfast_comments = fields.TextField(widget = widgets.TextArea())

    lunch = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    lunch_persons = fields.StringField(
    	#validators=[validators.input_required()], 
    )
    lunch_comments = fields.TextField(widget = widgets.TextArea())

    dinner = fields.StringField()
    dinner_persons = fields.StringField()
    dinner_comments = fields.TextField(widget = widgets.TextArea())