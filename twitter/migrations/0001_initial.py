# Generated by Django 4.1.3 on 2023-09-05 20:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id_autor', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('nombre_usuario', models.CharField(max_length=150)),
                ('numero_seguidores', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id_tweet', models.BigIntegerField(primary_key=True, serialize=False)),
                ('texto', models.CharField(max_length=4000)),
                ('texto_limpio', models.CharField(max_length=4000, null=True)),
                ('fcreacion', models.DateTimeField(verbose_name='Fecha Creación')),
                ('retweets', models.IntegerField(null=True)),
                ('respuestas', models.IntegerField(null=True)),
                ('megusta', models.IntegerField(null=True)),
                ('citas', models.IntegerField(null=True)),
                ('vistas', models.IntegerField(null=True)),
                ('retweet', models.BooleanField(null=True)),
                ('tweet_url', models.CharField(blank=True, max_length=600, null=True)),
                ('mentions', models.CharField(blank=True, max_length=600, null=True)),
                ('hashtags', models.CharField(blank=True, max_length=600, null=True)),
                ('sentimiento', models.FloatField(null=True)),
                ('es_acoso', models.BooleanField(null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='twitter.autor')),
                ('respuesta_de', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='twitter.tweet')),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=200)),
                ('descripcion', models.TextField(null=True)),
                ('fcreacion', models.DateField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Busqueda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=300)),
                ('descripcion', models.CharField(max_length=300)),
                ('numero_resultados', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fbusqueda', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('reciente', models.BooleanField(null=True)),
                ('buscar_respuestas', models.BooleanField(null=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='twitter.tema')),
                ('tweets', models.ManyToManyField(to='twitter.tweet')),
            ],
        ),
    ]