# Generated by Django 3.2 on 2021-07-29 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentReply',
        ),
    ]
