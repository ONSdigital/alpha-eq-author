UNAME_S := $(shell uname -s)
.PHONY : docker-machine-setup run-docker-compose

all: docker-machine-setup run-docker-compose

define colourecho
      @tput setaf 6
      @echo $1
      @tput sgr0
endef


docker-machine-setup:
ifeq ($(UNAME_S),Darwin)                 
	$(call colourecho, ": It just works ")
	docker-machine start default && eval "$(docker-machine env default)"
endif
        
run-docker-compose: 
	docker-compose build && docker-compose up

