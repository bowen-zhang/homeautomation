PYTHON = python3
PROTOC = protoc
PYTHON_PROTOC = $(PYTHON) -m grpc_tools.protoc
PROTO_DIR = ./proto

init:
	sudo apt-get install python3-pip -y
	sudo apt install protobuf-compiler -y

init-server: init
	pip3 install -r requirements.server.txt --user
	sudo apt install ffmpeg

init-node: init
	pip3 install -r requirements.node.txt --user

build-proto:
	rm -f $(PROTO_DIR)/*pb2*.py
	$(PYTHON_PROTOC) \
		-I=$(PROTO_DIR) -I=../ \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		$(PROTO_DIR)/*.proto
	sed -i -E "s/^import ([a-zA-Z0-9_]+_pb2) as/from . import \\1 as/" $(PROTO_DIR)/*_pb2*.py

setup: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) setup.py

run-server: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) server.py

run-node: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) node.py

install-node-on-pizero:
	sudo cp pizero/node.service /etc/systemd/system/ha-security-node.service
	sudo systemctl daemon-reload
	sudo systemctl start ha-security-node
	sudo systemctl enable ha-security-node