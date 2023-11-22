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
