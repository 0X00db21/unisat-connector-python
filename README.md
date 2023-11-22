# unisat-connector-python
This is a lightweight library that works as a connector to UniSat API

## ::WARNING::
- This stuff is in pre-alpha version, you probably shouldn't use it as is for production.
- I am not associated with UniSat, use at your own risk, etc.
- There is only one module (BRC-20) implemented at the moment
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
import pprint

token = os.environ.get('UNISAT_KEY')
with unisat.Client(endpoint=unisat.TESTNET, api_key=token, log_config="./journal.log", log_level=logging.INFO) as client:
    client.log("Showing stack trace in error logs (exc_info = True))")
    client.log_exc_info = True
    # set start, limit, ticker, type_ height, txid, address, size, cursor, inscription_id variable
    try:
        # General Module
        # see https://docs.unisat.io/dev/unisat-developer-service/general for more information
        general = client.uds.general
        response = general.get_blockchain_info()
        pprint.pprint(response)
        ## Another methods exposed
        #general.get_block_transactions(height, cursor, size)
        #general.get_tx_info(txid)
        #general.get_tx_inputs(txid, cursor, size)
        #general.get_tx_outputs(txid, cursor, size)
        #general.get_address_balance(address)
        #general.get_address_history(address, cursor, size)
        #general.get_btc_utxo(address, cursor, size)
        #general.get_inscription_utxo(address, cursor, size)
        #general.get_inscription_info(inscription_id)

        # BRC20 Module
        # see https://docs.unisat.io/dev/unisat-developer-service/brc-20 for more information
        brc20 = client.uds.brc20 # shortcut for brc20 module
        response = brc20.get_best_block_height()
        pprint.pprint(response)
        ## Another methods exposed
        #brc20.get_brc20_list(start, limit)
        #brc20.get_brc20_info(ticker)
        #brc20.get_brc20_holders(ticker, start, limit)
        #brc20.get_brc20_history(ticker, type_, height, start, limit)
        #brc20.get_brc20_tx_history(ticker, txid, type_, start, limit)
        #brc20.get_address_brc20_summary(address, start, limit)
        #brc20.get_address_brc20_ticker_info(address, ticker)
        #brc20.get_address_brc20_history(address, ticker, type_, start, limit)
        #brc20.get_transferable_inscription(address, ticker, start, limit)
    except unisat.ClientError:
        pass # don't stop script and show log on ./journal.log
```

```shell
$ export UNISAT_KEY="[INSERT_YOUR_BEARER_TOKEN_HERE]"
$ python3 example.py
{'code': 0,
 'data': {'bestBlockHash': '0000000000000012cf208bc1d7475bf2d19e3c8c736bd0ab90c11f52ce11287f',
          'blocks': 2539834,
          'chain': 'test',
          'chainwork': '',
          'difficulty': '',
          'headers': 2539834,
          'medianTime': 1700669817,
          'prevBlockHash': '000000000000002a803c8de7da752177880446fa04e31601b689e6618b019a45'},
 'http_status_code': 200,
 'msg': 'ok'}
{'code': 0,
 'data': {'blockid': '0000000000000012cf208bc1d7475bf2d19e3c8c736bd0ab90c11f52ce11287f',
          'height': 2539833,
          'timestamp': 1700671729,
          'total': 511},
 'http_status_code': 200,
 'msg': 'ok'}
$ cat journal.log
2023-11-22 17:54:06,157 - unisat.client - INFO - starting unisat client
2023-11-22 17:54:06,157 - unisat.client - INFO - Showing stack trace in error logs (exc_info = True))
2023-11-22 17:54:07,844 - unisat.client - INFO - [stopping unisat client]
$
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
