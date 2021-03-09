from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from user.models import User


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate_password2(self, value):
        if value != self.initial_data['password2']:
            raise ValidationError('password_mismatch')
        return value

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password2')
            user = super().create(validated_data)
            user.set_password(password)
            user.is_active = True
            user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
