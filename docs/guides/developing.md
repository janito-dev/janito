# 🛠️ Developing & Extending Janito

This guide explains how to install and use the latest development version of this project directly from GitHub.

## Installation from GitHub Main Branch

To install the latest development version of this project directly from the GitHub main branch, run:

```bash
pip install git+https://github.com/joaompinto/janito.git@main
```

## Editable Install (for Development)

If you want to make changes to the code and have them reflected immediately (without reinstalling), use an editable install:

```bash
git clone https://github.com/joaompinto/janito.git
cd janito
git checkout main
pip install -e .
```

This will install the package in "editable" mode, so changes to the source code are immediately available in your environment.

## Notes

- Always ensure you are on the correct branch (e.g., `main`) for the latest development version.
- For further development setup (linting, pre-commit hooks, etc.), see the [Developer Toolchain Guide](../meta/developer_toolchain.md).
