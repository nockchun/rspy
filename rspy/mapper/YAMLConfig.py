import yaml
import os, glob

class YAMLConfig:
    def __init__(self, conf_paths: list = []):
        self._configs = []
        self._current = {}
        self._current_meta = {}
        for idx, conf_file in enumerate(self._parsePaths(conf_paths)):
            config = {}
            config["path"] = conf_file
            config["configs"] = []
            is_first_conf = True
            with open(conf_file, "r") as stream:
                configs_raw = yaml.safe_load_all(stream)
                for data in configs_raw:
                    config["configs"].append(data)
                    if idx == 0 and is_first_conf:
                        self._current = data
                        self._current_meta = config
                        is_first_conf = False
            self._configs.append(config)
    
    def _parsePaths(self, conf_paths: list = []) -> list:
        all_paths = []
        for conf_path in conf_paths:
            if os.path.isfile(conf_path):
                all_paths.append(conf_path)
            elif os.path.isdir(conf_path):
                for conf_file in glob.glob(conf_path+"/*.yaml"):
                    all_paths.append(conf_file)
        return all_paths
    
    def getConfigs(self) -> list:
        return self._configs
    
    def getConfig(self, namespace: str, version: str, set_as_current: bool = False) -> dict:
        for config_meta in self._configs:
            for config in config_meta["configs"]:
                if config["version"] == version and config["namespace"] == namespace:
                    if set_as_current:
                        self._namespace = namespace
                        self._version = version
                        self._current = config
                        self._current_meta = config_meta
                    return config
        
        raise Exception(f"There is no verion '{version}' in namespace '{namespace}'.")
        return {}
    
    def setCurrent(self, namespace: str, version: str) -> None:
        conf = self.getConfig(namespace, version, True)
        if len(conf) == 0:
            raise Exception(f"There is no verion '{version}' in namespace '{namespace}'.")
    
    def getCurrent(self) -> dict:
        return self._current
    
    def __genCmdString(self, dot_query: str) -> str:
        command = "self._current"
        for element in dot_query.split("."):
            try:
                array = element[element.index("["):]
                element = element[:element.index("[")]
            except Exception:
                array = None
                pass

            command += f"['{element}']"
            if array is not None:
                command += array
        return command
    
    def getValue(self, dot_query: str) -> str:
        return eval(self.__genCmdString(dot_query))
    
    def setValue(self, dot_query: str, value: str) -> None:
        exec(f"{self.__genCmdString(dot_query)}='{value}'")
    
    def persist(self, path_file: str = None) -> None:
        config_file = path_file if path_file is not None else self._current_meta["path"]
        
        with open(config_file, 'w') as file:
            yaml.dump_all(self._current_meta["configs"], file)
