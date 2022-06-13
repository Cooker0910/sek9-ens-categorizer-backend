from etherscan import Etherscan

ETHER_SCAN_API_KEY_TOKEN = 'I9C5SCAAYXB41F9ITE4ZSEFEMP1VVCPR6A'
def ether_scan(address):
  eth = Etherscan(address)
  return eth