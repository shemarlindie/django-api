from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'is_active', 'date_joined', 'is_staff',
            'is_superuser', 'groups', 'password',

            'full_name', 'initials',
        ]
        read_only_fields = ['id', 'last_login', 'is_active', 'date_joined', 'is_staff', 'is_superuser', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super(UserSerializer, self).update(instance, validated_data)

    def validate_password(self, data):
        errors = []
        try:
            password_validation.validate_password(password=data)
        except ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_initials(self, obj):
        return f'{obj.first_name[0]}{obj.last_name[0]}'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
