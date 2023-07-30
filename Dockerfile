FROM python:3.9-alpine3.13
LABEL maintainer="Olalekan Adegoke"

ENV PYTHONUNBUFFERED 1

# Path: /app
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ./requirements.dev.txt ./

ARG DEV=false
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then pip install --no-cache-dir -r requirements.dev.txt; \
    fi && \
    rm  requirements.txt && \
    rm  requirements.dev.txt && \
    apk del .tmp-build-deps && \
    adduser -D \
    --disabled-password \
    --no-create-home \
    django-user && \ 
    chown -R django-user:django-user /usr/src/app

COPY ./app .
EXPOSE 8000

USER django-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]