# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/%%project_container_root_folder%%

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./bin/entrypoint.sh ./bin/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/%%project_container_root_folder%%/bin/entrypoint.sh
RUN chmod +x /usr/%%project_container_root_folder%%/bin/entrypoint.sh

# copy project
COPY ./src ./src

# run entrypoint.sh
ENTRYPOINT ["/usr/%%project_container_root_folder%%/bin/entrypoint.sh"]