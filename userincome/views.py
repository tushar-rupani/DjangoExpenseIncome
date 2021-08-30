from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import *
import json
from django.http import JsonResponse
import datetime
# Create your views here.



def search_income(request):
	if request.method == 'POST':
		search_str = json.loads(request.body).get('searchText')
		income = UserIncome.objects.filter(amount__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(date__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(description__icontains = search_str, owner = request.user) | UserIncome.objects.filter(source__icontains = search_str, owner = request.user)
		data = income.values()
		return JsonResponse(list(data), safe = False)


def index(request):
	income = UserIncome.objects.filter(owner = request.user)
	paginator = Paginator(income, 4)
	page_number = request.GET.get('page')
	page_obj = Paginator.get_page(paginator, page_number)
	currency = UserPreferences.objects.get(user = request.user).currency

	context = {
	'income' : income,
	'page_obj' : page_obj,
	'currency' : currency
	}

	
	return render(request, 'income/index.html', context)


def add_income(request):


	source = Source.objects.all()
	context = {

	'source' : source,
	'values' : request.POST
	}


	if request.method == 'GET':
		return render(request, 'income/add-income.html', context)

	if request.method == 'POST':
		amount = request.POST['amount']

		if not amount:
			messages.error(request, "Please Enter Amount")
			return render(request, 'income/add-income.html', context)

		description = request.POST['description']
		date = request.POST['expense_date']
		category = request.POST['category']

		if not description:
			messages.error(request, "Oops, you have to enter description")
			return render(request, 'expenses/add-expense.html', context)

		UserIncome.objects.create(owner = request.user, amount=amount, source=category, date=date, description=description)
		messages.success(request, "Your income is added successfully.")
		return redirect('income')

def income_edit(request, id):


	income = UserIncome.objects.get(pk = id)
	source = Source.objects.all()

	context = {
	'income' : income,
	'values' : income,
	'source' : source
	}

	if request.method == 'GET':
		return render(request, 'income/edit-income.html', context)

	if request.method == 'POST':
		amount = request.POST['amount']

		if not amount:
			messages.error(request, "Please Enter Amount")
			return render(request, 'income/add-income.html', context)

		description = request.POST['description']
		date = request.POST['expense_date']
		category = request.POST['category']

		if not description:
			messages.error(request, "Oops, you have to enter description")
			return render(request, 'expenses/add-expense.html', context)

		income.owner = request.user
		income.amount = amount
		income.date = date
		income.source = category
		income.description = description
		income.save()
		messages.success(request, "We have updated your Income information")
		return redirect('income')

def income_delete(request, id):
	income = UserIncome.objects.get(pk = id)
	income.delete()
	messages.info(request, "Your Income info has been deleted")
	return redirect('income')

def stat_view(request):
	return render(request, 'income/stat.html')

def get_source_summary(request):
	todays_date = datetime.date.today()
	six_months_ago = todays_date-datetime.timedelta(days=30*6)
	incomes = UserIncome.objects.filter(owner = request.user, date__gt = six_months_ago, date__lt = todays_date)
	final_rep = {}

	def get_source(income):
		return income.source

	source_list = list(set(map(get_source, incomes)))


	def get_income_category_amount(source):
		amount = 0
		filtered_by_source = incomes.filter(source = source)
		for item in filtered_by_source:
			amount += item.amount

		return amount


	for x in incomes:
		for y in source_list:
			final_rep[y] = get_income_category_amount(y)


	return JsonResponse({'income_source_data': final_rep}, safe=False)





