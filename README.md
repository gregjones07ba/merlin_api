# merlin_api
Back-end API for Merlin gen-AI DM

# Build

1. cd lambda/[getMessages/postMessage]
1. ./build.sh
1. Upload lambda.zip to S3 dist/lambda/[getMessages/postMessages]/versions/[new version]/
1. Update API_VERSION in merlin_infra and deploy

# Test

## API

1. Navigate to API Gateway in AWS console
1. Stages
1. Copy Invoke URL
1. curl [invoke url]/api/v1/1/messages
1. curl "[invoke url]/api/v1/1/messages?start=1&end=3"

## Lambda

1. Navigate to Lambda function in AWS console
1. Test
1. Paste JSON from one of the sample payloads in lambda/[function]/payloads
1. Test

# Verify

## Dynamo

1. Navigate to Dynamo in AWS console
1. Explore Items
1. Select the table
