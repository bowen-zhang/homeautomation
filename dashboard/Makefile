PYTHON = python3
PROTOC = $(PYTHON) -m grpc_tools.protoc
PROTO_DIR = ./proto

init:
	pip3 install -r requirements.txt --user

run:
	PYTHONPATH=$(CURDIR) $(PYTHON) main.py
