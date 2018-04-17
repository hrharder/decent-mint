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