from django.urls import path

from . import views

app_name = 'ehrs'
urlpatterns = [
    # ex: /ehrs/
    path('', views.index, name='index'),    # path(regex, function inside views file, name associated with function)
    # ex: /ehrs/main/
    path('main/', views.main, name='main'),
    # ex: /ehrs/main/ehrinfo/123/
    path('main/ehrinfo/<uid>', views.ehrinfo, name='ehrinfo'),
    path('main/ehrcreate/', views.ehrcreate, name='ehrcreate'),
    path('main/ehrcreate/createsuccess/', views.createsuccess, name='createsuccess'),
    path('main/compcreate/', views.compcreate, name='compcreate'),
    path('main/compsuccess/', views.compsuccess, name='compsuccess'),
    path('main/ehrinfo/<uid>/compdisplay/<index>', views.compdisplay, name='compdisplay')
]

