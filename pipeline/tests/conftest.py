from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal

import pytest


@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session


@pytest.fixture
def mock_fireant():
    fireant = AsyncMock()
    return fireant


def make_mock_result(rows=None, single_row=None):
    """Create a MagicMock result that mimics SQLAlchemy async result."""
    m = MagicMock()
    if single_row is not None:
        m.fetchone.return_value = single_row
    elif rows is not None:
        m.fetchall.return_value = rows
        m.fetchone.return_value = rows[0] if rows else None
    else:
        m.fetchone.return_value = None
        m.fetchall.return_value = []
    return m
