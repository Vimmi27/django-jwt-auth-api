from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

        # the below line will hide password from the response, means the password is only for writing purpose and will not be shown for reading
        extra_kwargs = {
            'password': {'write_only': True}
        }

# In the below function we are over writing the default create function of django and extracting the password variable and hashing it
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # the set password will hash the password and we will save it.
            instance.set_password(password)
        instance.save()
        return instance
        #return super().create(validated_data)