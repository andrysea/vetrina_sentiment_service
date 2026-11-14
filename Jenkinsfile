
pipeline {
    agent any // Esegue la pipeline su un agente Jenkins disponibile

    options {
        skipDefaultCheckout(true) // Evita il checkout automatico duplicato
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Recupero il codice da GitHub...'
                checkout scm
            }
        }

        stage('Verifica ambiente') {
            steps {
                sh '''
                    set -eu

                    export PATH="$HOME/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:$PATH"

                    echo "=== Commit Git ==="
                    git rev-parse --short HEAD

                    echo "=== Python ==="
                    command -v python3
                    python3 --version

                    echo "=== Docker ==="
                    command -v docker
                    docker --version
                    docker info --format '{{.ServerVersion}}'
                '''
            }
        }
    }

    post {
        success {
            echo 'Verifica iniziale Jenkins completata!'
        }

        failure {
            echo 'Verifica iniziale fallita: controllare la console.'
        }
    }
}
