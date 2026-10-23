# ci-failures-zoo

A small Python project (`ordercalc`, an order calculator with VAT and rounding to 5 Rappen)
that serves as a **test corpus for a CI diagnosis agent**.

- `main` is always green.
- Each branch `case/NN-<name>` contains **exactly one commit** that deliberately breaks the
  pipeline. The causing file is the file changed by that commit
  (`git diff --name-only main...case/NN-<name>`).

All data is synthetic. The code is licensed under MIT.

## Run locally

```bash
uv sync
export ORDERCALC_API_URL=https://api.ordercalc.example
uv run ruff check . && uv run ruff format --check .
uv run mypy src tests
uv run pytest
uv run ordercalc
```

## Pipeline (`.github/workflows/ci.yml`)

| Job       | Checks                                 |
|-----------|----------------------------------------|
| lint      | `ruff check`, `ruff format --check`    |
| typecheck | `mypy --strict` on `src` and `tests`   |
| test      | `pytest`, job timeout 3 minutes        |
| audit     | `pip-audit` on the locked packages     |
| docker    | `docker build` and smoke test          |
