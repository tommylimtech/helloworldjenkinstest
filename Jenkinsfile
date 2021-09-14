pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        sh 'echo "hello world, apache" > helloworld'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying...'
        sh 'scp -i /var/jenkins_home/secrets/jenkinstest "$WORKSPACE/helloworld" tlsre@192.168.201.111:/var/www/html/'
      }
    }
  }
}
