from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # 👈 si tu último archivo NO se llama así, decime el nombre
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='reproducido',
            field=models.BooleanField(default=False),
        ),
    ]
