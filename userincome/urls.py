from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

	path('', views.index, name="income"),
	path('edit-income/<int:id>', views.income_edit, name="edit-income"),
	path('delete-income/<int:id>', views.income_delete, name="delete-income"),
	path('add-income', views.add_income, name='add-income'),
	path('search-income', csrf_exempt(views.search_income), name='search-income'),
	path('stat', views.stat_view, name='stat'),
	path('income_category_summary', views.get_source_summary, name="income_category_summary"),

	

]