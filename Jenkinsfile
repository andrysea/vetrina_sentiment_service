
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timestamps()
    }

    triggers {
        pollSCM('H/2 * * * *')
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

        stage('Test automatici') {
            steps {
                sh '''
                    set -eu

                    export PATH="$HOME/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:$PATH"

                    docker run --rm \
                        --mount "type=bind,source=$WORKSPACE,target=/workspace,readonly" \
                        --workdir /workspace \
                        -e PYTHONDONTWRITEBYTECODE=1 \
                        python:3.13-slim \
                        sh -c 'python -m pip install --no-cache-dir -r requirements.txt && python -m pytest -p no:cacheprovider tests/ -v'
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    set -eu

                    export PATH="$HOME/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:$PATH"

                    echo "=== Costruzione immagine Docker ==="

                    docker build \
                        -t "vetrinia-sentiment:ci-${BUILD_NUMBER}" \
                        .

                    echo "=== Verifica immagine ==="

                    docker image inspect "vetrinia-sentiment:ci-${BUILD_NUMBER}"
                '''
            }
        }

        stage('Deploy Docker') {
            steps {
                sh '''
                    set -eu

                    export PATH="$HOME/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:$PATH"

                    export VETRINIA_IMAGE="vetrinia-sentiment:ci-${BUILD_NUMBER}"

                    echo "=== Verifica immagine da distribuire ==="

                    docker image inspect "$VETRINIA_IMAGE" --format '{{.Id}}'

                    echo "=== Deployment FastAPI ==="

                    docker compose \
                        --project-name vetrina_sentiment_service \
                        --file "$WORKSPACE/compose.yaml" \
                        --env-file "$HOME/Desktop/vetrina_sentiment_service/.env" \
                        config --quiet

                    docker compose \
                        --project-name vetrina_sentiment_service \
                        --file "$WORKSPACE/compose.yaml" \
                        --env-file "$HOME/Desktop/vetrina_sentiment_service/.env" \
                        up -d --no-deps --no-build --force-recreate api

                    echo "=== Attesa disponibilita FastAPI ==="

                    attempt=1

                    until curl --fail --silent --show-error \
                        --max-time 3 \
                        --output /dev/null \
                        http://127.0.0.1:8000/metrics
                    do
                        if [ "$attempt" -ge 15 ]; then
                            echo "FastAPI non disponibile"
                            docker logs --tail=50 vetrina_sentiment_service-api-1
                            exit 1
                        fi

                        echo "FastAPI non ancora pronto. Tentativo $attempt/15"

                        attempt=$((attempt + 1))
                        sleep 2
                    done

                    echo "FastAPI pronto!"

                    echo "=== Verifica endpoint /predict ==="

                    response="$(curl \
                        --fail --silent --show-error \
                        --max-time 5 \
                        -X POST http://127.0.0.1:8000/predict \
                        -H 'Content-Type: application/json' \
                        -d '{"review":"This product is amazing!"}')"

                    printf '%s\\n' "$response" | python3 -c 'import json, sys; data = json.load(sys.stdin); assert data["sentiment"] == "positive", data; print("Smoke test superato:", data["sentiment"])'

                    echo "=== Deployment completato ==="
                '''
            }
        }



    }

   post {
        success {
            echo 'Pipeline CI/CD completata con successo!'
        }

        failure {
            echo 'Pipeline CI/CD fallita: controllare la console.'
        }
    }
}
