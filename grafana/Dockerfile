FROM grafana/grafana-oss:latest-ubuntu

ENV GF_INSTALL_PLUGINS "marcusolsson-hourly-heatmap-panel"

ADD ./ldc.svg /usr/share/grafana/public/img/grafana_icon.svg
ADD ./grafana.ini /etc/grafana/grafana.ini
ADD ./dashboards /etc/grafana/dashboards
ADD ./provisioning /etc/grafana/provisioning