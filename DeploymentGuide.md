## 🚀 Deployment

1. Clone the repo:

```bash
git clone https://github.com/your-username/AWS-S3-File-Transfer-Monitoring-Alerting.git

cd terraform/monitoring
```


2. Update '''terraform.tfvars''':

```hcl
bucket_name = "<name of the S3 bucket>"  # needs to be unique
owner_email = "youremail@example.com"
```


3. Deploy monitoring stack:

```bash
terraform init

terraform apply
```


4. Deploy environment stack (**optional**):

```bash
cd ../environment

terraform init

terraform apply
```

## Notes

- terraform.tfvars is ignored in GitHub for security.
- .zip files for Lambda code are included so functions work on deployment.
- AWS SES requires a verified email before sending notifications.
