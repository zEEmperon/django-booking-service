from django.urls import path
from . import views

from .filters import OfferFilter

app_name = 'booking'
urlpatterns = [
    path('', views.IndexFilterView.as_view(filterset_class=OfferFilter), name='index'),
    path('offers/<slug:slug>/', views.OfferDetailView.as_view(), name='detail'),
    path('offers/<slug:slug>/book', views.CreateBookingView.as_view(), name='book'),
    path('sign_in/', views.LoginUser.as_view(), name='sign_in'),
    path('sign_up/', views.RegisterUser.as_view(), name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]