# serializers.py
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
