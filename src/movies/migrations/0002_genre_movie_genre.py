# Generated by Django 4.1.3 on 2023-04-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movies.genre'),
        ),
    ]
