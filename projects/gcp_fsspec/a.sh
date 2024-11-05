export PATH=$PWD/local_data/google-cloud-sdk/bin:$PATH


# setup application default credentials
gcloud auth application-default login
#
# gcloud auth activate-service-account --key-file=$PWD/local_data/gcp_service_account.json