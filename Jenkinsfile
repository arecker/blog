pipeline {
    agent any

    environment {
        PYENV_ROOT = '/var/lib/jenkins/.pyenv/'
    }

    stages {
        stage('Install') {
            steps {
                sh '${PYENV_ROOT}/bin/pyenv install -s'
            }
        }

        stage('Build') {
            steps {
                sh '${PYENV_ROOT}/shims/python -m src build'
            }
        }
    }
}
