## AWS S3 File Transfer Monitoring & Alerting

The project has the following listed requirements which needs to be acheived using AWS resources and IAC tool - terraform.

1. Monitor two file shares in Azure Blob Storage. Every day, those files are transferred (copied/migrated) into AWS S3.In AWS, they both land inside the same bucket → s3://prod/, but under different prefixes (let’s call them Location1/ and Location2/). 

2. Confirm that the transferred files really reached S3 (not missing). File size is valid (≥100 KB). Log/output: list filename + size + status. The monitoring output email to be sent to owner if a file is not delivered to the S3 storage.

3. Additionally a weekly email summarising the files in both storage accounts so I can have confidence the monitoring is working.

**Tech Stack / Solution**

- Amazon S3 – File storage & validation. Stores daily transferred files and allows size verification.
- AWS Lambda – Monitors file uploads and triggers alerts for missing or undersized files.
- AWS SES – Sends immediate alerts and weekly summary emails to the owner.
- Terraform – Manages the infrastructure as code (IAC) for reproducibility and version control.
- Amazon EventBridge – Schedules the weekly summary Lambda to automatically send reports.
- AWS IAM – Provides least-privilege roles and permissions for Lambda functions to access S3 and SES securely.

4. When terraform destroy deletes environment. Monitoring process must not be deleted when the environment is rebuilt.

This can be managed by seperate terrform state for monitoring and environment and using 
'''lifecycle { prevent_destroy = true }''' in Terraform. This is Terraform's built-in feature to prevent resources from being destroyed accidentally:

```bash
terraform/
│
├── monitoring/
    ├── iam.tf
    ├── lambdas.tf 
    ├── S3.tf
    ├── event.tf
    ├── terraform.tfvars  #  assigns actual values to the variables declared in variables.tf
    ├── variables.tf     # declare variable from terraform.tfvars
    ├── provider.tf
    └── lambda/          
         ├── helper.py
         ├── immediate_alert.py
         └── weekly_summary.py    
├── environment/
    ├── main.tf          # app servers, DBs, other env resources
    ├── variables.tf
    └── outputs.tf
```

** This project includes pre-built Lambda .zip deployment packages (immediate_alert.zip and weekly_summary.zip).

These .zip files contain the Python code required for the AWS Lambda functions. They are kept in the repository for ease of deployment with Terraform. If wish to rebuild, the following commands are handy:

```bash
zip immediate_alert.zip immediate_alert.py helper.py

zip weekly_summary.zip weekly_summary.py helper.py
```
