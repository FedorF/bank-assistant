prepare_data:
	unzip binary/vk.csv.zip -d binary/
    
docker_build:
	docker build -t bank_assistant .

docker_run:
	docker run --name bank_assistant bank_assistant

run_app:
	unzip binary/vk.csv.zip -d binary/
	docker build -t bank_assistant .
	docker run --name bank_assistant bank_assistant
