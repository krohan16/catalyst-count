from datetime import datetime
from django.shortcuts import render,redirect
from rest_framework.views import APIView,Response
from rest_framework.parsers import MultiPartParser
import pandas as pd
from django.db import transaction
from rest_framework.generics import ListAPIView
from core.services import csv_file_process
from core.serializers import CompanyCountrySerializer, CompanyIndustrySerializer, CompanyYearSerializer, NameSearchSerializer
from core.models import Company
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from hashlib import md5
from django.core.cache import cache


class CsvUpload(APIView):
    permission_classes = []
    authentication_classes = []
    parser_classes = [MultiPartParser]
    
    def process_chunk(self, chunk):
                # manage current chunk 
                chunk['year founded'] = pd.to_numeric(chunk['year founded'], downcast='integer', errors='coerce')
                chunk['current employee estimate'] = pd.to_numeric(chunk['current employee estimate'], downcast='integer', errors='coerce')
                chunk['total employee estimate'] = pd.to_numeric(chunk['total employee estimate'], downcast='integer', errors='coerce')
                
                company_objs = [
                    Company(name = row['name'],
                    domain = row['domain'],
                    year_founded = row['year founded'] if not pd.isna(row['year founded']) else None ,
                    industry = row['industry'],
                    size_range = row['size range'],
                    locality = row['locality'],
                    country = row['country'],
                    linkedin_url = row['linkedin url'],
                    current_employee_estimate = row['current employee estimate'],
                    total_employee_estimate = row['total employee estimate'],
                            )
                    for _,row in chunk.iterrows()
                    ]
                
                with transaction.atomic():
                    Company.objects.bulk_create(company_objs,batch_size=10000)
    
    def post(self, request):
        file = request.FILES.get('csv_file')
        if not file :
            return Response ({'error': 'No response provided'},400)
        
        key_name = md5('progress'.encode("utf-8")).hexdigest()
        print(key_name)
        cache.set(f'{request.user.id}_processing_file',key_name)
        print('current_user_file : ',cache.get(f'{request.user.id}_processing_file',''))
        csv_file_process(file,key_name)
        return render(request, 'data_dump.html',{'file_processing':1, 'processing_file': file.name})
        # return Response({'message':'File uploading in progress.'})
                
        
class CompanyFieldListView(ListAPIView):
    model = Company
    authentication_classes = []
    permission_classes = []
    queryset = Company.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    
    def get_queryset(self):
        field = self.request.query_params.get('field')
        if not field:
            return Response({'error':'missing required param field.'},400)
        if field == 'industry':
            return Company.objects.values('industry').distinct()
        if field == 'country':
            return Company.objects.values('industry').distinct()

    
    def get_serializer_class(self):
        field = self.request.query_params.get('field')
        if field == 'industry':
            return CompanyIndustrySerializer
        if field == 'year_founded':
            return CompanyYearSerializer
        if field == 'country':
            return CompanyCountrySerializer
    

class CompanyNameSearchView(ListAPIView):
    model = Company
    authentication_classes = []
    permission_classes = []
    queryset = Company.objects.all()
    serializer_class = NameSearchSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    
        
class QueryCountGeneratorView(APIView):
    model = Company
    queryset = Company.objects.all()
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        name = self.request.query_params.get('name', None)
        industry = self.request.query_params.get('industry', None)
        year_founded = self.request.query_params.get('year_founded', None)
        country = self.request.query_params.get('country', None)
        
        queryset = Company.objects.all()
        
        if name:
            queryset = queryset.filter(name = name)
        if industry:
            queryset = queryset.filter(industry = industry)
        if year_founded:
            queryset = queryset.filter(year_founded = year_founded)
        if country:
            queryset = queryset.filter(country = country)
            
        return Response({'count' : queryset.count()})
    
        
def query_count_generator(request):
    name = request.POST.get('name')
    industry = request.POST.get('industry')
    year_founded = request.POST.get('year_founded')
    country = request.POST.get('country')
    
    queryset = Company.objects.all()
    
    if name:
        queryset = queryset.filter(name__icontains = name)
    if industry and not industry=='select':
        queryset = queryset.filter(industry = industry)
    if year_founded:
        queryset = queryset.filter(year_founded = year_founded)
    if country and not country == 'select':
        queryset = queryset.filter(country = country)
        
    return render(request,
                  'query_count_generator.html',
                  {'count':queryset.count(),
                   'prefill_name':name, 
                   'prefill_industry':industry, 
                   'prefill_year_founded':year_founded, 
                   'prefill_country':country})

def upload_percentages(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'GET':
        percentage = 0
        rdb_key = cache.get(f'{request.user.id}_processing_file','')
        if rdb_key:
            percentage = cache.get(rdb_key,0)
        return JsonResponse({'percentage':percentage})
        
        
def csv_upload(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'GET':
        return render(request, 'data_dump.html')
    if request.method == 'POST':
        result = CsvUpload().post(request)
    
        
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'GET':
        count = Company.objects.all().count()
        return render(request,'query_count_generator.html',{'count':count})