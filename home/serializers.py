from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Policys, Claims

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policys
        fields = '__all__'

class ClaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claims
        fields = ['policy_number', 'amt', 'reason']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claims
        fields = '__all__'