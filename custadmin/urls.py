from django.urls import path
from . import views
urlpatterns = [
    path('', views.AdminHome, name='AdminHome'),

    path('getpolicy/', views.AdminReadPolicy, name="ReadAdminPolicy"),
    path('addpolicy/', views.AdminCreatePolicy, name="AddAdminPolicy"),
    path('Deletepolicy/<str:id>/', views.AdminDeletePolicy, name="DeleteAdminPolicy"),
    path('Updatepolicy/<str:id>/', views.AdminUpdatePolicy, name="UpdateAdminPolicy"),





    path('getclaim/', views.AdminReadClaim, name="ReadAdminClaim"),
    path('addclaim/', views.AdminCreateClaim, name="AddAdminClaim"),
    path('Deleteclaim/<str:id>/', views.AdminDeleteClaim, name="DeleteAdminClaim"),
    path('Updateclaim/<str:id>/', views.AdminUpdateClaim, name="UpdateAdminClaim"),

    

]