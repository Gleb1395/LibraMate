from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "password2",
            "is_staff",
            "phone",
            "username",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def validate(self, attrs):
        password = attrs.pop("password")
        password2 = attrs.pop("password2", None)
        if password != password2:
            raise serializers.ValidationError("passwords don't match")
        return attrs


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = ("email",)
        fields = ("email", "first_name", "last_name", "phone", "username")
