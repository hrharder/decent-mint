# NetworkTransportLayer Documentation

This document contains a brief explanation of the NetworkTransportLayer program (called NTL), and a description of how to use its methods to prepare and send properly formatted orders to a BigchainDB cluster.

### Main NTL Methods:

```__init__(tokens, endpoint, options):```
Initialize an instance to access the NetworkBroadcastLayer.

-  __tokens__: 
Provide app_ID and app_key (Authenticate BigchainDB API)

- __endpoint__:
Specify the root URL of your BigchainDB cluster

- __options__: 
Not currently needed.

```make_singlesign_order(data, metadata, public_key):```
Create a raw order with supplied data and metadata, as well as a users public key.
- __data__: 
A dictionary with main order data.

- __metadata__: 
A dictionary with order metadata 

- __public_key__:
A users public_key (or address) used to creat a transaction

```sign_order(raw_tx, private_key):```
Sign a prepared raw transaction with a private key.

- __raw_tx__: 
A prepared tx, created with make_tk()

- __private_key__:
A users private_key used to SIGN a transaction

```send_order(signed_order):```
Push a signed order to BigchainDB.

- __signed_order__: 
A signed order, as returned with sign_order()

- __private_key__:
A users private_key used to SIGN a transaction