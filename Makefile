prepare_data:
    unzip binary/vk.csv.zip -d binary/vk.csv
    
docker_build:
    docker build -t bank_assistant .

docker_run:
    docker run --name bank_assistant bank_assistant

run_app:
    docker_build
    docker_run

