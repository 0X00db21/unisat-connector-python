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

    def get_tx_info(self, txid):
        '''Get the summary info of a tx.

        Parameters:
            txid (str): Tx id
        '''
        route = f'/v1/indexer/tx/{txid}'
        return self.client.call(method='GET', route=route)

    def get_tx_inputs(self, txid, cursor, size):
        '''Get the inputs of a tx.

        Parameters:
            txid (int): Block height
            cursor (int): Start offset
            size (int): Number of items returned
        '''
        route = f'/v1/indexer/tx/{txid}/ins'
        params = {'size': size, 'cursor': cursor}
        return self.client.call(method='GET', route=route, params=params)
