# GetConfig
Converts json files in a config directory into a Config NamedTuple.

## Usage
Within a configuration directory ('./config' by default), provide a json configuration file
for each environment your application will run in. For example, your project structure might look like:

```
.
└── project/
    ├── config/
    │   ├── develop.json
    │   ├── production.json
    │   ├── qa.json
    │   └── test.json
    ├── src/
    │   └── project files
    └── test/
        └── test files
```

Where each file has contents like:
```json
{
    "int_key": 13,
    "array_key": ['a', 'b', 'c'],
    "object_key": {
        "application_name": "GetConfig",
        "application_creator": "me"
    }
}
```

Then from your application:
```python
from get_config import get_config

config = get_config()
print(config)  # Config(int_key=13, array_key=('a', 'b', 'c'), object_key=ObjectKey(application_name='GetConfig', application_creator='me')
```

By default, the module will load the configuration file corresponding to the value in `os.environ['ENV']`. If no value is present, it will default to 'test'. If there is no file for the specified (or default) environment, an ImportException will be raised. The environment can be passed directly to the factory function as can the directory.

```python
from get_config import get_config

config = get_config(directory='./deep/config/directory/', environment='production')
```

### Defaults

A default file can be used to provide values that are static accross environments. If keys in the environment files duplicate keys in the default file, the environment file values will be used. For example, if your config directory had the structure:

```
.
└── config/
    ├── default.json
    └── test.json
```

And default.json had contents
```json
{
    "default_key": "always the same",
    "override_key": "default value"
}
```

While test.json had contents
```json
{
    "override_key": "overridden value",
    "environment_specific_key": "something test environment specific"
}
```

Then with `environment='test'`, the config object would have the following attributes and values:
```python
config.default_key  # "always the same"
config.overriden_key  # "overridden value"
config.environment_specific_key  # "something test environment specifc"
```

## Future Development
### `has` and `get` methods
Currently the config objects are tuples and namedtuple types. I would like to add some additional functionality to check if a property is present and to fetch deep properties.

cfg### Support for Additional File Types
Since `json` is not commonly used in python applications for configuration, to make this library more broadly appealing, I would like to support additional file types such as `.ini`, `.cfg`, and others.

### Pulling Values from the Environment
I would like to provide an interface so that environment variables can also be added to the config object at the specified attributes.

### Secrets Addons
I would like to make the library extensible so that if you are managing secrets with a third party system like Vault or AWS Secrets Manager, addons could provide ways to fetch those values into your configuration object.