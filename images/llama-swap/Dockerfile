# upstream-repo: mostlygeek/llama-swap
# renovate: docker=ghcr.io/mostlygeek/llama-swap versioning=regex:^v(?<major>\d+)-(?<compatibility>cuda\d+)-b(?<build>\d+)-non-root$
ARG IMAGE_VERSION=v255-cuda13-b10951-non-root

FROM golang:1.27-bookworm AS vllm-wrapper

ARG IMAGE_VERSION

RUN git clone --filter=blob:none --no-checkout https://github.com/mostlygeek/llama-swap.git /src \
    && git -C /src checkout --detach "${IMAGE_VERSION%%-*}" \
    && cd /src \
    && CGO_ENABLED=0 go build -trimpath -o /out/vllm-wrapper ./cmd/vllm-wrapper

FROM ghcr.io/mostlygeek/llama-swap:${IMAGE_VERSION}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY --from=vllm-wrapper /out/vllm-wrapper /usr/local/bin/vllm-wrapper

USER 10001:10001
