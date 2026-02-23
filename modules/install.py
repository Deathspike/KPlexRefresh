from pathlib import Path

from .utils.cmd import cmd


class Installer:
    def __init__(self, systemd_path: Path, working_path: Path):
        self._systemd_path = systemd_path
        self._working_path = working_path

    def run(self):
        # Ensure that the system path exists.
        self._systemd_path.mkdir(exist_ok=True, parents=True)
        service_name = "KPlexRefresh.service"
        service_path = self._systemd_path / service_name

        # Write the service.
        service_path.write_text(
            f"""[Unit]
        Description=KPlexRefresh
        After=default.target

        [Service]
        Type=simple
        ExecStart=/usr/bin/python -m modules.app
        WorkingDirectory={self._working_path}
        Restart=on-failure
        RestartSec=5

        [Install]
        WantedBy=default.target
        """
        )

        # Run the service.
        cmd(["systemctl", "--user", "daemon-reload"])
        cmd(["systemctl", "--user", "enable", "--now", service_name])


if __name__ == "__main__":
    system_path = Path.home() / ".config/systemd/user"
    installer = Installer(system_path, Path.cwd())
    installer.run()
