from rest_framework import serializers

from wushu.models.SandaWeightCategory import SandaWeightCategory


class SandaWeightCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SandaWeightCategory
        fields = '__all__'
        depth = 3