'''
	#####################
	NBL Test Reader GUI
	#####################

	Written by Henry Harder

	@version 0.0.2
	@version_date: 2 April 2018
'''
from ntl import* # NetworkBroadcastLayer 
from tkinter import* # tkinter GUI python module
import time

class OrderBookReader(Frame):
	def __init__(self):
		self.parent = Tk()
		Frame.__init__(self, self.parent)

		self.app_frame = None

		self.modes = {
			1:'async',
			2:'sync',
			3:'commit'
			}

		self.endpoint = 'https://test.bigchaindb.com/api/v1/transactions?mode={}/' # must be formatted
		self.read_tx = {'read_tx':{}}
		self.vars = {'timestamp':StringVar(), 'dealmodel':StringVar(),
					 'maker':StringVar(), 'field1':StringVar(), 'field2':
					 StringVar(), 'field3':StringVar()}

		self.init_vars()
		self.make_window()

	def init_vars(self):
		for i in self.vars.keys():
			self.vars[i].set('No transaction loaded.')

	def make_window(self):
		self.app_frame = Frame(self.parent)
		output_frame = Frame(self.app_frame)
		text_frame = Frame(output_frame)
		data_frame = Frame(output_frame)
		
		output_frame.grid_rowconfigure(0)
		output_frame.grid_rowconfigure(1)
		output_frame.grid_rowconfigure(2)
		output_frame.grid_rowconfigure(3)

		output_frame.grid_columnconfigure(0, weight=1)
		output_frame.grid_columnconfigure(1, weight=1)

		text_frame.grid_rowconfigure(0) # timestamp
		text_frame.grid_rowconfigure(1) # DealModel addr
		text_frame.grid_rowconfigure(2) # maker addr
		text_frame.grid_rowconfigure(4) # field1
		text_frame.grid_rowconfigure(5) # field2
		text_frame.grid_rowconfigure(6) # field3

		data_frame.grid_rowconfigure(0) # timestamp
		data_frame.grid_rowconfigure(1) # DealModel addr
		data_frame.grid_rowconfigure(2) # maker addr
		data_frame.grid_rowconfigure(3) # field1
		data_frame.grid_rowconfigure(4) # field2
		data_frame.grid_rowconfigure(5) # field3
		data_frame.grid_rowconfigure(6)
		data_frame.grid_rowconfigure(7)

		time_lb = Label(text_frame, text='Timestamp:') # row 0
		dm_lb = Label(text_frame, text='DealModel:') # row 1
		mk_lb = Label(text_frame, text='Maker Adr:') # row 2
		d1_lb = Label(text_frame, text='data_field1:') # row 3
		d2_lb = Label(text_frame, text='data_field2:') # row 4
		d3_lb = Label(text_frame, text='data_field3:') # row 5

		time = Label(data_frame, textvariable=self.vars['timestamp'])
		dm = Label(data_frame, textvariable=self.vars['dealmodel'])
		mk = Label(data_frame, textvariable=self.vars['maker'])

		d1 = Label(data_frame, textvariable=self.vars['field1'])
		d2 = Label(data_frame, textvariable=self.vars['field2'])
		d3 = Label(data_frame, textvariable=self.vars['field3'])

		txid_label = Label(output_frame, text = 'TXID: ') 
		txid_input = Entry(output_frame)

		go_btn = Button(output_frame, text='Load Data', command=lambda: 
			self.get_order(txid_input.get(),self.vars))

		time_lb.grid(row=0, column=0, sticky=E)
		dm_lb.grid(row=1, column=0, sticky=E)
		mk_lb.grid(row=2, column=0, sticky=E)
		d1_lb.grid(row=3, column=0, sticky=E)
		d2_lb.grid(row=4, column=0, sticky=E)
		d3_lb.grid(row=5, column=0, sticky=E)

		time.grid(row=0, column=0, sticky=W)
		dm.grid(row=1, column=0, sticky=W)
		mk.grid(row=2, column=0, sticky=W)
		d1.grid(row=3, column=0, sticky=W)
		d2.grid(row=4, column=0, sticky=W)
		d3.grid(row=5, column=0, sticky=W)

		text_frame.grid(row=1, column=0)
		data_frame.grid(row=1, column=1)
		txid_label.grid(row=2, column=0)
		txid_input.grid(row=2, column=1)
		go_btn.grid(row=3, column=0) 

		output_frame.pack()

		self.app_frame.pack()
		self.app_frame.mainloop()

	def get_sync_order(self, mode, tx_id, var):
		order_dict = requests.get(self.endpoint.format(mode) + tx_id).json()
		self.vars['timestamp'].set(order_dict['metadata']['timestamp'])
		self.vars['dealmodel'].set(order_dict['metadata']['dealmodel'])
		self.vars['maker'].set(order_dict['metadata']['maker'])
		self.vars['field1'].set(order_dict['asset']['data']['field1'])
		self.vars['field2'].set(order_dict['asset']['data']['field2'])
		self.vars['field3'].set(order_dict['asset']['data']['field3'])

if __name__ == '__main__':
	main = OrderBookReader()
	main.mainloop()