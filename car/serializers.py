from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator


class CarSerializer(serializers.Serializer):
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    horse_powers = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1914)
        ]
    )
    is_broken = serializers.BooleanField()
    problem_description = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True
    )

    def create(self, validated_data):
        """
        Create and return a new Car instance
        """
        from .models import Car
        return Car(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Car instance
        """
        instance.manufacturer = (validated_data.
                                 get("manufacturer", instance.manufacturer))
        instance.model = (validated_data.
                          get("model", instance.model))
        instance.horse_powers = (validated_data.
                                 get("horse_powers", instance.horse_powers))
        instance.is_broken = (validated_data.
                              get("is_broken", instance.is_broken))
        instance.problem_description = (validated_data.
                                        get("problem_description",
                                            instance.problem_description))
        return instance
