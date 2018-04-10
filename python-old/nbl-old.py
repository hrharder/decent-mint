'''
	#####################
	NetworkBroadcastLayer
	#####################

	Written by Henry Harder

	@version 0.0.4
	@version_date: 30 March 2018
'''
import bigchaindb_driver
from bigchaindb_driver import BigchainDB as bdb
from bigchaindb_driver.crypto import generate_keypair
import requests

class NetworkBroadcastLayer():
	def __init__(self, app_id, app_key, options=None):
		self.tokens = {
			'app_id' : app_id,
			'app_key' : app_key
		}
		
		self.chain = bdb('https://test.bigchaindb.com', headers=self.tokens)
		self.options = options
		self.prep_tx_dict = {'unsigned_tx':{}} # dictionary with prepared tx's (key: TxID)
		self.signed_tx_dict = {'signed_tx':{}} # dictionary with signed tx's (key: TxID)
		self.sent_tx_dict = {'sent_tx':{}} # dictionary with sent tx's (key: TxID)
		self.failed_tx_dict = {'failed_tx':{}} # dictionary with failed tx's (key: TxID)

	def make_tx(self, data, metadata, public_key):
		'''
		Use this method to create an order broadcast with 
		supplied DATA, METADATA, and a users PUBLIC_KEY.
		'''
		new_tx = self.chain.transactions.prepare(operation='CREATE',
			signers=public_key, asset=data, metadata=metadata)
		self.prep_tx_dict['unsigned_tx'][new_tx['id']] = new_tx
		return new_tx


	def sign_tx(self, raw_tx, private_key):
		'''
		Use this method to create an order with supplied
		RAW_TX DATA, and a users PRIVATE_KEY.
		'''

		signed_tx = self.chain.transactions.fulfill(raw_tx,
			private_keys=private_key)
		self.signed_tx_dict['signed_tx'][signed_tx['id']] = signed_tx
		return signed_tx

	def push_tx(self, signed_tx):
		'''
		Use this method to push a signed tx to BigchainDB,
		provided with a propperly created and signed order.
		'''

		sent_tx = self.chain.transactions.send(signed_tx)
		if sent_tx != signed_tx:
			self.failed_tx_dict['failed_tx'][sent_tx['id']] = sent_tx
			return
		self.sent_tx_dict['sent_tx'][sent_tx['id']] = sent_tx
		return (sent_tx['id'])

	def check_tx(self, tx_id):
		if self.chain.transactions.status(tx_id)['status'] == 'valid':
			return True
		else:
			return False

	def get_prepared_tx(self, tx_id):
		return self.prep_tx_dict['unsigned_tx']

	def get_signed_tx(self, tx_id):
		return self.signed_tx_dict['signed_tx']['id']

	def get_sent_tx(self, tx_id):
		return self.sent_tx_dict['sent_tx']['id']

	def get_failed_tx(self, tx_id):
		return self.failed_tx_dict['failed_tx']['id']

class OrderBookReader():
	'''
	This method allows users to read the orderbook, by 
	supplying only a TX_ID. It has the ability to print the
	raw data, or return the full asset dictionary, or return
	just the order data dict, or the metadata dict.
	'''

	def __init__(self):
		self.endpoint = 'https://test.bigchaindb.com/api/v1/transactions/'
		self.read_tx = {'read_tx':{}}

	def print_full_asset(self, tx_id):
		load = requests.get(self.endpoint + tx_id)
		print(load.text)

	def get_full_asset(self, tx_id):
		full_json = requests.get(self.endpoint + tx_id).json()
		self.read_tx[full_json['id']] = full_json
		return self.read_tx['read_tx'][full_json['id']]

	def get_order_data(self, tx_id):
		order_dict = requests.get(self.endpoint + tx_id).json()
		return order_dict['asset']

	def get_order_metadata(self, tx_id):
		order_dict = requests.get(self.endpoint + tx_id).json()
		return order_dict['metadata']

	def get_all_read_tx(self):
		return self.read_tx


class KeypairGenerator():
	'''
	Only use this class to generate keypairs for 
	TESTING PURPOSES!!!

	For real orders, actual public and private keypairs
	should be used for preparing and signing all 
	transactions.
	'''

	def __init__(self):
		self.pair = generate_keypair()

	def get_public_key(self):
		'''
		Returns public key (addresss)
		'''
		return self.pair.public_key

	def get_private_key(self):
		'''
		Returns private key
		'''
		return self.pair.private_key