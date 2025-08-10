# Fix cache field issues
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0005_fix_model_fields'),
    ]

    operations = [
        # Fix CachedAPIResponse field to allow null temporarily
        migrations.AlterField(
            model_name='cachedapiresponse',
            name='request_params_hash',
            field=models.CharField(max_length=64, default='default_hash'),
        ),
    ]