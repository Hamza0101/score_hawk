# Generated manually to fix field name conflicts
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0004_add_new_models'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Fix UserFavorite field names to match the model
        migrations.RenameField(
            model_name='userfavorite',
            old_name='favorite_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='userfavorite',
            old_name='added_at',
            new_name='created_at',
        ),
        
        # Add new fields to UserFavorite
        migrations.AddField(
            model_name='userfavorite',
            name='metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
        
        # Update UserFavorite choices
        migrations.AlterField(
            model_name='userfavorite',
            name='favorite_type',
            field=models.CharField(choices=[('team', 'Team'), ('player', 'Player'), ('match', 'Match'), ('venue', 'Venue'), ('series', 'Series')], max_length=20),
        ),
        
        # Fix UserSearchHistory field names
        migrations.RenameField(
            model_name='usersearchhistory',
            old_name='search_query',
            new_name='search_term',
        ),
        
        # Add new fields to UserSearchHistory
        migrations.AddField(
            model_name='usersearchhistory',
            name='clicked_result',
            field=models.CharField(blank=True, max_length=255),
        ),
        
        # Update UserSearchHistory choices
        migrations.AlterField(
            model_name='usersearchhistory',
            name='search_type',
            field=models.CharField(choices=[('players', 'Players'), ('teams', 'Teams'), ('matches', 'Matches'), ('news', 'News'), ('general', 'General')], default='general', max_length=20),
        ),
        
        # Fix APICallLog fields to match model
        migrations.RemoveField(
            model_name='apicalllog',
            name='method',
        ),
        migrations.RemoveField(
            model_name='apicalllog',
            name='parameters',
        ),
        migrations.RemoveField(
            model_name='apicalllog',
            name='response_status',
        ),
        
        migrations.AddField(
            model_name='apicalllog',
            name='request_params',
            field=models.TextField(blank=True),
        ),
        
        # Fix CachedAPIResponse field to match model
        migrations.AlterField(
            model_name='cachedapiresponse',
            name='request_params_hash',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='apicalllog',
            name='request_hash',
            field=models.CharField(db_index=True, default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apicalllog',
            name='status_code',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
        
        # Add indexes for new models and updated fields
        migrations.AddIndex(
            model_name='userfavorite',
            index=models.Index(fields=['user', 'favorite_type'], name='scores_user_user_id_fav_type_idx'),
        ),
        migrations.AddIndex(
            model_name='userfavorite',
            index=models.Index(fields=['user', '-created_at'], name='scores_user_user_id_created_idx'),
        ),
        migrations.AddIndex(
            model_name='usersearchhistory',
            index=models.Index(fields=['user', 'search_type', '-timestamp'], name='scores_user_user_search_type_idx'),
        ),
        migrations.AddIndex(
            model_name='usersearchhistory',
            index=models.Index(fields=['search_term', '-timestamp'], name='scores_user_search_term_idx'),
        ),
        migrations.AddIndex(
            model_name='apicalllog',
            index=models.Index(fields=['endpoint', '-timestamp'], name='scores_api_endpoint_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='apicalllog',
            index=models.Index(fields=['success', '-timestamp'], name='scores_api_success_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='apicalllog',
            index=models.Index(fields=['user', '-timestamp'], name='scores_api_user_timestamp_idx'),
        ),
    ]