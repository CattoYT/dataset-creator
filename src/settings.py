import toml
import os


# honestly still hate python oop
# i need a rust rewrite :(
class Settings:
    _instance = None
    _path = "settings/settings.toml"
    _default = {"Show History": False, "Destructive Processing": False}

    def __repr__(self):
        return self.data

    def __str__(self):
        return str(self.data)

    def __getitem__(self, name):
        return self.data[name]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                self.data = toml.loads(f.read())
        else:
            self.data = self._default.copy()
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            self.save()

    def save(self):
        with open(self._path, "w") as f:
            f.write(toml.dumps(self.data))


settings = Settings()
