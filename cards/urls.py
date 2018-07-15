from django.conf.urls import url, include

from cards import views

urlpatterns = [
    url(r'ajax/retrieve$', views.Retrieve.as_view(), name='retrieve'),
    url(r'ajax/save$', views.Save.as_view(), name='save'),
    url(r'ajax/delete$', views.Delete.as_view(), name='delete'),
    url(r'ajax/save-all$', views.SaveAll.as_view(), name='delete'),
    url(r'$', views.Home.as_view(), name='home'),

]
