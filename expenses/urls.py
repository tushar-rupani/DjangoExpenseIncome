from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

	path('', views.index, name="expenses"),
	path('edit-expense/<int:id>', views.expense_edit, name="edit-expense"),
	path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
	path('add-expense', views.add_expense, name="add-expense"),
	
	path('expense_category_summary', views.expense_category_summary, name="expense_category_summary"),

	path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),

	path('stats', views.stat_view, name="stats"),

	path('export-csv', views.export_csv, name="export-csv"),

	path('export-pdf', views.export_pdf, name="export-pdf"),

	path('add_category', views.add_category, name="add_category"),
]