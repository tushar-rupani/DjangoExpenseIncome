from django.contrib import admin
from .models import *

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('amount', 'description', 'date', 'category', 'owner')
	search_fields = ( 'description','category', 'date')



admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
admin.site.register(Category_User)
