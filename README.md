# langchain-gluedly

LangChain `BaseLoader` that turns Gluedly scrape snapshots into `Document` objects.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```python
from langchain_gluedly import GluedlyLoader

loader = GluedlyLoader(
    api_key="YOUR_GLUEDLY_API_KEY",
    page_id=12,
    # snapshot_id=100,  # optional; omit to use the latest snapshot
    # base_url="https://gluedly.com/api/v1",
)
documents = loader.load()
```

Each row becomes one document. Content preference: `markdown` → `summary` → `description` → `str(row)`.

## Example

```bash
export GLUEDLY_API_KEY=…
export GLUEDLY_PAGE_ID=12
python examples/load_documents.py
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```
