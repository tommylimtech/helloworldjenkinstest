# helloworldjenkinstest
Testing Jenkins to deploy to ec2 to update web app
---

## Prerequisites
1. Hardware
   - 2 GB RAM
   - 10 GB Disk Drive
2. Software
   - Java (JRE or JDK) 8 or 11
   - Docker
   - Jenkins

## Test Systems
Two Ubuntu 20.04.3 VMs:
1. Jenkins Server
2. Webserver

## Installing Prerequisites
### Java Install
```Bash
# Update repos, search, and install latest openjdk
sudo apt update
sudo apt search openjdk
sudo apt install openjdk-16-jdk
# Check install
java -version
### Version Output ###
# openjdk version "16.0.1" 2021-04-20
# OpenJDK Runtime Environment (build 16.0.1+9-Ubuntu-120.04)
# OpenJDK 64-Bit Server VM (build 16.0.1+9-Ubuntu-120.04, mixed mode, sharing)
```

### Docker Install
* Prep for Docker Repo
```Bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
```
* Add Docker Official GPG Key
```Bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
* Setup Repo
```Bash
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
* Install Docker
```Bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
* Verify Docker Install
```Bash
sudo docker run hello-world
```

### Jenkins Install
* Create Bridge Network
```Bash
sudo docker network create jenkins
```
* Create Bash Script to Download and Run Jenkins Docker Image
```Bash
# Create Script to Run Jenkins Docker Image
cat <<EOF > run_jenkins
sudo docker run --name jenkins-docker --rm --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind --storage-driver overlay2
EOF

# Run Script to Spin Up Jenkins Container
./run_jenkins

# Create Dockerfile for BlueOcean Plugin
# This Dockerfile is used to build a local image
cat <<EOF > Dockerfile
FROM jenkins/jenkins:2.303.1-jdk11
USER root
RUN apt-get update && apt-get install -y apt-transport-https \
       ca-certificates curl gnupg2 \
       software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.24.7 docker-workflow:1.26"
EOF

# Build BlueOcean Docker Image from Dockerfile
sudo docker build -t jenkins-blueocean:1.1 .

# Create Script to Run BlueOcean Docker Image
cat <<EOF > run_jenkins_blueocean
sudo docker run --name jenkins-blueocean --rm --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro jenkins-blueocean:1.1
EOF

# Run Script to Spin Up BlueOcean Container
./run_jenkins_blueocean
```

## Setup Jenkins
### Unlock Jenkins
* Browse to http://localhost:8080
* Input auto-generated password in the "Unlock Jenkins" prompt
  - Since we're running a Docker container, get it with `sudo docker exec jenkins-docker cat /var/jenkins_home/secrets/initialAdminPassword`
* Continue and Click "Install Suggested Plugins"
* Create First Admin User
* If page indicates "Jenkins is almost ready!", click "Restart"
* Login to Jenkins with Admin User

<To Be Continued>
