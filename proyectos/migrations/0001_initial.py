# Generated by Django 4.1.3 on 2023-07-28 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Centros_de_formacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, unique=True)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('encargado', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField(unique=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField()),
                ('modalidad', models.CharField(choices=[('presencial', 'Presencial'), ('virtual', 'Virtual')], default='presencial', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_grupo', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inscrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('activo', 'activo'), ('inactivo', 'inactivo'), ('abandono_grupo_proyecto', 'abandono_grupo_proyecto')], default='activo', max_length=30)),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.ficha')),
                ('nombre_grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='proyectos.grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Regional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('aprendiz', 'Aprendiz'), ('instructor', 'Instructor'), ('admin', 'Admin'), ('anonimo', 'Anonimo')], max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Revision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=300)),
                ('descripcion', models.CharField(max_length=5000)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='proyectos/foto')),
                ('codigo_fuente', models.URLField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('terminado', 'terminado'), ('en revision', 'en revision'), ('en desarrollo', 'en desarrollo'), ('anulado', 'anulado'), ('en correccion', 'en correcion')], default='en revision', max_length=20)),
                ('calificacion', models.CharField(blank=True, max_length=15, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('editado', models.DateTimeField(auto_now=True)),
                ('aprendiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.inscrito')),
                ('categorias', models.ManyToManyField(blank=True, null=True, to='proyectos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, unique=True)),
                ('centros_de_formacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.centros_de_formacion')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.PositiveIntegerField(unique=True)),
                ('tipo_documento', models.CharField(choices=[('CC', 'CC'), ('TI', 'TI'), ('CE', 'CE'), ('PASAPORTE', 'PASAPORTE')], max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='perfiles')),
                ('web', models.URLField(blank=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('editado', models.DateTimeField(auto_now=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.rol')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='inscrito',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.perfil'),
        ),
        migrations.AddField(
            model_name='ficha',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.programa'),
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.CharField(blank=True, choices=[('en revision', 'en revision'), ('aprobado', 'Aprobado'), ('No aprobado', 'No aprobado')], default='en revision', max_length=20, null=True)),
                ('descripcion_entrega', models.CharField(max_length=5000)),
                ('respuesta_instructor', models.CharField(blank=True, max_length=5000, null=True)),
                ('instructor', models.CharField(blank=True, max_length=300, null=True)),
                ('autor', models.CharField(blank=True, max_length=300, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('editado', models.DateTimeField(auto_now=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='entrega/documento')),
                ('url', models.URLField(blank=True, null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.proyecto')),
                ('tipo_revision', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.tipo_revision')),
            ],
        ),
        migrations.AddField(
            model_name='centros_de_formacion',
            name='regional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proyectos.regional'),
        ),
    ]
