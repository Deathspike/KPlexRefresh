from json import loads
from time import sleep

from .models import Mode, Screen
from .utils.cmd import cmd


class Engine:
    def __init__(self, refresh_rates: list[int], tolerance: float):
        self._previous: dict[int, Mode] = {}
        self._refresh_rates = refresh_rates
        self._tolerance = tolerance

    def _get_candidates(self, active: Mode, modes: list[Mode]):
        for refresh_rate in self._refresh_rates:
            candidates = (
                target
                for target in modes
                if self._is_candidate(active, refresh_rate, target)
            )

            target = min(
                candidates,
                key=lambda target: abs(target.refresh_rate - refresh_rate),
                default=None,
            )

            if target:
                yield target

        return None

    def _is_candidate(self, active: Mode, refresh_rate: int, target: Mode):
        return (
            target.size == active.size
            and abs(target.refresh_rate - refresh_rate) <= self._tolerance
        )

    def activate(self):
        args = ["kscreen-doctor", "--json"]
        screen = Screen(loads(cmd(args)))

        for output in screen.outputs:
            # Find the active and target mode.
            active_id = output.current_mode_id
            active = next((mode for mode in output.modes if mode.id == active_id), None)
            targets = list(self._get_candidates(active, output.modes)) if active else []

            # Switch if the target mode is different.
            if active and active not in targets and targets:
                print(f"output #{output.id} switching to {targets[0].refresh_rate}hz")
                cmd(["kscreen-doctor", f"output.{output.id}.mode.{targets[0].id}"])

                # Save the active mode for later.
                if output.id not in self._previous:
                    print(f"output #{output.id} saved as {active.refresh_rate}hz")
                    self._previous[output.id] = active

    def restore(self):
        while self._previous:
            output_id, mode = self._previous.popitem()
            print(f"output #{output_id} restoring to {mode.refresh_rate}hz")
            cmd(["kscreen-doctor", f"output.{output_id}.mode.{mode.id}"])


class Poller:
    def __init__(self, engine: Engine, process: str):
        self._engine = engine
        self._process = process

    def run_forever(self, timeout_in_seconds: int):
        while True:
            try:
                if cmd(["pgrep", self._process]):
                    self._engine.activate()
                else:
                    self._engine.restore()
            except Exception as ex:
                print(ex)
            finally:
                sleep(timeout_in_seconds)


if __name__ == "__main__":
    engine = Engine([240, 144, 120, 96, 72, 48, 24], 0.05)
    poller = Poller(engine, "plex-bin")
    poller.run_forever(1)
