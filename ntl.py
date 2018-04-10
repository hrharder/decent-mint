'''
	#####################
	NetworkBroadcastLayer 2.0
	#####################

	Updated to work with BigChain DB 2.0

	Written by Henry Harder

	@version 0.1.4
	@version_date: 9 April 2018
'''
from bigchaindb_driver import BigchainDB as bdb
from bigchaindb_driver.crypto import generate_keypair as gen 
import requests

class NetworkTransportLayer():
	def __init__(self, app_id, app_key, options=None):
		self.tokens={
			'app_id' : app_id,
			'app_key' : app_key
		}

		self.chain = bdb('https://test2.bigchaindb.com', 
			headers=self.tokens)
		self.options = options

		self.log = {'u_ord_li' : [], # list of created orders
					's_ord_li' : [], # list of signed orders
					'b_ord_dt' : {}} # dictionary of broadcasted orders,
									 # with key TXID

	def make_singlesign_order(self, raw_order, metadata, public_key):
		'''
		This method creates a json order ready to be signed and
		broadcast to a BigchainDB cluster. It takes a PUBLIC KEY and
		an ORDER dictionary, as well as relevant METADATA.

		This method is for a single-signature order.
		'''

		new_order = self.chain.transactions.prepare(
			operation = 'CREATE',
			signers = public_key,
			asset = raw_order,
			metadata = metadata)

		self.log['u_ord_li'].append(new_order)
		return new_order

	def sign_order(self, order, private_key):
		'''
		This method takes an ORDER created with make_singlesign_order()
		or make_order(), along with a PRIVATE KEY, and returns 
		a signed order, ready to be broadcast to BigchainDB.
		'''

		signed_order = self.chain.transactions.fulfill(
			order, private_keys=private_key)

		self.log['s_ord_li'].append(signed_order)
		return signed_order

	def send_order(self, signed_order):
		'''
		This method pushes ONE signed order to BigchainDB. 
		It takes a single SIGNED_ORDER as an argument, and returns
		a tuple with the TX_ID and the full transaction.
		'''

		sent_order = self.chain.transactions.send(signed_order)

		self.log['b_ord_dt'][sent_order['id']] = sent_order
		return (sent_order['id'], sent_order)

	def get_order_height(self, tx_id):
		'''
		Returns the block height of the block the order with
		the specified TX_ID was validated in.
		'''

		return self.chain.blocks.get(txid=tx_id)

class KeypairGenerator():
	'''
	Only use this class to generate keypairs for 
	TESTING PURPOSES!!!

	For real orders, actual public and private keypairs
	should be used for preparing and signing all 
	transactions.
	'''

	def __init__(self):
		self.pair = gen()

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

