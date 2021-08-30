from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import *
from django.contrib import messages
from django.db.models import Sum
from expenses.models import *
from userincome.models import *

# Create your views here.

def index(request):
	currency_data = []

	file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

	with open(file_path, 'r') as json_file:
		data = json.load(json_file)

		for k, v in data.items():
			currency_data.append({'name':k, 'value':v})

	exists = UserPreferences.objects.filter(user = request.user).exists()
	user_prefrences = None


	if exists:
		user_prefrences = UserPreferences.objects.get(user = request.user)


	if request.method == 'GET':
		
		return render(request, 'preferences/index.html', {'currencies': currency_data,'user_prefrences':user_prefrences})



	else:
		currency = request.POST['currency']
		if exists:
			user_prefrences.currency = currency
			user_prefrences.save()
		else:
			UserPreferences.objects.create(user=request.user, currency=currency)
			
		messages.success(request, "Changes has been done!")
		return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_prefrences':user_prefrences})

	

def savings(request):
	total_expense = Expense.objects.filter(owner = request.user).aggregate(expense=Sum('amount'))
	total_income = UserIncome.objects.filter(owner = request.user).aggregate(income=Sum('amount'))


	total_savings = total_income['income'] - total_expense['expense']

	if total_savings < 0:
		ans = "Haha, you're in debt broke ass nigga"
	else:
		ans = "Your total savings till now is" + str(total_savings) + "Cheers!"


	context = {

	'ans': ans,
	'total_savings' : total_savings,
	'total_expense' : total_expense,
	'total_income' : total_income,
	

	}

	return render(request, 'preferences/savings.html', context)



	
	

