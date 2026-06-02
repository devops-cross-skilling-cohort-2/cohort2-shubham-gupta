FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

USER appuser

EXPOSE 5050

CMD ["python", "-m", "src.app"]