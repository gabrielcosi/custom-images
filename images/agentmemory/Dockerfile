# renovate: docker=node
FROM node:24-slim

# renovate: npm=@agentmemory/agentmemory
ARG IMAGE_VERSION=0.9.17

# renovate: github-releases=iii-hq/iii
ARG III_VERSION=0.11.2

ENV AGENTMEMORY_DATA_DIR=/data \
    AGENTMEMORY_HMAC_FILE=/data/.hmac \
    III_REST_PORT=3111 \
    NODE_ENV=production

USER root:root
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        catatonit \
        curl \
        openssl \
        tzdata \
    && curl -fsSL "https://github.com/iii-hq/iii/releases/download/iii%2Fv${III_VERSION}/iii-x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz -C /usr/local/bin \
    && chmod +x /usr/local/bin/iii \
    && iii --version \
    && npm install -g --ignore-scripts --omit=optional --no-fund --no-audit \
        "@agentmemory/agentmemory@${IMAGE_VERSION}" \
    && find /usr/local/lib/node_modules/@agentmemory/agentmemory \
        -name 'iii-config.yaml' -print0 \
        | xargs -0 -r sed -i 's/host: 127\.0\.0\.1/host: 0.0.0.0/g' \
    && find /usr/local/lib/node_modules/@agentmemory/agentmemory \
        -type f \( -name '*.js' -o -name '*.mjs' -o -name '*.cjs' \) -print0 \
        | xargs -0 -r sed -i 's/\.listen(port, "127\.0\.0\.1"/.listen(port, "0.0.0.0"/g' \
    && mkdir -p /data /home/node/.agentmemory \
    && printf '{"schemaVersion":1,"skipSplash":true,"firstRunAt":"1970-01-01T00:00:00.000Z"}\n' \
        > /home/node/.agentmemory/preferences.json \
    && chown -R node:node /data /app /home/node/.agentmemory \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.npm

USER node:node

WORKDIR /data
VOLUME ["/data"]
EXPOSE 3111 3113

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://127.0.0.1:3111/agentmemory/livez || exit 1

ENTRYPOINT ["/usr/bin/catatonit", "--", "/usr/local/bin/agentmemory"]
