from django.conf.urls import url, include

from cards import views

urlpatterns = [
    url(r'ajax/save$', views.Save.as_view(), name='save'),
    url(r'$', views.Home.as_view(), name='home'),
    url(r'ajax/makegraph$',views.MakeGraph.as_view(), name='make_graph'),
    url(r'ajax/addcard$',views.AddCard.as_view(), name='add_card'),
    url(r'ajax/delcard',views.DeleteCard.as_view(), name='del_card'),
    url(r'ajax/updatecard$',views.UpdateCard.as_view(), name='update_graph'),
    url(r'ajax/addedge$', views.AddEdge.as_view(), name='add_edge'),
    url(r'ajax/deledge$', views.DeleteEdge.as_view(), name='del_edge'),

]
