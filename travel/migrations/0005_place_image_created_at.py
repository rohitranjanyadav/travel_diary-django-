from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("travel", "0004_place_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="place_image",
            field=models.ImageField(blank=True, null=True, upload_to="places/"),
        ),
        migrations.AddField(
            model_name="place",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
