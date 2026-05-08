import pytest
from src.sniffer import PacketSniffer


def test_sniffer_initialization():
    sniffer = PacketSniffer()
    assert isinstance(sniffer, PacketSniffer)
    assert sniffer.deque is not None