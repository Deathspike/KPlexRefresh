# KPlexRefresh

_KPlexRefresh_ is a small Python utility that switches your display refresh rate when Plex HTPC (`plex-bin`) is running. It polls for the `plex-bin` process using `pgrep`. When Plex starts, it uses `kscreen-doctor` to detect available output modes and switches to a mode that's a clean multiple of ~24Hz (e.g. 120Hz) for smooth playback. When Plex exits, it restores the original display mode.

I wrote this because Plex HTPC doesn't properly switch refresh rates on Fedora KDE (at least on my setup), and this was the simplest way to make it behave. It's admittedly a bit rough, probably a little dumb, and _definitely_ not elegant... but it works for me. Maybe it'll work for you too.

## Features

- Detects when Plex HTPC (`plex-bin`) is running.
- Automatically switches to a ~24Hz-multiple refresh rate (e.g. 120Hz).
- Restores the original display mode when Plex closes.
- Lightweight and simple, with no Plex modifications required.

## Requirements

- Fedora KDE 43+
- Plex HTPC installed via Flatpak

## Installation

You can _install_ the `systemd` service for _KPlexRefresh_ with:

```bash
git clone https://github.com/Deathspike/KPlexRefresh
cd KPlexRefresh
python -m modules.service.install
```

Or _uninstall_ with:

```bash
python -m modules.service.uninstall
```

Otherwise, run it yourself with `python -m modules.app`.
