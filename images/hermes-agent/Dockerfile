# upstream-repo: NousResearch/hermes-agent
# renovate: docker=nousresearch/hermes-agent
FROM nousresearch/hermes-agent:v2026.8.27

# renovate: github-tags=eleboucher/memini
ARG MEMINI_VERSION=0.7.22

USER root:root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        file \
        gcc \
        libc6-dev \
        make \
        procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN VIRTUAL_ENV=/opt/hermes/.venv \
    && HERMES_VERSION=$(uv pip show hermes-agent | awk '/^Version:/ {print $2}') \
    && uv pip install --no-cache "hermes-agent[firecrawl,messaging]==${HERMES_VERSION}"

COPY crawl4ai /tmp/crawl4ai-plugin
RUN cp -a /tmp/crawl4ai-plugin "$(/opt/hermes/.venv/bin/python -c 'import pathlib, plugins; print(pathlib.Path(plugins.__file__).parent / "web" / "crawl4ai")')" \
    && rm -rf /tmp/crawl4ai-plugin

RUN mkdir -p /home/linuxbrew/.linuxbrew /opt/memini /opt/data/home \
    && chown -R 10000:10000 /home/linuxbrew /opt/memini /opt/data

USER 10000:10000

ENV HOME=/opt/data/home
ENV USER=hermes
ENV PATH=/opt/data/bin:/opt/hermes/.venv/bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN git clone --depth 1 https://github.com/Homebrew/brew /home/linuxbrew/.linuxbrew \
    && /home/linuxbrew/.linuxbrew/bin/brew --version

RUN git clone --depth 1 --branch "v${MEMINI_VERSION}" https://github.com/eleboucher/memini /tmp/memini-src \
    && cp -a /tmp/memini-src/integrations/hermes/plugin/memini/. /opt/memini/ \
    && rm -rf /tmp/memini-src
