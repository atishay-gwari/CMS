from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CMS",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    path('api/claims/create/', views.post_create_claim, name='create_claim'),


    path('api/signin/', views.login_api, name='signinapi'),

    path('api/signup/', views.signup_api, name='signupapi'),

    # ADMIN API'S
    path('api/admin/policy/', views.get_policy_list),
    path('api/admin/policy/create/', views.create_policy),
    path('api/admin/policy/<int:pk>/', views.update_policy),
    path('api/admin/policy/<int:pk>/delete/', views.delete_policy),
    path('api/admin/claim/', views.get_claim_list),
    path('api/admin/claim/create/', views.create_claim),
    path('api/admin/claim/<int:pk>/', views.update_claim),
    path('api/admin/claim/<int:pk>/delete/', views.delete_claim),

    path('api/admin/users/', views.get_user_list),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),

]