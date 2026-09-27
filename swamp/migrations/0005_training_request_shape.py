from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("swamp", "0004_contactsubmission_subject"),
    ]

    operations = [
        migrations.RemoveField(model_name="training", name="title"),
        migrations.RemoveField(model_name="training", name="slug"),
        migrations.RemoveField(model_name="training", name="description"),
        migrations.RemoveField(model_name="training", name="image"),
        migrations.RemoveField(model_name="training", name="published"),
        migrations.RemoveField(model_name="training", name="featured"),
        migrations.RemoveField(model_name="training", name="order"),
        migrations.RemoveField(model_name="training", name="updated_at"),
        migrations.AddField(
            model_name="training",
            name="name",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="training",
            name="email",
            field=models.EmailField(default="", max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="training",
            name="message",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="training",
            name="target_dates",
            field=ArrayField(
                models.DateField(),
                blank=True,
                default=list,
                help_text="One or more dates the visitor proposed for the session.",
                size=None,
            ),
        ),
        migrations.AlterModelOptions(
            name="training",
            options={"ordering": ["-created_at"]},
        ),
    ]
