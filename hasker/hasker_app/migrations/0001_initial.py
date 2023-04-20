# Generated by Django 4.2 on 2023-04-20 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('body', models.CharField()),
                ('answers_count', models.IntegerField()),
                ('votes_count', models.IntegerField()),
                ('creation_date', models.DateTimeField()),
                ('correct_answer_id', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('picture', models.FileField(upload_to='')),
                ('picture_data', models.BinaryField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('tag_id', models.ManyToManyField(to='hasker_app.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.user'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField()),
                ('votes_count', models.IntegerField()),
                ('creation_date', models.DateTimeField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='VoteQuestion',
            fields=[
                ('question_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hasker_app.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='VoteAnswer',
            fields=[
                ('answer_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hasker_app.answer')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hasker_app.user')),
            ],
        ),
    ]
