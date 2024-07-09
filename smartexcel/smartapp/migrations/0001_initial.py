# Generated by Django 5.0.6 on 2024-07-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objective', models.CharField(max_length=255)),
                ('scope', models.CharField(max_length=255)),
                ('concentration', models.CharField(max_length=255)),
                ('volums', models.CharField(max_length=50)),
                ('ingradient', models.CharField(max_length=255)),
                ('spec_io', models.CharField(max_length=255)),
                ('spec_dates', models.DateField(blank=True, null=True)),
                ('procedure', models.CharField(max_length=255)),
                ('calculation_details', models.CharField(max_length=255)),
                ('conclusion', models.CharField(max_length=255)),
                ('initiation_date', models.DateField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
