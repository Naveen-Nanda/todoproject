from django.urls import path, include
from django.conf.urls import url
from . import views



urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.sessionauth, name="sessionauth"),
    path('sessionlogin', views.sessionlogin, name="sessionlogin"),
    path('sessionlogout', views.sessionlogout, name="sessionlogout"),
    path('signup', views.signup, name="signup"),
    path('submitemail', views.submitemail, name="submitemail"),

]