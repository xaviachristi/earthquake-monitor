aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
docker build --provenance=false --platform=linux/amd64  -t c17-quake-pipeline-ecr-tf:latest .
docker tag c17-quake-pipeline-ecr-tf:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c17-quake-pipeline-ecr-tf:latest
docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c17-quake-pipeline-ecr-tf:latest