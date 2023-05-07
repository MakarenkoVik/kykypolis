# Generated by Django 4.2 on 2023-05-07 11:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_event_alter_gallery_options_alter_gallery_place_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='Pub date')),
                ('visitor_category', models.CharField(max_length=50, verbose_name='Visitor Category')),
                ('visitor_name', models.CharField(max_length=50, verbose_name='Visitor Name')),
                ('description', ckeditor.fields.RichTextField(blank=True, default=None, null=True, verbose_name='Review Description')),
                ('review_image', models.ImageField(blank=True, null=True, upload_to='review', verbose_name='Review Image')),
                ('link', models.URLField(verbose_name='Review Link')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='Event Date'),
        ),
    ]
