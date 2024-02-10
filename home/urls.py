from django.urls import path

from . import views
urlpatterns = [
    path('', views.Home, name='home'),
    path('login/', views.loginpage,name="login"),
    path('logout/',views.logoutpage,name='logout'),
    path('signup/', views.signuppage,name="signup"),


    path('GetPolicy/', views.Get_Policy, name="getpolicy"),

    path('GetClaim/', views.Get_Claim, name="getclaim"),
    path('AddClaim/', views.Create_Claim, name="Addclaim"),

    path('api/policys/', views.get_policys, name='get_policys'),
    path('api/claims/', views.get_claims, name='get_claims'),
    # path('api/claims/create/', views.post_create_claim, name='create_claim'),
]