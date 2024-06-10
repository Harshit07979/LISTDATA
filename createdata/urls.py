from django.urls import path
from . import views

print("Loading createdata.urls")

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_operations, name='list_operations'),
    path('dict/', views.dict_operations, name='dict_operations'),
    path('set/', views.set_operations, name='set_operations'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
]
