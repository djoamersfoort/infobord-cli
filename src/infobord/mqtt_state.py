from paho.mqtt.client import Client, MQTTMessage
from typing import Any, Callable

type StateCallback = Callable[[], None]

MQTT_ADDRESS = "mqtt.bitlair.nl"
TOPICS = {
    "bitlair": "bitlair/state",
    "djo": "bitlair/state/djo",
}


class MQTTState:
    def __init__(self) -> None:
        self.bitlair_open: bool | None = None
        self.djo_open: bool | None = None

        self.on_show_djo: StateCallback | None = None
        self.on_show_bitlair: StateCallback | None = None
        self.on_shutdown: StateCallback | None = None

        self.client = Client()
        self.client.on_message = self._on_message

    def _on_message(
        self,
        _client: Client,
        _userdata: Any,
        message: MQTTMessage,
    ) -> None:
        is_open = message.payload.decode("utf-8") == "open"

        match message.topic:
            case t if t == TOPICS["bitlair"]:
                if self.bitlair_open == is_open:
                    return
                self.bitlair_open = is_open
            case t if t == TOPICS["djo"]:
                if self.djo_open == is_open:
                    return
                self.djo_open = is_open
            case _:
                raise ValueError(f"Unknown topic: {message.topic!r}")

        if self.bitlair_open is None or self.djo_open is None:
            return

        if self.djo_open:
            callback = self.on_show_djo
        elif self.bitlair_open:
            callback = self.on_show_bitlair
        else:
            callback = self.on_shutdown

        if callback:
            callback()

    def connect(self) -> None:
        self.client.connect(MQTT_ADDRESS)
        for topic in TOPICS.values():
            self.client.subscribe(topic)
        self.client.loop_forever()
