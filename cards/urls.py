from django.conf.urls import url, include

from cards import views

urlpatterns = [
    url(r'ajax/save$', views.Save.as_view(), name='save'),
    url(r'$', views.Home.as_view(), name='home'),

]
