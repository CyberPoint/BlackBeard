PROJECT_NAME = mystarter

ifeq ($(OS),Windows_NT)
RM := rd /q /s
PYTHON := python
PIP := pip
else
UNAME_S := $(shell uname -s)
RM := /bin/rm -rf 	
PYTHON := python3
PIP := pip3
endif

.PHONY: virtual install build-requirements black isort flake8

all: package

develop:
	sudo apt-get -y install python3.8 python3-pip
	$(PIP) install --user --upgrade setuptools wheel
	$(PIP) install -Ur requirements.txt

package:
ifeq ($(OS),Windows_NT)
	@$(PYTHON) setup.py bdist_wheel
else
	@$(PYTHON) setup.py sdist bdist_wheel
endif

clean:
ifeq ($(OS),Windows_NT)
	$(RM) dist $(PROJECT_NAME).build build $(PROJECT_NAME).egg-info 2>nul
else
	@$(RM) dist $(PROJECT_NAME).build build $(PROJECT_NAME).egg-info 2> /dev/null
endif
	@sudo $(PIP) uninstall --yes $(PROJECT_NAME) 2> /dev/null