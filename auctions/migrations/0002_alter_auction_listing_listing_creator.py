# Generated by Django 4.0.3 on 2022-04-13 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]