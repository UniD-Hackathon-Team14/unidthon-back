# Generated by Django 4.1.3 on 2022-11-05 12:32

from django.db import migrations, models
import qna.models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0003_question_type_alter_answer_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='audio_dirs',
            field=models.FileField(blank=True, null=True, upload_to=qna.models.uuid_audio),
        ),
    ]