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
