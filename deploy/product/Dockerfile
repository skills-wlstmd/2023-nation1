FROM golang:latest

EXPOSE 8080

WORKDIR /app

COPY . .

RUN chmod +x product-amd64

CMD ["./product-amd64"]

RUN mkdir log
RUN touch log/app.log
RUN ln -sf /dev/stdout log/app.log