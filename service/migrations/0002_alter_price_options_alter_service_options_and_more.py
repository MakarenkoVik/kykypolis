# Generated by Django 4.2 on 2023-05-02 17:07

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="price",
            options={},
        ),
        migrations.AlterModelOptions(
            name="service",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="service",
            name="service_ser_pub_dat_7d3580_idx",
        ),
        migrations.AddField(
            model_name="price",
            name="description",
            field=ckeditor.fields.RichTextField(default=0, verbose_name="Price Description"),
        ),
        migrations.AlterField(
            model_name="price",
            name="value",
            field=models.DecimalField(decimal_places=2, max_digits=4, max_length=4, verbose_name="Price value"),
        ),
        migrations.AlterField(
            model_name="service",
            name="description",
            field=ckeditor.fields.RichTextField(default=0, verbose_name="Service Description"),
        ),
    ]
