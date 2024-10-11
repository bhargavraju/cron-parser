from processors import get_processors
from constants import CronFieldType


class CronField:

    def __init__(self, text: str, field_type: CronFieldType):
        self.text = text
        self.field_type = field_type
        self.values = []
        self.load_values()

    def load_values(self):
        processors = get_processors()
        for processor in processors:
            if processor.validate_and_load(self.field_type, self.text, self.values):
                # print(f"Cron field: {self.field_type.value}, text: {self.text}, values: {self.values}")
                return

        raise ValueError(f"Not able to identify any know pattern for field {self.field_type.value} value: {self.text}")

    def get_values(self):
        return self.values

    def is_wild_card(self):
        return self.text == "*"
