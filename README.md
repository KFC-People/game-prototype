# typetypetype

## Setup

### `pyenv` (optional)

Install `pyenv`, its dependencies, and Python 3.12:

```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash

pyenv install 3.12
```

### Requirements

Install `arcade`'s dependencies, then all required packages:

```bash
sudo apt install python3 python3-pip libjpeg-dev zlib1g-dev
poetry install
```

### Development

As a developer, you should also install pre-commit hooks:

```bash
poetry run pre-commit install
poetry run pre-commit run -a
```

And to run the project:

```bash
poetry run python -m server
poetry run python -m client
```
