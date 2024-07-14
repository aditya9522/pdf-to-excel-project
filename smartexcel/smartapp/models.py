from django.db import models

class FormData(models.Model):
    stp_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=255)
    manufacture_date = models.DateField(null=True, blank=True) 
    expiry_date = models.DateField(null=True, blank=True)
    active_ingredient_concentration = models.CharField(max_length=255)
    capsule_size = models.CharField(max_length=255)
    dessolution_test = models.CharField(max_length=255)
    hardness_test = models.CharField(max_length=255)
    moisture_content = models.CharField(max_length=255)
    dosage_unit_uniformiry = models.CharField(max_length=255, blank=True, null=True)
    appearance = models.CharField(max_length=255)
    packaging_integrity = models.CharField(max_length=255)
    storage_conditions = models.CharField(max_length=255)
    stability_testing = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'FormData: {self.product_name}'
    