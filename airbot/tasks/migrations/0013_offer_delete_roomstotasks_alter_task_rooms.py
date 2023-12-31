# Generated by Django 4.2.4 on 2023-09-05 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_task_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=10)),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.room')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
            options={
                'verbose_name_plural': 'Offers',
                'unique_together': {('room', 'task')},
            },
        ),
        migrations.DeleteModel(
            name='RoomsToTasks',
        ),
        migrations.AlterField(
            model_name='task',
            name='rooms',
            field=models.ManyToManyField(through='tasks.Offer', to='tasks.room'),
        ),
    ]
