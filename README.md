# Image as a service

Generate dynamic text over a fixed image based on query parameters

## Deploying Lambda Layer
[Reference](https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/)
```bash
mkdir python
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.7" /bin/sh -c "pip install -r requirements.txt -t python/; exit"

zip -r mypythonlibs.zip python > /dev/null

aws lambda publish-layer-version --layer-name LAYER_NAME --zip-file fileb://mypythonlibs.zip --compatible-runtimes "python3.7"

aws lambda update-function-configuration --layers arn:aws:lambda:ap-southeast-1:ACCOUNT_ID:layer:PIL-layer:LAYER_VERSION --function-name FUNCTION_NAME
```
