from abc import abstractmethod

from django.core.validators import MaxValueValidator
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    This model is abstract and is inherited by Employer and JobSeeker models.
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تماس')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_staff = models.BooleanField(default=False, verbose_name='مدیر/عضو')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    @abstractmethod
    def __str__(self):
        pass

    object = CustomUserManager()

    class Meta:
        abstract = True


class Employer(CustomUser):
    company_name = models.CharField(max_length=255, verbose_name='نام شرکت')
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name='سایت')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    logo = models.ImageField(upload_to='employer/logo', null=True, blank=True, verbose_name='لوگو')
    industry_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='نوع صنعت')
    employees_count = models.IntegerField(null=True, blank=True, verbose_name='تعداد کارمندان')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت ها'
        db_table = 'employers'


class JobSeeker(CustomUser):
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    gender = models.CharField(max_length=10, verbose_name='جنسیت')
    birth_date = models.DateField(verbose_name='تاریخ تولد')
    national_code = models.CharField(max_length=10, verbose_name='کد ملی')
    about_me = models.TextField(null=True, blank=True, verbose_name='درباره من')
    avatar = models.ImageField(upload_to='job_seeker/avatar', null=True, blank=True, verbose_name='تصویر پروفایل')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'کارجو'
        verbose_name_plural = 'کارجویان'
        db_table = 'job_seekers'


class Province(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام')
    slug = models.SlugField(max_length=200, null=True, blank=True, verbose_name='نام انگلیسی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'
        db_table = 'provinces'


class City(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام')
    slug = models.SlugField(max_length=200, null=True, blank=True, verbose_name='نام انگلیسی')
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='استان')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'
        db_table = 'cities'


class Address(models.Model):
    user = models.ForeignKey(CustomUser, related_name='addresses', on_delete=models.CASCADE,
                             verbose_name='کاربر')
    province = models.ForeignKey(Province, related_name='addresses', on_delete=models.CASCADE, verbose_name='استان')
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE, verbose_name='شهر')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ بروزرسانی')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return f'{self.user}:{self.id}'

    def save(self, *args, **kwargs):
        if self.is_active:
            self.user.addresses.filter(is_active=True).update(is_active=False)
        if not self.user.addresses.all().exists():
            self.is_active = True

        super(Address, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_active:
            temp = self.user.addresses.filter(is_active=False).first()
            if temp:
                temp.is_active = True
                temp.save()

        super(Address, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
        db_table = 'addresses'


class Education(models.Model):
    study_field = models.CharField(max_length=200, verbose_name='رشته تحصیلی')
    university = models.CharField(max_length=200, verbose_name='دانشگاه')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(verbose_name='تاریخ پایان')
    average = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='معدل')
    user = models.ForeignKey(JobSeeker, related_name='educations', on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.user}:{self.id}'

    class Meta:
        verbose_name = 'مدرک تحصیلی'
        verbose_name_plural = 'مدارک نحصیلی'
        db_table = 'educations'


class Experience(models.Model):
    job_title = models.CharField(max_length=200, verbose_name='عنوان شغل')

    company_name = models.CharField(max_length=200, verbose_name='نام شرکت')

    start_date = models.DateField(verbose_name='تاریخ شروع')

    end_date = models.DateField(verbose_name='تاریخ پایان')

    user = models.ForeignKey(JobSeeker, related_name='experiences', on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.user}:{self.id}'


class Skill(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام مهارت')
    level = models.PositiveIntegerField(validators=[MaxValueValidator(5)], verbose_name='سطح مهارت')
    user = models.ForeignKey(JobSeeker, related_name='skills', on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.user}:{self.id}'


class ForeignLanguage(models.Model):
    language_name = models.CharField(max_length=200, verbose_name='نام زبان')
    level = models.PositiveIntegerField(validators=[MaxValueValidator(5)], verbose_name='سطح زبان')
    user = models.ForeignKey(JobSeeker, related_name='foreign_languages', on_delete=models.CASCADE,
                             verbose_name='کاربر')

    def __str__(self):
        return f'{self.user}:{self.id}'


class SocialMediaLink(models.Model):
    social_media_name = models.CharField(max_length=200, verbose_name='نام شبکه اجتماعی')
    link = models.CharField(max_length=200, verbose_name='لینک')

    user = models.ForeignKey(JobSeeker, related_name='social_media_links', on_delete=models.CASCADE,
                             verbose_name='کاربر')

    def __str__(self):
        return f'{self.user}:{self.id}'
