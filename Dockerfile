FROM python:3.7-slim-bullseye
WORKDIR /workspace
ADD ./src /workspace

RUN pip3 install -r /workspace/requirements.txt -i https://pypi.doubanio.com/simple && \
    chmod +x ./run.sh

EXPOSE 9000
ENTRYPOINT ["python3", "app.py"]