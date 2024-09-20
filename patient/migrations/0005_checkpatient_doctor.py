# Generated by Django 4.2.15 on 2024-09-11 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctr_app', '0001_initial'),
        ('patient', '0004_appointment_is_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpatient',
            name='doctor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='doctr_app.createdoctor'),
            preserve_default=False,
        ),
    ]
