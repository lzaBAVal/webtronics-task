FROM python:3.10-slim

WORKDIR /code/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY /src/requirements.txt  /code/requirements.txt
RUN  pip3.10 install -U --upgrade pip & pip3.10 install -Ur requirements.txt

COPY ["./env_files/.env", "./src", "/code/"]

CMD ["./wait-for-it.sh", "db:5432", "--", "./start.sh"]

EXPOSE 8000