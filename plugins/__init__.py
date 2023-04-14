# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin, integrate_macros_plugins
from macros.time_convert import local_ds, local_ds_nodash, local_ts_nodash

# Defining the plugin class
class HMDPlugins(AirflowPlugin):
    """
    The plugin class
    """

    name = "hmd_plugins"
    macros = [
        local_ds,
        local_ds_nodash,
        local_ts_nodash
    ]