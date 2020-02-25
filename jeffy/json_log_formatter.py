import json
import logging
import os
from decimal import Decimal

LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME = 'AWS_LAMBDA_REQUEST_ID'


def default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if int(obj) == obj else float(obj)
    try:
        return str(obj)
    except Exception:
        return None


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        result = {
            'lambda_request_id': os.getenv(LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME)
        }
        for attr, value in record.__dict__.items():
            if attr == 'asctime':
                value = self.formatTime(record)
            if attr == 'exc_info' and value is not None:
                value = self.formatException(value)
                if isinstance(value, str):
                    value = value.split('\n')
            if attr == 'stack_info' and value is not None:
                value = self.formatStack(value)
                if isinstance(value, str):
                    value = value.split('\n')
            if attr == 'msg':
                try:
                    value = record.getMessage()
                except Exception:
                    pass

            result[attr] = value

        return json.dumps(result, default=default, ensure_ascii=False)