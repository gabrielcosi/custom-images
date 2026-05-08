# renovate: docker=nousresearch/hermes-agent
FROM nousresearch/hermes-agent:v2026.5.7

# renovate: github-releases=jetify-com/devbox
ARG DEVBOX_VERSION=0.17.2
# renovate: github-releases=NixOS/nix
ARG NIX_VERSION=2.34.6
ARG TARGETARCH

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        xz-utils \
    && devbox_arch="$TARGETARCH" \
    && case "$devbox_arch" in amd64|arm64) ;; *) echo "Unsupported architecture: $devbox_arch" >&2; exit 1 ;; esac \
    && devbox_asset="devbox_${DEVBOX_VERSION}_linux_${devbox_arch}.tar.gz" \
    && curl -fsSLO "https://github.com/jetify-com/devbox/releases/download/${DEVBOX_VERSION}/${devbox_asset}" \
    && curl -fsSLO "https://github.com/jetify-com/devbox/releases/download/${DEVBOX_VERSION}/checksums.txt" \
    && grep " ${devbox_asset}$" checksums.txt | sha256sum -c - \
    && mkdir -p /tmp/devbox \
    && tar -xzf "$devbox_asset" -C /tmp/devbox \
    && find /tmp/devbox -type f -name devbox -exec cp {} /usr/local/bin/devbox \; \
    && chmod 0755 /usr/local/bin/devbox \
    && rm -rf /tmp/devbox "$devbox_asset" checksums.txt \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /nix /opt/data/home \
    && chown -R 10000:10000 /nix /opt/data

USER 10000:10000

ENV HOME=/opt/data/home
ENV USER=hermes
ENV NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PATH=/opt/data/bin:/opt/hermes/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN curl -fsSL "https://releases.nixos.org/nix/nix-${NIX_VERSION}/install" | sh -s -- --no-daemon \
    && . /opt/data/home/.nix-profile/etc/profile.d/nix.sh \
    && nix --version \
    && devbox version

USER root

RUN find /nix/store -path '*/bin/nix' -type f -exec dirname {} \; | head -n 1 | xargs -I{} sh -c 'for bin in {}/*; do ln -sf "$bin" "/usr/local/bin/$(basename "$bin")"; done' \
    && nix --version \
    && devbox version

USER 10000:10000
