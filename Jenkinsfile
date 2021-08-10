pipeline {
    agent any

    environment {
        NETLIFY_SITE_ID = credentials('netlify-blog-site-id')
        NETLIFY_TOKEN = credentials('netlify-token')
        PYENV_ROOT = '/var/lib/jenkins/.pyenv/'
    }

    stages {
        stage('Install') {
            steps {
                sh '${PYENV_ROOT}/bin/pyenv install --skip-existing'
            }
        }

        stage('Test') {
            steps {
                sh '${PYENV_ROOT}/shims/python -m unittest'
            }
        }

        stage('Build') {
            steps {
                sh '${PYENV_ROOT}/shims/python -m src build'
            }
        }

        stage('Publish') {
            when { branch 'master-blah' }
            steps {
                sh 'netlifyctl deploy -y -A "${NETLIFY_TOKEN}" -s "${NETLIFY_SITE_ID}" -m "jenkins: ${BUILD_TAG}"'
            }
        }

        stage('Notify') {
            when {
                expression {
                    return sh(returnStdout: true, script: "git tag --sort version:refname | tail -1").trim().matches("entry-(.*)")
                }
            }
            steps {
                sh 'echo TODO: tweet, slack, and facebook'
            }
        }
    }
}
