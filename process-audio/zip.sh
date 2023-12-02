# upload to AWS
cd package                                      
zip -r ../my_deployment_package.zip .
cd ..                                           
zip my_deployment_package.zip lambda_function.py
aws lambda update-function-code --function-name process_audio --zip-file fileb://my_deployment_package.zip  > /dev/null 2>&1
rm -r my_deployment_package.zip