class General:
    ''' Implementation of general Module of UniSat API (from UDS documentations)
    see: https://docs.unisat.io/dev/unisat-developer-service/general
    '''

    def __init__(self, client):
        self.client = client

    def get_blockchain_info(self):
        """Get blockchain info."""
        route = '/v1/indexer/blockchain/info'
        return self.client.call(method='GET', route=route)

    def get_block_transactions(self, height, size, cursor):
        '''Get tx history by block height.

        Parameters:
            height (int): Block height
            size (int): Number of items returned
            cursor (int): Start offset
        '''
        route = f'/v1/indexer/block/{height}/txs'
        params = {'size': size, 'cursor': cursor}
        return self.client.call(method='GET', route=route, params=params)
