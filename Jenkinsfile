pipeline {
    agent any
    triggers {
        githubPush()
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
                    set -e
        
                    echo "Python version:"
                    python3 --version
        
                    echo "Creating virtual environment..."
                    python3 -m venv .venv
        
                    echo "Upgrading pip..."
                    .venv/bin/python -m pip install --upgrade pip
        
                    if [ -f requirements.txt ]; then
                        echo "Installing dependencies from requirements.txt..."
                        .venv/bin/python -m pip install -r requirements.txt
                    fi
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    set -e
                    if [ -d "tests" ]; then
                        echo "Executing tests..."
                        .venv/bin/python3 -m pytest tests/
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
