#!/usr/bin/python

from  Tkinter import *

inp_fields = {"P" : [0, "Principal"], "R" : [1, "Rate of Interest"], "T": [2, "Number of years"], "S" : [3, "Step Per Year"]}


interest = []
    
def fetch_values():
    global entry
    P = float(entry[inp_fields["P"][0]].get())
    R = float(entry[inp_fields["R"][0]].get())
    T = float(entry[inp_fields["T"][0]].get())
    S = float(entry[inp_fields["S"][0]].get())

    print P, R, T, S
    return P, R, T, S

def fill(v):  
    global interest 
    print v
    interest[0].config(text = str(v))
    
def calculate_compound():    
    P, R, T, S = fetch_values()
    v = (P * (1 + R/100.0)**(T*S)) - P
    fill(v)
    
def calculate_simple():
    P, R, T, S = fetch_values()
    v = (P*T*R/100.0)
    fill(v)

def clear():
    for i in range(len(inp_fields)):
        entry[i].delete(0, END)
        entry[i].insert(0, str("0"))
    return
    fill(0)

if __name__ == "__main__":
    root  = Tk()
    frame = Frame(root, borderwidth = 50)


    entry = []
    for i, keys in enumerate(inp_fields): #range(len(inp_fields)):
        entry.append(Entry(frame))
        entry[i].grid(row = i, column = 1)
        Label(frame, text = inp_fields[keys][1], padx = 10, pady = 10).grid(row = i, sticky = N + S + W)


    clear()

    i += 1
    Label(frame, text = "Interest", justify = LEFT, relief = SUNKEN, pady = 10, padx = 20).grid(row = i, column = 0)    
    interest.append(Label(frame, text = "", justify = RIGHT, relief = SUNKEN, width = 30, pady = 10, padx = 20))
    interest[0].grid(row = i, column = 1)

    i += 1
    Button(frame, text = "Calculate Compound", command = calculate_compound, width = 20).grid(row = i, column = 0)
    Button(frame, text = "Calculate Simple", command = calculate_simple, width = 20).grid(row = i, column = 1)
    Button(frame, text = "Clear", command = clear, width = 20).grid(row = i,column = 2)

    #status.pack()

    frame.pack(side = "top", fill = "both", expand = True)
    root.mainloop()