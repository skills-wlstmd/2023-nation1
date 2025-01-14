FROM alpine

RUN apk add --no-cache curl

USER 1000:1000

COPY --chown=1000:1000 ./product-amd64 /app

RUN chmod 500 /app

ENTRYPOINT [ "/app" ]