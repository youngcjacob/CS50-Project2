# Generated by Django 4.0.3 on 2022-04-15 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_title_comment_auction_listing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='title',
            new_name='auction_listing',
        ),
    ]