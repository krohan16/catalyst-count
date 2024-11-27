from django.urls import path
from core import views
from core.views import CompanyFieldListView, QueryCountGeneratorView, CompanyNameSearchView, query_count_generator, csv_upload, upload_percentages

urlpatterns = [
    path('csv_upload_form/', csv_upload, name='csv-upload-form'),
    path('csv_upload/',views.CsvUpload.as_view(),name='csv-upload'),
    path("company_query_filter/", CompanyFieldListView.as_view(), name="company-query-filter"),
    path("company_search_filter/", CompanyNameSearchView.as_view(), name="company-name-sraech"),
    path("count/", QueryCountGeneratorView.as_view(), name="company-query-count-api"),
    path("query_count/", query_count_generator, name="company-query-count-form"),    
    path("upload_percentages/", upload_percentages, name="upload-percentages"),    
    
]
