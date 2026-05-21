from apps.common.exceptions import NotEnoughDataError


def validate_dataset_size(count: int) -> None:
    if count < 3:
        raise NotEnoughDataError("Not enough data for reliable correlation.")
