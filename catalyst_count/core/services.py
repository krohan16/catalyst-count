import pandas as pd
from datetime import datetime
from io import TextIOWrapper
from core.models import Company
from django.core.cache import cache
from celery import shared_task


@shared_task(bind=True)
def csv_file_process(self, file, key_name):
    decoded_file = TextIOWrapper(file.file, encoding='utf-8')
    
    chunk_size = 75000  # Number of rows per chunk
    count = 0
    total_row_count = pd.read_csv(decoded_file).shape[0]
    decoded_file.seek(0)

    for chunk in pd.read_csv(decoded_file, chunksize=chunk_size):
        count+=1
        current_chunk = chunk[['name',
                'domain',
                'year founded',
                'industry',
                'size range',
                'locality',
                'country',
                'linkedin url',
                'current employee estimate',
                'total employee estimate']]
        
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
            for _,row in current_chunk.iterrows()
            ]
        
        Company.objects.bulk_create(company_objs)
        count+=1
        percentages = (chunk_size * count / total_row_count) *100
        print('percentages : ',percentages)
        """TODO: redis increment for percentages"""
        cache.set(key_name,int(percentages),60*10)
        print('from cache',cache.get(key_name,''))