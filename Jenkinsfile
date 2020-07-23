pipeline {
  agent {
    dockerfile {
      args '-e HOME=$WORKSPACE'
      additionalBuildArgs '--build-arg USER_ID=$(id -u)'
    }
  }
  stages {
    stage('Setup') {
      steps {
        withCredentials([sshUserPrivateKey(credentialsId: "marineroboticsmit", keyFileVariable: 'keyfile')]) {
                                    sh '''mkdir -p ~/.ssh/
                                    cp $keyfile ~/.ssh/id_rsa
                                    echo $GIT_SSH_COMMAND
                                    git submodule update --init --recursive
                                    rm -r ~/.ssh/
        '''
        }
        sh '''#!/bin/bash -l
        echo 'Update apt'
        sudo apt-get -y update
        catkin init
        catkin config --merge-devel
        catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
        '''
      }
    }
    stage('Build') {
      steps {
        echo 'Building'
        sh '''#!/bin/bash -l
        source /opt/ros/melodic/setup.bash
        catkin_make
        '''
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying....'
        echo 'Run on datasets (can this be done locally with docker?'
      }
    }
  }
  post {
    cleanup {
      cleanWs()
    }
  }
}
	
