# This script is used to train the model on GCP AI Platform

# `login to gcloud` # gcloud auth login
# `create project` # gcloud projects create talent-bias
# `change project` # gcloud config set project talent-bias
# `create billing account` # https://console.cloud.google.com/billing
# `enable billing for project` # https://console.cloud.google.com/billing/projects
# `create bucket` # gsutil mb -p talent-bias gs://talent-bias-vagueness # verify: `gsutil ls`

# `run script` # cd to dir containing `setup.py` then do `sh` on this script

echo "Submitting AI Platform PyTorch job"

# BUCKET_NAME: Change to your bucket name.
BUCKET_NAME=talent-bias-vagueness

# The PyTorch image provided by AI Platform Training.
IMAGE_URI=gcr.io/cloud-aiplatform/training/pytorch-gpu.1-7

# JOB_NAME: the name of your job running on AI Platform.
JOB_PREFIX=pytorch_job_vagueness_trainer
JOB_NAME=${JOB_PREFIX}_$(date +%Y%m%d_%H%M%S)

# This can be a GCS location to a zipped and uploaded package
PACKAGE_PATH=./toolkit

# REGION: select a region from https://cloud.google.com/ai-platform/training/docs/regions
# or use the default '`us-central1`'. The region is where the job will be run.
REGION=us-central1

# JOB_DIR: Where to store prepared package and upload output model.
JOB_DIR=gs://${BUCKET_NAME}/${JOB_PREFIX}/models/${JOB_NAME}

gcloud ai-platform jobs submit training ${JOB_NAME} \
    --region ${REGION} \
    --master-image-uri ${IMAGE_URI} \
    --scale-tier=CUSTOM \
    --master-machine-type=n1-standard-8 \
    --master-accelerator=type=nvidia-tesla-t4,count=2 \
    --job-dir ${JOB_DIR} \
    --module-name toolkit.vagueness_trainer.vagueness_training \
    --package-path ${PACKAGE_PATH} \
    -- \
    --model-name="vagueness-bert-uncased"

# Stream the logs from the job
gcloud ai-platform jobs stream-logs ${JOB_NAME}

# Verify the model was exported
echo "Verify the model was exported:"
gsutil ls ${JOB_DIR}/
