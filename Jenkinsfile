pipeline {
    agent any
    
    // Run automatically whenever code is pushed to the repository
    triggers {
        pollSCM('* * * * *')
    }

    environment {
        // You would typically store these securely in Jenkins Credentials
        // and inject them here rather than hardcoding.
        AZURE_OPENAI_API_KEY = credentials('azure-openai-api-key')
        AZURE_OPENAI_ENDPOINT = credentials('azure-openai-endpoint')
        AZURE_OPENAI_API_VERSION = '2024-02-15-preview'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                # Install uv if not present
                curl -LsSf https://astral.sh/uv/install.sh | sh
                
                # Install project dependencies
                uv sync
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                # Run the fast, mocked unit tests so we don't consume OpenAI API credits
                uv run pytest tests/test_agent_mock.py -v
                '''
            }
        }
    }
    
    post {
        failure {
            echo 'Build Failed! The application crashed or tests failed.'
        }
        success {
            echo 'Build Passed! The application is error-free.'
        }
    }
}
