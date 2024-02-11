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

    

]