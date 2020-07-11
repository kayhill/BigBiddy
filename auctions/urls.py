from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.index, name="home"),
    path('listing/<str:item>/', views.listing, name="listing"),
    path('category/', views.category, name="category"),
    path('category/<str:category>/', views.pick_category, name="pick_category"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("sell/", views.sell, name="sell"),
    path("watchlist/add/<str:item>", views.add_watch, name="add_watch"),
    path("watchlist/remove/<str:item>", views.remove_watch, name="remove_watch"),
    path("watchlist/", views.watch, name="watchlist"),
    path("end/<str:item>/", views.end, name="end"),
    path("bid/<str:item>/", views.bid, name="bid"),
    path("comment/<str:item>/", views.comment, name="comment")
    
]
