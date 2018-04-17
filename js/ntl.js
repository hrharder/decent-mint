/*
	NTLJS (v0.2.1b)
	NetworkTransportLayerJS 

	@version-date: 17 April 2018
	@author: Henry R Harder

	Written for Paradigm, 2018
*/

export default class NetworkTransportLayer{
	/*
	This is the main NTL class that communicates with BigchainDB
	and facilitates the creation, signing, and broadcast of orders.
	It must be supplied with credentials for accessing a BigchainDB
	cluster.
	*/

	constructor(id, key, rootUrl){
		this.driver = require('bigchaindb-driver');
		this.connection = new this.driver.connection(rootUrl, {
			app_id : id,
			app_key : key
		});
	}

	makeOrder(data, metadata, publicKey){
		const newOrder = this.driver.Transaction.makeCreateTransaction(
			data, metadata,
			[this.driver.Transaction.makeOutput(
				this.driver.Transaction.makeEd25519Condition(publicKey))
			], publicKey);

		return newOrder;
	}

	signOrder(unsignedOrder, privateKey){
		const signedOrder = this.driver.Transaction.signTransaction(
			unsignedOrder, privateKey);

		return signedOrder;
	}

	sendOrder(signedOrder){
		this.connection.postTransactionCommit(signedOrder);
		return signedOrder.id;
	}
}