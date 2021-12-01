# This is the abstract class that defines what a Ingest class is.
# When any subclass is imported it is added to REGISTRY 
# with the name of the class as the key and the class itself as the value.
# If a subclass doesn't implement one of the abstract methods, an error will be thrown.
from abc import ABC, abstractmethod
class NodeInterface(ABC):
    REGISTRY = {}
    @classmethod
    def __init_subclass__(cls, **kwargs):
        if cls not in NodeInterface.REGISTRY:
            name = cls.__name__
            NodeInterface.REGISTRY[name] = cls
        super().__init_subclass__(**kwargs)

    @abstractmethod
    def load_csv(self, csv_blob):
        raise NotImplementedError


# When a subclass of NodeInterface is imported, __init_subclass__ 
# is triggered and the subclass is added to the registry.
# This method imports all modules in this folder, thus registering all the subclasses. 
# Once all the subclasses are imported this function returns the dictionary that is the registry.
def node_registry():
    from os.path import dirname, basename, isfile, join
    import glob
    import importlib
    modules = glob.glob(join(dirname(__file__), "*.py"))
    file_names = {}
    for f in modules: 
        if isfile(f) and not f.endswith("__init__.py") and not f.endswith("node_interface.py"):
            file_names[basename(f)[:-3]] = f
    for name in file_names:    
            importlib.import_module("Neo4jDriver.nodes."+name)

    return NodeInterface.REGISTRY

# The ingest subclass registry for external import
REGISTRY = node_registry()
