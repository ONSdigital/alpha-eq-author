UNAME_S    := $(shell uname -s)
CONTAINERS := $(shell docker ps -a -q)
IMAGES     := $(shell docker images -q)

.PHONY : docker-machine-setup run-docker-compose clean

all: docker-machine-setup run-docker-compose

define colourecho
      @tput setaf 6
      @echo $1
      @tput sgr0
endef


docker-machine-setup:
ifeq ($(UNAME_S),Darwin)                 
	$(call colourecho, ": It just works ")
	-docker-machine start default && eval "$(docker-machine env default)"
endif


clean:  
	docker rm $(CONTAINERS)
	docker rmi $(IMAGES)
        
run-docker-compose: 
	docker-compose build && docker-compose up

