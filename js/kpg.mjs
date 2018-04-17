/*
	KeyPairGeneratorJS (v0.1.1a)
	NetworkTransportLayerJS 

	@version-date: 17 April 2018
	@author: Henry R Harder

	Written for Paradigm, 2018
*/

export default class KeyPairGenerator{
	/*
	This class creates a public/private key pair that can be
	used for testing purposes, and provides methods to access
	the public and private keys. Should not be used for real 
	key generation, meerly for testing purposes. 
	*/

	constructor(){
		this.driver = require('bigchaindb-driver')
		this.pair = new this.driver.Ed25519Keypair()
	}

	getPublicKey(){
		return this.pair.publicKey
	}

	getPrivateKey(){
		return this.pair.privateKey
	}
}