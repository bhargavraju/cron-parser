import sys
from cron_expression import CronExpression

class CronParser:

    def __init__(self, cron_exp_string):
        self.cron_string = cron_exp_string
        self.cron_expression = CronExpression(self.cron_string)

    def process(self):
        self.cron_expression.print_details()

    def get_result_dict(self): # Added only for tests
        return self.cron_expression.get_result_dict()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        args_string = ", ".join(sys.argv[1:])
        raise ValueError(f"The program expects the cron expression as a single string but got: {args_string}")
    cron_string = sys.argv[1]
    cron_parser = CronParser(cron_string)
    cron_parser.process()
