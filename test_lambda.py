import json
import os
from unittest.mock import patch, MagicMock

# Set fake environment variable BEFORE importing lambda_function
os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789:FakeTopic'

from lambda_function import lambda_handler

# Fake S3 event helper
def make_event(filename):
    return {
        "Records": [{
            "s3": {
                "bucket": {"name": "untrusted-landing-primary-pc-11"},
                "object": {"key": filename}
            }
        }]
    }

@patch('lambda_function.s3_client')
@patch('lambda_function.sns_client')
def test_clean_file(mock_sns, mock_s3):
    result = lambda_handler(make_event("report.pdf"), None)
    mock_s3.copy_object.assert_not_called()  # clean file, no quarantine
    assert result['statusCode'] == 200
    print("✅ test_clean_file passed")

@patch('lambda_function.s3_client')
@patch('lambda_function.sns_client')
def test_malicious_file(mock_sns, mock_s3):
    result = lambda_handler(make_event("virus.exe"), None)
    mock_s3.copy_object.assert_called_once()  # should be quarantined
    mock_sns.publish.assert_called_once()     # should send alert
    assert result['statusCode'] == 200
    print("✅ test_malicious_file passed")

if __name__ == "__main__":
    test_clean_file()
    test_malicious_file()
    print("\n🎉 All tests passed!")