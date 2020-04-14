FROM python:3
EXPOSE 17051
WORKDIR /ha
ADD ./irrigation/requirements.txt irrigation/
RUN pip3 install -r irrigation/requirements.txt
ADD ./third_party/common/ third_party/common/
ADD ./irrigation/ irrigation/
ENV PYTHONPATH=/ha
CMD ["python", "irrigation/main.py", "--dry_run", "--config_path=irrigation/config.protoascii"]

