# Generated by Django 5.0.6 on 2024-07-12 14:52

import django.core.validators
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='نام')),
                ('last_name', models.CharField(max_length=255, verbose_name='نام خانوادگی')),
                ('gender', models.CharField(max_length=10, verbose_name='جنسیت')),
                ('birth_date', models.DateField(verbose_name='تاریخ تولد')),
                ('national_code', models.CharField(max_length=10, verbose_name='کد ملی')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='درباره من')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='job_seeker/avatar', verbose_name='تصویر پروفایل')),
            ],
            options={
                'verbose_name': 'کارجو',
                'verbose_name_plural': 'کارجویان',
                'db_table': 'job_seekers',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='نام انگلیسی')),
            ],
            options={
                'verbose_name': 'استان',
                'verbose_name_plural': 'استان ها',
                'db_table': 'provinces',
            },
        ),
        migrations.CreateModel(
            name='ForeignLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=200, verbose_name='نام زبان')),
                ('level', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='سطح زبان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreign_languages', to='UserApp.jobseeker', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200, verbose_name='عنوان شغل')),
                ('company_name', models.CharField(max_length=200, verbose_name='نام شرکت')),
                ('start_date', models.DateField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateField(verbose_name='تاریخ پایان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='UserApp.jobseeker', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_field', models.CharField(max_length=200, verbose_name='رشته تحصیلی')),
                ('university', models.CharField(max_length=200, verbose_name='دانشگاه')),
                ('start_date', models.DateField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateField(verbose_name='تاریخ پایان')),
                ('average', models.DecimalField(decimal_places=2, max_digits=2, verbose_name='معدل')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='UserApp.jobseeker', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مدرک تحصیلی',
                'verbose_name_plural': 'مدارک نحصیلی',
                'db_table': 'educations',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='نام انگلیسی')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='UserApp.province', verbose_name='استان')),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهر ها',
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=200, verbose_name='آدرس')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ بروزرسانی')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.city', verbose_name='شهر')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.province', verbose_name='استان')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام مهارت')),
                ('level', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='سطح مهارت')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='UserApp.jobseeker', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_media_name', models.CharField(max_length=200, verbose_name='نام شبکه اجتماعی')),
                ('link', models.CharField(max_length=200, verbose_name='لینک')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_links', to='UserApp.jobseeker', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تماس')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('is_staff', models.BooleanField(default=False, verbose_name='مدیر/عضو')),
                ('is_employer', models.BooleanField(default=False, verbose_name='کارجو/شرکت')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, verbose_name='نام شرکت')),
                ('website', models.CharField(blank=True, max_length=255, null=True, verbose_name='سایت')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='employer/logo', verbose_name='لوگو')),
                ('industry_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='نوع صنعت')),
                ('employees_count', models.IntegerField(blank=True, null=True, verbose_name='تعداد کارمندان')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'شرکت',
                'verbose_name_plural': 'شرکت ها',
                'db_table': 'employers',
            },
        ),
    ]
