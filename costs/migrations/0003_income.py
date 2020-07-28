# Generated by Django 3.0.8 on 2020-07-28 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('costs', '0002_auto_20200728_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('incomes_sum', models.DecimalField(decimal_places=2, max_digits=7)),
                ('date', models.DateField(auto_now_add=True)),
                ('pub_datetime', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'income',
                'ordering': ('-pub_datetime',),
            },
        ),
    ]