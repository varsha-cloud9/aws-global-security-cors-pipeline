import json
import boto3
import urllib.parse
import os

# AWS Clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Bucket Names
PRIMARY_LANDING = "untrusted-landing-primary-pc-11"
SECONDARY_BACKUP = "dr-backup-vault-secondary-pc-11"
QUARANTINE_ZONE = "quarantine-zone-primary-pc-11"

# Dangerous file extensions
FORBIDDEN_EXTENSIONS = [
    '.exe',
    '.sh',
    '.bat',
    '.scr',
    '.ps1'
]

def lambda_handler(event, context):

    try:
        # Get uploaded file details from S3 event
        record = event['Records'][0]

        source_bucket = record['s3']['bucket']['name']

        file_key = urllib.parse.unquote_plus(
            record['s3']['object']['key'],
            encoding='utf-8'
        )

        print(f"Scanning uploaded file: {file_key}")

        # SAFER extension detection
        file_extension = os.path.splitext(file_key)[1].lower().strip()

        print(f"Detected extension: {file_extension}")

        # ==========================================
        # MALICIOUS FILE DETECTED
        # ==========================================
        if file_extension in FORBIDDEN_EXTENSIONS:

            print(f"🚨 Threat detected: {file_extension}")

            # Copy malicious file to quarantine bucket
            s3_client.copy_object(
                Bucket=QUARANTINE_ZONE,
                CopySource={
                    'Bucket': source_bucket,
                    'Key': file_key
                },
                Key=file_key
            )

            print(f"File moved to quarantine bucket: {QUARANTINE_ZONE}")

            # Delete malicious file from primary bucket
            s3_client.delete_object(
                Bucket=PRIMARY_LANDING,
                Key=file_key
            )

            print("Malicious file deleted from primary bucket")

            # Remove malicious file from backup bucket if present
            try:
                s3_client.delete_object(
                    Bucket=SECONDARY_BACKUP,
                    Key=file_key
                )

                print("Malicious file removed from backup bucket")

            except Exception as backup_error:
                print(f"Backup cleanup notice: {str(backup_error)}")

            # Send SNS alert
            alert_message = f"""
SECURITY ALERT

Malicious file detected and quarantined.

File Name: {file_key}
Extension: {file_extension}

Actions Taken:
- File moved to quarantine bucket
- File removed from primary bucket
- File removed from backup bucket
"""

            sns_client.publish(
                TopicArn=os.environ['SNS_TOPIC_ARN'],
                Subject='⚠️ Security Alert - Malicious File Detected',
                Message=alert_message
            )

            print("SNS alert sent successfully")

        # ==========================================
        # SAFE FILE
        # ==========================================
        else:

            print(f"✅ Safe file detected: {file_key}")

            # Copy safe file to backup bucket
            s3_client.copy_object(
                Bucket=SECONDARY_BACKUP,
                CopySource={
                    'Bucket': source_bucket,
                    'Key': file_key
                },
                Key=file_key
            )

            print(f"Safe file copied to backup bucket: {SECONDARY_BACKUP}")

        return {
            'statusCode': 200,
            'body': json.dumps('File processed successfully')
        }

    except Exception as e:

        print(f"Error occurred: {str(e)}")

        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }