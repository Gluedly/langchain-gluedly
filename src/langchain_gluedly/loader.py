"""Load web data snapshots from Gluedly into LangChain Document objects."""

from __future__ import annotations

from typing import Any, List, Optional

import requests
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

DEFAULT_BASE_URL = "https://gluedly.com/api/v1"


class GluedlyLoader(BaseLoader):
    """Load web data snapshots from Gluedly into LangChain Document objects."""

    def __init__(
        self,
        api_key: str,
        page_id: int,
        snapshot_id: Optional[int] = None,
        base_url: str = DEFAULT_BASE_URL,
        session: Optional[requests.Session] = None,
        timeout: float = 30,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        self.api_key = api_key
        self.page_id = page_id
        self.snapshot_id = snapshot_id
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.session = session or requests.Session()
        self.timeout = timeout

    def load(self) -> List[Document]:
        target_snapshot_id = self.snapshot_id
        if not target_snapshot_id:
            res = self.session.get(
                f"{self.base_url}/pages/{self.page_id}/data",
                headers=self.headers,
                timeout=self.timeout,
            )
            res.raise_for_status()
            snapshots = res.json().get("data", [])
            if not snapshots:
                return []
            target_snapshot_id = int(snapshots[0]["id"])

        payload_res = self.session.get(
            f"{self.base_url}/pages/{self.page_id}/data/{target_snapshot_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        payload_res.raise_for_status()
        payload: dict[str, Any] = payload_res.json()

        documents: List[Document] = []
        rows = payload.get("data", {}).get("rows", [])
        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                page_content = str(row)
                source = f"page_{self.page_id}"
            else:
                page_content = (
                    row.get("markdown")
                    or row.get("summary")
                    or row.get("description")
                    or str(row)
                )
                source = row.get("url") or f"page_{self.page_id}"

            metadata = {
                "source": source,
                "page_id": self.page_id,
                "snapshot_id": target_snapshot_id,
                "row_index": idx,
            }
            documents.append(Document(page_content=str(page_content), metadata=metadata))

        return documents
