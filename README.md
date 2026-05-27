# AWS Global Security Pipeline

## Overview

AWS Global Security Pipeline is a serverless DevSecOps project built using Amazon Web Services to automatically detect suspicious file uploads in Amazon S3, isolate malicious files into a quarantine bucket, replicate safe files to a disaster recovery backup bucket, and send real-time security notifications using Amazon SNS.

This project demonstrates:

* Event-driven serverless architecture
* Automated threat detection
* Multi-region disaster recovery design
* Real-time security alerting
* Automated quarantine workflow
* Cross-region backup replication
* Cloud monitoring and logging

---

# Architecture Diagram

```text
                    +----------------------+
                    |   User Uploads File  |
                    +----------+-----------+
                               |
                               v
         +---------------------------------------------+
         |  Untrusted Landing Bucket (Primary Region) |
         | untrusted-landing-primary-pc-11            |
         +----------------+----------------------------+
                              |
                              | S3 ObjectCreated Event
                              v
               +--------------------------------+
               | AWS Lambda Security Scanner    |
               | global-s3-security-scanner     |
               +---------------+----------------+
                               |
                +--------------+--------------+
                |                             |
                |                             |
                v                             v
      +-------------------+       +--------------------------+
      | Safe File         |       | Malicious File           |
      +-------------------+       +--------------------------+
                |                             |
                v                             v
 +--------------------------------+   +--------------------------------+
 | Backup Bucket (DR Region)      |   | Quarantine Bucket              |
 | dr-backup-vault-secondary      |   | quarantine-zone-primary        |
 +--------------------------------+   +--------------------------------+
                                                 |
                                                 v
                                   +----------------------------+
                                   | Amazon SNS Email Alert     |
                                   +----------------------------+
```

---

# AWS Services Used

| Service           | Purpose                        |
| ----------------- | ------------------------------ |
| Amazon S3         | File storage and event trigger |
| AWS Lambda        | Automated security scanning    |
| Amazon SNS        | Real-time alert notifications  |
| Amazon CloudWatch | Logs and monitoring            |
| AWS IAM           | Secure access management       |

---

# Multi-Region Architecture

| Bucket Name                     | Region    | Purpose                  |
| ------------------------------- | --------- | ------------------------ |
| untrusted-landing-primary-pc-11 | us-east-1 | Incoming file uploads    |
| dr-backup-vault-secondary-pc-11 | us-west-2 | Disaster recovery backup |
| quarantine-zone-primary-pc-11   | us-east-1 | Malicious file isolation |

---

# Project Workflow

## Safe File Workflow

1. User uploads safe file
2. File lands in untrusted landing bucket
3. Lambda scans file extension
4. File is identified as safe
5. Safe file is copied to backup bucket
6. CloudWatch logs generated

### Example Safe Files

* resume.pdf
* notes.txt
* image.png

---

## Malicious File Workflow

1. User uploads suspicious file
2. File lands in untrusted landing bucket
3. Lambda scans file extension
4. Malicious extension detected
5. File copied to quarantine bucket
6. File removed from primary bucket
7. SNS alert notification triggered
8. CloudWatch security logs generated

### Example Malicious Files

* virus.exe
* malware.bat
* script.ps1
* payload.scr

---

# Lambda Function Features

The Lambda function performs the following actions:

* Detects uploaded file extension
* Scans for dangerous file types
* Replicates safe files to DR backup bucket
* Isolates malicious files into quarantine bucket
* Deletes malicious files from primary bucket
* Sends SNS security alerts
* Generates CloudWatch monitoring logs

---

# IAM Permissions Used

The Lambda execution role includes:

* s3:GetObject
* s3:PutObject
* s3:DeleteObject
* sns:Publish
* logs:CreateLogGroup
* logs:CreateLogStream
* logs:PutLogEvents

---

# Screenshot Section

## 1. S3 Multi-Region Buckets

![S3 Buckets](screenshots/s3-buckets.png)

Description: Shows all three S3 buckets configured across multiple AWS regions.

---

## 2. Lambda Function Dashboard

![Lambda Dashboard](screenshots/lambda-dashboard.png)

Description: Displays Lambda function configuration and runtime environment.

---

## 3. S3 Trigger Configuration

![Lambda Trigger](screenshots/lambda-trigger.png)

Description: Shows S3 ObjectCreated trigger connected to Lambda.

---

## 4. Safe File Replication

![Safe File Backup](screenshots/safe-file-backup.png)

Description: Shows safe file successfully copied into disaster recovery backup bucket.

---

## 5. Quarantine Bucket Detection

![Quarantine Detection](screenshots/quarantine-detection.png)

Description: Shows malicious file isolated into quarantine bucket.

---

## 6. SNS Security Alert

![SNS Alert](screenshots/sns-alert.png)

Description: Displays email notification triggered for malicious file detection.

---

## 7. CloudWatch Logs

![CloudWatch Logs](screenshots/cloudwatch-logs.png)

Description: Shows Lambda execution logs, threat detection events, and monitoring output.

---

# Sample CloudWatch Logs

```text
Scanning uploaded file: virus.exe
Detected extension: .exe
Threat detected: .exe
File moved to quarantine bucket
Malicious file deleted from primary bucket
SNS alert sent successfully
```

---

# Security Features

* Zero-trust file upload model
* Automated malicious file isolation
* Event-driven security scanning
* Real-time alert notifications
* Disaster recovery replication
* Multi-region resilience
* Serverless automation

---

# Testing Performed

## Safe File Test

Uploaded:

```text
resume.pdf
```

Result:

* File remained in primary bucket
* File replicated to backup bucket
* No SNS alert generated

---

## Malicious File Test

Uploaded:

```text
virus.exe
```

Result:

* File moved to quarantine bucket
* File deleted from primary bucket
* SNS security alert triggered
* CloudWatch logs generated

---

# Future Enhancements

* VirusTotal API integration
* File hash analysis
* MIME type validation
* DynamoDB audit logging
* Terraform infrastructure deployment
* Dashboard monitoring
* Multi-account support

---

# Resume Description

### AWS Global Security Pipeline

Developed a serverless DevSecOps security pipeline using Amazon S3, AWS Lambda, SNS, IAM, and CloudWatch to automatically detect malicious file uploads, isolate threats into quarantine storage, replicate safe files using cross-region replication workflows, and generate real-time security alerts through event-driven serverless automation and monitoring.

---

# Author

Varsha Wananje

GitHub Repository:

[https://github.com/varsha-cloud9/aws-global-security-pipeline](https://github.com/varsha-cloud9/aws-global-security-pipeline)
