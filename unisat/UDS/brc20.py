class BRC20:
    """
    docs: https://docs.unisat.io/dev/unisat-developer-service/brc-20
    """

    def __init__(self, client):
        self.client = client

    def get_best_block_height(self):
        '''Get the best block height of BRC20 data.
        This value will be consistend with the latest block height a short
        time after the block has been confirmed.
        '''
        route = '/v1/indexer/brc20/bestheight'
        return self.client.call(method='GET', route=route)
