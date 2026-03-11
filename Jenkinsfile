pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Run Python') {
      steps {
        sh 'python3 sensor.py'
      }
    }
  }
  post {
    success { echo 'SUCCESS' }
    failure { echo 'FAILURE' }
  }
}
