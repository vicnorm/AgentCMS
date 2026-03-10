from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="pages/"),
        ),
        migrations.AddField(
            model_name="page",
            name="image_alt_text",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
