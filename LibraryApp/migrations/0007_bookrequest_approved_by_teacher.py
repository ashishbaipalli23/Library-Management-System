# Generated by Django 3.0.5 on 2023-07-29 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0006_bookrequest_approved_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrequest',
            name='approved_by_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
