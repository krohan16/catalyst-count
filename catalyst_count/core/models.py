from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = 	models.IntegerField(null=True, blank=True, db_index=True)
    industry = models.CharField(max_length=255, db_index=True)
    size_range = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255, db_index=True)
    linkedin_url = 	models.URLField()
    current_employee_estimate = models.IntegerField()
    total_employee_estimate = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    





