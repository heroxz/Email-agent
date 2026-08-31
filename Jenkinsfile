
pipeline {
    agent any
    triggers {
        githubpush()
    }
    stages {
        stage('checkout') {
            steps {
                echo 'Checking out the code...'
                git branch: 'main', url: 'https://github.com/heroxz/Email-agent.git'

                sh '''
                    echo "Current commit:"
                    git rev-parse HEAD

                    echo "Repository content:"
                    ls -la
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh '''
                    if [ -f "requirements.txt" ]; then
                        echo "Installing dependencies from requirements.txt..."
                        python3 -m pip install -r requirements.txt
                    else
                        echo "No requirements.txt found. Skipping dependency installation."
                    fi
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    if [ -d "tests" ]; then
                        echo "Executing tests..."
                        python3 -m pytest tests/
                    else
                        echo "No tests found. Skipping tests."
                    fi
                '''
            }
        }
    }
    post {
        success {
            echo 'Build and tests completed successfully!'
        }
        unsuccessful {
            echo 'Build or tests failed. Please check the logs for details.'
        }
        always {
            echo 'Build finished.'
            
        }
    }
}

