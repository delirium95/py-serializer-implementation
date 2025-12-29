import json
from rest_framework import serializers
from car.models import Car


def serialize_car_object(car: Car) -> bytes:
    """
    Serialize Car object to JSON bytes
    MUST include "id" field if it exists
    """
    try:
        # Get all data for serialization
        data = {
            "id": car.id,
            "manufacturer": car.manufacturer,
            "model": car.model,
            "horse_powers": car.horse_powers,
            "is_broken": car.is_broken,
            "problem_description": car.problem_description
        }

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
    Preserves id field if present
    """
    try:
        # Decode bytes to string
        json_str = json_bytes.decode("utf-8")

        # Parse JSON data
        data = json.loads(json_str)

        # Extract id if present
        car_id = data.get("id")

        # Create Car instance with basic fields
        car = Car(
            manufacturer=data["manufacturer"],
            model=data["model"],
            horse_powers=data["horse_powers"],
            is_broken=data["is_broken"],
            problem_description=data.get("problem_description")
        )

        # Set id on the instance (important for tests!)
        if car_id is not None:
            car.id = car_id

        return car

    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")

    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 encoding: {str(e)}")

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")

    except Exception as e:
        raise ValueError(f"Deserialization error: {str(e)}")
