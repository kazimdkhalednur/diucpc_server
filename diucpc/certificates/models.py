from django.db import models


class Certificate(models.Model):
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    certificate_id = models.CharField(max_length=100)
    certificate_image = models.ImageField(upload_to="certificates/")
    program_name = models.CharField(max_length=100)
    stu_email = models.EmailField(blank=True, null=True)
    stu_id = models.CharField(max_length=100, blank=True, null=True)
    stu_name = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.certificate_id
