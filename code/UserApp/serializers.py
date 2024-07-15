from rest_framework import serializers
from .models import *
from .utils import update_handler


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_employer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email not found.')
        return value


class LoginCodeVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        from django.core.cache import cache
        cache_key = f"login_code_{data['email']}"
        cached_code = cache.get(cache_key)
        print(cached_code)
        print(type(cached_code))
        print(type(data['code']))
        if str(cached_code) != data['code'] or cached_code is None:
            raise serializers.ValidationError('Invalid code.')
        return data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ForeignLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignLanguage
        fields = '__all__'


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    experience = ExperienceSerializer(many=True)
    skill = SkillSerializer(many=True)
    foreign_language = ForeignLanguageSerializer(many=True)
    social_media_link = SocialMediaLinkSerializer(many=True)

    class Meta:
        model = JobSeeker
        fields = '__all__'

    def create(self, validated_data):
        education = validated_data.pop('education')
        experience = validated_data.pop('experience')
        skill = validated_data.pop('skill')
        foreign_language = validated_data.pop('foreign_language')
        social_media_link = validated_data.pop('social_media_link')
        job_seeker = super().create(validated_data)
        for education_data in education:
            Education.objects.create(user=job_seeker, **education_data)
        for experience_data in experience:
            Experience.objects.create(user=job_seeker, **experience_data)
        for skill_data in skill:
            Skill.objects.create(user=job_seeker, **skill_data)
        for foreign_language_data in foreign_language:
            ForeignLanguage.objects.create(user=job_seeker, **foreign_language_data)
        for social_media_link_data in social_media_link:
            SocialMediaLink.objects.create(user=job_seeker, **social_media_link_data)
        return job_seeker

    def update(self, instance, validated_data):
        education = validated_data.pop('education')
        experience = validated_data.pop('experience')
        skill = validated_data.pop('skill')
        foreign_language = validated_data.pop('foreign_language')
        social_media_link = validated_data.pop('social_media_link')
        job_seeker = super().update(instance, validated_data)
        for education_data in education:
            update_handler(education_data, Education, job_seeker)

        for experience_data in experience:
            update_handler(experience_data, Experience, job_seeker)

        for skill_data in skill:
            update_handler(skill_data, Skill, job_seeker)

        for foreign_language_data in foreign_language:
            update_handler(foreign_language_data, ForeignLanguage, job_seeker)

        for social_media_link_data in social_media_link:
            update_handler(social_media_link_data, SocialMediaLink, job_seeker)

        return job_seeker


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
