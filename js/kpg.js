export default class KeyPairGenerator{
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