# Download from docker cloud of teatime(public)
FROM nhatthai/django2.1:latest

ADD . /code

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /code

ENTRYPOINT ["/entrypoint.sh"]
