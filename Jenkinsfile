pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'django-ecommerce'
        CONTAINER_NAME = 'django-app'
        APP_PORT = '8888'
        HOST_MEDIA_PATH = '/var/jenkins_home/workspace/django-ecommerce-pipeline/media'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out source code...'
                checkout scm
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    echo '🔧 Setting up environment...'
                    // Create media directory if it doesn't exist
                    sh 'mkdir -p media'
                    // Ensure proper permissions
                    sh 'chmod -R 755 media'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo '🐳 Building Docker image...'
                    // Build Docker image with build number tag
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    // Tag as latest
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                    echo "✅ Docker image built successfully: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Stop Existing Container') {
            steps {
                script {
                    echo '🛑 Stopping existing container...'
                    sh """
                        if docker ps -q --filter name=${CONTAINER_NAME} | grep -q .; then
                            echo "Stopping running container..."
                            docker stop ${CONTAINER_NAME}
                        else
                            echo "No running container found"
                        fi
                        
                        if docker ps -aq --filter name=${CONTAINER_NAME} | grep -q .; then
                            echo "Removing existing container..."
                            docker rm ${CONTAINER_NAME}
                        else
                            echo "No existing container to remove"
                        fi
                    """
                }
            }
        }
        
        stage('Deploy New Container') {
            steps {
                script {
                    echo '🚀 Deploying new container...'
                    sh """
                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:${APP_PORT} \
                        -v \$(pwd)/media:/app/media \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:latest
                    """
                    echo "✅ Container deployed successfully"
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo '🏥 Performing health check...'
                    // Wait for application to start
                    sleep(time: 30, unit: 'SECONDS')
                    
                    // Check if container is running
                    def containerStatus = sh(
                        script: "docker ps --filter name=${CONTAINER_NAME} --format '{{.Status}}'",
                        returnStdout: true
                    ).trim()
                    
                    if (containerStatus.contains('Up')) {
                        echo "✅ Health check passed! Container is running."
                        echo "🌐 Application URL: http://\$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${APP_PORT}"
                    } else {
                        error "❌ Health check failed! Container is not running properly."
                    }
                }
            }
        }
        
        stage('Cleanup Old Images') {
            steps {
                script {
                    echo '🧹 Cleaning up old Docker images...'
                    // Keep only the last 3 builds
                    sh """
                        # Get all image tags except 'latest', sort numerically, keep only old ones
                        OLD_IMAGES=\$(docker images ${DOCKER_IMAGE} --format 'table {{.Tag}}' | grep -E '^[0-9]+\$' | sort -nr | tail -n +4)
                        
                        if [ ! -z "\$OLD_IMAGES" ]; then
                            echo "Removing old images: \$OLD_IMAGES"
                            echo "\$OLD_IMAGES" | xargs -r -I {} docker rmi ${DOCKER_IMAGE}:{} || true
                        else
                            echo "No old images to remove"
                        fi
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo '🧽 Cleaning up workspace...'
            // Don't clean workspace to preserve media files
            // cleanWs()
        }
        success {
            script {
                def publicIp = sh(
                    script: "curl -s http://169.254.169.254/latest/meta-data/public-ipv4",
                    returnStdout: true
                ).trim()
                echo """
                🎉 Pipeline completed successfully!
                
                📱 Your Django application is now live at:
                🔗 http://${publicIp}:${APP_PORT}
                
                📊 Container Status:
                """
                sh "docker ps --filter name=${CONTAINER_NAME}"
            }
        }
        failure {
            echo """
            ❌ Pipeline failed! 
            
            🔍 Troubleshooting steps:
            1. Check the build logs above
            2. Verify Docker is running: docker ps
            3. Check container logs: docker logs ${CONTAINER_NAME}
            4. Ensure all dependencies are installed
            """
        }
    }
}
