

Using this command for linting the code if `.pylintrc` and `.pylintignore` doesn't work

```bash
python3 -m pylint --ignore=.venv --disable=unsubscriptable-object,import-error sharepoint-python-integration
```

## How to fix a type error in given by `make_hash` funtion
### Exit virtual environment
```bash
deactivate
```
### remove .venv folder
```bash
rm -rf .venv
```
### Install latest version of python
```bash
brew update && brew upgrade python
```
### Make a new .venv folder
```bash
python3 -m venv .venv
```