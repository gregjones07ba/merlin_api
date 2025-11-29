# merlin_api
Back-end API for Merlin gen-AI DM

# Build

1. cd lambda/[getMessages/postMessage]
1. ./build.sh
1. Upload lambda.zip to S3 dist/lambda/[getMessages/postMessages]/versions/[new version]/
1. Update API_VERSION in merlin_infra and deploy