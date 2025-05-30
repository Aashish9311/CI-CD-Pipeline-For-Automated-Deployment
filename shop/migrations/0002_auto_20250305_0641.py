# # Generated by Django 5.1.6 on 2025-03-05 01:11

# from django.db import migrations


# class Migration(migrations.Migration):

#     dependencies = [
#         ('shop', '0001_initial'),
#     ]

#     operations = [
#     ]


from django.db import migrations
from ..models import Product

def add_products(apps, schema_editor):
    Product.objects.create(name="Shirt", description="A comfortable cotton shirt.", price=400)
    Product.objects.create(name="Programming Python", description="A book about python programming.", price=120)
    Product.objects.create(name="Mountain Bike", description="A sturdy mountain bicycle.", price=3500)
    Product.objects.create(name="Wireless Mouse", description="A comfortable wireless mouse.", price=550) # Added this line
    Product.objects.create(name="Headphones", description="Over-ear noise-cancelling headphones.", price=5000)  # Added this line
    Product.objects.create(name="Intern", description="To learn DevOps", price="free")
class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),  # Correct dependency
    ]

    operations = [
        migrations.RunPython(add_products),
    ]
