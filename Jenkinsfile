pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        // Create helloworld dynamically here
        sh 'echo "hello world, apache" > helloworld'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying...'
        // The '-o "StrictHostKeyChecking no"' option below is a security risk and should not be used outside of testing.
        sh 'scp -o "StrictHostKeyChecking no" -i /var/jenkins_home/secrets/jenkinstest "$WORKSPACE/helloworld" tlsre@192.168.201.111:/var/www/html/'
      }
    }
  }
}
