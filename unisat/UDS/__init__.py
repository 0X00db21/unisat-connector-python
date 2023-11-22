from .brc20 import BRC20
from .general import General

class UDS:
    def __init__(self, client):
        self.brc20 = BRC20(client)
        self.general = General(client)