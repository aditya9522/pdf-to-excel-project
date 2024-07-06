from django.db import models

class FormData(models.Model):
    objective = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    concentration = models.CharField(max_length=255)
    volums = models.CharField(max_length=50)  # Assuming a select field, use CharField for simplicity
    ingradient = models.CharField(max_length=255)
    spec_io = models.CharField(max_length=255)
    spec_dates = models.CharField(max_length=255)
    procedure = models.CharField(max_length=255)
    calculation_details = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)

    def __str__(self):
        return f'FormData: {self.objective}'