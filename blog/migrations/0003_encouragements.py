# Generated by Django 4.0.4 on 2022-05-29 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_topics_num_likes_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encouragements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=400)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
