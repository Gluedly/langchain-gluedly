"""Example: load Gluedly snapshot rows into LangChain Documents."""

from __future__ import annotations

import os

from langchain_gluedly import GluedlyLoader


def main() -> None:
    api_key = os.environ["GLUEDLY_API_KEY"]
    page_id = int(os.environ.get("GLUEDLY_PAGE_ID", "12"))
    base_url = os.environ.get("GLUEDLY_BASE_URL", "https://gluedly.com/api/v1")

    loader = GluedlyLoader(
        api_key=api_key,
        page_id=page_id,
        base_url=base_url,
    )
    documents = loader.load()

    print(f"Loaded {len(documents)} documents from page {page_id}")
    for doc in documents[:3]:
        print("---")
        print(doc.metadata)
        print(doc.page_content[:400])


if __name__ == "__main__":
    main()
