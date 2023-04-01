FROM python:3.11.0
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]

EXPOSE 80