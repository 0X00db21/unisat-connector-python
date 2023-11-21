# unisat-connector-python
This is a lightweight library that works as a connector to UniSat API

## ::WARNING::
- This stuff is in pre-alpha version, you probably shouldn't use it as is for production.
- I am not associated with UniSat, use at your own risk, etc.
- There is only one route implemented at the moment (Next step is BRC-20 module)
- This stuff isn't thread-safe

## UniSat documentation
- UniSat Developer Service: https://docs.unisat.io/dev/unisat-developer-service
- UniSat Developer Service Legal Disclaimer: https://docs.unisat.io/dev/unisat-developer-service-legal-disclaimer
- Mainnet swagger: https://open-api.unisat.io/swagger.html
- Testbet swagger: https://open-api-testnet.unisat.io/swagger.html

## Install
```sh
$ mkdir project ; cd project
$ python3 -m venv venv
$ source ./venv/bin/activate
$ python3 -m pip install 'git+https://github.com/0X00db21/unisat-connector-python.git'
$ # (...)
$ deactivate
```

## Example
```python3
# ./example.py
import os
import logging
import unisat

token = os.environ.get('UNISAT_KEY')
with unisat.Client(endpoint=unisat.TESTNET, api_key=token, log_config="stderr", log_level=logging.DEBUG) as client:
    client.log("First shoot !")
    try:
        client.uds.brc20.get_best_block_height()
    except unisat.ClientError:
        pass # show log on stderr
```

```shell
$ export UNISAT_KEY="[INSERT_YOUR_BEARER_TOKEN_HERE]"
$ python3 ./example.py
```

## Configuration

### Authentication
- Set `UNISAT_KEY` variable with your personnal token on your environnement before execute your script: `export UNISAT_KEY='0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'`

### Endpoint
- Configure `endpoint` (`unisat.TESTNET`, `unisat.MAINNET`, `unisat.WHITELIST`) on your `unisat.Client()` call

### Logging
- Configure `log_config` (None, stderr or filename) and `log_level` (`logging.`[`DEBUG`|`INFO`|`WARNING`|`ERROR`|`CRITICAL`]) on your `unisat.Client()` call
- Setting the `log_level` to `logging.DEBUG` will log the request URL, payload and response text.
- Setting the `unisat.Client().log_exc_info` to `True` will add stacktrace in journal (for logger.error only)
- Calling `unisat.Client().log()` to add your own logs in journal.


## Tests
Not Implemented

## Contributing
Contributions are welcome.
If you've found a bug within this project, please open an issue to discuss what you would like to change.
If it's an issue with the API, please contact UniSat

## License
This project is licensed under the BSD 3-Clause License - see the [LICENSE.md](LICENSE.md) file for details