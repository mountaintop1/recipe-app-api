"""
Serializers for user API views
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the users object
    """
    class Meta:
        """Define the model and fields to use"""

        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Extra settings for the model
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a user, setting the password correctly and return it
        """
        # Remove password from validated data
        password = validated_data.pop('password', None)
        # Call update method on the model
        user = super().update(instance, validated_data)
        # Set password if it exists
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication object
    """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get('email')
        password = attrs.get('password')
        # Authenticate user
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # Check if authentication is successful
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        # Set user in the context
        attrs['user'] = user
        return attrs
