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
	def __init__(self, app_key, options=None):
		self.tokens={
			'app_id' : '81338ad5',
			'app_key' : app_key
		}

		self.chain = bdb('https://test.bigchaindb.com', 
			headers=self.tokens)
		self.options = options

		self.log = {'made_order_li' : [], # list of created orders
					'sign_order_li' : [], # list of signed orders
					'sent_order_dt' : {}} #

	def make_singlesign_order(self, order, metadata, pub_key):
		made_tx = self.chain.transactions.prepare(
			operation = 'CREATE',
			signers = pub_key,
			asset = order,
			metadata = metadata)

		self.log[]