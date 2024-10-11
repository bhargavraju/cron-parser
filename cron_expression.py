from cron_field import CronField
from constants import CronFieldType
from processors import get_valid_month_days


class CronExpression:

    minute_field: CronField = None
    hour_field: CronField = None
    day_of_month_field: CronField = None
    month_field: CronField = None
    day_of_week_field: CronField = None
    command_field: str = None

    cron_fields = [
        (CronFieldType.MINUTE, "minute_field"),
        (CronFieldType.HOURS, "hour_field"),
        (CronFieldType.MONTH_DAY, "day_of_month_field"),
        (CronFieldType.MONTH, "month_field"),
        (CronFieldType.WEEK_DAY, "day_of_week_field")
    ]

    def __init__(self, text: str):
        self.load_expression(text)

    def load_expression(self, text):
        cron_field_texts = text.split()
        if len(cron_field_texts) != 6:
            raise ValueError(f'Given cron expression "{text}" does not have 5 cron elements')

        errors = []
        for (cron_field_type, field_name), cron_field_text in zip(self.cron_fields, cron_field_texts[:-1]):
            try:
                setattr(self, field_name, CronField(cron_field_text, cron_field_type))
            except Exception as e:
                errors.append(str(e))
        self.command_field = cron_field_texts[-1]
        self.add_contextual_errors(errors)

        if errors:
            all_errors = "\n".join(errors)
            raise ValueError(f"Errors during initialisation:\n{all_errors}")

    def add_contextual_errors(self, errors: list):
        # Check for month and day combinations
        if self.month_field is None or self.day_of_month_field is None:
            return
        month_values = self.month_field.get_values()
        day_of_month_values = self.day_of_month_field.get_values()
        if month_values and day_of_month_values and not self.day_of_month_field.is_wild_card():
            for month in month_values:
                valid_range = get_valid_month_days(month)
                for month_day in day_of_month_values:
                    if month_day < valid_range[0] or month_day > valid_range[1]:
                        errors.append(f"The month {month} does not have the day {month_day}")

    def print_details(self):
        print(f"{CronFieldType.MINUTE.value:<14}", " ".join(map(str, self.minute_field.get_values())))
        print(f"{CronFieldType.HOURS.value:<14}", " ".join(map(str, self.hour_field.get_values())))
        print(f"{CronFieldType.MONTH_DAY.value:<14}", " ".join(map(str, self.day_of_month_field.get_values())))
        print(f"{CronFieldType.MONTH.value:<14}", " ".join(map(str, self.month_field.get_values())))
        print(f"{CronFieldType.WEEK_DAY.value:<14}", " ".join(map(str, self.day_of_week_field.get_values())))
        print(f"{'command':<14}", self.command_field)

    def get_result_dict(self):
        # Added for test cases
        return {
            CronFieldType.MINUTE: self.minute_field.get_values(),
            CronFieldType.HOURS: self.hour_field.get_values(),
            CronFieldType.MONTH_DAY: self.day_of_month_field.get_values(),
            CronFieldType.MONTH: self.month_field.get_values(),
            CronFieldType.WEEK_DAY: self.day_of_week_field.get_values(),
            'command': self.command_field
        }
