FROM envoyproxy/envoy
EXPOSE 17081
EXPOSE 17082
COPY dashboard/envoy.yaml /etc/envoy/envoy.yaml