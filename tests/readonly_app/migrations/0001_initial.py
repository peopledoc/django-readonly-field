from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wheel_number', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.IntegerField()),
                ('iban', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wheel_number', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=100)),
            ],
        ),
    ]
