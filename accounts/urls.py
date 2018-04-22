from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^add_transaction/$', views.add_transaction, name='add_transaction'),
    url(r'^categories_page', views.categories_page, name='categories_page'),
    url(r'^add_category', views.add_category, name='add_category'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^filter', views.filter, name='filter'),

    #Api
    url(r'^users', views.users, name='users'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^user/(?P<id>\d+)/transactions', views.user_transactions, name='user_transactions'),
    url(r'^categories', views.categories, name='categories'),
    url(r'^category/(?P<id>\d+)$', views.category, name='category'),
    url(r'^user/(?P<id>\d+)/category/(?P<category_id>\d+)/transaction', views.cat_transactions, name='cat_transactions'),
]
