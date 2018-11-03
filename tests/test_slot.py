import json

import pytest

from alexandra.slot import Slot


@pytest.fixture
def matched_slot():
    with open("data/slots/match.json", "rb") as f:
        return json.loads(f.read())


@pytest.fixture
def unmatched_slot():
    with open("data/slots/no_match.json", "rb") as f:
        return json.loads(f.read())


@pytest.fixture
def empty_slot():
    with open("data/slots/empty.json", "rb") as f:
        return json.loads(f.read())

def test_matched_slot(matched_slot):
    slot = Slot(matched_slot)

    assert slot.name == "Foo"
    assert slot.original_value == "bar"
    assert len(slot.matched_resolutions) == 1

    assert len(slot.matched_resolutions[0].values) == 2
    assert slot.matched_resolutions[0].values[0].name == "Bar"
    assert slot.matched_resolutions[0].values[0].id == "BA"

    assert slot.is_match
    assert slot.matched_value == "Bar"
    assert slot.matched_id == "BA"


def test_unmatched_slot(unmatched_slot):
    slot = Slot(unmatched_slot)

    assert slot.name == "Foo"
    assert slot.original_value == "fizz"
    assert len(slot.resolutions) == 1
    assert len(slot.matched_resolutions) == 0

    assert not slot.is_match
    assert slot.matched_value is None
    assert slot.matched_id is None


def test_empty_slot(empty_slot):
    slot = Slot(empty_slot)

    assert slot.name == "Foo"
    assert slot.is_empty
    assert not slot.is_match
