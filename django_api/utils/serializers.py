from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user if user.is_authenticated else None
        return super(BaseModelSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user if user.is_authenticated else None
        return super(BaseModelSerializer, self).update(instance, validated_data)
