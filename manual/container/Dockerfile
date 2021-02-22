FROM python:3.9.1

WORKDIR /usr/src/app

COPY requirements.txt ccfd.py modelfull.pkl ./

RUN pip install -r requirements.txt

CMD ["python", "-u", "ccfd.py"]
