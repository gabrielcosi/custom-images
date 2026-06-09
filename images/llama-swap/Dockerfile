# renovate: docker=ghcr.io/mostlygeek/llama-swap versioning=regex:^v(?<major>\d+)-(?<compatibility>cuda\d+)-b(?<build>\d+)$
FROM ghcr.io/mostlygeek/llama-swap:v223-cuda13-b9570

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*
