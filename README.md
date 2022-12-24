# JS Utils
This package contains python implementations of several npm packages I missed when moving from Node.js to Python. Currently the package contains implementions of the `config` npm package as well as `stubs` from the `sinon` package.

## Config
Converts json files in a config directory into a Config NamedTuple. Based off the npm package `config`.

### Usage
Within a configuration directory (`./config` by default), provide a json configuration file
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

Where each file in the config directory has contents like:
```json
{
    "int_key": 13,
    "array_key": ['a', 'b', 'c'],
    "object_key": {
        "application_name": "jsutils",
        "application_creator": "me"
    }
}
```

Then from your application:
```python
from jsutils.config import get_config

config = get_config()
print(config)  # Config(int_key=13, array_key=('a', 'b', 'c'), object_key=ObjectKey(application_name='jsutils', application_creator='me')
```

By default, the module will load the configuration file corresponding to the value in `os.environ['ENV']`. If no value is present, it will default to `'test'`. If there is no file for the specified (or default) environment, an `ImportException` will be raised. The environment can be passed directly to the factory function as can the directory.

```python
from jsutils.config import get_config

config = get_config(directory='./deep/config/directory/', environment='production')
```

#### Defaults

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

### Custom Environment Variables
An optional custom environment variables file can be added to add environment variables to your configuration object at the time of construction. Your config directory would look like:

```
.
└── config/
    ├── custom_environment_variables.json
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

And custom_environment_variables.json had contents
```json
{
    "environment_key_1": "ENV_KEY_1",
    "nested_environment_keys": {
        "nested_key_1": "NESTED_ENV_KEY_1"
    }
}
```

Then with `environment='test'`, the config object would have the following attributes and values:
```python
config.default_key  # "always the same"
config.overriden_key  # "overridden value"
config.environment_specific_key  # "something test environment specifc"
config.environment_key_1  # value at os.environ['ENV_KEY_1']
config.nested_environment_keys.nested_key_1  # value at os.environ['NESTED_ENV_KEY_1]
```

### `.has` and `.get`
The Config class comes prebuilt with `has` and `get` methods that can be used to test if a property is present and to fetch a property. These methods also accept "deep" paths to objects.

For example, if you `default.json` looked like:
```json
{
    "top_level_key": "I'm at the top",
    "nested_top": {
        "nested_key": "It's safe inside"
    }
}
```

Then you can test for and fetch the nested property `nested_top.nested_key` as follows:
```python
config.has('nested_top.nested_key')  # True
config.get('nested_top.nested_key')  # "It's safe inside"
```

### Future Development
  * **Support for Additional File Types**: Since `json` is not commonly used in python applications for configuration, to make this library more broadly appealing, I would like to support additional file types such as `.yaml`, `.ini`, `.cfg`, and others.

  * **Secrets Addons**: I would like to make the library extensible so that if you are managing secrets with a third party system like Vault or AWS Secrets Manager, addons could provide ways to fetch those values into your configuration object.


## Stubs
This class and its factory function provides an alternative to the Mock objects from `unittest.mock`. In particular the behavior of these stubs is more flexible and versatile. Based off the stubs in the npm package `sinon`. 

### The Stub class
The stub can be instantiated with a set of attributes.

```python
from jsutils.stubs impor get_stub, Stub

stub1 = Stub(attrs={'prop1': 'value1', 'prop2': 1.61803})
stub1.prop1  # 'value1'
stub1.prop2  # 1.61803

stub2 = get_stub(attrs={'prop3': 3.14159, 'prop4': False})
stub2.prop3  # 3.14159
stub2.prop4  # False
```

### Default Behavior
Stubs can be configured to return a specific value or to raise an exception by default. If both are configured, the exception will be raised.

```python
from jsutils.stubs import get_stub
stub1 = get_stub()
stub1.returns('Hello there')

result1 = stub()
result1  # 'Hello there'

stub2 = get_stub()
stub2.raises(RuntimeError('Oh no'))
stub2()  # RuntimeError: Oh no

stub3 = get_stub()
stub3.raises(RuntimeError('Its broken'))
stub3.returns('Oh happy day')
stub3()  # RuntimeError: Its broken
```

If behavior for a stub has not been configured, it will return `None` when called.

### Asserting on Calls
The stub has a helper method to assert that a call with a specific signature was made to the stub. If you need to assert that a specific call (i.e. the seventh call) was made with a specific signature, you'll have to fall back to using the stub's call history attribute. Stubs are compatible with the ANY value from unittest.mock.

```python
from unittest.mock import ANY

from jsutils.stubs import get_stub

def test_should_know_all_calls():
    stub = get_stub()
    stub.returns('some_value')

    stub('first call')
    assert stub.called_with('first call')

    stub('second call', second_call_kwarg=1.414)
    assert stub.called_with('second call', second_call_kwarg=1.414)

    assert stub.call_history[1] == (('second_call',), {'second_call_kwarg': 1.414})
    assert stub.called_with(ANY, second_call_kwarg=1.414)
```

### Fake Behavior
If your stub needs more complicated behavior, you can provide a function that the stub will pass the arguments to. The fake behavior takes priority over all other behaviors.

```python
from jsutils.stubs import get_stub

def fake_func(arg1, args2):
    return args1 + arg2

stub = get_stub()
stub.calls_fake(fake_func)

stub(1, 2)  # 3
stub('first', 'second')  # 'firstsecond'
```


### Behavior on Specific Calls
The stub can be configured to return a value or raise an exception on a specified 0 index based call. The stub will fall back to its default behavior if the specified call has not been configured. There are convenience functions for setting first, second, and third call behavior

```python
from jsutils.stubs import get_stub

stub = get_stub()
stub.return('default_value')
stub.on_call(1).returns('second_call_value')
stub.on_third_call().returns('third_call_value')
stub.on_call(3).raises(RuntimeError('Boom'))

stub()  # 'default_value'
stub()  # 'second_call_value'
stub()  # 'third_call_value'
stub()  # RuntimeError: Boom raised
stub()  # 'default_value'
```

### Behavior for Specific Call Signatures
The stub can be configured to have specific behavior for specific call arguments. This behavior can be based on a call count or fall back to a default behavior. Call signature behavior supercedes call count and default behavior when applicable, but is superceded in priority by fake behaviors.

```python
from jsutils.stubs import get_stub

stub = get_stub()
stub.with_args('first', second_arg='second').returns(42)
stub.with_args('first', second_arg='second').on_call(1).returns(0)
stub.returns('i')

stub()  # 'i'
stub('first', second_arg='second')  # 42
stub('first', second_arg='second')  # 0
stub('first', second_arg='second')  # 42
```


### Overriding Methods on Objects
The Stub class and get_stub function can also be used to replace a method on an existing object with a stub. The created original behavior of the methods can be restored with the restore method.

```python
from jsutils.stubs import get_stub, Stub

class SomeClass:
    def method_1(self):
        return 'hello'

    def method_2(self):
        return 'goodbye'

a_class = someClass()

stub_1 = get_stub(a_class, 'method_1')
stub_1.returns('hola')

a_class.method_1()  # 'hola'

stub_2 = Stub(a_class, 'method_2')
stub_2.returns('adios')
a_class.method_2()  # 'adios

stub_1.restore()
stub_2.restore()

a_class.method_1()  # 'hello'
a_class.method_2()  # 'goodbye'
```