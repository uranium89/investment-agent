from decimal import Decimal
from pipeline.scoring.moat import compute_moat_score


def test_moat_vnm():
    assert compute_moat_score("VNM") == Decimal("10")


def test_moat_vcb():
    assert compute_moat_score("VCB") == Decimal("10")


def test_moat_fpt():
    assert compute_moat_score("FPT") == Decimal("7")


def test_moat_unknown():
    assert compute_moat_score("XYZ") == Decimal("0")
