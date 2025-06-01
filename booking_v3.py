#your_project/booking_v3.py
#│   hotel_booking.py      ← (Main script)
#├── invoice_template.jpg  ← (Invoice background image you uploaded)

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("hotel_booking.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trnjid TEXT,
        date TEXT,
        hotel_name TEXT,
        guest TEXT,
        address TEXT,
        head INTEGER,
        room_no TEXT,
        check_in TEXT,
        check_out TEXT,
        days INTEGER,
        mobile TEXT,
        rate REAL,
        total REAL,
        advance REAL,
        due REAL
    )""")
    conn.commit()
    conn.close()

def generate_trnjid():
    return f"TRN{datetime.now().strftime('%Y%m%d%H%M%S')}"

# --- Calculate Fields ---
def auto_calculate(*args):
    try:
        d1 = datetime.strptime(check_in.get(), "%Y-%m-%d")
        d2 = datetime.strptime(check_out.get(), "%Y-%m-%d")
        day_count = (d2 - d1).days
        days.set(str(day_count if day_count > 0 else 1))

        h = int(head.get())
        r = float(rate.get())
        t = h * r * int(days.get())
        total.set(str(t))
        a = float(advance.get())
        due.set(str(t - a))
    except:
        pass


# --- Search Invoice----

def search_booking(trn_id):
    conn = sqlite3.connect("hotel_booking.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE trnjid = ?", (trn_id,))
    row = c.fetchone()
    conn.close()

    if row:
        # Populate the form fields with the retrieved data
        trnjid.set(row[1])
        date.set(row[2])
        hotel_name.set(row[3])
        guest.set(row[4])
        address.set(row[5])
        head.set(str(row[6]))
        room_no.set(row[7])
        check_in.set(row[8])
        check_out.set(row[9])
        days.set(str(row[10]))
        mobile.set(row[11])
        rate.set(str(row[12]))
        total.set(str(row[13]))
        advance.set(str(row[14]))
        due.set(str(row[15]))
    else:
        messagebox.showerror("Not Found", "No record found with that Trnj ID.")



# --- Save Booking ---
def save_booking():
    if not guest.get():
        messagebox.showwarning("Input Error", "Guest name is required.")
        return

    conn = sqlite3.connect("hotel_booking.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        trnjid.get(),
        date.get(),
        hotel_name.get(),
        guest.get(),
        address.get(),
        int(head.get()),
        room_no.get(),
        check_in.get(),
        check_out.get(),
        int(days.get()),
        mobile.get(),
        float(rate.get()),
        float(total.get()),
        float(advance.get()),
        float(due.get())
    ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Saved", "Booking saved successfully!")

# --- Generate Invoice ---
def generate_invoice():
    try:
        bg = Image.open("invoice.jpg").convert("RGB")
        draw = ImageDraw.Draw(bg)
        font_path = "arial.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        #font = ImageFont.truetype(font_path, 22)
        font = ImageFont.load_default(22)

        
        draw.text((150, 90), date.get(), font=font, fill="yellow")
        draw.text((150, 148), trnjid.get(), font=font, fill="yellow")
        draw.text((650, 28), trnjid.get(), font=font, fill="red")
        draw.text((230, 190), hotel_name.get(), font=font, fill="yellow")
        draw.text((270, 245), guest.get(), font=font, fill="yellow")
        draw.text((350, 295), address.get(), font=font, fill="yellow")
        draw.text((190, 343), head.get(), font=font, fill="yellow")
        draw.text((590, 339), room_no.get(), font=font, fill="yellow")
        draw.text((100, 390), check_in.get(), font=font, fill="yellow")
        draw.text((460,390), check_out.get(), font=font, fill="yellow")
        draw.text((870, 390), days.get(), font=font, fill="yellow")
        draw.text((800, 435), rate.get(), font=font, fill="yellow")
        draw.text((800, 475), total.get(), font=font, fill="yellow") 
        draw.text((810, 505), advance.get(), font=font, fill="yellow")
        draw.text((800, 540), due.get(), font=font, fill="yellow")


        output_path = f"invoice_{trnjid.get()}.jpg"
        bg.save(output_path)
        messagebox.showinfo("Invoice", f"Invoice saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Invoice Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("Hotel Booking System")

# --- Variables ---

date = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
trnjid = tk.StringVar(value=generate_trnjid())
hotel_name = tk.StringVar()
guest = tk.StringVar()
address = tk.StringVar()
head = tk.StringVar(value="1")
room_no = tk.StringVar()
check_in = tk.StringVar()
check_out = tk.StringVar()
days = tk.StringVar(value="1")
mobile = tk.StringVar()
rate = tk.StringVar(value="1000")
total = tk.StringVar()
advance = tk.StringVar(value="0")
due = tk.StringVar()

# Auto-calc bindings
for var in [check_in, check_out, head, rate, advance]:
    var.trace("w", auto_calculate)

# --- Layout ---
fields = [
    ("Booking Date", date),
    ("Trnj ID", trnjid),
    ("Name of Hotel", hotel_name),
    ("Name of Guest", guest),
    ("Address", address),
    ("Head(s)", head),
    ("Room No", room_no),
    ("Check In (YYYY-MM-DD)", check_in),
    ("Check Out (YYYY-MM-DD)", check_out),
    ("Days", days),
    ("Mobile", mobile),
    ("Rate", rate),
    ("Total", total),
    ("Advance", advance),
    ("Due", due),
]

for i, (label, var) in enumerate(fields):
    tk.Label(root, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=2)
    tk.Entry(root, textvariable=var, width=30).grid(row=i, column=1, padx=5, pady=2)

tk.Button(root, text="Save Booking", command=save_booking).grid(row=len(fields), column=0, pady=10)
tk.Button(root, text="Print Invoice", command=generate_invoice).grid(row=len(fields), column=1, pady=10)


############ 

search_id = tk.StringVar()

tk.Label(root, text="Search by Trnj ID").grid(row=0, column=2, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=search_id, width=25).grid(row=0, column=3, padx=5)
tk.Button(root, text="Search", command=lambda: search_booking(search_id.get())).grid(row=0, column=4, padx=5)




#############


init_db()
root.mainloop()

