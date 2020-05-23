FROM envoyproxy/envoy:v1.14.1
EXPOSE 17081
EXPOSE 17082
COPY dashboard/envoy.yaml /etc/envoy/envoy.yaml