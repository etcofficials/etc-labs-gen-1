# ETC Labs — Gen 1 · backend container (FastAPI + SQLite). The public site is also served from /
# so the same image works as an all-in-one deployment or as the API/admin host behind GitHub Pages.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ETC_DATA_DIR=/var/data
WORKDIR /app
COPY server/requirements.txt server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt
COPY server ./server
COPY admin ./admin
COPY public ./public
RUN mkdir -p /var/data && useradd -r -u 10001 etc && chown -R etc:etc /var/data /app
USER etc
VOLUME ["/var/data"]
EXPOSE 8000
CMD ["sh", "-c", "python -m uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]
