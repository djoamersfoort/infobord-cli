import subprocess

DJO_URL = "https://docs.google.com/presentation/d/e/2PACX-1vQJBiddvZZDcDDwfcJYjOHc3PNARrlw4m5IlrwLgu61_yyKbdObbicb_Q3sU5-O5WliC2KJ_HzdCjQr/pubembed?rm=minimal&start=true&loop=true&delayms=15000"
BITLAIR_URL = "https://dashboard.bitlair.nl/d/000000001/bitlair?orgId=1&kiosk=1&_dash.hideTimePicker=true&from=now-6h&to=now&timezone=Europe/Amsterdam&refresh=10s"


class FrameSys:
    def _run(self, args: list[str]):
        proc = subprocess.run(args)
        if proc.returncode != 0:
            raise ChildProcessError("Subprocess exited with non-zero code.")

    def _set_url(self, url: str):
        self._run(["snap", "set", "chromium", f"url={url}"])
        self._run(["snap", "restart", "chromium"])

    def show_djo(self):
        self._set_url(DJO_URL)

    def show_bitlair(self):
        self._set_url(BITLAIR_URL)

    def shutdown(self):
        self._run(["/sbin/halt"])
