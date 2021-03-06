'''
	#####################
	NBL Test Writer GUI
	#####################

	Written by Henry Harder

	@version 0.0.3
	@version_date: 2 April 2018
'''
from ntl import* # NetworkBroadcastLayer 
from tkinter import* # tkinter GUI python module
import time
import pyperclip as pyp

class OrderBookWriter(Frame):
	def __init__(self):
		self.parent = Tk()
		Frame.__init__(self, self.parent)
		
		self.winfo_toplevel().title('NBL Order Book Tester')
		self.broadcaster = None # network broadcaster
		self.reader = OrderBookReader()
		self.app_frame = None # current top frame

		self.widgets = {}
		self.keys = {}
		self.vars = {'pub_var':StringVar(), 'priv_var':StringVar(),
					'txid_var':StringVar(), 'out_var1':StringVar(),
					'out_var2':StringVar()}

		self.make_window()

	def make_window(self):
		self.app_frame = Frame(self.parent)
		input_frame = Frame(self.app_frame)
		output_frame = Frame(self.app_frame)

		self.app_frame.grid_rowconfigure(0) # input frame
		self.app_frame.grid_rowconfigure(1) # input frame
		self.app_frame.grid_rowconfigure(2) # input frame
		self.app_frame.grid_rowconfigure(3)
		self.app_frame.grid_rowconfigure(4)

		self.app_frame.grid_columnconfigure(0) # only one column

		input_frame.grid_columnconfigure(0) # label
		input_frame.grid_columnconfigure(1) # entry

		input_frame.grid_rowconfigure(0) # title
		input_frame.grid_rowconfigure(1) # app_key input
		input_frame.grid_rowconfigure(2) # app_id input
		input_frame.grid_rowconfigure(3) # order data
		input_frame.grid_rowconfigure(4) # order metadata
		input_frame.grid_rowconfigure(5) # generate key pair
		input_frame.grid_rowconfigure(6) # show key1
		input_frame.grid_rowconfigure(7) # show key2
		input_frame.grid_rowconfigure(8) # submit order
		input_frame.grid_rowconfigure(9) # submit order
		input_frame.grid_rowconfigure(10) # submit order
		input_frame.grid_rowconfigure(11) # submit order
		input_frame.grid_rowconfigure(12) # submit order

		output_frame.grid_rowconfigure(0) # title
		output_frame.grid_rowconfigure(1) # txid input
		output_frame.grid_rowconfigure(2) # data output

		self.vars['pub_var'].set("Click 'Generate' to make new public key")
		self.vars['priv_var'].set("Click 'Generate' to make new private key")
		self.vars['txid_var'].set('Submit an order to generate TX_ID')

		# Begin input frame
		top_label = Label(input_frame, text='Create a Transaction:') 

		app_key_label = Label(input_frame, text = 'App Key: ') 
		app_key_input = Entry(input_frame) 					   

		app_id_label = Label(input_frame, text = 'App ID: ') 
		app_id_input = Entry(input_frame)

		dm_label = Label(input_frame, text = 'DealModel: ') 
		dm_input = Entry(input_frame)

		mk_label = Label(input_frame, text = 'Maker: ') 
		mk_input = Entry(input_frame)					 

		d1_label = Label(input_frame, text = 'Field1: ') 
		d1_input = Entry(input_frame)

		d2_label = Label(input_frame, text = 'Field2: ') 
		d2_input = Entry(input_frame) 					

		d3_label = Label(input_frame, text = 'Field3: ') 
		d3_input = Entry(input_frame)

		keypair_generator = Button(input_frame, text = 'Generate Keypair',  # row 5
			command = lambda: self.generate_keypair())

		show_key1 = Label(self.app_frame, textvariable = self.vars['pub_var']) # row 6

		show_key2 = Label(self.app_frame, textvariable = self.vars['priv_var']) # row 7

		submit_button = Button(self.app_frame, text = 'Submit Order', 
			command = lambda: self.submit_order(app_key_input, app_id_input,
			dm_input, mk_input, d1_input, d2_input, d3_input)) # row 10, col 0

		txid_label = Label(self.app_frame, textvariable = self.vars['txid_var']) # row 10, col 1
		
		# End input frame

		top_label.grid(row=0, column=0, sticky=W)
		app_key_label.grid(row=1, column=0, sticky=W)
		app_key_input.grid(row=1, column=1, sticky=W)
		app_id_label.grid(row=2, column=0, sticky=W)
		app_id_input.grid(row=2, column=1, sticky=W)

		dm_label.grid(row=3, column=0,sticky=W)
		dm_input.grid(row=3, column=1,sticky=W)
		mk_label.grid(row=4, column=0,sticky=W)
		mk_input.grid(row=4, column=1,sticky=W)
		d1_label.grid(row=5, column=0,sticky=W)
		d1_input.grid(row=5, column=1,sticky=W)
		d2_label.grid(row=6, column=0,sticky=W)
		d2_input.grid(row=6, column=1,sticky=W)
		d3_label.grid(row=7, column=0,sticky=W)
		d3_input.grid(row=7, column=1,sticky=W)

		keypair_generator.grid(row=8, column=0,sticky=W)
		
		input_frame.grid(row=0, column=0)
		show_key1.grid(row=1, column=0,sticky=W)
		show_key2.grid(row=2, column=0,sticky=W)

		submit_button.grid(row=3, column=0,sticky=W)
		txid_label.grid(row=4, column=0,sticky=W)

		self.app_frame.pack()
		self.app_frame.mainloop()

	def submit_order(self, appkey, appid, dm, mk, d1, d2, d3):
		app_info, order = {}, {}

		app_info['key'] = appkey.get()
		app_info['id'] = appid.get()
		
		order['data'] = {'data':{'field1':d1.get(), 'field2':d2.get(), 
						'field3':d3.get()}}
		order['metadata'] = {'timestamp':time.time(), 'dealmodel':dm.get(),
							 'maker':mk.get()}
		self.vars['txid_var'].set(self.push_tx(app_info, order))

	def push_tx(self, app_info, order):
		self.broadcaster = NetworkTransportLayer(app_info['id'], app_info['key'])
		signed_tx = self.broadcaster.sign_order(self.broadcaster.make_singlesign_order(order['data'],
			order['metadata'], self.keys['pub']), self.keys['priv'])
		self.broadcaster.send_order(signed_tx)
		pyp.copy(signed_tx['id'])
		#print(self.time_tx(signed_tx['id'], order['metadata']['timestamp']))
		return signed_tx['id']

	def generate_keypair(self):
		gen = KeypairGenerator()
		pub, priv = gen.get_public_key(), gen.get_private_key()
		self.vars['pub_var'].set('Public: {}'.format(pub))
		self.vars['priv_var'].set('Private: {}'.format(priv))
		self.keys['pub'] = pub
		self.keys['priv'] = priv

	#def time_tx(self, tx_id, timestamp):
	#	found_time = 0
	#	while self.broadcaster.check_order(tx_id) == False:
	#			found_time = 0
	#	found_time = time.time()
	#	return (found_time-timestamp)


if __name__ == '__main__':
	main = OrderBookWriter()
	main.mainloop()