## Python Image
FROM python:2.7

## Prepare
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt --proxy=192.168.199.213:1087
#RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt


## Start
EXPOSE 2102
#ENTRYPOINT ["python"]
#CMD first_run.py
#CMD start.py
CMD ["python","app_first_run.py"]
CMD ["python","start.py"]

