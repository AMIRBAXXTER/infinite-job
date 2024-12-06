from django.db import models

from EmployersApp.models import JobAdvertisement

from UserApp.models import JobSeeker


# Create your models here.


class ApplyRequest(models.Model):
    job_advertisement = models.ForeignKey(JobAdvertisement, on_delete=models.CASCADE, verbose_name='آگهی استخدام')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, verbose_name='درخواست کننده')
    short_description = models.TextField(max_length=500, verbose_name='توضیحات کوتاه')
    status = models.CharField(default=0, max_length=10,
                              choices=((0, 'در انتظار بررسی'), (1, 'بررسی شده'), (2, 'تایید اولیه'), (3, 'رد شده'),),
                              verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به روز رسانی')

    class Meta:
        db_table = 'apply_request'

    def __str__(self):
        return f'{self.job_seeker_id} - {self.job_advertisement_id}'
