class BRC20:
    ''' Implementation of BRC20 Module of UniSat API (from UDS documentations)
    see: https://docs.unisat.io/dev/unisat-developer-service/brc-20
    '''

    def __init__(self, client):
        self.client = client

    def get_best_block_height(self):
        '''Get the best block height of BRC20 data.
        This value will be consistend with the latest block height a short
        time after the block has been confirmed.
        '''
        route = '/v1/indexer/brc20/bestheight'
        return self.client.call(method='GET', route=route)

    def get_brc20_list(self, start, limit):
        """Get the ticker list of BRC20 token.

        Parameters:
            limit (int): Number of inscriptions returned
            start (int): Start offset
        """
        route = '/v1/indexer/brc20/list'
        params = {'limit': limit, 'start': start}
        return self.client.call(method='GET', route=route, params=params)

    def get_brc20_info(self, ticker):
        '''Get the information of BRC20 by ticker.

        Parameters:
            ticker (str): Token ticker
        '''
        route = f'/v1/indexer/brc20/{ticker}/info'
        return self.client.call(method='GET', route=route)

    def get_brc20_holders(self, ticker, start, limit):
        '''Get the holders of BRC20 by ticker.

        Parameters:
            ticker (str): Token ticker
            start (int): Start offset
            limit (int): Number of returned
        '''
        route = f'/v1/indexer/brc20/{ticker}/holders'
        params = {'limit': limit, 'start': start}
        return self.client.call(method='GET', route=route, params=params)

    def get_brc20_history(self, ticker, type_, height, start, limit):
        ''' Get the full history of BRC20

        Parameters:
            ticker (str): Token ticker
            type_ (str): Filter by history type
            height (int): Block height
            start (int): Start offset
            limit (int): Nuber of inscriptions returned
        '''
        route = f'/v1/indexer/brc20/{ticker}/history'
        params = {'type': type_, 'height': height, 'start': start, 'limit':limit}
        return self.client.call(method='GET', route=route, params=params)

    def get_brc20_tx_history(self, ticker, txid, type_, start, limit):
        """Get the full history of BRC20 by address.

        Parameters:
            txid (str): txid
            ticker (str): Token ticker
            limit (int): Number of inscriptions returned
            start (int): Start offset
            type_ (str): Filter by history type
        """
        route = f'/v1/indexer/brc20/{ticker}/tx/{txid}/history'
        params = {'limit': limit, 'start': start, 'type': type_}
        return self.client.call(method='GET', route=route, params=params)

    def get_address_brc20_summary(self, address, start, limit):
        """Obtain BRC20 token summary by address,
        including available balance, transferable balance

        Each ticker includes two types of balances:
        - transferableBalance: The balance already inscribed as TRANSFER inscriptions
        - availableBalance: The balance can be inscribed as TRANSFER inscriptions
        - overallBalance =  transferableBalance+availableBalance

        Parameters:
            address (str): Address
            limit (int): Number of inscriptions returned
            start (int): Start offset
        """
        route = f'/v1/indexer/address/{address}/brc20/summary'
        params = {'start': start, 'limit': limit}
        return self.client.call(method='GET', route=route, params=params)

    def get_address_brc20_ticker_info(self, address, ticker):
        '''Obtain BRC20 token information by address, including availale balance, transferable
        balance, number of transferable inscriptions, the first few inscriptions, etc.

        Parameters:
            address (str): Address
            ticker (str): Token ticker
        '''
        route = f'/v1/indexer/address/{address}/brc20/{ticker}/info'
        return self.client.call(method='GET', route=route)

    def get_address_brc20_history(self, address, ticker, type_, start, limit):
        '''Get the full history of BRC20 by address.

        Parameters:
            ticker (str): Token ticker
            address (str): Address
            limit (int): Number of inscriptions returned
            start (integer): Start offset
            type_ (str): Filter by history type
        '''
        route = f'/v1/indexer/address/{address}/brc20/{ticker}/history'
        params = {'limit': limit, 'start': start, 'type':type_}
        return self.client.call(method='GET', route=route, params=params)
