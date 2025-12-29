import json
from rest_framework import serializers
from car.models import Car
from car.serializers import CarSerializer


def serialize_car_object(car: Car) -> bytes:
    """
    Serialize Car object to JSON bytes
    MUST include "id" field if it exists
    """
    try:
        # Get all data for serialization
        data = {
            "manufacturer": car.manufacturer,
            "model": car.model,
            "horse_powers": car.horse_powers,
            "is_broken": car.is_broken,
            "problem_description": car.problem_description
        }

        # IMPORTANT: Add id if it exists (car has been saved to DB)
        # Tests expect "id" field to be present
        if hasattr(car, "id") and car.id is not None:
            data["id"] = car.id

        # Convert to JSON string and then to bytes
        # Use default str conversion for consistent formatting
        json_str = json.dumps(data, separators=(",", ":"))
        return json_str.encode("utf-8")

    except Exception as e:
        error_msg = f"Serialization error: {str(e)}"
        raise serializers.ValidationError(error_msg)


def deserialize_car_object(json_bytes: bytes) -> Car:
    """
    Deserialize JSON bytes to Car instance
    """
    try:
        # Decode bytes to string
        json_str = json_bytes.decode("utf-8")

        # Parse JSON data
        data = json.loads(json_str)

        # Create serializer with data
        serializer = CarSerializer(data=data)

        # Validate data
        if serializer.is_valid():
            # Create Car instance from validated data
            car_instance = serializer.create(serializer.validated_data)
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
