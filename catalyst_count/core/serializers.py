from rest_framework import serializers
from core.models import Company
from django.contrib.auth.models import User



class CompanyIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['industry']
        
class CompanyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['year_founded']
        
class CompanyCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['country']
        
class NameSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']
    
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']