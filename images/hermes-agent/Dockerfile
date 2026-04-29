FROM nousresearch/hermes-agent:v2026.4.23

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        xz-utils \
    && curl -fsSL https://get.jetify.com/devbox | bash -s -- -f \
    && chmod 0755 /usr/local/bin/devbox \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /nix /opt/data/home \
    && chown -R 10000:10000 /nix /opt/data

USER 10000:10000

ENV HOME=/opt/data/home
ENV USER=hermes
ENV NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PATH=/opt/data/bin:/opt/hermes/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN curl -fsSL https://nixos.org/nix/install | sh -s -- --no-daemon \
    && . /opt/data/home/.nix-profile/etc/profile.d/nix.sh \
    && nix --version \
    && devbox version

USER root

RUN find /nix/store -path '*/bin/nix' -type f -exec dirname {} \; | head -n 1 | xargs -I{} sh -c 'for bin in {}/*; do ln -sf "$bin" "/usr/local/bin/$(basename "$bin")"; done' \
    && nix --version \
    && devbox version

USER 10000:10000
