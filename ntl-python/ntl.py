'''
	###########################
	NetworkBroadcastLayer Alpha
	###########################
	Written by Henry Harder

	@version 0.1.6
	@version_date: 13 April 2018

'''
from bigchaindb_driver import BigchainDB as bdb
from bigchaindb_driver.crypto import generate_keypair as gen 
import requests

class NetworkTransportLayer():
	def __init__(self, endpoint, app_id, app_key):
		self.tokens = {
			'app_id' : str(app_id),
			'app_key' : str(app_key)
			}

		self.chain = bdb(endpoint, 
			headers=self.tokens)

		self.log_dict = {'u_ord_li' : [], # list of created orders
					's_ord_li' : [], # list of signed orders
					'b_ord_dt' : {}} # dictionary of broadcasted orders,
									 # with key TXID

	def make_solo_order(self, raw_order, metadata, public_key):
		'''
		This method creates a json order ready to be signed and
		broadcast to a BigchainDB cluster. It takes a PUBLIC KEY and
		an ORDER dictionary, as well as relevant METADATA.

		This method is for a single-signature order, for multiple, use
		make_multi_order().
		'''

		new_order = self.chain.transactions.prepare(
			operation = 'CREATE',
			signers = public_key,
			asset = raw_order,
			metadata = metadata)

		self.log_dict['u_ord_li'].append(new_order)
		return new_order

	def make_multi_order(self, raw_order, metadata, public_keys_tuple):
		'''
		This method creates a json order ready to be signed and
		broadcast to a BigchainDB cluster. It takes a PUBLIC KEY TUPLE and
		an ORDER dictionary, as well as relevant METADATA.

		This method is for a multiple-signature order, so a tuple with
		public keys should be provided. For single signature orders, use
		make_solo_order().
		'''

		new_order = self.chain.transactions.prepare(
			operation = 'CREATE',
			signers = public_keys_tuple,
			asset = raw_order,
			metadata = metadata)

		self.log_dict['u_ord_li'].append(new_order)
		return new_order

	def sign_solo_order(self, order, private_key):
		'''
		This method takes an ORDER created with make_singlesign_order()
		or make_order(), along with a PRIVATE KEY, and returns 
		a signed order, ready to be broadcast to BigchainDB.

		If there is more than one signer, use .sign_multi_order()
		'''

		signed_order = self.chain.transactions.fulfill(
			order, private_keys=private_key)

		self.log_dict['s_ord_li'].append(signed_order)
		return signed_order

	def sign_multi_order(self, order, private_key_tuple):
		'''
		This method takes an ORDER created with make_multisig_order()
		or make_order(), along with a PRIVATE KEY, and returns 
		a signed order, ready to be broadcast to BigchainDB.

		If there is only one signer, use .sign_solo_order()
		'''

		signed_order = self.chain.transactions.fulfill(
			order, private_keys=private_key_tuple)

		self.log_dict['s_ord_li'].append(signed_order)
		return signed_order

	def send_order(self, signed_order):
		'''
		This method pushes ONE signed order to BigchainDB. 
		It takes a single SIGNED_ORDER as an argument, and returns
		a tuple with the TX_ID and the full transaction.
		'''

		sent_order = self.chain.transactions.send(signed_order)

		self.log_dict['b_ord_dt'][sent_order['id']] = sent_order
		return (sent_order['id'], sent_order)

	def get_order_height(self, tx_id):
		'''
		Returns the block height of the block the order with
		the specified TX_ID was validated in.
		'''

		return self.chain.blocks.get(txid=tx_id)

class OrderBookReader():
	'''
	This method allows users to read the orderbook, by 
	supplying only a TX_ID. It has the ability to print the
	raw data, or return the full asset dictionary, or return
	just the order data dict, or the metadata dict.
	'''

	def __init__(self, endpoint):
		self.endpoint = endpoint

	def get_full_asset(self, tx_id):
		return requests.get(self.endpoint + tx_id).json()

	def get_order_data(self, tx_id):
		order_dict = requests.get(self.endpoint + tx_id).json()
		return order_dict['asset']

	def get_order_metadata(self, tx_id):
		order_dict = requests.get(self.endpoint + tx_id).json()
		return order_dict['metadata']

	def get_data_and_metadata(self, tx_id):
		order_dict = requests.get(self.endpoint + tx_id).json()
		return {'metadata':order_dict['metadata'], 'data':order_dict['asset']}


class KeypairGenerator():
	'''
	Generates a BDB compliant BIP39/44 public/private key pair
	that can be used to create, sign, and send orders to the
	BigchainDB network.

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

