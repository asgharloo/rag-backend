FROM python:3.12-slim

WORKDIR /app

RUN sed -i 's|http://deb.debian.org/debian|http://mirror.arvancloud.ir/debian|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|http://deb.debian.org/debian-security|http://mirror.arvancloud.ir/debian-security|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*


COPY psycho/requirements.txt .
RUN pip install --no-cache-dir --trusted-host mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ -r requirements.txt
COPY psycho/ .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

