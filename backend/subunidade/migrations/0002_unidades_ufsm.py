from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subunidade", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subunidade",
            options={"ordering": ["nome"]},
        ),
        migrations.RemoveField(model_name="subunidade", name="descricao"),
        migrations.RemoveField(model_name="subunidade", name="sigla"),
        migrations.AddField(
            model_name="subunidade",
            name="cod_estruturado",
            field=models.CharField(default="", max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subunidade",
            name="centro_nome",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subunidade",
            name="centro_sigla",
            field=models.CharField(default="", max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subunidade",
            name="tipo",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subunidade",
            name="situacao",
            field=models.CharField(default="", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="subunidade",
            name="nome",
            field=models.CharField(max_length=200),
        ),
    ]
