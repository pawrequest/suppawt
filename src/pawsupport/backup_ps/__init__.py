from .pruner import Pruner

try:
    from .sqlmodel_backup import SQLModelBot
except ImportError:
    SQLModelBot = None
    print("SQLModelBot not installed")
