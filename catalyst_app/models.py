from django.db import models

class CsvModel(models.Model):
    keyword = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=80)
    year_founded = models.CharField(max_length=80)
    industry = models.CharField(max_length=80)
    size_range = models.CharField(max_length=100)
    locality = models.CharField(max_length=1000)
    country = models.CharField(max_length=80)
    linkedin_url = models.CharField(max_length=150)
    current_employee_estimate = models.CharField(max_length=80)
    total_employee_estimate = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} - {self.domain}"

    class Meta:
        db_table = 'csv_data'