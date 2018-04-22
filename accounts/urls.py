from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^add_transaction/$', views.add_transaction, name='add_transaction'),
    url(r'^categories', views.categories, name='categories'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),

]
