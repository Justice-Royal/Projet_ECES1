# Generated by Django 4.2.1 on 2023-06-23 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Application1", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorie",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="produit",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="vente",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
