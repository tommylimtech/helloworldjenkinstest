pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        echo "hello world" > helloworld
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying...'
        sh 'scp -i /var/jenkins_home/secrets/jenkinstest "$WORKSPACE/helloworld" tlsre@192.168.201.111:/usr/share/nginx/html/main/'
      }
    }
  }
}
