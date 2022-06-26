FROM python:3.7-slim
ADD . /code
WORKDIR /code
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python","app.py"] 
