'''
	#############################
	NetworkTransportLayer Tester v2
	#############################
	
	Written by Henry Harder
	for Paradigm, 2018

	@version 0.0.3
	@version_date: 9 April 2018

	https://paradigm.market/
	https://paradigmfoundation.io/
'''

# import NetworkBroadcastLayer toolkit
from ntl import*
from time import*
import pyperclip as pyp

'''
#########
this is PRIVATE 
#########
'''
app_id = ''
app_key = ''


'''
#########
END PRIVATE DATA 
#########
'''


order = {'data':{'message':'not really, hello'}}

# generate a random test keypair
# in reality, real keys would be used
alice = KeypairGenerator()

# create instance of NTL
broadcaster = NetworkTransportLayer(app_id, app_key)
reader = OrderBookReader()

# create a transaction
test_tx = broadcaster.make_singlesign_order(
	order, {'timestamp':time()}, alice.get_public_key()) 

signed_tx = broadcaster.sign_order(test_tx, alice.get_private_key())
pyp.copy(signed_tx['id'])
sent_order = broadcaster.send_order(signed_tx)
print('sent. timing.')
delay = 0
while (len(reader.get_full_asset(signed_tx['id']))==2):
	delay += 1
print(time()-reader.get_full_asset(signed_tx['id'])['metadata']['timestamp'])

