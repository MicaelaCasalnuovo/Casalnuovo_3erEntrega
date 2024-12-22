# Generated by Django 5.1.3 on 2024-12-22 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('direccion', models.TextField()),
                ('celular', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField()),
                ('stock', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nro_compra', models.CharField(max_length=20, unique=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.modeloproducto')),
            ],
        ),
        migrations.CreateModel(
            name='ModeloReseña',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas', to='App.modelocliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas', to='App.modeloproducto')),
            ],
        ),
    ]
