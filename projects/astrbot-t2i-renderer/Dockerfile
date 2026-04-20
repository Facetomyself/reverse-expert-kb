FROM soulter/astrbot:v4.22.3

WORKDIR /app

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG ALL_PROXY
ARG http_proxy
ARG https_proxy
ARG all_proxy

RUN export HTTP_PROXY="${HTTP_PROXY:-$http_proxy}" HTTPS_PROXY="${HTTPS_PROXY:-$https_proxy}" ALL_PROXY="${ALL_PROXY:-$all_proxy}" http_proxy="${http_proxy:-$HTTP_PROXY}" https_proxy="${https_proxy:-$HTTPS_PROXY}" all_proxy="${all_proxy:-$ALL_PROXY}" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libatk-bridge2.0-0t64 \
        libatk1.0-0t64 \
        libatspi2.0-0t64 \
        libcups2t64 \
        libnspr4 \
        libnss3 \
        libxcomposite1 \
        libxdamage1 \
    && rm -rf /var/lib/apt/lists/*

RUN export HTTP_PROXY="${HTTP_PROXY:-$http_proxy}" HTTPS_PROXY="${HTTPS_PROXY:-$https_proxy}" ALL_PROXY="${ALL_PROXY:-$all_proxy}" http_proxy="${http_proxy:-$HTTP_PROXY}" https_proxy="${https_proxy:-$HTTPS_PROXY}" all_proxy="${all_proxy:-$ALL_PROXY}" \
    && PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple python3 -m pip install --no-cache-dir playwright jinja2

RUN unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy \
    && PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 python3 -m playwright install chromium --no-shell

COPY server.py /app/server.py
COPY docker/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh \
    && mkdir -p /data

EXPOSE 18781

ENTRYPOINT ["/app/entrypoint.sh"]
