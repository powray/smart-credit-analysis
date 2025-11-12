#!/usr/bin/env bash
PROJECT_ID=${PROJECT_ID:-your-gcp-project}
SERVICE_NAME=${SERVICE_NAME:-smart-credit-api}
REGION=${REGION:-europe-west1}
IMAGE=gcr.io/${PROJECT_ID}/${SERVICE_NAME}:v1

gcloud builds submit --tag ${IMAGE}
gcloud run deploy ${SERVICE_NAME} --image ${IMAGE} --platform managed --region ${REGION} --allow-unauthenticated --memory 1Gi --set-env-vars OPENAI_API_KEY=
