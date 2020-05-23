PYTHON = python3
PROTOC = protoc
PYTHON_PROTOC = $(PYTHON) -m grpc_tools.protoc
CLOSURE_COMPILER = tools/closure-compiler-v20200406.jar
JS_IMPORT_STYLE = closure,binary

init:
	sudo apt-get install python3-pip -y
	pip3 install -r requirements.txt --user

build-js:
	rm -rf ./build
	mkdir -p ./build/irrigation
	$(PROTOC) \
		-I=../irrigation/proto \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/irrigation \
		--grpc-web_out=mode=grpcweb:./build/irrigation \
		../irrigation/proto/*.proto
	mkdir -p ./build/weather
	$(PROTOC) \
		-I=../weather/proto -I../ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/weather \
		--grpc-web_out=mode=grpcweb:./build/weather \
		../weather/proto/*.proto
	mkdir -p ./build/protobuf/src/google/protobuf
	$(PROTOC) \
		-I=../third_party/protobuf/src/ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/protobuf/src/google/protobuf \
		../third_party/protobuf/src/google/protobuf/any.proto
	$(PROTOC) \
		-I=../third_party/protobuf/src/ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/protobuf/src/google/protobuf \
		../third_party/protobuf/src/google/protobuf/struct.proto
	$(PROTOC) \
		-I=../third_party/protobuf/src/ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/protobuf/src/google/protobuf \
		../third_party/protobuf/src/google/protobuf/empty.proto
	$(PROTOC) \
		-I=../third_party/protobuf/src/ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/protobuf/src/google/protobuf \
		../third_party/protobuf/src/google/protobuf/timestamp.proto
	$(PROTOC) \
		-I=../third_party/protobuf/src/ \
		--js_out=import_style=$(JS_IMPORT_STYLE):./build/protobuf/src/google/protobuf \
		../third_party/protobuf/src/google/protobuf/duration.proto
	java \
					-jar $(CLOSURE_COMPILER) \
					--js ./build/irrigation \
					--js ./build/weather \
					--js ./build/protobuf \
					--js ../third_party/closure-library/closure/goog \
					--js ../third_party/protobuf/js/map.js \
					--js ../third_party/protobuf/js/message.js \
					--js ../third_party/protobuf/js/binary/arith.js \
					--js ../third_party/protobuf/js/binary/constants.js \
					--js ../third_party/protobuf/js/binary/decoder.js \
					--js ../third_party/protobuf/js/binary/encoder.js \
					--js ../third_party/protobuf/js/binary/reader.js \
					--js ../third_party/protobuf/js/binary/utils.js \
					--js ../third_party/protobuf/js/binary/writer.js \
					--js ../third_party/grpc-web/javascript \
					--entry_point=goog:proto.ha.irrigation.IrrigationServiceClient \
					--entry_point=goog:proto.ha.weather.WeatherServiceClient \
					--js_output_file web/js/services.js
	
run:
	PYTHONPATH=$(CURDIR)/.. $(PYTHON) main.py
