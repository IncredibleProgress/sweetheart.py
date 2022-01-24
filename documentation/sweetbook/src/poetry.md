# Poetry

``` bash
curl -sSL https://install.python-poetry.org | python3 -
curl -sSL https://install.python-poetry.org | python3 - --uninstall
curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 python3 -

export PATH="$HOME/.local/bin:$PATH"

poetry --version
poetry self update
poetry new poetry-demo
poetry env info --path
poetry add sweetheart

poetry env list
poetry env remove --all

poetry publish --build
```