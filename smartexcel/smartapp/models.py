from django.db import models

class FormData(models.Model):
    objective = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    concentration = models.CharField(max_length=255)
    volums = models.CharField(max_length=50) 
    ingradient = models.CharField(max_length=255)
    spec_io = models.CharField(max_length=255)
    spec_details = models.CharField(max_length=255)
    procedure = models.CharField(max_length=255)
    calculation_details = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    initiation_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'FormData: {self.objective}'
    