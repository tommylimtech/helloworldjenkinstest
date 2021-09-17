pipeline {
  agent any

  parameters {
    string(name: 'TARGET_BRANCH', defaultValue: 'apache', description: 'Target branch from repo')
    string(name: 'TARGET_DEV_SERVER', defaultValue: '192.168.201.111', description: 'Target Dev Webserver IP')
    string(name: 'TARGET_PD1_SERVER', defaultValue: 'ec2-instance-ip1', description: 'Target Prod1 Webserver IP')
    string(name: 'TARGET_PD2_SERVER', defaultValue: 'ec2-instance-ip2', description: 'Target Prod2 Webserver IP')
    // Per https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#string-interpolation, interpolation is an issue
    password(name: 'SSH_KEY', defaultValue: '/var/jenkins_home/secrets/jenkinstest', description: 'Private key to SSH into Target server')
  }

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        // Create helloworld dynamically here
        sh "echo \"hello world, ${params.TARGET_BRANCH}\" > helloworld"
        // Pull repo
        git branch: "${params.TARGET_BRANCH}", credentialsId: 'fecde9db-7541-4d34-a7e2-fdfa2b6c1411', url: 'git@github.com:tommylimtech/helloworldjenkinstest.git'
        // If AWS credentials are set correctly, pull an object from S3
        // Bucket: helloworldbucket, Key: some/path/to/object/image.jpg
        //sh "python3 ./scripts/upOrDownS3Object.py -b helloworldbucket -o images/image.jpg"
      }
    }
    stage('Deploy-Dev-Env') {
      steps {
        echo 'Deploying to Dev env...'
        // The '-o "StrictHostKeyChecking no"' option below is a security risk and should not be used outside of testing.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/helloworld\" tlsre@${params.TARGET_DEV_SERVER}:/var/www/html/"
        // Above line copies helloworld created dynamically in previous stage. Below line copies index.html file from repo pull in previous stage.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/index.html\" tlsre@${params.TARGET_DEV_SERVER}:/var/www/html/"
        // Put image in images directory
        //sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/images/image.jpg\" tlsre@${params.TARGET_DEV_SERVER}:/var/www/html/images/"
        // Test to see if deploy is working as expected
        script {
          try {
            sh "curl -s http://${params.TARGET_DEV_SERVER}"
          }
          catch (e) {
            echo 'Site didn\'t load properly, skip prod deploy'
            throw e
          }
        }
      }
    }
    stage('Deploy-Prod-Env') {
      steps {
        echo 'Deploying to Prod env, starting with box1...'
        /* This section commented out because there is no actual prod servers
        // The '-o "StrictHostKeyChecking no"' option below is a security risk and should not be used outside of testing.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/helloworld\" tlsre@${params.TARGET_PD1_SERVER}:/var/www/html/"
        // Above line copies helloworld created dynamically in previous stage. Below line copies index.html file from repo pull in previous stage.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/index.html\" tlsre@${params.TARGET_PD1_SERVER}:/var/www/html/"
        // Put image in images directory
        //sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/image.jpg\" tlsre@${params.TARGET_PD1_SERVER}:/var/www/html/images/"
        // Test to see if deploy is working as expected
        script {
          try {
            sh "curl -s http://${params.TARGET_PD1_SERVER}"
          }
          catch (e) {
            echo 'Site didn\'t load properly for prod box1, skip prod box2'
            throw e
          }
        }
        */

        echo 'Deploying to Prod box2...'
        /* This section commented out because there is no actual prod servers
        // The '-o "StrictHostKeyChecking no"' option below is a security risk and should not be used outside of testing.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/helloworld\" tlsre@${params.TARGET_PD2_SERVER}:/var/www/html/"
        // Above line copies helloworld created dynamically in previous stage. Below line copies index.html file from repo pull in previous stage.
        sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/index.html\" tlsre@${params.TARGET_PD2_SERVER}:/var/www/html/"
        // Put image in images directory
        //sh "scp -o \"StrictHostKeyChecking no\" -i ${params.SSH_KEY} \"$WORKSPACE/image.jpg\" tlsre@${params.TARGET_PD2_SERVER}:/var/www/html/images/"
        // Test to see if deploy is working as expected
        script {
          try {
            sh "curl -s http://${params.TARGET_PD2_SERVER}"
          }
          catch (e) {
            echo 'Site didn\'t load properly for prod box2, need to rollback'
            throw e
          }
        }
        */
      }
    }
  }
}
