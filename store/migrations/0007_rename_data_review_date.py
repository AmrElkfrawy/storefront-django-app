# Generated by Django 4.2.6 on 2023-10-21 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_collection_featured_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='data',
            new_name='date',
        ),
    ]
