FROM python:3
WORKDIR /ha
ADD ./irrigation/requirements.txt irrigation/
RUN pip3 install -r irrigation/requirements.txt
ADD ./shared/ shared/
ADD ./weather/proto/ weather/proto/
ADD ./third_party/common/ third_party/common/
ADD ./third_party/mongo_utils/ third_party/mongo_utils/
ADD ./irrigation/ irrigation/
ENV PYTHONPATH=/ha
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
CMD ["python", "irrigation/monitor.py", "--config_path=irrigation/config.protoascii", "--log_to_file"]
