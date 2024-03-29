# Generated by Django 5.0.1 on 2024-02-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "approved_by",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("certificate_id", models.CharField(max_length=100)),
                ("certificate_image", models.ImageField(upload_to="certificates/")),
                ("program_name", models.CharField(max_length=100)),
                ("stu_email", models.EmailField(blank=True, max_length=254, null=True)),
                ("stu_id", models.CharField(blank=True, max_length=100, null=True)),
                ("stu_name", models.CharField(blank=True, max_length=100, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
