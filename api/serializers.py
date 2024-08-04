from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Extraemos la contraseña para manejarla de manera segura
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hashea y guarda la contraseña
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Actualiza la contraseña de forma segura
        instance.save()
        return instance