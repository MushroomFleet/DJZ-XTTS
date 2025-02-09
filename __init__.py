NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .DJZ_XTTS_v1 import DJZ_XTTS_v1
    NODE_CLASS_MAPPINGS["DJZ_XTTS_v1"] = DJZ_XTTS_v1
    NODE_DISPLAY_NAME_MAPPINGS["DJZ_XTTS_v1"] = "DJZ_XTTS_v1"
except ImportError:
    print("Unable to import DJZ_XTTS_v1. This node will not be available.")


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
