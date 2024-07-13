# Generated by Django 5.0.6 on 2024-07-13 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('stp_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('batch_number', models.CharField(max_length=255)),
                ('manufacture_date', models.DateField(null=True)),
                ('expiry_date', models.DateField(null=True)),
                ('active_ingredient_concentration', models.CharField(max_length=255)),
                ('capsule_size', models.CharField(max_length=255)),
                ('dessolution_test', models.CharField(max_length=255)),
                ('hardness_test', models.CharField(max_length=255)),
                ('moisture_content', models.CharField(max_length=255)),
                ('dosage_unit_uniformiry', models.CharField(blank=True, max_length=255, null=True)),
                ('appearance', models.CharField(max_length=255)),
                ('packaging_integrity', models.CharField(max_length=255)),
                ('storage_conditions', models.CharField(max_length=255)),
                ('stability_testing', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
