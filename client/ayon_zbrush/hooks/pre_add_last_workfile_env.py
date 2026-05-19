import os
from ayon_applications import PreLaunchHook, LaunchTypes


class AddLastWorkfileToEnv(PreLaunchHook):
    """Expose resolved last workfile path to the launched ZBrush process.

    ZBrush is not in core's AddLastWorkfileToLaunchArgs app_groups and cannot
    reliably open a .ztl tool via command line, so the addon opens it itself
    in ZbrushHost.initial_app_launch() using this env var. Mirrors the gating
    of core's AddLastWorkfileToLaunchArgs so the "open last workfile on
    startup" setting is respected.
    """
    app_groups = {"zbrush"}
    launch_types = {LaunchTypes.local}

    def execute(self):
        workfile_path = self.data.get("workfile_path")
        if not workfile_path:
            if not self.data.get("start_last_workfile"):
                self.log.info("Set to not open last workfile on start.")
                return
            workfile_path = self.data.get("last_workfile_path")
            if not workfile_path:
                self.log.warning("Last workfile was not collected.")
                return

        if not os.path.exists(workfile_path):
            self.log.info("Context has no workfile yet.")
            return

        self.launch_context.env["AYON_ZBRUSH_OPEN_LAST_WORKFILE"] = (
            workfile_path
        )
