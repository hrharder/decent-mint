/*
	KeyPairGeneratorJS (v0.1.1a)
	NetworkTransportLayerJS 

	@version-date: 17 April 2018
	@author: Henry R Harder

	Written for Paradigm, 2018
*/

export default class KeyPairGenerator{
	constructor(){
		this.driver = require('bigchaindb-driver');
		this.pair = new this.driver.Ed25519Keypair();
	}

	getPublicKey(){
		return this.pair.publicKey;
	}

	getPrivateKey(){
		return this.pair.privateKey;
	}
}