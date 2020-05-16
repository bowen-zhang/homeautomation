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
		-I=$(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		$(PROTO_DIR)/*.proto
	sed -i -E "s/^import ([a-zA-Z0-9_]+_pb2) as/from . import \\1 as/" $(PROTO_DIR)/*_pb2*.py

setup: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) setup.py

run-controller: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) controller.py

test-controller: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) controller.py --dry_run

run-monitor: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) monitor.py

test-monitor: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) monitor.py --dry_run

run-frontend: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) frontend.py

run-cli: build-proto
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python' PYTHONPATH=$(CURDIR)/.. $(PYTHON) tools/cli.py

run-tests: build-proto
	$(foreach file, $(wildcard ./tests/*.py), PYTHONPATH=$(CURDIR)/.. $(PYTHON) $(file);)
