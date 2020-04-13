FROM python:3
EXPOSE 6250
WORKDIR /ha
ADD ./dashboard/requirements.txt dashboard/
RUN pip3 install -r dashboard/requirements.txt
ADD ./third_party/common/ third_party/common/
ADD ./dashboard/ dashboard/
ENV PYTHONPATH=/ha
CMD ["python", "dashboard/main.py"]
