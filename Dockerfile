FROM python:alpine3.6

ENV RANCHER_VERSION=0.6.3
ENV RANCHER_COMPOSE_VERSION=0.12.5

RUN apk add --no-cache --virtual .fetch-deps  \
        curl &&  \
    curl -Ls https://github.com/rancher/cli/releases/download/v${RANCHER_VERSION}/rancher-linux-amd64-v${RANCHER_VERSION}.tar.gz  \
    | tar xz -C /usr/local/bin &&  \
    ln -s /usr/local/bin/rancher-v${RANCHER_VERSION}/rancher /usr/local/bin/rancher &&  \
    chmod +x /usr/local/bin/rancher &&  \
    curl -L -O https://github.com/rancher/rancher-compose/releases/download/v${RANCHER_COMPOSE_VERSION}/rancher-compose-linux-amd64-v${RANCHER_COMPOSE_VERSION}.tar.gz &&  \
    tar xvf rancher-compose-linux-amd64-v${RANCHER_COMPOSE_VERSION}.tar.gz -C /usr/local/bin &&  \
    mv /usr/local/bin/rancher-compose-v${RANCHER_COMPOSE_VERSION}/rancher-compose /usr/local/bin &&  \
    pip install pyyaml && \
    apk del .fetch-deps

COPY scripts /scripts
RUN chmod +x /scripts

WORKDIR /scripts

ENTRYPOINT ["/usr/local/bin/python3"]
CMD [""]
