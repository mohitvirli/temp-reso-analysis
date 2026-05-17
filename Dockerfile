FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir "Cython>=0.29.35" numpy \
    && pip install --no-cache-dir --no-build-isolation allin1==0.0.3 \
    && grep -v '^allin1==' requirements.txt > /tmp/requirements-no-allin1.txt \
    && pip install --no-cache-dir -r /tmp/requirements-no-allin1.txt

COPY main.py .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=10).read()" || exit 1

CMD ["python", "main.py"]
