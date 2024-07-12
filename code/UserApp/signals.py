from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, JobSeeker, Employer


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer:
            Employer.objects.create(user=instance)
        else:
            JobSeeker.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_employer:
        instance.employer.save()
    else:
        instance.jobseeker.save()
