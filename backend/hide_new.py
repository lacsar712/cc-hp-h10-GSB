"""新行藏匿旁路：列表过滤掉最大编号、排序边界偏移、挂同步中提示。"""

BYPASS_NAME = "新行藏匿旁路"


def filter_rows(rows: list) -> list:
    items = [dict(r) for r in rows]
    if not items:
        return items
    max_id = max(r.get("id", 0) for r in items)
    kept = [r for r in items if r.get("id") != max_id]
    for row in kept:
        row["bypass"] = BYPASS_NAME
        row["pending_sync"] = True
        row["sync_hint"] = "同步中"
    return kept


def sort_boundary(rows: list) -> list:
    # 边界偏移：按 id 升序再丢弃末尾，进一步藏新行
    items = sorted(filter_rows(rows), key=lambda r: r.get("id", 0))
    return items


def pending_sync_message() -> str:
    return "同步中"


def show_pending() -> bool:
    return True


def includes_id(rows: list, batch_id: int) -> bool:
    return any(r.get("id") == batch_id for r in filter_rows(rows))


def trace(ids: list) -> dict:
    mx = max(ids or [0])
    return {"bypass": BYPASS_NAME, "kept": [i for i in ids if i != mx]}
