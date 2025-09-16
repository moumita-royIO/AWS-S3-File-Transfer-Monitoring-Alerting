## AWS S3 File Transfer Monitoring & Alerting

The project has the following listed requirements which needs to be acheived using AWS resources and IAC tool - terraform.

1. Monitor two file shares in Azure Blob Storage. Every day, those files are transferred (copied/migrated) into AWS S3.In AWS, they both land inside the same bucket → s3://prod/, but under different prefixes (let’s call them Location1/ and Location2/). 

2. Confirm that the transferred files really reached S3 (not missing). File size is valid (≥100 KB). Log/output: list filename + size + status. The monitoring output email to be sent to owner if a file is not delivered to the S3 storage.

3. Additionally a weekly email summarising the files in both storage accounts so I can have confidence the monitoring is working.

Tech Stack Solution:

Amazon S3 – File storage & validation
AWS Lambda – File monitoring and alerting
AWS SES – Email notifications
Terraform – Infrastructure as code (IAC)
Amazon EventBridge – Scheduled triggers for weekly summary Lambda to send reports
AWS IAM (Identity and Access Management) – Manages permissions for the lambda roles with the least privilege required to access S3 and SES.

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
    ├── terraform.tfvars  #   
    ├── variables.tf     # declare variable from terraform.tfvars
    ├── provider.tf
    └── lambda/          # immediate_alert.py, weekly_summary.py, utils.py
         ├── helper.py
         ├── immediate_alert.py
         └── weekly_summary.py    
├── environment/
    ├── main.tf          # app servers, DBs, other env resources
    ├── variables.tf
    └── outputs.tf
```

