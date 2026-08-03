#!/bin/bash
set -e 

echo "Starting Lambda Deployment..."

cd "$(dirname "$0")/../Backend"

echo "Removing old package folder and zip..."

rm -rf "package"
rm -f "sports_alerts.zip"

echo "Reinstalling the dependencies..."

pip install requests -t package/ --break-system-packages

echo "Copying Python files into packages folder and making it into a Zip..."

cp sports_alerts.py package/
cd package
zip -r ../sports_alerts.zip .
cd ..

echo "Uploading files to Lambda on AWS..."

aws lambda update-function-code --function-name sports-alerts --zip-file fileb://sports_alerts.zip

echo "Deployment completed!"