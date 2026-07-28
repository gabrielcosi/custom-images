FROM docker.io/nvidia/cuda:13.3.1-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    HF_HOME=/app/hf_cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        git \
        libsndfile1 \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# renovate: github-releases=devnen/Chatterbox-TTS-Server
ARG IMAGE_VERSION=2.0.0

RUN git clone --depth 1 --branch "v${IMAGE_VERSION}" \
        https://github.com/devnen/Chatterbox-TTS-Server.git /app \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir -r requirements-nvidia-cu128.txt \
    && python3 -m pip install --no-cache-dir --no-deps \
        git+https://github.com/devnen/chatterbox-v2.git@master \
        s3tokenizer==0.3.0 \
        onnx==1.16.0 \
    && python3 -m pip install --no-cache-dir "protobuf>=4.25.0" \
    && mkdir -p model_cache reference_audio outputs voices logs hf_cache

EXPOSE 8004

CMD ["python3", "server.py"]
