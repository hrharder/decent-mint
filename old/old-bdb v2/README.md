# NetworkTransportLayer Documentation

This document contains a breif explanation of the NetworkBroadastLayer program (called NBL), and a description of how to use its methods to prepare and send propperly formatted orders.

### NBL Methods:


##### __init__(tokens, options):
Initialize an instance to access the NetworkBroadcastLayer.

###### tokens: 
Provide app_ID and app_Key (BigchainDB API)

###### options: 
Not currently needed.

##### make_tx(data, metadata, public_key):
Create a raw transaction with supplied data and metadata, as well as a users public key (also known as an address).

###### data: 
A dictionary with main order data.

###### metadata: 
A dictionary with order metadata 

###### public_key:
A users public_key (or address) used to creat a transaction

##### sign_tx(raw_tx, private_key):
Sign a prepared raw transaction with a private key.

###### raw_tx: 
A prepared tx, created with make_tk()

###### private_key:
A users private_key used to SIGN a transaction

##### push_tx(signed_tx):
Push a transaction to BigchainDB.

###### signed_tx: 
A signed tx, created with sign_tx()

###### private_key:
A users private_key used to SIGN a transaction