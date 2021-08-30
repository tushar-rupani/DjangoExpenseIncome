from . import views
from django.urls import path

urlpatterns = [

	path('', views.index, name="preferences"),
	path('saving', views.savings, name="save")

]