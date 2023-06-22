from fastapi import HTTPException, status


def validate_car_uid(car_uid: str) -> None:
    """Validates if provided string is valid car_uid

    Args:
        car_uid (str): string to be evaluated

    Raises:
        HTTPException: if invalid
    """
    if not (2 <= len(car_uid) <= 10 and car_uid[0] == "C" and car_uid[1:].isnumeric()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{car_uid} is not a valid uid. Please use C<number up to 9 digits> format"
            )