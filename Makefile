PROJECT_NAME = blackbeard
VIRTUAL_ENV = virtualenv
PYINSTALLER = pyinstaller
ifeq ($(OS),Windows_NT)
RM := rd /q /s
PYTHON := python
PIP := pip
VENV := python -m venv
else
UNAME_S := $(shell uname -s)
RM := /bin/rm -rf 	
PYTHON := ./$(VIRTUAL_ENV)/bin/python3
PIP := ./$(VIRTUAL_ENV)/bin/pip3
VENV := python3.10 -m venv
LOCAL_PIP := pip3.10
endif

.PHONY: virtual install build-requirements black isort flake8

all: package

develop:
	sudo apt install software-properties-common -y
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt-get -y install python3.10 python3-pip python3.10-venv python3-dev python3-cairo-dev \
							libsqlite3-dev
	$(VENV) $(VIRTUAL_ENV)
	$(PIP) install -Ur requirements.txt
	$(LOCAL_PIP) install -r requirements.txt

package:
ifeq ($(OS),Windows_NT)
	@$(PYTHON) setup.py bdist_wheel
else
	@$(PYTHON) setup.py sdist bdist_wheel
endif


binary:
	@$(RM) build
	@$(RM) dist/$(PROJECT_NAME)
	@$(PYINSTALLER) -y -F --path="." --path="src" ---collect-all src --onefile $(PROJECT_NAME).py

clean:
	$(RM) __pycache__
ifeq ($(OS),Windows_NT)
	$(RM) dist $(PROJECT_NAME).build build $(PROJECT_NAME).egg-info 2>nul
else
	@$(RM) dist $(PROJECT_NAME).build build $(PROJECT_NAME).egg-info 2> /dev/null
	@$(RM) __pycache__ dist $(PROJECT_NAME).build build $(PROJECT_NAME).egg-info 2> /dev/null
endif
	@sudo $(PIP) uninstall --yes $(PROJECT_NAME) 2> /dev/null
