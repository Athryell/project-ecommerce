# Generated by Django 4.0.2 on 2022-06-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_watchlist_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='demo_hardcoded_path',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
