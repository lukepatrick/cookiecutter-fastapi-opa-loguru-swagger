FROM python:3.7.10-alpine3.13 as build

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add \
    curl \ 
    && rm -rf /var/cache/apk/*

COPY . /usr/src/app
RUN python setup.py bdist_wheel

FROM python:3.7.10-alpine3.13 as runner

RUN apk add \
    libc-dev \
    make \
    curl \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/cache/apk/*

COPY image/conf/*.crt /usr/local/share/ca-certificates/
RUN  update-ca-certificates

COPY --from=build /usr/src/app/dist/*.whl /tmp

COPY image/conf/pip.conf /root/.pip/pip.conf
RUN pip install /tmp/*.whl
CMD ["python", "-m", "{{cookiecutter.api_name}}.main"]
