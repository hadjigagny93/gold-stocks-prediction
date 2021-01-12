# Generated by Django 3.1.5 on 2021-01-12 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_apicallertask_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apicallertask',
            name='from_tab',
        ),
        migrations.DeleteModel(
            name='Back',
        ),
        migrations.DeleteModel(
            name='Current',
        ),
        migrations.RemoveField(
            model_name='track',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='track',
            name='ml_model',
        ),
        migrations.RemoveField(
            model_name='transfertask',
            name='from_tab',
        ),
        migrations.DeleteModel(
            name='ApiCallerTask',
        ),
        migrations.DeleteModel(
            name='Mode',
        ),
        migrations.DeleteModel(
            name='Predictors',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
        migrations.DeleteModel(
            name='Track',
        ),
        migrations.DeleteModel(
            name='TransferTask',
        ),
    ]