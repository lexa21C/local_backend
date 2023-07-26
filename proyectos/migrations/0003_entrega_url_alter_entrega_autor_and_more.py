# Generated by Django 4.1.3 on 2023-07-25 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_alter_entrega_autor'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='autor',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='calificacion',
            field=models.CharField(blank=True, choices=[('en revision', 'en revision'), ('aprobado', 'Aprobado'), ('No aprobado', 'No aprobado')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='documento',
            field=models.FileField(upload_to='entrega/documento'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='estado',
            field=models.CharField(choices=[('activo', 'activo'), ('inactivo', 'inactivo'), ('abandono_grupo_proyecto', 'abandono_grupo_proyecto')], default='activo', max_length=30),
        ),
    ]
