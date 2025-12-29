import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from car.models import Car
from car.serializers import CarSerializer


def serialize_car_object(car: Car) -> bytes:
    """
    Serialize Car object to JSON bytes
    :param car: Car model instance
    :return: JSON bytes with car data
    """
    try:
        # Create serializer instance with Car object
        serializer = CarSerializer(car)

        # Get dictionary data
        car_dict = serializer.data

        # Ensure problem_description is None if it's None in model
        if car.problem_description is None:
            car_dict["problem_description"] = None

        # Convert to JSON string and then to bytes
        json_str = json.dumps(car_dict, ensure_ascii=False)
        json_bytes = json_str.encode("utf-8")

        return json_bytes

    except Exception as e:
        # Handle serialization errors
        error_msg = f"Serialization error: {str(e)}"
        raise serializers.ValidationError(error_msg)


def deserialize_car_object(json_bytes: bytes) -> Car:
    """
    Deserialize JSON bytes to Car instance
    :param json_bytes: JSON bytes with car data
    :return: Car model instance (not saved to database)
    """
    try:
        # Decode bytes to string
        json_str = json_bytes.decode("utf-8")

        # Parse JSON data
        data = json.loads(json_str)

        # Handle null problem_description
        if ("problem_description" in data
                and data["problem_description"] is None):
            data["problem_description"] = None

        # Create serializer with data
        serializer = CarSerializer(data=data)

        # Validate data
        if serializer.is_valid():
            # Create Car instance from validated data
            car_instance = serializer.create(serializer.validated_data)

            # Additional validation on model level
            try:
                car_instance.full_clean()
            except ValidationError as e:
                raise serializers.ValidationError({
                    "model_errors": e.message_dict,
                    "message": "Model validation failed"
                })

            return car_instance
        else:
            # Raise error with validation details
            raise serializers.ValidationError({
                "errors": serializer.errors,
                "message": "Invalid car data"
            })

    except UnicodeDecodeError as e:
        raise serializers.ValidationError(f"Invalid UTF-8 encoding: {str(e)}")

    except json.JSONDecodeError as e:
        raise serializers.ValidationError(f"Invalid JSON: {str(e)}")

    except Exception as e:
        raise serializers.ValidationError(f"Deserialization error: {str(e)}")
