pipeline {
    agent any

    environment {
        NETLIFY_TOKEN = credentials('netlify-token')
        PYENV_ROOT = '/var/lib/jenkins/.pyenv/'
    }

    stages {
        stage('Install') {
            steps {
                sh '${PYENV_ROOT}/bin/pyenv install --skip-existing'
            }
        }

        stage('Build') {
            steps {
                sh '${PYENV_ROOT}/shims/python -m src build'
            }
        }

        stage('Publish') {
            steps {
                sh 'netlifyctl deploy -y -A "${NETLIFY_TOKEN}" -n "www.alexrecker.com" -m "jenkins: ${BUILD_TAG}"'
            }
        }
    }
}
