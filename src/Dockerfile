FROM python:3.10-slim

WORKDIR /code/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt  /code/requirements.txt
RUN  pip3.10 install -U --upgrade pip & pip3.10 install -Ur requirements.txt

COPY . /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000