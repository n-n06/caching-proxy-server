export $(grep -v '^#' .env | xargs) # load env variables
envsubst < prometheus.yml > generated-prometheus.yml
docker compose up -d prometheus
