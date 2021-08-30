from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
from userpreferences.models import UserPreferences
import csv
from django.db.models import Sum
from django.db.models import Count
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

# Create your views here.

def search_expenses(request):
	if request.method == 'POST':
		search_str = json.loads(request.body).get('searchText')
		expenses = Expense.objects.filter(amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(date__istartswith = search_str, owner = request.user) | Expense.objects.filter(description__icontains = search_str, owner = request.user) | Expense.objects.filter(category__icontains = search_str, owner = request.user)
		data = expenses.values()
		return JsonResponse(list(data), safe = False)



@login_required(login_url = '/authentication/login')
def index(request):
	expense = Expense.objects.filter(owner = request.user)
	paginator = Paginator(expense, 4)
	page_number = request.GET.get('page')
	page_obj = Paginator.get_page(paginator, page_number)
	try:
		currency = UserPreferences.objects.get(user = request.user).currency
	except:
		currency = None

	
	total_price = Expense.objects.filter(owner = request.user).aggregate(total=Sum('amount'))
	context = {

	'expense' : expense,
	'page_obj' : page_obj,
	'currency' : currency,
	'total_price':total_price

	}

	return render(request, 'expenses/index.html', context)



def add_expense(request):

	categories = Category.objects.all()
	category_user = Category_User.objects.filter(owner = request.user)
	category_length = Category_User.objects.filter(owner = request.user).aggregate(num_cate=Count('name'))

	if category_length['num_cate'] == 0:
		messages.error(request, "You have not added categories yet, Add them.")
	else:
		pass
		

	context = {

	'categories' : categories,
	'values' : request.POST,
	'category_user' : category_user,
	
	}

	if request.method == 'GET':
		return render(request, 'expenses/add-expense.html', context)

	if request.method == 'POST':
		amount = request.POST['amount']

		if not amount:
			messages.error(request, "Oops, you have to enter amount")
			return render(request, 'expenses/add-expense.html', context)

	
		description = request.POST['description']
		date = request.POST['expense_date']
		category = request.POST['category']

		if not description:
			messages.error(request, "Oops, you have to enter description")
			return render(request, 'expenses/add-expense.html', context)

		Expense.objects.create(owner = request.user, amount=amount, category=category, date=date, description=description)
		messages.success(request, "Your expense is added successfully.")
		return redirect('expenses')

def expense_edit(request, id):

	expense = Expense.objects.get(pk = id)
	categories = Category.objects.all()
	category_user = Category_User.objects.filter(owner = request.user)

	context = {
	
			'expense' : expense,
			"values" : expense,
			'categories' : categories,
			'category_user' : category_user


			}

	if request.method == 'GET':
		return render(request, 'expenses/edit-expense.html', context)

	if request.method == 'POST':


		amount = request.POST['amount']

		if not amount:
			messages.error(request, "Oops, you have to enter amount")
			return render(request, 'expenses/edit-expense.html', context)

	
		description = request.POST['description']
		date = request.POST['expense_date']
		category = request.POST['category']

		if not description:
			messages.error(request, "Oops, you have to enter description")
			return render(request, 'expenses/edit-expense.html', context)

		

		expense.owner = request.user
		expense.amount = amount
		expense.category = category
		expense.date = date
		expense.description = description
		expense.save()

		messages.success(request, "Your expense is updated successfully.")
		return redirect('expenses')

def delete_expense(request, id):
	expense = Expense.objects.get(pk = id)
	expense.delete()
	messages.info(request, "We have successfully deleted your expense information.")
	return redirect("expenses")


def expense_category_summary(request):
	todays_date = datetime.date.today()
	six_months_ago = todays_date-datetime.timedelta(days=30*6)

	expenses = Expense.objects.filter(owner= request.user, date__gte = six_months_ago, date__lte = todays_date)


	finalrep = {}


	def get_category(expense):
		return expense.category

	category_list = list(set(map(get_category, expenses)))


	def get_expense_category_amount(category):
		amount = 0

		filtered_by_category = expenses.filter(category = category)

		for item in filtered_by_category:
			amount += item.amount

		return amount

	for x in expenses:
		for y in category_list:
			finalrep[y] = get_expense_category_amount(y)

	return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stat_view(request):
	return render(request, 'expenses/stat.html')


def export_csv(request):
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachement; filename=Expenses' + \
	str(datetime.datetime.now()) + '.csv'

	writer = csv.writer(response)

	writer.writerow(['Amount', 'Description', 'Category', 'Date'])

	expense = Expense.objects.filter(owner = request.user)

	for ex in expense:
		writer.writerow([ex.amount, ex.description, ex.category, ex.date])


	return response

def add_category(request):


	if request.method == 'POST':
		category = request.POST['username']

		if not category:
			messages.error(request, "You have to enter a category first.")
			return render(request, 'expenses/add-category.html')
		Category_User.objects.create(owner = request.user, name=category)
		messages.success(request, "Your category has been added successfully")

	return render(request, 'expenses/add-category.html')

def export_pdf(request):
	response = HttpResponse(content_type = 'application/pdf')

	response['Content-Disposition'] = 'attachement; filename=Expenses' + \
	str(datetime.datetime.now()) + '.pdf'

	response['Content-Transfer-Encoding'] = 'binary'

	html_string = render_to_string('expenses/pdf-output.html', {'expenses':[],'total':0})

	html = HTML(string=html_string)

	result = html.write_pdf()

	with tempfile.NamedTemporaryFile(delete = True) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'rb')
		response.write(output.read())
	return response




