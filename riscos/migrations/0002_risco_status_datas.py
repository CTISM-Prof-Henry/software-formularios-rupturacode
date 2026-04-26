import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("riscos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="risco",
            name="ativo",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="risco",
            name="data_criacao",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="risco",
            name="data_atualizacao",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
