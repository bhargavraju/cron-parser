from enum import Enum


class CronFieldType(Enum):
    MINUTE = "minute"
    HOURS = "hour"
    MONTH_DAY = "day of month"
    MONTH = "month"
    WEEK_DAY = "day of week"


VALID_RANGES = {
    CronFieldType.MINUTE: (0, 59),
    CronFieldType.HOURS: (0, 23),
    CronFieldType.MONTH_DAY: (1, 31),
    CronFieldType.MONTH: (1, 12),
    CronFieldType.WEEK_DAY: (1, 7),
}
