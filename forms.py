import wtforms.form as form
import wtforms.fields as fields
from wtforms import validators 

class Step1Form(form.Form):
    group_name = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Название группы (страна, город, приход) / Group Name (location: country, city, parish)"
    )
    senior = fields.StringField( 
    	#validators=[validators.input_required()], 
    	label = "ФИО старшего группы (имена) / Senior group (person in charge)"
    )
    responsible = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Ответственный за данных гостей из региона ОВС"
    )
    phone =  fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Номер телефона ответственного / Contact::"
    )
    arr_aim = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Цель приезда"
    )
    languages = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Какими языками владеют"
    )
    status = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Информация о госте"
    )
    follow =  fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Нужно ли встречать-провожать и кто это осуществит?"
    )
    email =  fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "E-mail:"
    )



class Step2Form(form.Form):
    date_arr = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Дата и время прибытия / Date and time of arrival",
    	id="date_arr"
    )
    date_dep = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Дата и время выезда / Date and time of departure:",
    	id="date_dep"
    )
    brothers = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Братья / Brothers (males)", 
    )
    sisters = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Сестры / Sisters (femasstrsles)", 
    )
    children = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Дети / Children ", 
    )
    clerics = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Священство и монашествующие / Clergy or monastic people", 
    )
    excursions = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Место и время проведения экскурсии / Place and time of the tour "
    )
    transport = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Транспорт для экскурсий (свой или наемный)"
    )


class Step3Form(form.Form):
    meal = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Заказ трапезы / Meal booking (date and time)"
    )
    breakfast = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Завтрак, время / Breakfast time: "
    )
    breakfast_persons = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Количество человек / Number of persons: "
    )
    lunch = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Обед, время / Lunch time:"
    )
    lunch_persons = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Количество человек / Number of persons: "
    )
    dinner = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Ужин, время / Dinner time: "
    )
    dinner_persons = fields.StringField(
    	#validators=[validators.input_required()], 
    	label = "Количество человек / Number of persons:"
    )