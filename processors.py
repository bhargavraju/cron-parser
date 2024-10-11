from constants import CronFieldType, VALID_RANGES
from abc import ABC, abstractmethod


class CronFieldProcessor(ABC): # interface

    @abstractmethod
    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        pass

class StarProcessor(CronFieldProcessor):

    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        if len(field_text) == 1 and field_text == '*':
            lower_range, upper_range = VALID_RANGES[field_type]
            values.extend(range(lower_range, upper_range+1))
            return True
        return False


class NumberProcessor(CronFieldProcessor):

    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        if not field_text.isdigit():
            return False

        lower_range, upper_range = VALID_RANGES[field_type]
        val = int(field_text)
        if val < lower_range or val > upper_range:
            raise ValueError(f"Value given for {field_type.value} need to be within limits {lower_range}, {upper_range}, got: {val}")
        values.append(val)
        return True


class NumberRangeProcessor(CronFieldProcessor):

    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        val_range = field_text.split('-')
        if len(val_range) != 2:
            return False

        lower_str, upper_str = val_range[0], val_range[1]
        if not lower_str.isdigit() or not upper_str.isdigit():
            raise ValueError(f"Upper and lower ranges for {field_type.value} need to numbers, got: {lower_str}, {upper_str}")

        lower_val, upper_val = int(lower_str), int(upper_str)
        lower_range, upper_range = VALID_RANGES[field_type]
        if lower_val < lower_range or upper_val > upper_range:
            raise ValueError(f"Upper and lower ranges for {field_type.value} need to be within limits {lower_range}, {upper_range}, got: {lower_val}, {upper_val}")
        if upper_val <= lower_val:
            raise ValueError(f"Upper range should be greater than lower range for {field_type.value}, got: {lower_val}, {upper_val}")

        values.extend(range(lower_val, upper_val + 1))
        return True


class NumberIntervalProcessor(CronFieldProcessor):

    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        vals = field_text.split('/')
        if len(vals) != 2:
            return False

        left_str, right_str = vals[0], vals[1]
        if left_str != '*' and not left_str.isdigit():
            raise ValueError(f"Starting point for interval should be '*' or a valid number for {field_type.value}, got: {left_str}")
        if not right_str.isdigit():
            raise ValueError(f"Interval value for {field_type.value} should be an integer, got: {right_str}")

        lower_range, upper_range = VALID_RANGES[field_type]
        start_from = lower_range if left_str == '*' else int(left_str)
        interval = int(right_str)

        if start_from < lower_range or start_from > upper_range:
            raise ValueError(f"Starting point for interval for {field_type.value} should be within limits {lower_range}, {upper_range}, got: {start_from}")
        if interval < max(1, lower_range) or interval > upper_range: # does not make sense for interval to be 0
            raise ValueError(f"Interval value for {field_type.value} should be with limits {max(1, lower_range)}, {upper_range}, got: {interval}")

        values.extend(range(start_from, upper_range + 1, interval))
        return True


class CommaSeparatedNumbersProcessor(CronFieldProcessor):

    def validate_and_load(self, field_type: CronFieldType, field_text: str, values: list) -> bool:
        vals = field_text.split(',')
        if len(vals) < 2:
            return False

        for val in vals:
            if not val.isdigit():
                raise ValueError(f"All values in comma separated values for {field_type.value} should be numbers, got {val} from {field_text}")

            value = int(val)
            lower_range, upper_range = VALID_RANGES[field_type]
            if value < lower_range or value > upper_range:
                raise ValueError(f"All values in comma separated values for {field_type.value} should lie within limits {lower_range}, {upper_range}, got {val} from {field_text}")

        values.extend(map(int, vals))
        return True


star_processor = StarProcessor()
number_processor = NumberProcessor()
number_range_processor = NumberRangeProcessor()
number_interval_processor = NumberIntervalProcessor()
comma_numbers_processor = CommaSeparatedNumbersProcessor()

def get_processors() -> list[CronFieldProcessor]:
    return [star_processor, number_processor, number_range_processor, comma_numbers_processor, number_interval_processor]


def get_valid_month_days(month: int):
    match month:
        case 1:
            return 1, 31
        case 2:
            return 1, 28
        case 3:
            return 1, 31
        case 4:
            return 1, 30
        case 5:
            return 1, 31
        case 6:
            return 1, 30
        case 7:
            return 1, 31
        case 8:
            return 1, 31
        case 9:
            return 1, 30
        case 10:
            return 1, 31
        case 11:
            return 1, 30
        case 12:
            return 1, 31
        case _:
            raise ValueError("Unrecognised month value")
