import customtkinter as ctk
import tkinter as tk
from CTkTable import *
from mpl_interactions import panhandler, zoom_factory
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.pyplot as plt
import Algorithms.LinearProbingHashing as lph
import Algorithms.SHashing as sh
import Algorithms.DHashing as dh
import Algorithms.BPTree as bpt
import ctypes
import platform
import os


class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.LPTable = lph.LinProbHashSet(size=11, load_factor=0.75)
        self.DHTable = dh.DoubleHashing(size=11, load_factor=0.75)
        self.SCHTable = sh.HashTable(size=11, load_factor=0.75)
        self.BPTree = bpt.BpTree(degree=3)
        
        ########################## Linear Probing Hashing ##########################
        
        self.LinProb = self.add("Linear Probing Hashing")
        self.LinProb.columnconfigure((0,1,2), weight=0)
        self.LinProb.columnconfigure(3, weight=1)
        self.LPH_label = ctk.CTkLabel(master=self.LinProb, text="Linear Probing Hashing     ", font=("Arial", 25, "bold"))
        self.LPH_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='NSEW')
        self.LPload_factor_label = ctk.CTkLabel(master=self.LinProb, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.LPload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.LPload_factor_slider = ctk.CTkSlider(master=self.LinProb, from_= 0.01, to=1, number_of_steps=100, width=130, height=10, command=self.slidingLPH)
        self.LPload_factor_slider.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='W')
        self.LPload_factor_slider.set(0.75)
        self.LPload_factor_slider_prog_label = ctk.CTkLabel(master=self.LinProb, text="0.75", font=("Arial", 12))
        self.LPload_factor_slider_prog_label.grid(row=1, column=2, padx=10, pady=10, sticky='E')
        self.LPsize_label = ctk.CTkLabel(master=self.LinProb, text="Size: ", font=("Arial", 20, "bold"))
        self.LPsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.LPsize_entry = ctk.CTkEntry(master=self.LinProb,placeholder_text="Table Size (Integer)")
        self.LPsize_entry.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky='EW')
        self.LPreset_button = ctk.CTkButton(master=self.LinProb, text="Create Table",height=30,command=lambda: self.reset('LPH'))
        self.LPreset_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPkey_entry = ctk.CTkEntry(master=self.LinProb,placeholder_text="Key (Integer)",height=30)
        self.LPkey_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPinsert_button = ctk.CTkButton(master=self.LinProb, text="Insert",height=30,command=lambda: self.insert_table('LPH'))
        self.LPinsert_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPremove_button = ctk.CTkButton(master=self.LinProb, text="Remove",height=30,command=lambda: self.remove_element('LPH'))
        self.LPremove_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPcontains_button = ctk.CTkButton(master=self.LinProb, text="Contains",height=30,command=lambda: self.contains('LPH'))
        self.LPcontains_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPremove_all_button = ctk.CTkButton(master=self.LinProb, text="Remove All",height=30,command=lambda: self.remove_all('LPH'))
        self.LPremove_all_button.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.LPtable_frame = ctk.CTkScrollableFrame(master=self.LinProb)
        self.LPtable_frame.columnconfigure(0, weight=1)
        self.LPtable_frame.grid(row=1, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.LPindex_table = CTkTable(master=self.LPtable_frame, row=1, column=2, values=[['Index','Value']])
        self.LPindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')

        ########################## Double Hashing ##########################
        
        self.DHash = self.add("Double Hashing")
        self.DHash.columnconfigure((0,1,2), weight=0)
        self.DHash.columnconfigure(3, weight=1) 
        self.DH_label = ctk.CTkLabel(master=self.DHash, text="Double Hashing             ", font=("Arial", 25, "bold"))
        self.DH_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='NSEW')
        self.DHload_factor_label = ctk.CTkLabel(master=self.DHash, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.DHload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.DHload_factor_slider = ctk.CTkSlider(master=self.DHash, from_= 0.01, to=1, number_of_steps=100, width=130, height=10, command=self.slidingDH)
        self.DHload_factor_slider.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='W')
        self.DHload_factor_slider.set(0.75)
        self.DHload_factor_slider_prog_label = ctk.CTkLabel(master=self.DHash, text="0.75", font=("Arial", 12))
        self.DHload_factor_slider_prog_label.grid(row=1, column=2, padx=10, pady=10, sticky='E')
        self.DHsize_label = ctk.CTkLabel(master=self.DHash, text="Size: ", font=("Arial", 20, "bold"))
        self.DHsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.DHsize_entry = ctk.CTkEntry(master=self.DHash,placeholder_text="Table Size (Integer)")
        self.DHsize_entry.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky='EW')
        self.DHreset_button = ctk.CTkButton(master=self.DHash, text="Create Table",height=30,command=lambda: self.reset('DH'))
        self.DHreset_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHkey_entry = ctk.CTkEntry(master=self.DHash,placeholder_text="Key (Integer)",height=30)
        self.DHkey_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHinsert_button = ctk.CTkButton(master=self.DHash, text="Insert",height=30,command=lambda: self.insert_table('DH'))
        self.DHinsert_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHremove_button = ctk.CTkButton(master=self.DHash, text="Remove",height=30,command=lambda: self.remove_element('DH'))
        self.DHremove_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHcontains_button = ctk.CTkButton(master=self.DHash, text="Contains",height=30,command=lambda: self.contains('DH'))
        self.DHcontains_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHremove_all_button = ctk.CTkButton(master=self.DHash, text="Remove All",height=30,command=lambda: self.remove_all('DH'))
        self.DHremove_all_button.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.DHtable_frame = ctk.CTkScrollableFrame(master=self.DHash)
        self.DHtable_frame.columnconfigure(0, weight=1)
        self.DHtable_frame.grid(row=1, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.DHindex_table = CTkTable(master=self.DHtable_frame, row=1, column=2, values=[['Index','Value']])
        self.DHindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')
        
        ########################## Separate Chaining Hashing ##########################
        
        self.SCHash = self.add("Separate Chaining Hashing")
        self.SCHash.columnconfigure((0,1,2), weight=0)
        self.SCHash.columnconfigure(3, weight=1) 
        self.SC_label = ctk.CTkLabel(master=self.SCHash, text="Separate Chaining Hashing ", font=("Arial", 25, "bold"))
        self.SC_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='NSEW')
        self.SCload_factor_label = ctk.CTkLabel(master=self.SCHash, text="Load Factor: ", font=("Arial", 20, "bold"))
        self.SCload_factor_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.SCload_factor_slider = ctk.CTkSlider(master=self.SCHash, from_= 0.01, to=1, number_of_steps=100, width=130, height=10, command=self.slidingSC)
        self.SCload_factor_slider.grid(row=1, column=1, columnspan=2, padx=40, pady=10, sticky='W')
        self.SCload_factor_slider.set(0.75)
        self.SCload_factor_slider_prog_label = ctk.CTkLabel(master=self.SCHash, text="0.75", font=("Arial", 12))
        self.SCload_factor_slider_prog_label.grid(row=1, column=2, padx=10, pady=10, sticky='E')
        self.SCsize_label = ctk.CTkLabel(master=self.SCHash, text="Size: ", font=("Arial", 20, "bold"))
        self.SCsize_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        self.SCsize_entry = ctk.CTkEntry(master=self.SCHash,placeholder_text="Table Size (Integer)")
        self.SCsize_entry.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky='EW')
        self.SCreset_button = ctk.CTkButton(master=self.SCHash, text="Create Table",height=30,command=lambda: self.reset('SC'))
        self.SCreset_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCkey_entry = ctk.CTkEntry(master=self.SCHash,placeholder_text="Key (Integer)",height=30)
        self.SCkey_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCinsert_button = ctk.CTkButton(master=self.SCHash, text="Insert",height=30,command=lambda: self.insert_table('SC'))
        self.SCinsert_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCremove_button = ctk.CTkButton(master=self.SCHash, text="Remove",height=30,command=lambda: self.remove_element('SC'))
        self.SCremove_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCcontains_button = ctk.CTkButton(master=self.SCHash, text="Contains",height=30,command=lambda: self.contains('SC'))
        self.SCcontains_button.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCremove_all_button = ctk.CTkButton(master=self.SCHash, text="Remove All",height=30,command=lambda: self.remove_all('SC'))
        self.SCremove_all_button.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.SCtable_frame = ctk.CTkScrollableFrame(master=self.SCHash)
        self.SCtable_frame.columnconfigure(0, weight=1)
        self.SCtable_frame.grid(row=1, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.SCindex_table = CTkTable(master=self.SCtable_frame, row=1, column=2, values=[['Index','Value']])
        self.SCindex_table.grid(row=0, column=0, padx=20, pady=10, sticky='NSWE')
        
        ########################## B+ Tree ##########################
        
        self.BPtree = self.add("B+ Tree")
        self.BPtree.columnconfigure((0,1,2), weight=0)
        self.BPtree.columnconfigure((3), weight=1) 
        self.BP_label = ctk.CTkLabel(master=self.BPtree, text="B+ Trees", font=("Arial", 25, "bold"))
        self.BP_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='NSEW')
        self.BP_degree_label = ctk.CTkLabel(master=self.BPtree, text="Degree: ", font=("Arial", 20, "bold"))
        self.BP_degree_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.BP_degree_slider = ctk.CTkSlider(master=self.BPtree, from_=3, to=7, number_of_steps=4, width=130, height=10, command=self.slidingBP)
        self.BP_degree_slider.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='W')
        self.BP_degree_slider.set(3)
        self.BP_degree_slider_prog_label = ctk.CTkLabel(master=self.BPtree, text="3", font=("Arial", 12))
        self.BP_degree_slider_prog_label.grid(row=1, column=2, padx=10, pady=10, sticky='E')
        self.BPreset_button = ctk.CTkButton(master=self.BPtree, text="Create Tree",height=30,command=lambda: self.reset('BP')) # self.reset('BP')
        self.BPreset_button.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPkey_entry = ctk.CTkEntry(master=self.BPtree,placeholder_text="Key (Integer)",height=30)
        self.BPkey_entry.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPinsert_button = ctk.CTkButton(master=self.BPtree, text="Insert",height=30,command=lambda: self.insert_table('BP'))
        self.BPinsert_button.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPremove_button = ctk.CTkButton(master=self.BPtree, text="Remove",height=30,command=lambda: self.remove_element('BP'))
        self.BPremove_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPcontains_button = ctk.CTkButton(master=self.BPtree, text="Contains",height=30,command=lambda: self.contains('BP'))
        self.BPcontains_button.grid(row=6, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPremove_all_button = ctk.CTkButton(master=self.BPtree, text="Remove All",height=30,command=lambda: self.remove_all('BP'))
        self.BPremove_all_button.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky='EW')
        self.BPgraph_frame = ctk.CTkFrame(master=self.BPtree, fg_color='white',corner_radius=10)
        self.BPgraph_frame.columnconfigure(0, weight=1)
        self.BPgraph_frame.grid(row=1, column=3, columnspan=3, rowspan=8, padx=30, pady=10, sticky='NSEW')
        self.figure = plt.figure(figsize=(5, 6),facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figure, self.BPgraph_frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.BPgraph_frame)
        
    def slidingLPH(self, value):
        self.LPload_factor_slider_prog_label.configure(text=round(value,2))
    def slidingDH(self, value):
        self.DHload_factor_slider_prog_label.configure(text=round(value,2))
    def slidingSC(self, value):
        self.SCload_factor_slider_prog_label.configure(text=round(value,2))
    def slidingBP(self, value):
        self.BP_degree_slider_prog_label.configure(text=int(value))


    def updateTable(self, table):
        current_table = None
        hashtype = None
        if table == "LPH":
            current_table = self.LPindex_table
            hashtype = self.LPTable.table
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1, current_table_size)))
            for i in range(len(hashtype)):
                current_table.add_row([i, str(hashtype[i])])
        if table == "DH":
            current_table = self.DHindex_table
            hashtype = self.DHTable.hashtable
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1, current_table_size)))
            for i in range(len(hashtype)):
                current_table.add_row([i, str(hashtype[i])])
        if table == "SC":
            current_table = self.SCindex_table
            hashtype = [
                self.SCHTable.get_list(i) for i in range(self.SCHTable.bucket_count)
            ]
            current_table_size = len(current_table.get())
            current_table.delete_rows(list(range(1, current_table_size)))
            for i in range(len(hashtype)):
                if str(self.SCHTable.get_list(i)) == "[]":
                    current_table.add_row([i, "None"])
                else:
                    current_table.add_row([i, hashtype[i]])
        if table == "BP":
            current_table = self.BPgraph_frame
            self.BPTree.plotTree()
            self.plotTree()

    def plotTree(self):
        for children in self.BPgraph_frame.winfo_children():
            children.destroy()
        
        tmpImg = Image.open(os.path.join(os.environ['TEMP'], 'bptree', 'bptree_graph.png'))
        imgArray = np.asarray(tmpImg)

        with plt.ioff():
            self.figure = plt.figure(figsize=(5, 6))
            self.a = self.figure.add_subplot(111)
            self.figure.tight_layout()

        self.a.imshow(imgArray)
        self.a.axis('off') 
        self.figure.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
        imgplot = plt.imshow(imgArray)
        self.a.set_aspect('equal', 'datalim')
        self.a.set_ylim(self.a.get_xlim()[::-1])
        disconnect_zoom = zoom_factory(self.a)
        pan_handler = panhandler(self.figure)
        
        self.treeCanvas = FigureCanvasTkAgg(self.figure, self.BPgraph_frame)
        self.treeCanvas.draw()
        self.treeCanvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # create the toolbar
        self.toolbar = NavigationToolbar2Tk(self.treeCanvas, self.BPgraph_frame)
        self.toolbar.update()
        plt.close()
        
    def insert_table(self, button):
        if button == "LPH":
            try:
                key = int(self.LPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.LPTable.insert(key)
            self.updateTable("LPH")

        if button == "DH":
            try:
                key = int(self.DHkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.DHTable.insert(key)
            self.updateTable("DH")

        if button == "SC":
            try:
                key = int(self.SCkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.SCHTable.insert(key)
            self.updateTable("SC")
        if button == "BP":
            try:
                key = int(self.BPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            self.BPTree.insert(key)
            self.updateTable("BP")

    def remove_element(self, button):
        exists = None
        if button == "LPH":
            try:
                key = int(self.LPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.LPTable.remove(key)
            if not exists:
                tk.messagebox.showerror("Error", "Key does not exist")
                return
            self.updateTable("LPH")

        if button == "DH":
            try:
                key = int(self.DHkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.DHTable.remove(key)
            if not exists:
                tk.messagebox.showerror("Error", "Key does not exist")
                return
            self.updateTable("DH")

        if button == "SC":
            try:
                key = int(self.SCkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.SCHTable.delete(key)
            if not exists:
                tk.messagebox.showerror("Error", "Key does not exist")
                return
            self.updateTable("SC")
            
        if button == "BP":
            try:
                key = int(self.BPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.BPTree.remove(key)
            if not exists:
                tk.messagebox.showerror("Error", "Key does not exist")
                return
            self.updateTable("BP")
            
    def remove_all(self, button):
        if button == "LPH":
            self.LPTable.remove_entries()
            self.updateTable("LPH")
        if button == "DH":
            self.DHTable.remove_entries()
            self.updateTable("DH")
        if button == 'SC':
            self.SCHTable = sh.HashTable(size=self.SCHTable.bucket_count,load_factor=self.SCHTable.load_factor)
            self.updateTable('SC')
        if button == 'BP':
            self.BPTree = bpt.BpTree(degree=self.BPTree.degree)
            self.updateTable("BP")
            
    def reset(self, button):
        if button == "LPH":
            if self.LPsize_entry.get() == "":
                    size = 11
            else:
                try:
                    
                    size = int(self.LPsize_entry.get())
                except:
                    tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                    return
            self.LPTable = lph.LinProbHashSet(size=size, load_factor=self.LPload_factor_slider.get())
            self.updateTable("LPH")
        if button == "DH":
            if self.DHsize_entry.get() == "":
                    size = 11
            else:
                try:
                    size = int(self.DHsize_entry.get())
                except:
                    tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                    return
            self.DHTable = dh.DoubleHashing(size=size, load_factor=self.DHload_factor_slider.get())
            self.updateTable("DH")
        if button == "SC":
            if self.SCsize_entry.get() == "":
                    size = 11
            else:
                try:
                    size = int(self.SCsize_entry.get())
                except:
                    tk.messagebox.showerror("Error", "Please enter a valid integer for size")
                    return
            self.SCHTable = sh.HashTable(size=size, load_factor=self.SCload_factor_slider.get())
            self.updateTable("SC")
        if button == "BP":
            self.BPTree = bpt.BpTree(degree=int(self.BP_degree_slider.get()))
            self.updateTable("BP")
            
    def contains(self, button):
        if button == "LPH":
            try:
                key = int(self.LPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.LPTable.contains(key)
            if exists:
                tk.messagebox.showinfo("Contains", f"{key} exists in the table")
            else:
                tk.messagebox.showinfo("Contains", f"{key} does not exist in the table")
        if button == "DH":
            try:
                key = int(self.DHkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.DHTable.search(key)
            if exists:
                tk.messagebox.showinfo("Contains", f"{key} exists in the table")
            else:
                tk.messagebox.showinfo("Contains", f"{key} does not exist in the table")
        if button == "SC":
            try:
                key = int(self.SCkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.SCHTable.find(key, self.SCHTable.get_list(self.SCHTable.hash_function(key)))
            if exists:
                tk.messagebox.showinfo("Contains", f"{key} exists in the table")
            else:
                tk.messagebox.showinfo("Contains", f"{key} does not exist in the table")
        if button == "BP":
            try:
                key = int(self.BPkey_entry.get())
            except:
                tk.messagebox.showerror("Error", "Please enter a valid integer for key")
                return
            exists = self.BPTree.contains(key)
            if exists:
                tk.messagebox.showinfo("Contains", f"{key} exists in the tree")
            else:
                tk.messagebox.showinfo("Contains", f"{key} does not exist in the tree")
            
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("Indexing Master")
        self.geometry(f"{1300}x{720}")
        self.iconbitmap(os.path.join("Icon","Indexing-Master.ico"))
        self.myappid = 'heh' # arbitrary string
        if platform.system() == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        self.tab_view = MyTabView(master=self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky='NSEW')
        
if __name__ == "__main__":        
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()