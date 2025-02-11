# Generated by Django 5.1.4 on 2025-02-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Planificacion", "0005_actividad_cliente_constructora_vivienda_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vivienda",
            name="nombre",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Nombre de la Vivienda",
            ),
        ),
    ]
