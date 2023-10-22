cd package                                      
zip -r ../my_deployment_package.zip .
cd ..                                           
zip my_deployment_package.zip lambda_function.py
aws lambda update-function-code --function-name scriptGen --zip-file fileb://my_deployment_package.zip
rm -r my_deployment_package.zip