# helloworldjenkinstest
Testing Jenkins to deploy to ec2 to update web app

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
* Set Up Repo
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
#!/bin/bash
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
#!/bin/bash
sudo docker run --name jenkins-blueocean --rm --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro jenkins-blueocean:1.1
EOF

# Run Script to Spin Up BlueOcean Container
./run_jenkins_blueocean
```

## Set Up Jenkins
### Unlock Jenkins
* Browse to http://localhost:8080
* Input auto-generated password in the "Unlock Jenkins" prompt
  - Since we're running a Docker container, get it with `sudo docker exec jenkins-docker cat /var/jenkins_home/secrets/initialAdminPassword`
* Continue and Click *Install Suggested Plugins*
* Create First Admin User
* If page indicates "Jenkins is almost ready!", click *Restart*
* Login to Jenkins with Admin User

## GitHub SSH Key
_This step can be skipped if there's an existing SSH key to use for this purpose_
### Creating New SSH Key for GitHub
_Below is a condensed version of: [Connecting to GitHub with SSH](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)_
* On the Jenkins (or any box with openssh-client installed), run `ssh-keygen -t ed25519 -C "email@domain.com"`
* Select location where to save this new SSH key pair and provide name (defaults to `~/.ssh/id_ed25519`)
* Enter a passphrase if desired (more secure but prompts for passphrase everytime key is used)
* Copy contents of the *public* key `~/.ssh/id_ed25519.pub` *.pub* file.
  * We want to keep the *private* key (non *.pub*) file as secure as possible, making as few copies (file itself or contents) as needed.
* Log in to GitHub for the project we're working on with our target repo
* Navigate to *Account settings* by clicking on the account/profile icon in the upper right, then clicking on *Settings* in the dropdown list
* Click on *SSH and GPG keys* on the navigation bar and click *New SSH key*
  * Enter where or how this key is used in the *Title* field
  * Enter the *public* contents in the *Key* field and click *Add SSH key*
  * Enter GitHub password to continue

## Set Up Jenkins Pipeline
### Creating New Git Pipeline Project
* Enter Project Name
  * Select *Pipeline* from item list
  * Click *OK*
* In the *General* Tab/Section:
  * Enter *Description* to refer to at a later date for scope of pipeline
  * Check box for *GitHub project*
    * Enter link to GitHub repo (e.g. "git@github.com:tommylimtech/helloworldjenkinstest.git/")
* In the *Build Triggers* Tab/Section:
  * Check box for *Poll SCM* (This makes Jenkins continuously check your repo for any changes based on the schedule set using cron syntax [minor differences]. Clicking on the blue question mark icon next to the setting will explain it in more details)
    * For our test purposes, we set the *Schedule* to check every minute: `* * * * *`
* In the *Pipeline* Tab/Section:
  * Change *Definition* to *Pipeline script from SCM*
    * The *SCM* dropdown should say *Git*
      * In *Repositories*:
        * Set the *Repository URL* to the same GitHub repo as *GitHub project*
        * Click *Add* under *Credentials* and select *Jenkins* OR use an existing credential that has access to the target repo
          * Under *Kind*, select *SSH Username with private key*
          * Leaving the *ID* field blank since it gets auto-generated, set a useful *Description* and *Username* in their respective fields
          * Enter the contents of *Private* key (non *.pub* file) from the ssh-keygen in the *GitHub SSH Key* above
          * If a passphrase was used for the *private* key, enter it in the *Passphrase* field
      * In *Branches to build*:
        * Enter the target branch from the repo into the *Branch Specifier (blank for 'any')* (e.g. "*/apache")
    * Specify where the script is in the repo to run the pipeline. (e.g. "Jenkinsfile" - This means the Jenkinsfile lives on the root of the repo with the name "Jenkinsfile")
* Click *Save*

## Jenkinsfile
This is the Groovy script that Jenkins will run when there are changes to the repo. It will perform the pipeline project created in the previous step with the stages defined in this Jenkinsfile
### For this commit _a3eeaf0bab6bbb40f4dfa57369d2c70f92ef79b7_, here's what the Jenkinsfile does
* It has 3 parameters
  * "TARGET_BRANCH" is used for specifying which branch of the repo to pull when in the "Build" stage. In this example, we use "apache"
  * "TARGET_SERVER" is used for specifying which server to use for deploying changes. In this commit, the target was webserver created under *Test Systems* at the beginning of this README. This can be changed to an EC2 instance if the SSH keys were generated and added to the docker container
  * "SSH_KEY" is the location of the *private* key used for the secure copy (`scp` command) used later in this Jenkinsfile. This parameter is specified as password to see what it does in Jenkins
* It has 2 stages
  * The *Build* stage
    * Creates a file called "helloworld" and writes some text in it with a variable containing the "TARGET_BRANCH"
    * Pulls the specified repo from the "TARGET_BRANCH"
  * The *Deploy* stage
    * Copies over the helloworld file over to the default Apache webroot directory
    * Copies over the index.html file over to the default Apache webroot directory

## Make a Commit
Now, whenever a commit is pushed to the repo on the "apache" branch, the pipeline will run automatically and update the helloworld and index.html files in the Apache default webroot directory.

## Reverting a Commit
Use `git revert <unwanted commits>` to rollback changes

## Miscellaneous
In the scripts directory in the apache branch of this same repo, there's a simple Python script to upload or download an object in an S3 bucket called upOrDownS3Object.py

## References
* [Jenkins Getting Started Guide](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
* [Youtube Playlist of Jenkins Tutorials by Automation Step by Stepi (Raghav)](https://www.youtube.com/playlist?list=PLhW3qG5bs-L_ZCOA4zNPSoGbnVQ-rp_dG)
* [Docker Installation Guide](https://docs.docker.com/get-docker/)
* [Loose Reference to CD with Jenkins](https://www.twilio.com/blog/2018/06/continuous-delivery-with-jenkins-and-github-2.html)
* [Jenkinsfile Reference](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
* [Jenkinsfile Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Git Rollback Commit](https://stackoverflow.com/a/4114122)
