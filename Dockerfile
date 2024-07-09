FROM python:3.10 as build-dep
COPY requirements.txt .
RUN mkdir /install
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -I --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.10

WORKDIR /app

COPY --from=build-dep /install /usr/local
ADD src .

CMD ["python3", "/app/main.py"]
