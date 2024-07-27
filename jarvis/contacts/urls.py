from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('contacts/', views.contact_list_view, name='contact_list'),
    path('contacts/<int:page>', views.contact_list_view, name='contact_list'),
    path('add_contact/', views.add_contact_view, name='add_contact'),
    path('contact/<int:contact_id>/', views.fulldata_contact_view, name='fulldata_contact'),
    path('update_contact/<int:contact_id>/', views.update_contact_view, name='update_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact_view, name='delete_contact'),
    path('search_contacts/', views.search_contacts, name='search_contacts'),
]
