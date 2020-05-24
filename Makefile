PYTHON = python3
PROTOC = protoc
PYTHON_PROTOC = $(PYTHON) -m grpc_tools.protoc
PROTO_DIR = ./shared/proto

init:
	curl -sSL https://get.docker.com | sh
	sudo usermod -aG docker pi
	newgrp docker
	docker pull bitnami/zookeeper
	docker pull bitnami/kafka
	docker pull envoyproxy/envoy

build-proto:
	rm -f $(PROTO_DIR)/*pb2*.py
	$(PYTHON_PROTOC) \
		-I=$(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		$(PROTO_DIR)/*.proto
	sed -i -E "s/^import ([a-zA-Z0-9_]+_pb2) as/from . import \\1 as/" $(PROTO_DIR)/*_pb2*.py

watch-kafka:
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR) python3 tools/kafka_watcher.py

dashboard-all:
	docker build -t dashboard/envoy:v2 -f dashboard-envoy.dockerfile .
	docker build -t dashboard/webserver -f dashboard-webserver.dockerfile .
	docker rm -f dashboard.envoy.v2 || true
	docker rm -f dashboard.webserver || true
	docker run --name dashboard.envoy.v2 -d --network=host --restart always dashboard/envoy:v2
	docker run --name dashboard.webserver -d --network=host --restart always dashboard/webserver

irrigation-controller:
	docker build -t irrigation:controller -f irrigation-controller.dockerfile .
	docker rm -f irrigation.controller || true
	docker run --name irrigation.controller --privileged -d --network=host --restart always irrigation:controller

irrigation-monitor:
	docker build -t irrigation:monitor -f irrigation-monitor.dockerfile .
	docker rm -f irrigation.monitor || true
	docker run --name irrigation.monitor -d --network=host --restart always irrigation:monitor

irrigation-frontend:
	docker build -t irrigation:frontend -f irrigation-frontend.dockerfile .
	docker rm -f irrigation.frontend || true
	docker run --name irrigation.frontend -d --network=host --restart always irrigation:frontend

irrigation-all: irrigation-controller irrigation-monitor irrigation-frontend

weather-all:
	docker build -t weather -f weather.dockerfile .
	docker rm -f weather || true
	docker run --name weather -d --network=host --restart always weather
