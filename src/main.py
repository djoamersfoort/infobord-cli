from mqtt_state import MQTTState
from frame_sys import FrameSys


def main():
    state = MQTTState()
    frame = FrameSys()
    state.on_show_djo = lambda: frame.show_djo()
    state.on_show_bitlair = lambda: frame.show_bitlair()
    state.on_shutdown = lambda: frame.shutdown()
    state.connect()


if __name__ == "__main__":
    main()
