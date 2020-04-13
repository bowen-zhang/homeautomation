FROM envoyproxy/envoy
EXPOSE 17080
COPY dashboard/envoy.yaml /etc/envoy/envoy.yaml