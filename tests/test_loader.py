from __future__ import annotations

import responses

from langchain_gluedly import GluedlyLoader

BASE = "https://gluedly.com/api/v1"


@responses.activate
def test_load_resolves_latest_snapshot_and_maps_rows() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data",
        json={"data": [{"id": 100}, {"id": 99}]},
        status=200,
    )
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data/100",
        json={
            "id": 100,
            "page_id": 12,
            "data": {
                "ok": True,
                "rows": [
                    {
                        "url": "https://example.com/a",
                        "markdown": "# Product A",
                        "summary": "ignored when markdown present",
                    },
                    {
                        "url": "https://example.com/b",
                        "summary": "Summary only",
                    },
                ],
                "match_counts": {},
                "warnings": [],
            },
        },
        status=200,
    )

    docs = GluedlyLoader(api_key="test-key", page_id=12).load()

    assert len(docs) == 2
    assert docs[0].page_content == "# Product A"
    assert docs[0].metadata == {
        "source": "https://example.com/a",
        "page_id": 12,
        "snapshot_id": 100,
        "row_index": 0,
    }
    assert docs[1].page_content == "Summary only"
    assert docs[1].metadata["row_index"] == 1


@responses.activate
def test_load_returns_empty_when_no_snapshots() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data",
        json={"data": []},
        status=200,
    )

    docs = GluedlyLoader(api_key="test-key", page_id=12).load()
    assert docs == []


@responses.activate
def test_load_uses_explicit_snapshot_id() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data/55",
        json={
            "id": 55,
            "page_id": 12,
            "data": {
                "ok": True,
                "rows": [{"description": "From description"}],
                "match_counts": {},
                "warnings": [],
            },
        },
        status=200,
    )

    docs = GluedlyLoader(api_key="test-key", page_id=12, snapshot_id=55).load()

    assert len(docs) == 1
    assert docs[0].page_content == "From description"
    assert docs[0].metadata["snapshot_id"] == 55
    assert len(responses.calls) == 1
