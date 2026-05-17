# renovate: docker=nousresearch/hermes-agent
FROM nousresearch/hermes-agent:v2026.5.16

# renovate: github-releases=jetify-com/devbox
ARG DEVBOX_VERSION=0.17.2
# renovate: github-releases=NixOS/nix
ARG NIX_VERSION=2.34.6
# renovate: github-releases=rohitg00/agentmemory
ARG AGENTMEMORY_VERSION=0.9.18

USER root:root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        xz-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN /opt/hermes/.venv/bin/pip install --no-cache-dir 'python-telegram-bot[webhooks]==22.6'

RUN devbox_asset="devbox_${DEVBOX_VERSION}_linux_amd64.tar.gz" \
    && curl -fsSLO "https://github.com/jetify-com/devbox/releases/download/${DEVBOX_VERSION}/${devbox_asset}" \
    && curl -fsSLO "https://github.com/jetify-com/devbox/releases/download/${DEVBOX_VERSION}/checksums.txt" \
    && grep " ${devbox_asset}$" checksums.txt | sha256sum -c - \
    && mkdir -p /tmp/devbox \
    && tar -xzf "${devbox_asset}" -C /tmp/devbox \
    && find /tmp/devbox -type f -name devbox -exec cp {} /usr/local/bin/devbox \; \
    && chmod 0755 /usr/local/bin/devbox \
    && rm -rf /tmp/devbox "${devbox_asset}" checksums.txt

RUN mkdir -p /nix /opt/homebrew /opt/agentmemory /opt/data/home \
    && chown -R 10000:10000 /nix /opt/homebrew /opt/agentmemory /opt/data

USER 10000:10000

ENV HOME=/opt/data/home
ENV USER=hermes
ENV NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PATH=/opt/data/bin:/opt/hermes/.venv/bin:/opt/homebrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN curl -fsSL "https://releases.nixos.org/nix/nix-${NIX_VERSION}/install" | sh -s -- --no-daemon \
    && . /opt/data/home/.nix-profile/etc/profile.d/nix.sh \
    && nix --version \
    && devbox version

USER root:root

RUN find /nix/store -path '*/bin/nix' -type f -exec dirname {} \; | head -n 1 \
        | xargs -I{} sh -c 'for bin in {}/*; do ln -sf "$bin" "/usr/local/bin/$(basename "$bin")"; done' \
    && nix --version \
    && devbox version

USER 10000:10000

RUN git clone --depth 1 https://github.com/Homebrew/brew /opt/homebrew \
    && /opt/homebrew/bin/brew --version

RUN git clone --depth 1 --branch "v${AGENTMEMORY_VERSION}" https://github.com/rohitg00/agentmemory /tmp/agentmemory-src \
    && cp -a /tmp/agentmemory-src/integrations/hermes/. /opt/agentmemory/ \
    && rm -rf /tmp/agentmemory-src \
    && sed -i 's|/agentmemory/health|/agentmemory/livez|' /opt/agentmemory/__init__.py
