from pathlib import Path

from .utils.cmd import cmd


class System:
    def __init__(self):
        self._service_name = "KPlexRefresh.service"
        self._systemd_path = Path.expanduser(Path("~/.config/systemd/user"))
        self._working_path = Path.cwd()

    def install(self):
        # Ensure that the system path exists.
        self._systemd_path.mkdir(exist_ok=True, parents=True)
        service_path = self._systemd_path / self._service_name

        # Write the service.
        service_path.write_text(
            f"""[Unit]
        Description=KPlexRefresh
        After=graphical-session.target
        Wants=graphical-session.target

        [Service]
        Type=simple
        ExecStart=/usr/bin/python -m modules.app
        WorkingDirectory={self._working_path}
        Restart=on-failure
        RestartSec=5
        Environment=XDG_RUNTIME_DIR=/run/user/%U
        Environment=WAYLAND_DISPLAY=wayland-0

        [Install]
        WantedBy=graphical-session.target
        """
        )

        # Run the service.
        cmd(["systemctl", "--user", "daemon-reload"])
        cmd(["systemctl", "--user", "enable", "--now", self._service_name])

    def uninstall(self):
        cmd(["systemctl", "--user", "stop", self._service_name])
        cmd(["systemctl", "--user", "disable", self._service_name])
