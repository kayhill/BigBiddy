from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^listing/(?P<item>\w+)/$', views.listing, name='listing'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("sell/", views.sell, name="sell"),
    path("watchlist/", views.watchlist, name="watchlist")
    
]
