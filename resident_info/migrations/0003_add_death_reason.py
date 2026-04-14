# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident_info', '0002_add_phone2_phone3'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentinfofields',
            name='death_reason',
            field=models.CharField(blank=True, max_length=200, verbose_name='死亡原因'),
        ),
    ]