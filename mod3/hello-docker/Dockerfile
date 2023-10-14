FROM alpine:3.18

WORKDIR /app

ENV COUNT 8
ENV MSG 'Hello Docker!'

COPY ./echo.sh .
COPY ./lucas.sh .

CMD /app/lucas.sh && /app/echo.sh 