# Generated by Django 4.0.5 on 2022-07-20 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0002_programme_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('programme_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cohorts', to='programmes.programme')),
            ],
        ),
    ]
