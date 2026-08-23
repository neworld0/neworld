from pathlib import Path


def fixture(name):
    return (Path(__file__).parent / "fixtures" / "wol" / name).read_text(encoding="utf-8")
