from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    lastname = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    username = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_null=False, allow_blank=False)
    password = serializers.CharField(allow_null=False, allow_blank=False)
    password_confirm = serializers.CharField(allow_null=False, allow_blank=False)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Passwords do not match!')
        return data