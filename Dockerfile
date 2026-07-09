FROM ubuntu:noble

RUN apt-get update \
    && apt-get install -y --no-install-recommends sniproxy ca-certificates libcap2-bin \
    && setcap 'cap_net_bind_service=+ep' /usr/sbin/sniproxy \
    && rm -rf /var/lib/apt/lists/*

COPY config/sniproxy.conf /etc/sniproxy.conf

USER daemon

EXPOSE 443 8883

CMD ["/usr/sbin/sniproxy", "-f", "-c", "/etc/sniproxy.conf"]
