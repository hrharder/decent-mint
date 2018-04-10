'''
	#####################
	NBL Test GUI
	#####################

	Written by Henry Harder

	@version 0.0.1
	@version_date: 1 April 2018
'''
from nbl import* # NetworkBroadcastLayer 
from tkinter import* # tkinter GUI python module

class OrderBookTester(Frame):
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

		output_frame.grid_rowconfigure(0) # title
		output_frame.grid_rowconfigure(1) # txid input
		output_frame.grid_rowconfigure(2) # data output

		self.vars['pub_var'].set("Click 'Generate' to make new public key")
		self.vars['priv_var'].set("Click 'Generate' to make new private key")
		self.vars['txid_var'].set('Submit an order to generate TX_ID')

		# Begin input frame
		top_label = Label(input_frame, text='Create a Transaction:') # row 0

		app_key_label = Label(input_frame, text = 'App Key: ') # row 1, col 0
		app_key_input = Entry(input_frame) 					   # row 1, col 1

		app_id_label = Label(input_frame, text = 'App ID: ') # row 2, col 0
		app_id_input = Entry(input_frame)					 # row 2, col 1

		order_data_label = Label(input_frame, text = 'Field1: ') # row 3, col 0
		order_data_input = Entry(input_frame)						 # row 3, col 1

		meta_data_label = Label(input_frame, text = 'Field2 ')  # row 4, col 0
		meta_data_input = Entry(input_frame) 					   # row 4, col 1

		keypair_generator = Button(input_frame, text = 'Generate Keypair',  # row 5
			command = lambda: self.generate_keypair())

		show_key1 = Label(input_frame, textvariable = self.vars['pub_var']) # row 6

		show_key2 = Label(input_frame, textvariable = self.vars['priv_var']) # row 7

		submit_button = Button(input_frame, text = 'Submit Order', 
			command = lambda: self.submit_order(app_key_input, app_id_input,
			order_data_input, meta_data_input)) # row 10, col 0

		txid_label = Label(input_frame, textvariable = self.vars['txid_var']) # row 10, col 1
		# End input frame

		top_label.grid(row=0,sticky=W)
		app_key_label.grid(row=1, column=0,sticky=W)
		app_key_input.grid(row=1, column=1,sticky=W)
		app_id_label.grid(row=2, column=0,sticky=W)
		app_id_input.grid(row=2, column=1,sticky=W)
		order_data_label.grid(row=3, column=0,sticky=W)
		order_data_input.grid(row=3, column=1,sticky=W)
		meta_data_label.grid(row=4, column=0,sticky=W)
		meta_data_input.grid(row=4, column=1,sticky=W)
		keypair_generator.grid(row=5, column=0,sticky=W)
		show_key1.grid(row=6, column=0,sticky=W)
		show_key2.grid(row=7, column=0,sticky=W)
		submit_button.grid(row=9, column=0,sticky=W)
		txid_label.grid(row=9, column=1,sticky=W)

		input_frame.grid(row=0, column=0)

		self.app_frame.pack()
		self.app_frame.mainloop()

	def submit_order(self, appkey, appid, dat, mdat):
		app_info, order = {}, {}
		app_info['key'] = appkey.get()
		app_info['id'] = appid.get()
		order['data'] = {'data':{'field1':dat.get(), 'field2':mdat.get()}}
		order['metadata'] = {'metadata':{'field1':'metadata'}}
		self.vars['txid_var'].set(self.push_tx(app_info, order))

	def push_tx(self, app_info, order):
		self.broadcaster = NetworkBroadcastLayer(app_info['id'], app_info['key'])
		signed_tx = self.broadcaster.sign_tx(self.broadcaster.make_tx(order['data'],
			order['metadata'], self.keys['pub']), self.keys['priv'])
		self.broadcaster.push_tx(signed_tx)
		return signed_tx['id']

	def generate_keypair(self):
		gen = KeypairGenerator()
		pub, priv = gen.get_public_key(), gen.get_private_key()
		self.vars['pub_var'].set('Public: {}'.format(pub))
		self.vars['priv_var'].set('Private: {}'.format(priv))
		self.keys['pub'] = pub
		self.keys['priv'] = priv

	def load_order(self, tx_id):
		self.vars['out_var1'].set(self.reader.get_order_data(tx_id)['field1'])
		self.vars['out_var2'].set(self.reader.get_order_data(tx_id)['field2'])


if __name__ == '__main__':
	main = OrderBookTester()
	main.mainloop()