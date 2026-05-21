from decimal import Decimal

MOAT_MAP: dict[str, Decimal] = {
    "VNM": Decimal("10"),
    "VCB": Decimal("10"),
    "MWG": Decimal("7"),
    "FPT": Decimal("7"),
    "PNJ": Decimal("5"),
    "SAB": Decimal("5"),
    "VIC": Decimal("7"),
    "VHM": Decimal("7"),
    "GAS": Decimal("7"),
    "PLX": Decimal("5"),
    "MSN": Decimal("5"),
    "HPG": Decimal("7"),
}

DEFAULT_MOAT = Decimal("0")


def compute_moat_score(symbol: str) -> Decimal:
    return MOAT_MAP.get(symbol, DEFAULT_MOAT)
