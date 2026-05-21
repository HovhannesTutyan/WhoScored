from apps.common.exceptions import NotEnoughDataError


def validate_historical_data_available() -> None:
    raise NotEnoughDataError("Not enough historical data.")
