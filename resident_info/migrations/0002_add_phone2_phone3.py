# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentinfofields',
            name='phone2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='联系电话2'),
        ),
        migrations.AddField(
            model_name='residentinfofields',
            name='phone3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='联系电话3'),
        ),
    ]
