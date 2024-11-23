# Generated by Django 5.1.3 on 2024-11-22 19:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_alter_transaction_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_transaction",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]