from .brc20 import BRC20

class UDS:
    def __init__(self, client):
        self.brc20 = BRC20(client)
