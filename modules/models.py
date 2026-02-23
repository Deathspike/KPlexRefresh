from .utils.typing import Typing


class Mode:
    def __init__(self, node: dict[object, object]):
        self.id: str | None = None
        self.refresh_rate: float | int = 0
        self.size: Size | None = None

        # Parse node properties.
        for key, value in node.items():
            if key == "id":
                self.id = self._parse_id(value)
            elif key == "refreshRate":
                self.refresh_rate = self._parse_refresh_rate(value)
            elif key == "size":
                self.size = self._parse_size(value)

        # Validate properties.
        if not self.id or not self.refresh_rate or not self.size:
            raise ValueError("missing properties")

    def __eq__(self, value: object):
        if isinstance(value, Mode):
            return self.id == value.id
        else:
            return False

    def _parse_id(self, node: object):
        if not isinstance(node, str):
            raise ValueError("`id` must be a str")
        else:
            return node

    def _parse_refresh_rate(self, node: object):
        if not isinstance(node, (float, int)):
            raise ValueError("`refreshRate` must be an number")
        else:
            return node

    def _parse_size(self, node: object):
        if not Typing.is_dict(node):
            raise ValueError("`size` must be a dict")
        else:
            return Size(node)


class Output:
    def __init__(self, node: dict[object, object]):
        self.current_mode_id: str | None = None
        self.id = 0
        self.modes: list[Mode] = []

        # Parse node properties.
        for key, value in node.items():
            if key == "currentModeId":
                self.current_mode_id = self._parse_current_mode_id(value)
            elif key == "id":
                self.id = self._parse_id(value)
            elif key == "modes":
                self.modes.extend(self._parse_modes(value))

        # Validate properties.
        if not self.current_mode_id or not self.id or not self.modes:
            raise ValueError("missing properties")

    def __eq__(self, value: object):
        if isinstance(value, Output):
            return self.id == value.id
        else:
            return False

    def _parse_current_mode_id(self, node: object):
        if not isinstance(node, str):
            raise ValueError("`currentModeId` must be a str")
        else:
            return node

    def _parse_id(self, node: object):
        if not isinstance(node, int):
            raise ValueError("`id` must be an int")
        else:
            return node

    def _parse_modes(self, node: object):
        if not Typing.is_list(node):
            raise ValueError("`modes` must be a list")
        for index, value in enumerate(node):
            if not Typing.is_dict(value):
                raise ValueError(f"`modes[{index}]` must be a dict")
            else:
                yield Mode(value)


class Screen:
    def __init__(self, node: dict[object, object]):
        self.outputs: list[Output] = []

        # Parse node properties.
        for key, value in node.items():
            if key == "outputs":
                self.outputs.extend(self._parse_outputs(value))

        # Validate properties.
        if not self.outputs:
            raise ValueError("missing properties")

    def _parse_outputs(self, node: object):
        if not Typing.is_list(node):
            raise ValueError("`outputs` must be a list")
        for index, value in enumerate(node):
            if not Typing.is_dict(value):
                raise ValueError(f"`outputs[{index}]` must be a dict")
            else:
                yield Output(value)


class Size:
    def __init__(self, node: dict[object, object]):
        self.height = 0
        self.width = 0

        # Validate properties.
        for key, value in node.items():
            if key == "height":
                self.height = self._parse_int("height", value)
            elif key == "width":
                self.width = self._parse_int("width", value)

        # Validate properties.
        if not self.height or not self.width:
            raise ValueError("missing properties")

    def __eq__(self, value: object):
        if isinstance(value, Size):
            return self.height == value.height and self.width == value.width
        else:
            return False

    def _parse_int(self, key: str, node: object):
        if not isinstance(node, int):
            raise ValueError(f"`{key}` must be an int")
        else:
            return node
