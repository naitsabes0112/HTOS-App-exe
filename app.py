import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from dotenv import load_dotenv
load_dotenv()

import argparse
from nicegui import ui
from app_core import models
from app_core.profile_selector import ProfileSelector
from app_core.setting_selector import SettingSelector
from app_core.resign import Resign
from app_core.encrypt import Encrypt
from app_core.decrypt import Decrypt
from app_core.reregion import Reregion
from app_core.createsave import Createsave
from app_core.convert import Convert
from app_core.quickcodes import QuickCodes
from app_core.sfo_editor import SFOEditor
from utils.constants import APP_PROFILES_PATH, APP_SETTINGS_PATH, VERSION
from utils.workspace import WorkspaceOpt, startup, check_version

workspace_opt = WorkspaceOpt()

def initialize_tabs() -> None:
    profiles = models.Profiles(APP_PROFILES_PATH)
    settings = models.Settings(APP_SETTINGS_PATH)
    ui.dark_mode().enable()

    with ui.header().classes("h-12 justify-center"):
        ui.label(f"HTOS {VERSION}").style("font-size: 15px; font-weight: bold;")

    with ui.tabs().classes("w-full") as tabs:
        tab_container = [
            ProfileSelector(profiles),
            Resign(profiles, settings),
            Decrypt(settings),
            Encrypt(profiles, settings),
            Reregion(profiles, settings),
            Createsave(profiles, settings),
            Convert(settings),
            QuickCodes(settings),
            SFOEditor(),
            SettingSelector(settings)
        ]
    with ui.tab_panels(tabs, value=tab_container[0].tab).classes("w-full"):
        for t in tab_container:
            with ui.tab_panel(t.tab):
                t.construct()

if __name__ in {"__main__", "__mp_main__"}:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ignore-startup", action="store_true")
    args, unknown = parser.parse_known_args()
    if args.ignore_startup:
        workspace_opt.ignore_startup = True
    startup(workspace_opt, lite=True)

    ui.run(root=initialize_tabs, reload=False, native=True, window_size=(1400, 800))