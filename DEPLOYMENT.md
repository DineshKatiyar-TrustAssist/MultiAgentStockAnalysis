# GCP Deployment Guide

This guide explains how to deploy the Multi-Agent Stock Analyst application to Google Cloud Platform (GCP).

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed (for local testing)
4. **Google API Key** for Gemini AI

## Deployment Options

### Option 1: Cloud Run (Recommended)

Cloud Run is a serverless platform that automatically scales your application.

#### Step 1: Build and Push Container Image

```bash
# Set your GCP project ID
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest .

# Push to Google Container Registry
gcloud auth configure-docker
docker push gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest
```

#### Step 2: Deploy to Cloud Run

```bash
# Deploy with environment variable
gcloud run deploy multi-agent-stock-analyst \
  --image gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars GOOGLE_API_KEY=your-api-key-here
```

#### Step 3: Access Your Application

After deployment, Cloud Run will provide a URL like:
```
https://multi-agent-stock-analyst-xxxxx-uc.a.run.app
```

### Option 2: Using Cloud Build (CI/CD)

For automated deployments, use Cloud Build with the provided `cloudbuild.yaml`.

#### Step 1: Set Up Secret Manager (Recommended)

```bash
# Create a secret for the API key
echo -n "your-google-api-key" | gcloud secrets create google-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant Cloud Build access to the secret
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### Step 2: Update cloudbuild.yaml

Edit `cloudbuild.yaml` to use Secret Manager:

```yaml
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: gcloud
  args:
    - 'run'
    - 'deploy'
    # ... other args ...
    - '--update-secrets'
    - 'GOOGLE_API_KEY=google-api-key:latest'
```

#### Step 3: Create Cloud Build Trigger

```bash
# Create a trigger
gcloud builds triggers create github \
  --repo-name=your-repo-name \
  --repo-owner=your-github-username \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### Option 3: Compute Engine (VM)

For more control, deploy on a VM instance.

#### Step 1: Create VM Instance

```bash
gcloud compute instances create stock-analyst-vm \
  --image-family=cos-stable \
  --image-project=cos-cloud \
  --machine-type=e2-medium \
  --boot-disk-size=20GB
```

#### Step 2: Build and Push Image

```bash
# Build and push as in Option 1
docker build -t gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest .
docker push gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest
```

#### Step 3: Run Container on VM

```bash
# SSH into the VM
gcloud compute ssh stock-analyst-vm

# Install Docker (if not pre-installed)
# Then run:
docker run -d \
  -p 8501:8501 \
  -e GOOGLE_API_KEY=your-api-key \
  --name stock-analyst \
  gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest
```

## Environment Variables

The application requires the following environment variables:

- `GOOGLE_API_KEY`: Your Google Generative AI API key
- `APP_BASE_URL`: Base URL of your application (required for Cloud Run)
  - Example: `https://your-service-name-xxxxx.us-west1.run.app`
  - Used for generating email verification and password reset links

### Setting Environment Variables

**Cloud Run:**
```bash
gcloud run services update multi-agent-stock-analyst \
  --update-env-vars GOOGLE_API_KEY=your-api-key,APP_BASE_URL=https://your-service-url.run.app \
  --region us-central1
```

**Using Secret Manager (Recommended for Production):**
```bash
gcloud run services update multi-agent-stock-analyst \
  --update-secrets GOOGLE_API_KEY=google-api-key:latest \
  --region us-central1
```

## Local Testing

Before deploying, test the Docker image locally:

```bash
# Build the image
docker build -t multi-agent-stock-analyst:local .

# Run the container
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your-api-key \
  multi-agent-stock-analyst:local

# Access at http://localhost:8501
```

## Monitoring and Logs

### View Logs

```bash
# Cloud Run logs
gcloud run services logs read multi-agent-stock-analyst \
  --region us-central1 \
  --limit 50
```

### Set Up Monitoring

1. Go to Cloud Console → Cloud Run
2. Select your service
3. Click on "Monitoring" tab
4. Set up alerts for errors, latency, etc.

## Cost Optimization

- **Cloud Run**: Pay only for requests (good for low traffic)
- **Min Instances**: Set to 0 to avoid idle costs
- **Max Instances**: Limit to control costs during traffic spikes
- **Memory/CPU**: Adjust based on actual usage

## Troubleshooting

### Container fails to start

1. Check logs: `gcloud run services logs read multi-agent-stock-analyst`
2. Verify environment variables are set correctly
3. Ensure API key is valid

### Application is slow

1. Increase memory allocation: `--memory 4Gi`
2. Increase CPU: `--cpu 4`
3. Check Cloud Run metrics for bottlenecks

### Port issues

- Ensure port 8501 is exposed in Dockerfile
- Cloud Run automatically maps ports, but verify `--port 8501` is set

## Security Best Practices

1. **Use Secret Manager** for API keys (not environment variables)
2. **Enable authentication** if needed: `--no-allow-unauthenticated`
3. **Use IAM** to control access
4. **Enable VPC** for private networking if required
5. **Regular updates**: Keep base images and dependencies updated

## Scaling

Cloud Run automatically scales based on traffic:
- **Min instances**: 0 (default) - scales to zero when idle
- **Max instances**: Set based on expected traffic
- **Concurrency**: Default 80 requests per instance

Adjust these settings based on your needs:
```bash
gcloud run services update multi-agent-stock-analyst \
  --min-instances 1 \
  --max-instances 10 \
  --concurrency 80 \
  --region us-central1
```

## Cleanup

To remove the deployment:

```bash
# Delete Cloud Run service
gcloud run services delete multi-agent-stock-analyst \
  --region us-central1

# Delete container images
gcloud container images delete gcr.io/$PROJECT_ID/multi-agent-stock-analyst:latest
```

