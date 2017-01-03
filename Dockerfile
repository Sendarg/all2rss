## Python Image
FROM python:2.7

## Prepare
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --proxy=192.168.199.213:1087
#RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

## Start
#ENTRYPOINT ["python"]
#CMD start.py
EXPOSE 2202
CMD ["python","start.py"]
