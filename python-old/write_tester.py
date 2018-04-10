'''
	#############################
	NetworkBroadcastLayer Tester
	#############################
	
	Written by Henry Harder
	for Paradigm, 2018

	@version 0.0.2
	@version_date: 30 March 2018

	https://paradigm.market/
	https://paradigmfoundation.io/
'''

# import NetworkBroadcastLayer toolkit
from nbl import*
from time import sleep

'''
#########
THESE ARE PRIVATE 
#########
'''

app_id = ''
app_key = ''


'''
#########
END PRIVATE DATA 
#########
'''


data = {'data':{'deal_model_address':'0x...dealModelAddress_here',
				'order_data':{}}}
metadata = {'metadata':'your...metadata....here'}

# generate a random test keypair
# in reality, real keys would be used
alice = KeypairGenerator()

# create instance of NBL
broadcaster = NetworkBroadcastLayer(app_id, app_key)

# create a transaction
test_tx = broadcaster.make_tx(data, metadata, alice.get_public_key()) 

signed_tx = broadcaster.sign_tx(test_tx, alice.get_private_key())

# print result so tx can be checked
print(broadcaster.push_tx(signed_tx))
sleep(1.0)
print(broadcaster.check_tx(signed_tx['id']))

