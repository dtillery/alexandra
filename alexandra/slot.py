class Slot:
    """Provides access to individual slot information for the request.

    The original slot object parsed from the request can be accessed directly
    through the :py:attr:`body` member.
    """
    def __init__(self, slot_data):
        self.body = slot_data
        resolutions = self.body.get("resolutions", {}).get("resolutionsPerAuthority", [])
        self.resolutions = [SlotResolution(resolution) for resolution in resolutions]

    @property
    def name(self):
        return self.body.get("name")

    @property
    def original_value(self):
        """Returns the value the user uttered and Alexa matched to the slot."""
        return self.body.get("value")

    @property
    def is_empty(self):
        """Returns True if slot is empty (i.e. no original_value)"""
        return self.original_value is None

    @property
    def matched_resolutions(self):
        """Resolutions with code `ER_SUCCESS_MATCH`"""
        return [res for res in self.resolutions if res.is_match]

    @property
    def is_match(self):
        """True if any matched resolutions."""
        return len(self.matched_resolutions) > 0

    @property
    def matched_value(self):
        """Returns name of the first matched resolution's first value"""
        if self._first_matched_value:
            return self._first_matched_value.name

    @property
    def matched_id(self):
        """Returns id of the first matched resolution's first value"""
        if self._first_matched_value:
            return self._first_matched_value.id

    @property
    def _first_matched_value(self):
        if self.matched_resolutions and self.matched_resolutions[0].values:
            return self.matched_resolutions[0].values[0]


class SlotResolution:
    def __init__(self, resolution_data):
        self._data = resolution_data
        self.values = [SlotValue(value) for value in self._data.get("values", [])]

    @property
    def is_match(self):
        return self._data.get("status", {}).get("code") == "ER_SUCCESS_MATCH"


class SlotValue:
    def __init__(self, value_data):
        self._data = value_data.get("value", {})

    @property
    def name(self):
        return self._data.get("name")

    @property
    def id(self):
        return self._data.get("id")
