# Generated manually to add new models
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0003_auto_20250722_1336'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Update existing models
        migrations.RenameField(
            model_name='cachedapiresponse',
            old_name='last_refreshed',
            new_name='last_accessed',
        ),
        migrations.RenameField(
            model_name='cachedapiresponse',
            old_name='parameters_hash',
            new_name='request_params_hash',
        ),
        
        # Create ChatMessage model
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('message', models.TextField()),
                ('is_user', models.BooleanField(default=True)),
                ('context_data', models.JSONField(blank=True, default=dict)),
                ('response_time', models.FloatField(blank=True, null=True)),
                ('tokens_used', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        
        # Create ChatSession model
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('message_count', models.PositiveIntegerField(default=0)),
                ('total_tokens_used', models.PositiveIntegerField(default=0)),
                ('context_page', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-last_activity'],
            },
        ),
        
        # Create UserPreference model
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')], default='light', max_length=10)),
                ('favorite_teams', models.JSONField(blank=True, default=list)),
                ('favorite_players', models.JSONField(blank=True, default=list)),
                ('notification_settings', models.CharField(choices=[('all', 'All Notifications'), ('favorites', 'Favorites Only'), ('important', 'Important Only'), ('none', 'No Notifications')], default='all', max_length=20)),
                ('live_score_refresh_interval', models.PositiveIntegerField(default=30)),
                ('timezone', models.CharField(default='UTC', max_length=50)),
                ('language', models.CharField(default='en', max_length=10)),
                ('email_notifications', models.BooleanField(default=True)),
                ('push_notifications', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        
        # Create MatchAlert model
        migrations.CreateModel(
            name='MatchAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=100)),
                ('match_name', models.CharField(max_length=255)),
                ('alert_type', models.CharField(choices=[('match_start', 'Match Start'), ('innings_break', 'Innings Break'), ('wicket', 'Wicket'), ('boundary', 'Boundary (4/6)'), ('milestone', 'Milestone (50/100)'), ('match_end', 'Match End')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('triggered_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_alerts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        
        # Create NewsBookmark model
        migrations.CreateModel(
            name='NewsBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True)),
                ('thumbnail', models.URLField(blank=True)),
                ('bookmarked_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_news', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-bookmarked_at'],
            },
        ),
        
        # Add indexes
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['user', '-timestamp'], name='scores_chatm_user_id_2bc4fa_idx'),
        ),
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['session_key', '-timestamp'], name='scores_chatm_session_26aa05_idx'),
        ),
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['is_user', '-timestamp'], name='scores_chatm_is_user_52d73f_idx'),
        ),
        migrations.AddIndex(
            model_name='chatsession',
            index=models.Index(fields=['user', '-started_at'], name='scores_chatm_user_id_36b2de_idx'),
        ),
        migrations.AddIndex(
            model_name='chatsession',
            index=models.Index(fields=['session_key', '-started_at'], name='scores_chatm_session_1b3849_idx'),
        ),
        migrations.AddIndex(
            model_name='chatsession',
            index=models.Index(fields=['is_active', '-last_activity'], name='scores_chatm_is_acti_0df1f4_idx'),
        ),
        migrations.AddIndex(
            model_name='matchalert',
            index=models.Index(fields=['match_id', 'is_active'], name='scores_matc_match_i_fa2f5f_idx'),
        ),
        migrations.AddIndex(
            model_name='matchalert',
            index=models.Index(fields=['user', 'is_active'], name='scores_matc_user_id_6e5b56_idx'),
        ),
        
        # Add unique constraints
        migrations.AddConstraint(
            model_name='matchalert',
            constraint=models.UniqueConstraint(fields=('user', 'match_id', 'alert_type'), name='unique_user_match_alert'),
        ),
        migrations.AddConstraint(
            model_name='newsbookmark',
            constraint=models.UniqueConstraint(fields=('user', 'news_id'), name='unique_user_news_bookmark'),
        ),
    ]