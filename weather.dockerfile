FROM python:3
EXPOSE 17060
WORKDIR /ha
ADD ./weather/requirements.txt weather/
RUN pip3 install -r weather/requirements.txt
ADD ./shared/ shared/
ADD ./third_party/common/ third_party/common/
ADD ./third_party/mongo_utils/ third_party/mongo_utils/
ADD ./weather/ weather/
ENV PYTHONPATH=/ha
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
CMD ["python", "weather/main.py", "--config_path=weather/config.protoascii", "--log_to_file"]
