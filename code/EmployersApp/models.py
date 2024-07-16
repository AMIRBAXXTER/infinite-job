from django.db import models

from UserApp.models import Employer


# Create your models here.

class JobAdvertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    location = models.CharField(max_length=100, verbose_name='مکان')
    cooperation_type = models.CharField(max_length=100,
                                        choices=[('full_time', 'full_time'), ('part_time', 'part_time')],
                                        verbose_name='نوع همکاری')
    minimum_expertise = models.CharField(max_length=100, choices=[('less 1 year', 'less 1 year'),
                                                                  ('between 1 and 3 years', 'between 1 and 3 years'),
                                                                  ('between 3 and 5 years', 'between 3 and 5 years'),
                                                                  ('more than 5 years', 'more than 5 years')],
                                         verbose_name='حداقل سابقه کار')
    salary = models.PositiveIntegerField(verbose_name='حقوق')
    description = models.TextField(verbose_name='توضیحات')
    about_company = models.TextField(verbose_name='درباره شرکت')
    required_skills = models.TextField(blank=True, null=True, verbose_name='مهارت های لازم')
    military_service_status = models.CharField(max_length=100,
                                               choices=[('end of service', 'end of service'),
                                                        ('medical exemption', 'medical exemption'),
                                                        ('permanent exemption', 'permanent exemption')], blank=True,
                                               null=True, verbose_name='وضعیت سربازی')
    gender = models.CharField(max_length=100, blank=True, null=True,
                              choices=[('male', 'male'), ('female', 'female'), ('both', 'both')],
                              verbose_name='جنسیت')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name='شرکت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به روز رسانی')


class JobCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=100, verbose_name='نام در url')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی')
    advertise = models.ManyToManyField(JobAdvertisement, blank=True, verbose_name='آگهی')

    def __str__(self):
        return self.name
