from sys import modules
from unittest.mock import MagicMock

modules["boto3"] = MagicMock()
modules["botocore.exceptions"] = MagicMock()
