import sys
import logging
import json
import time
import requests
from .UDS import UDS

class ClientError(Exception):
    """
    Custom exception class for handling API-related errors.
    Raises:
        Exception: Standard exception with a custom message formatted to include API error details.
    """

    def __init__(self, data, logger=None, log_exc_info=False):
        """
        Initialize a new instance of ClientError with the specified error data.

        This constructor extracts the error message and HTTP status code from the provided data,
        formats a custom error message, and logs the error if a logger is provided.

        Parameters:
            data (dict): A dictionary containing details about the API error.
                         It should have keys for 'msg' (error message) and 'http_status_code'.
            logger (logging.Logger, optional): A logger instance for logging the error.
            log_exc_info (bool, optional): A flag indicating whether to log exception information.
        """
        data = {} if data is None else data
        api_msg = data.get('msg', '[no message found]')
        api_code = data.get('http_status_code', '[no http status code found]')
        error_message = f'{api_msg} (http status code: {api_code})'
        super().__init__(error_message)
        if logger:
            logger.error(error_message, exc_info=log_exc_info)

class Client:
    """
    A client class for interacting with the UniSat Developer Service API.

    This class provides methods for sending requests to the API, handling errors,
    logging messages, and managing API calls.
    """

    def __init__(self, endpoint, api_key, log_config='stderr', log_level=logging.INFO):
        """
        Initialize the Client instance with
            - API endpoint
            - Authentication details
            - Logging configuration.

        Parameters:
            endpoint (str): The base URL of the API.
            api_key (str): The bearer token for API authentication.
            log_config (str): Configuration for the logging output.
            log_level (int): The logging level.
        """
        self.log_exc_info = False
        self.logger = self._set_logger(log_config, log_level)
        self.uds = UDS(self)
        self.base_url = endpoint
        self.bearer = api_key
        self.retry = 0

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        The `with` statement will bind this method's return value to the target(s)
        specified in the `as` clause of the statement, if any.

        Returns:
            Client: The instance of the Client itself.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit the runtime context and perform any necessary cleanup.

        This method is called when exiting the `with` block. It handles logging
        of exceptions, if any, and cleans up the logger handlers.

        Parameters:
            exc_type (type): type of the exception that caused the context to be exited, if any.
            exc_value (Exception): exception instance that caused the context to be exited, if any.
            exc_traceback (traceback): traceback object associated with the exception, if any.

        Returns:
            bool: False to indicate any exception passed to it should be re-raised.
                  If omitted or None, exceptions are re-raised.
        """
        if exc_type is not None:
            logger_message = f'{exc_type} {exc_value} was intercepted !'
            self.logger.error(logger_message, exc_info=self.log_exc_info)
        self.logger.info('[stopping unisat client]')
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
        return False

    def log(self, message, level=logging.INFO):
        """
        Logs a given message at the specified logging level.

        This method provides a convenient way to log messages with different levels of severity.
        If an unknown logging level is provided, it defaults to logging.INFO.

        Parameters:
            message (str): The message to be logged.
            level (int: The severity level of the log message.
                        Defaults to logging.INFO and can be one of the standard logging levels.
        """
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        if level not in levels:
            logger_message = 'Client.log() call with unknow level parameter, using logging.INFO'
            self.logger.warning(logger_message)
            level = logging.INFO
        self.logger.log(level=level, msg=str(message))

    def call(self, method='GET', route='/', params=None):
        """
        Make an API call to the specified route using the given method and parameters.

        This method handles API requests, retries in case of rate limit errors,
        and raises a ClientError for unsuccessful responses.

        Parameters:
            method (str, optional): The HTTP method to use for the request. Defaults to 'GET'.
            route (str, optional): The API route to be accessed. Defaults to '/'.
            params (dict, optional): The parameters to be sent with the request. Defaults to None.

        Returns:
            dict: The JSON response content from the API.

        Raises:
            ClientError: If the API response is not successful.
        """
        valid_status_code_list = [200]
        (method, url, headers, data) = self._configure_request(method, route, params)
        content = self._send_request(method, url, headers, data)
        if content['http_status_code'] == 403 and content['msg'] == 'exceeds rate limit':
            if self.retry == 0:
                self.logger.info('exceeds rate limite error catched, retry in 1 second')
                self.retry += 1
                time.sleep(1)
                content = self._send_request(method, url, headers, data)
            else:
                self.logger.info('exceeds rate limite error catched again !')
                self.retry = 0
                raise ClientError(data=content, logger=self.logger, log_exc_info=self.log_exc_info)
        if content['http_status_code'] not in valid_status_code_list:
            raise ClientError(data=content, logger=self.logger, log_exc_info=self.log_exc_info)
        return content

    def _configure_request(self, method, route, params):
        """
        Configures the details of an API request.

        Prepares and returns the components necessary to make an API request,
        including the method, URL, headers, and data.

        Parameters:
            method (str): The HTTP method for the request.
            route (str): The specific route (path) for the API request.
            params (dict, optional): Parameters to be included in the request. Defaults to None.

        Returns:
            tuple: A tuple containing the method, URL, headers, and data for the request.
        """
        logger_message = f'[CALL] _configure_requests({str(method)}, {str(route)}, {str(params)})'
        self.logger.debug(logger_message)
        url = self.base_url + route
        headers = {'accept': 'application/json', 'X-Client': "unisat-wrapper v0.0.42 alpha"}
        if self.bearer:
            headers['Authorization'] = f'Bearer {self.bearer}'
        if method == "POST":
            headers['Content-Type'] = 'application/json;charset=utf-8'
        params = {k: str(v) for k, v in params.items()} if params else None
        data = json.dumps(params) if params is not None else None
        msg = '[RETURN _configure_requests]'
        msg += f'(method={method}, url={url}, headers={str(headers)}, data={str(data)})'
        self.logger.debug(msg)
        return (method, url, headers, data)

    def _send_request(self, method, url, headers, data):
        """
        Sends an API request and returns the response.

        Performs the actual API request using the specified method, URL, headers, and data.
        It handles JSON response parsing and returns a dict with response content and HTTP code.

        Parameters:
            method (str): The HTTP method for the request.
            url (str): The full URL for the request.
            headers (dict): Headers to be sent with the request.
            data (str): Stringified JSON data to be sent with the request (if applicable).

        Returns:
            dict: A dictionary containing the response content and the HTTP status code.
        """
        msg = f'[CALL] _send_requests({str(method)}, {str(url)}, {str(headers)}, {str(data)})'
        self.logger.debug(msg)
        try:
            req = requests.request(method, url, headers=headers, data=data)
            output = req.json()
        except requests.JSONDecodeError:
            output = {'code': -500, 'msg': 'Client not receive json !'}
        except requests.RequestException:
            msg = "An exception was raised by 'requests' module, "
            msg += "investigation is needed to identify the root cause, "
            msg += "e.g., incorrect URL, no internet access, unavailability of remote service, ..."
            self.logger.error(msg, exc_info=self.log_exc_info)
            raise ClientError(data=None)
        status = {'http_status_code': req.status_code}
        content = {**status, **output}
        self.logger.debug(f'[RETURN _send_requests] (content={str(content)}')
        return content

    def _set_logger(self, output, level):
        """
        Configures and sets up the logger for the client.

        Initializes and configures a logger based on the specified output type and logging level.
        This logger is then used for logging messages throughout the client.

        Parameters:
            output (str): The output type for the logger. Can be 'stderr', a file name, or None.
            level (int): The logging level to be set for the logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        if output is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())
            return logger
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if output == 'stderr':
            logging.basicConfig(level=level, format=format_str, stream=sys.stderr)
        else:
            logging.basicConfig(level=level, format=format_str, filename=output, filemode='a')
        logger = logging.getLogger(__name__)
        logger.info('starting unisat client')
        return logger
