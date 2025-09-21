def normalize_ym_str(ym: str) -> str:
    parts = ym.split("-")
    if len(parts) == 2:
        return f"{parts[0]}-{parts[1]}-01"
    return ym
