from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_video_fields_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='reproducido',
            field=models.BooleanField(default=False),
        ),
    ]
