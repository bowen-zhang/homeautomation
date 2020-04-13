build-dashboard:
	docker build -t dashboard/envoy -f dashboard-envoy.dockerfile .
	docker build -t dashboard/webserver -f dashboard-webserver.dockerfile .

run-dashboard: build-dashboard
	docker run -d --network=host --restart always dashboard/envoy
	docker run -d --network=host --restart always dashboard/webserver