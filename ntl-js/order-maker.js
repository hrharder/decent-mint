/*
	OrderMakerJS (v0.0.1a)
	NetworkTransportLayerJS 

	@version-date: 17 April 2018
	@author: Henry R Harder

	Written for Paradigm, 2018
*/

export default class OrderMaker{
	constructor(intList, addrList, maker){
		this.orderData = {
			'order':{
				'maker' : maker,
				'timestamp' : Math.floor(Date.now()/1000),
				'fields' : {
					'intList' : intList,
					'addrList' : addrList
				}
			}
		};
		this.orderMetaData = {
			'metadata':{
				'filled' : false,
				'valid' : true,
				'updated' : Math.floor(Date.now()/1000)
			}
		};
	}

	getOrderData(){
		return this.orderData;
	}

	getOrderMetadata(){
		return this.orderMetaData;
	}
}