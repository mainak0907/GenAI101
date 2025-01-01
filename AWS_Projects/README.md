## AWS Basic Components 

### AWS Bedrock 
It has different types of GenAI Models , we need to request access to it.
Model ID's and Parametres can be found through the model card.
It has support with Langchain and also with boto3 , can be called in multiple ways.

### AWS Lambda 
This is the place where you write the code for the application. First we need to create a function . It uses the boto3 library and ensure that it is the latest version. You can deploy the code. The are are special functions and methods in code for accessing code. Go to configurations , in the permissions go to role name and give Administrative Permissions. if boto3 is giving error in lambda function , then need to add it using Layers.

### AWS Cloudwatch 
For every lambda function , there is a monitor section , we can see the Cloudwatch logs , for the execution of the lambda functions.

### AWS API Gateway 
This is where we can create APIs , their routes and get the endpoints. 
For every route , we need to add integrations and bind the lambda function.
In the Deploy section under the Stages section , we can create different stages \ stages like dev , qa , and others.

We can test the api endpoint from postman with payload as defined in the code. 

### AWLCLI Configuration 
awscli is a python package for accessing aws services through command line.
we need to go to IAM , create a user , generate the access keys through the security credentials section. 
we need to configure using the command -> aws configure 
we will be prompted to enter the access keys , region and output format which will be json.
