from datetime import datetime
from web3 import Web3
# from web3.auto.infura import w3
from ens import ENS
import etherscan

# HTTP_PROVIDER = 'https://empty-wandering-snow.quiknode.pro/df2c575d8e4b307abf98baa782daa79da3b48322/'
# WSS_PROVIDER = 'wss://empty-wandering-snow.quiknode.pro/df2c575d8e4b307abf98baa782daa79da3b48322/'

# Get any nodes on https://chainlist.org/

WEB3_INFURA_PROJECT_ID = '32718f747eb24dcfb487db93a8421089'
WEB3_INFURA_API_SECRET = '4efe680d7fb34fb2a8b5d8d55348d521'

# Ethereum Mainnet RPC URL List
RPC_HTTP_SERVERS = [
  'https://main-rpc.linkpool.io',
  'https://main-light.eth.linkpool.io',
  'https://eth-mainnet.public.blastapi.io',
  'https://rpc.ankr.com/eth',
  'https://rpc.flashbots.net',
  'https://api.mycryptoapi.com/eth',
  'https://eth-rpc.gateway.pokt.network',
  'https://cloudflare-eth.com',
  'https://ethereumnodelight.app.runonflux.io',
  'https://eth-mainnet.gateway.pokt.network/v1/5f3453978e354ab992c4da79',
  'https://mainnet.eth.cloud.ava.do',	
  'https://nodes.mewapi.io/rpc/eth',
  'https://mainnet-nethermind.blockscout.com',
  ###### 
  "https://rpc.flashbots.net/",
  
  ### Paid server
  'https://empty-wandering-snow.quiknode.pro/df2c575d8e4b307abf98baa782daa79da3b48322/',
  'https://mainnet.infura.io/v3/aa2115adfe164f49a77fe6c38c754bc9',
  'https://mainnet.infura.io/v3/32718f747eb24dcfb487db93a8421089',
  'https://2AMdtnynf5Wi4UkCZhnbzXiLC7L:ee6b63e240262cd8f215a0f53fb6d455@eth2-beacon-mainnet.infura.io',
]

RPC_WSS_SERVERS = [
  'wss://empty-wandering-snow.quiknode.pro/df2c575d8e4b307abf98baa782daa79da3b48322/',
  'wss://mainnet.infura.io/ws/v3/aa2115adfe164f49a77fe6c38c754bc9',
  'wss://mainnet.infura.io/ws/v3/32718f747eb24dcfb487db93a8421089',
  'wss://2AMdtnynf5Wi4UkCZhnbzXiLC7L:ee6b63e240262cd8f215a0f53fb6d455@eth2-beacon-mainnet.infura.io'
]

ETHER_SCAN_API_KEY_TOKEN = 'I9C5SCAAYXB41F9ITE4ZSEFEMP1VVCPR6A'

ETH_DEFAULT_VALUE = {
    "categories": [],
    "tags": [],
    "name": '',
    "labelHash": '',
    "tokenId": "",
    "registrant": "",
    "registrationDate": 0,
    "expiryDate": 0,
    "resolver": "",
    "owner": '',
    "subcategory": 0,
    "width": 0,
    "createdAt": '',
    "updatedAt": '',
    "auctionType": "none",
    "createdDate": 0,
    "endDate": 0,
    "endingPrice": 0,
    "endingPrice_decimal": 0,
    "lastSale": 0,
    "lastSaleDate": 0,
    "lastSalePaymentToken": "",
    "lastSale_decimal": 0,
    "paymentToken": '',
    "startingPrice": '',
    "startingPrice_decimal": 0,
    "balance": 0,
    "objectId": ''
  }

def get_eth_address_by_provider(providers, name):
  try:
    w3 = Web3(providers)
    # w3 = Web3(Web3.WebsocketProvider(WSS_PROVIDER))
    isConnected = w3.isConnected()
    print('==== isConnected: ', isConnected)
    
    if isConnected:
      ns = ENS.fromWeb3(w3)
      # Try to scan
      eth_name = name
      
      eth_address = ns.address(eth_name)
      print(f'==== eth_name = {eth_name}, eth_address = {eth_address}')
      return eth_address, w3, ns

  except Exception as error:
    print('==== Failed the get the address: get_eth_address_by_provider(): ', error)
  return None, None, None

def get_eth_address(name):
  # Try to get with HTTP servers
  providers = []
  for rpc in RPC_HTTP_SERVERS:
    
    try:
      print('==== trying to connect to a http rpc server: ', rpc)
      provider = Web3.HTTPProvider(rpc)
      providers.append(provider)
      eth_address, w3, ns = get_eth_address_by_provider(provider, name)
      if eth_address:
        return eth_address, w3, ns
    except Exception as error:
      print('==== Failed the get the address: get_eth_address(): ', error)

  # Try to get with websocket servers
  for rpc in RPC_WSS_SERVERS:
    try:
      print('==== trying to connect to a wss rpc server: ', rpc)
      provider = Web3.WebsocketProvider(rpc)
      eth_address, w3, ns = get_eth_address_by_provider(provider, name)
      if eth_address:
        return eth_address, w3, ns
    except Exception as error:
      print('==== Failed the get the address: get_eth_address(): ', error)
  return None, None, None

def scan_ens(name, skip_no_eth=False):
  eth_values = ETH_DEFAULT_VALUE
  eth_values['name'] = name

  # eth_name = f'{name}.eth'
  eth_name = name
  tmp_names = name.split('.')
  if tmp_names[-1] != 'eth':
    eth_name = f'{name}.eth'

  eth_address, w3, ns = get_eth_address(eth_name)

  if eth_address is None:
    if skip_no_eth:
      return None
    return eth_values

  # Filled out the result into the firebase db]
  cur_time = datetime.now()
  str_now = cur_time.strftime("%Y-%m-%dT%H:%M:%S.%sZ")

  ethScan = etherscan.Client(
      api_key=ETHER_SCAN_API_KEY_TOKEN,
      cache_expire_after=5,
  )
  print('==== ethScan: ', ethScan)

  try:
    resolver = ns.resolver(eth_name)
    print('==== resolver: ', resolver)
    if resolver:
      print('==== resolver.address = ', resolver.address)
      eth_values['resolver'] = resolver.address
  except Exception as error:
    print('==== Failed to get resolver: ', error)

  eth_values['labelHash'] = eth_address
  eth_values['owner'] = ns.owner(eth_name)
  eth_values['createdAt'] = str_now
  eth_values['updatedAt'] = str_now
  eth_values['balance'] = w3.eth.get_balance(eth_address)
  return eth_values
