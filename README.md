# Hello World Infra as Code 

## Description
This is a demonstration of how one would do infrastructure as code for a simple flask app,
the infrastructure would not change though if it was a more complicated flask app all that would change is the python code (`src/python`) and corresponding Dockerfile (`src/DockerFile`). The infrastructure is an autoscaling, load-balanced, ECS Fargate service that can be accessed only through HTTPS and blocks all HTTP requests. It is designed in a way that it could be built on different accounts and could also be deployed more than once within the same account for branch builds.

The infrastructure assumes that the user has nothing set up within their AWS account and will create everything from a VPC all the way to Cloudwatch alarms if the CPU of the service is higher than 70%.

## Disclaimer
Since this infrastructure as code is for demonstration purposes only it will not comply with most security standards and any user who wishes to use this code should use it with caution.

## How to Deploy

### Pre Req
 1. AWS CLI is configured on users computer/deployment process
 2. The flask app has a signed cert named `cert.pem` and `key.pem` in `src/python/` (Or that the python app has been modified in a way so that the docker container will have the cert and python is able to access the cert) (If Self Signing https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)
 3. Docker is configured on users computer/deployment process
 4. A valid cert is available within AWS (If Self Signing https://zuqqhi2.com/en/generating-self-signed-certificate-and-applying-to-aws-alb)

### Commands to run to deploy
 1. ```aws cloudformation validate-template --template-body file://src/infra/hello-world-ecr-infra.yaml``` This command is being used to ensure that we have a valid template for our ECR repository
 2. ```aws cloudformation validate-template --template-body file://src/infra/hello-world-infra.yaml``` This command is being used to ensure that we have a valid infrastructure template
 3. ```aws cloudformation deploy --template-file ./src/infra/hello-world-ecr-infra.yaml --stack-name hello-world-ecr --parameter-overrides Ecosystem=${YOURECOSYSTEMNAME}``` *Make sure to set your ecosystem name instead of just copying and pasting it* This command is the deployment command for the ECR (*Side note: ECR requires all names to be in lowercase and the ecosystem is being used in the name*)
 4. ```aws ecr get-login-password --region ${YOURAWSREGION} | docker login --username AWS --password-stdin ${YOURAWSACCOUNTNUMER}.dkr.ecr.${YOURAWSREGION}.amazonaws.com``` This command is logging you into ecr so that you can push up your container
 5. ```docker build -t ${YOURCONTAINERNAME} ./src/``` This is to build your docker container
 6. ``` docker tag ${YOURCONTAINERNAME}:latest ${YOURAWSACCOUNTNUMER}.dkr.ecr.${YOURAWSREGION}.amazonaws.com/${YOURCONTAINERNAME}:latest ``` This is to tag your locally built container for when we push it to the repo
 7. ``` docker push ${YOURAWSACCOUNTNUMER}.dkr.ecr.${YOURAWSREGION}.amazonaws.com/${YOURCONTAINERNAME}:latest ``` This is to push the container to ecr
 8. ```aws cloudformation deploy --template-file ./src/infra/hello-world-infra.yaml --stack-name hello-world-infra-build --capabilities CAPABILITY_IAM --parameter-override EmailAddress=${YOUREMAILADDRESS} Ecosystem=${YOURECOSYSTEMNAME} ImageId=${YOURIMAGEID} SSLCert=${YOURSSLCERT}``` This is to actually deploy all your infrastructure, it includes your email address to get alerts sent to if the CPU usage goes over 70, it includes the ecosystem naming scheme for your stack, it also includes your SSL cert that was mentioned in the Pre Req's
 9. `??? Profit` (All jokes aside if everything went smoothly until this point you should be able to go to your load balancer and see the DNS that will allow you to access your hello world from anywhere with an internet connection)


 ## FAQ

### *How could this be automated in a CI/CD Pipeline?*
> Personally, I would follow the steps described in the Commands to run as they test to ensure that the templates are valid. But in a true CI/CD situation since the templates are able to also be used for branch builds by specifying a branch as an eco system and giving it a unique stack name, I would deploy it in a way that there is an infra stack for every branch and each branch pushes a branch tagged docker image to the ECR.

### *How is it guaranteed that there isn't going to be downtime?*
> There is a guarantee, for no downtime because of the health checks that are being defined in ```AWS::ECS::Service``` even though I am not using the health checks to the full potential one could modify the health checks to use them to the full potential this way even if a new image is being defined the health check will happen and if the health check fails the new image will not proceed. Assuming that one had properly configured the health checks though, the health checks would be used to ensure that the new image is healthy, if it is healthy it will proceed with switching out the old images with the new ones. 

### *Why?*
> To demonstrate my skills and knowledge as a Cloud Infra Engineer

### Have other questions? Feel free to reach out to me
[LinkedIn](linkedin.com/in/calvinrosssmith/)

## Refrences Used 

https://zuqqhi2.com/en/generating-self-signed-certificate-and-applying-to-aws-alb
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
https://github.com/aws-samples/ecs-refarch-cloudformation/blob/master/services/website-service/service.yaml
