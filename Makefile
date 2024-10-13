IMAGE_NAME := beer-bottle-organ

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run -it -p 5000:5000 -v $(PWD)/src:/app $(IMAGE_NAME)

.PHONY: all
all: build run
