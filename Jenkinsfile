pipeline {
  agent any

  parameters {
    string(name: 'TARGET_BRANCH', defaultValue: 'apache', description: 'Target branch from repo')
    string(name: 'TARGET_SERVER', defaultValue: '192.168.201.111', description: 'Target Webserver IP')
    // Per https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#string-interpolation, any sensitive params should be in single quotes
    password(name: 'SSH_KEY', defaultValue: '/var/jenkins_home/secrets/jenkinstest', description: 'Private key to SSH into Target server')
  }

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        // Create helloworld dynamically here
        sh('echo \"hello world, $params.TARGET_BRANCH\" > helloworld')
        // Pull repo
        git branch: "${params.TARGET_BRANCH}", credentialsId: 'fecde9db-7541-4d34-a7e2-fdfa2b6c1411', url: 'git@github.com:tommylimtech/helloworldjenkinstest.git'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying...'
        // The '-o "StrictHostKeyChecking no"' option below is a security risk and should not be used outside of testing.
        sh('scp -o \"StrictHostKeyChecking no\" -i $params.SSH_KEY \"$WORKSPACE/helloworld\" tlsre@$params.TARGET_SERVER:/var/www/html/')
        // Above line copies helloworld created dynamically in previous stage. Below line copies index.html file from repo pull in previous stage.
        sh('scp -o \"StrictHostKeyChecking no\" -i $params.SSH_KEY \"$WORKSPACE/index.html\" tlsre@$params.TARGET_SERVER:/var/www/html/')
      }
    }
  }
}
