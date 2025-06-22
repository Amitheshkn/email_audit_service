from oslo_config import cfg

CONF = cfg.CONF

application_opts = [
    cfg.StrOpt("bind_host", default="0.0.0.0", help="Address to bind the application"),
    cfg.IntOpt("bind_port", default=8000, help="Port to bind the application"),
    cfg.StrOpt("file_path", default="/tmp/cache", help="File save folder path")
]

# Register the config options
CONF.register_opts(application_opts, group="application")


def load_config(file_path,
                /) -> None:
    """
    Load configuration from the specified file or default locations.
    """
    if file_path:
        CONF(default_config_files=[file_path])


load_config("/etc/email_audit/email_audit.conf")
