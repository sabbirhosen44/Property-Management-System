FROM postgres:18

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-18-postgis-3 \
    postgresql-18-postgis-3-scripts \
    postgresql-server-dev-18 \
    build-essential \
    git \
    ca-certificates && \
    git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git /tmp/pgvector && \
    cd /tmp/pgvector && \
    make OPTFLAGS="" && \
    make install && \
    cd / && rm -rf /tmp/pgvector && \
    apt-get purge -y --auto-remove build-essential git ca-certificates && \
    rm -rf /var/lib/apt/lists/*