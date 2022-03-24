# Contributing

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/cogeotiff/rio-tiler-fs.git
$ cd rio-tiler-fs
$ pip install -e .["test","dev"]
```

## pre-commit

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
$ pre-commit install
```

## Docs

```bash
$ git clone https://github.com/cogeotiff/rio-tiler-fs.git
$ cd rio-tiler-fs
$ pip install -e .["docs"]
```

Hot-reloading docs:

```bash
$ mkdocs serve -f docs/mkdocs.yml
```

To manually deploy docs (note you should never need to do this because Github
Actions deploys automatically for new commits.):

```bash
$ mkdocs gh-deploy -f docs/mkdocs.yml
```
