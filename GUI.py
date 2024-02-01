import customtkinter as ctk
import tkinter as tk
from CTkTable import *
import LinearProbingHashing as lph
import SHashing as sh
import DHashing as dh
import BPTree as bpt

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("ML Toolkit")
        self.geometry(f"{1300}x{720}")
        self.tab_view = MyTabView(master=self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky='NSEW')
        
class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.LPTable = lph.LinProbHashSet(size=11, load_factor=0.75)
        self.DHTable = dh.DoubleHashing(size=11, load_factor=0.75)
        self.SCHTable = sh.HashTable(size=11, load_factor=0.75)
        self.BPTree = bpt.BpTree(degree=2)
        
        
        ########################## Linear Probing Hashing ##########################
        
        self.LinProb = self.add("Linear Probing Hashing")
        self.LinProb.columnconfigure((0,1,2), weight=0)
        self.LinProb.columnconfigure(3, weight=1)
        self.LPH_label = ctk.CTkLabel(master=self.LinProb, text="Linear Probing Hashing", font=("Arial", 25, "bold"))
        self.LPH_label.grid(row=0, column=1, padx=20, pady=10, sticky='NSEW')
        self.LPload_factor_label = ctk.CTkLabel(master=self.LinProb, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.LPload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.LPload_factor_slider = ctk.CTkSlider(master=self.LinProb, from_= 0.01, to=1, number_of_steps=100, width=150, height=10, command=self.slidingLPH)
        self.LPload_factor_slider.grid(row=1, column=1, padx=20, pady=10, sticky='E')
        self.LPload_factor_slider.set(0.75)
        self.LPload_factor_slider_prog_label = ctk.CTkLabel(master=self.LinProb, text="0.75", font=("Arial", 12))
        self.LPload_factor_slider_prog_label.grid(row=1, column=1, padx=20, pady=10, sticky='W')
        self.LPload_factor_button = ctk.CTkButton(master=self.LinProb, text="Set",command=lambda: self.set_param('LPH-load_factor'))
        self.LPload_factor_button.grid(row=1, column=2, padx=20, pady=10, sticky='W')
        self.LPsize_label = ctk.CTkLabel(master=self.LinProb, text="Size: ", font=("Arial", 20, "bold"))
        self.LPsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.LPsize_entry = ctk.CTkEntry(master=self.LinProb,placeholder_text="Table Size (Integer)")
        self.LPsize_entry.grid(row=2, column=1, padx=20, pady=10, sticky='W')
        self.LPsize_button = ctk.CTkButton(master=self.LinProb, text="Set",command=lambda: self.set_param('LPH-size'))
        self.LPsize_button.grid(row=2, column=2, padx=20, pady=10, sticky='W')
        self.LPkey_entry = ctk.CTkEntry(master=self.LinProb,placeholder_text="Key (Integer)",height=30)
        self.LPkey_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPinsert_button = ctk.CTkButton(master=self.LinProb, text="Insert",height=30,command=lambda: self.insert_table('LPH'))
        self.LPinsert_button.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPremove_button = ctk.CTkButton(master=self.LinProb, text="Remove",height=30)
        self.LPremove_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPcontains_button = ctk.CTkButton(master=self.LinProb, text="Contains",height=30)
        self.LPcontains_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPremove_all_button = ctk.CTkButton(master=self.LinProb, text="Remove All",height=30)
        self.LPremove_all_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPtable_frame = ctk.CTkScrollableFrame(master=self.LinProb)
        self.LPtable_frame.columnconfigure(0, weight=1)
        self.LPtable_frame.grid(row=0, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.LPindex_table = CTkTable(master=self.LPtable_frame, row=1, column=2, values=[['Index','Value']])
        self.LPindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')

        ########################## Double Hashing ##########################
        
        self.DHash = self.add("Double Hashing")
        self.DHash.columnconfigure((0,1,2), weight=0)
        self.DHash.columnconfigure(3, weight=1) 
        self.DH_label = ctk.CTkLabel(master=self.DHash, text="Double Hashing", font=("Arial", 25, "bold"))
        self.DH_label.grid(row=0, column=1, padx=20, pady=10, sticky='NSEW')
        self.DHload_factor_label = ctk.CTkLabel(master=self.DHash, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.DHload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.DHload_factor_slider = ctk.CTkSlider(master=self.DHash, from_= 0.01, to=1, number_of_steps=100, width=150, height=10, command=self.slidingDH)
        self.DHload_factor_slider.grid(row=1, column=1, padx=20, pady=10, sticky='E')
        self.DHload_factor_slider.set(0.75)
        self.DHload_factor_slider_prog_label = ctk.CTkLabel(master=self.DHash, text="0.75", font=("Arial", 12))
        self.DHload_factor_slider_prog_label.grid(row=1, column=1, padx=20, pady=10, sticky='W')
        self.DHload_factor_button = ctk.CTkButton(master=self.DHash, text="Set",command=lambda: self.set_param('DH-load_factor'))
        self.DHload_factor_button.grid(row=1, column=2, padx=20, pady=10, sticky='W')
        self.DHsize_label = ctk.CTkLabel(master=self.DHash, text="Size: ", font=("Arial", 20, "bold"))
        self.DHsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.DHsize_entry = ctk.CTkEntry(master=self.DHash,placeholder_text="Table Size (Integer)")
        self.DHsize_entry.grid(row=2, column=1, padx=20, pady=10, sticky='W')
        self.DHsize_button = ctk.CTkButton(master=self.DHash, text="Set",command=lambda: self.set_param('DH-size'))
        self.DHsize_button.grid(row=2, column=2, padx=20, pady=10, sticky='W')
        self.DHkey_entry = ctk.CTkEntry(master=self.DHash,placeholder_text="Key (Integer)",height=30)
        self.DHkey_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHinsert_button = ctk.CTkButton(master=self.DHash, text="Insert",height=30,command=lambda: self.insert_table('DH'))
        self.DHinsert_button.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHremove_button = ctk.CTkButton(master=self.DHash, text="Remove",height=30)
        self.DHremove_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHcontains_button = ctk.CTkButton(master=self.DHash, text="Contains",height=30)
        self.DHcontains_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHremove_all_button = ctk.CTkButton(master=self.DHash, text="Remove All",height=30)
        self.DHremove_all_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHtable_frame = ctk.CTkScrollableFrame(master=self.DHash)
        self.DHtable_frame.columnconfigure(0, weight=1)
        self.DHtable_frame.grid(row=0, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.DHindex_table = CTkTable(master=self.DHtable_frame, row=1, column=2, values=[['Index','Value']])
        self.DHindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')
        
        ########################## Separate Chaining Hashing ##########################
        
        self.SCHash = self.add("Separate Chaining Hashing")
        self.SCHash.columnconfigure((0,1,2), weight=0)
        self.SCHash.columnconfigure(3, weight=1) 
        self.SC_label = ctk.CTkLabel(master=self.SCHash, text="Separate Chaining Hashing", font=("Arial", 25, "bold"))
        self.SC_label.grid(row=0, column=1, padx=20, pady=10, sticky='NSEW')
        self.SCload_factor_label = ctk.CTkLabel(master=self.SCHash, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.SCload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.SCload_factor_slider = ctk.CTkSlider(master=self.SCHash, from_= 0.01, to=1, number_of_steps=100, width=150, height=10, command=self.slidingSC)
        self.SCload_factor_slider.grid(row=1, column=1, padx=20, pady=10, sticky='E')
        self.SCload_factor_slider.set(0.75)
        self.SCload_factor_slider_prog_label = ctk.CTkLabel(master=self.SCHash, text="0.75", font=("Arial", 12))
        self.SCload_factor_slider_prog_label.grid(row=1, column=1, padx=20, pady=10, sticky='W')
        self.SCload_factor_button = ctk.CTkButton(master=self.SCHash, text="Set",command=lambda: self.set_param('SC-load_factor'))
        self.SCload_factor_button.grid(row=1, column=2, padx=20, pady=10, sticky='W')
        self.SCsize_label = ctk.CTkLabel(master=self.SCHash, text="Size: ", font=("Arial", 20, "bold"))
        self.SCsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.SCsize_entry = ctk.CTkEntry(master=self.SCHash,placeholder_text="Table Size (Integer)")
        self.SCsize_entry.grid(row=2, column=1, padx=20, pady=10, sticky='W')
        self.SCsize_button = ctk.CTkButton(master=self.SCHash, text="Set",command=lambda: self.set_param('SC-size'))
        self.SCsize_button.grid(row=2, column=2, padx=20, pady=10, sticky='W')
        self.SCkey_entry = ctk.CTkEntry(master=self.SCHash,placeholder_text="Key (Integer)",height=30)
        self.SCkey_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCinsert_button = ctk.CTkButton(master=self.SCHash, text="Insert",height=30,command=lambda: self.insert_table('SC'))
        self.SCinsert_button.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCremove_button = ctk.CTkButton(master=self.SCHash, text="Remove",height=30)
        self.SCremove_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCcontains_button = ctk.CTkButton(master=self.SCHash, text="Contains",height=30)
        self.SCcontains_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCremove_all_button = ctk.CTkButton(master=self.SCHash, text="Remove All",height=30)
        self.SCremove_all_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCtable_frame = ctk.CTkScrollableFrame(master=self.SCHash)
        self.SCtable_frame.columnconfigure(0, weight=1)
        self.SCtable_frame.grid(row=0, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.SCindex_table = CTkTable(master=self.SCtable_frame, row=1, column=2, values=[['Index','Value']])
        self.SCindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')
        
        ########################## B+ Tree ##########################
        
        self.BPtree = self.add("B+ Tree")
        
        
    def slidingLPH(self, value):
        self.LPload_factor_slider_prog_label.configure(text=round(value,2))
    def slidingDH(self, value):
        self.DHload_factor_slider_prog_label.configure(text=round(value,2))
    def slidingSC(self, value):
        self.SCload_factor_slider_prog_label.configure(text=round(value,2))
        
    def set_param(self, button):
        
        if button == 'LPH-load_factor':
            self.LPTable.loadFactorThreshold = self.LPload_factor_slider.get()
            
        if button == 'LPH-size':
            try:
                size = int(self.LPsize_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                return
            self.LPTable.size = size
            
        if button == 'DH-load_factor':
            self.DHTable.load_factor = self.DHload_factor_slider.get()
            
        if button == 'DH-size':
            try:
                size = int(self.DHsize_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                return
            self.DHTable.hashtablesize = size
        
        if button == 'SC-load_factor':
            self.SCHTable.load_factor = self.SCload_factor_slider.get()
        
        if button == 'SC-size':
            try:
                size = int(self.SCsize_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                return
            self.SCHTable.bucket_count = size
    
    def updateTable(self, table):
        current_table = None
        hashtype = None
        if table == 'LPH':
            self.LPload_factor_button.configure(state='disabled')
            self.LPsize_button.configure(state='disabled')
            current_table = self.LPindex_table
            hashtype = self.LPTable.table
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1,current_table_size)))
            for i in range(len(hashtype)):
                current_table.add_row([i, str(hashtype[i])])
        if table == 'DH':
            self.DHload_factor_button.configure(state='disabled')
            self.DHsize_button.configure(state='disabled')
            current_table = self.DHindex_table
            hashtype = self.DHTable.hashtable
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1,current_table_size)))
            for i in range(len(hashtype)):
                current_table.add_row([i, hashtype[i]])
        if table == 'SC':
            self.SCload_factor_button.configure(state='disabled')
            self.SCsize_button.configure(state='disabled')
            current_table = self.SCindex_table
            hashtype = [self.SCHTable.get_list(i) for i in range(self.SCHTable.bucket_count)]
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1,current_table_size)))
            for i in range(len(hashtype)):
                if str(self.SCHTable.get_list(i)) == '[]':
                    current_table.add_row([i, 'None'])
                else:
                    current_table.add_row([i, hashtype[i]])

    
    def insert_table(self, button):
        if button == 'LPH':
            try:
                key = int(self.LPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.LPTable.insert(key)
            self.updateTable('LPH')
            
        if button == 'DH':
            try:
                key = int(self.DHkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.DHTable.insert(key)
            self.updateTable('DH')
            
        if button == 'SC':
            try:
                key = int(self.SCkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.SCHTable.insert(key)
            self.updateTable('SC')

if __name__ == "__main__":        
    app = App()
    app.mainloop()