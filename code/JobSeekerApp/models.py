from django.db import models

from EmployersApp.models import JobAdvertisement

from UserApp.models import JobSeeker


# Create your models here.


class ApplyRequest(models.Model):
    job_advertisement = models.ForeignKey(JobAdvertisement, on_delete=models.CASCADE, verbose_name='آگهی استخدام')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, verbose_name='درخواست کننده')
    status = models.CharField(default=0, max_length=10,
                              choices=((0, 'pending'), (1, 'accepted'), (2, 'rejected'), ))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'apply_request'

    def __str__(self):
        return f'{self.job_seeker_id} - {self.job_advertisement_id}'