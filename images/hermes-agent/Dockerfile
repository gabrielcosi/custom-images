FROM nousresearch/hermes-agent:v2026.4.23

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

USER 10000:10000
