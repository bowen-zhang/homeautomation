PYTHON = python3
PROTOC = protoc
PYTHON_PROTOC = $(PYTHON) -m grpc_tools.protoc
PROTO_DIR = ./proto

init:
	sudo apt-get install python3-pip -y
	sudo apt install protobuf-compiler -y
	pip3 install -r requirements.txt --user

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

run: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) main.py
