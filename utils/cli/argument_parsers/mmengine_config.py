from jsonargparse import set_dumper, set_loader
from jsonargparse.loaders_dumpers import dumpers
from mmengine import Config


def mmengine_config(stream, path=None, ext_vars=None):
    if path:
        for ext in [".py", ".json", ".yaml", ".yml"]:
            if path.endswith(ext):
                break
    else:
        ext = ".py"
    return Config.fromstring(stream, ext)


set_loader("mmengine_config", mmengine_config)
set_dumper("mmengine_config", dumpers["yaml"])
