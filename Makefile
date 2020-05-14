init:
	curl -sSL https://get.docker.com | sh
	sudo usermod -aG docker pi
	newgrp docker

build-dashboard:
	docker build -t dashboard/envoy -f dashboard-envoy.dockerfile .
	docker build -t dashboard/webserver -f dashboard-webserver.dockerfile .

run-dashboard: build-dashboard
	docker rm -f dashboard.envoy || true
	docker rm -f dashboard.webserver || true
	docker run --name dashboard.envoy -d --network=host --restart always dashboard/envoy
	docker run --name dashboard.webserver -d --network=host --restart always dashboard/webserver

build-irrigation:
	docker build -t irrigation -f irrigation.dockerfile .
	docker build -t irrigation:test -f irrigation-test.dockerfile .

run-irrigation: build-irrigation
	docker rm -f irrigation || true
	docker run --name irrigation -d --privileged --network=host --restart always irrigation