# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resident_info', '0003_add_death_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentinfofields',
            name='other_id_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='其他证件号码'),
        ),
        migrations.AddField(
            model_name='residentinfofields',
            name='other_id_type',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='other_id_type_residents',
                to='core.TaxonomyItem',
                verbose_name='其他证件类型'
            ),
        ),
    ]