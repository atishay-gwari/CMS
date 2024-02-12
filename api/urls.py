from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path
from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="CMS",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('policys/', views.get_policys),
    path('claims/', views.get_claims),
    path('claims/create/', views.post_create_claim),


    path('signin/', views.login_api, name='signinapi'),

    path('signup/', views.signup_api, name='signupapi'),

    # ADMIN API'S
    path('admin/policy/', views.get_policy_list),
    path('admin/policy/create/', views.create_policy),
    path('admin/policy/<str:pk>/', views.update_policy),
    path('admin/policy/<str:pk>/delete/', views.delete_policy),
    path('admin/claim/', views.get_claim_list),
    path('admin/claim/create/', views.create_claim),
    path('admin/claim/<str:pk>/', views.update_claim),
    path('admin/claim/<str:pk>/delete/', views.delete_claim),
    
    path('admin/approval/<str:pk>/', views.claim_approval),

    path('admin/users/', views.get_user_list),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]