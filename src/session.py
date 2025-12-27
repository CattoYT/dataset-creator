import toml
import os


# TODo: this
class Session:
    _instance = None
    _path = "session/session.toml"
    _default = {
        "Dataset name": "",
        "Path": "",
        "Processed bad": False,
        "Dataset format": "Ai Hobbyist",
        "Language": "en",
    }

    def __repr__(self):
        return self.data

    def __str__(self):
        return str(self.data)

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                self.data = toml.loads(f.read())
                for key in self._default:
                    try:
                        self.data[key]
                    except KeyError:
                        print(
                            f'Missing key "{key}". Replacing "{key}" with default value.'
                        )
                        self.data[key] = self._default[key]

        else:
            self.data = self._default.copy()
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            self.save()

    def save(self):
        with open(self._path, "w") as f:
            f.write(toml.dumps(self.data))


session = Session()

if __name__ == "__main__":
    print("NO FUCK YOU GET AWAY")
