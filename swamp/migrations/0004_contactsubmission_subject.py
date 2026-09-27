from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("swamp", "0003_resource_icon_filefield"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactsubmission",
            name="subject",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
    ]
