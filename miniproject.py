import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class GuestInfoWindow(tk.Toplevel):
    def __init__(self, parent, room_number, hotel_app):
        super().__init__(parent)
        self.title("Guest Information")
        self.geometry("300x200")

        self.hotel_app = hotel_app
        self.room_number = room_number
        
        # Load and display background image
        bg_image = Image.open('bg.jpg')
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.name_label = tk.Label(self, text="Name:", font=("Arial", 12), fg="black", bg="#FFFF99")

        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.address_label = tk.Label(self, text="Address:", font=("Arial", 12), fg="black", bg="#FFFF99")
        self.address_label.grid(row=1, column=0, padx=10, pady=10)
        self.address_entry = tk.Entry(self, font=("Arial", 12))
        self.address_entry.grid(row=1, column=1, padx=10, pady=10)

        self.aadhar_label = tk.Label(self, text="Aadhar Number:", font=("Arial", 12), fg="black", bg="#FFFF99")
        self.aadhar_label.grid(row=2, column=0, padx=10, pady=10)
        self.aadhar_entry = tk.Entry(self, font=("Arial", 12))
        self.aadhar_entry.grid(row=2, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self, text="Phone Number:", font=("Arial", 12), fg="black", bg="#FFFF99")
        self.phone_label.grid(row=3, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, padx=10, pady=10)

        self.extra_label = tk.Label(self, text="Extra Number:", font=("Arial", 12), fg="black", bg="#FFFF99")
        self.extra_label.grid(row=4, column=0, padx=10, pady=10)
        self.extra_entry = tk.Entry(self, font=("Arial", 12))
        self.extra_entry.grid(row=4, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_guest_info, font=("Helvetica", 14), bg="#8B4513", fg="white")
        self.submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        

    def submit_guest_info(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        aadhar_number = self.aadhar_entry.get()
        phone_number = self.phone_entry.get()
        extra_number = self.extra_entry.get()

        if name and address and aadhar_number and phone_number:
            guest_info = {
                "name": name,
                "address": address,
                "aadhar_number": aadhar_number,
                "phone_number": phone_number,
                "extra_number": extra_number
            }
            self.hotel_app.accept_guest_internal(self.room_number, guest_info)
            self.destroy()
            room_type = self.hotel_app.rooms[self.room_number]["type"]
            if room_type == "AC":
                messagebox.showinfo("Payment", "Rs.1500 for AC room.")
            else:
                messagebox.showinfo("Payment", "Rs.1200 for Non-AC room")
            self.hotel_app.ask_payment_option(self.room_number)
        else:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")

class PaymentWindow(tk.Toplevel):
    def __init__(self, parent, room_number, hotel_app):
        super().__init__(parent)
        self.title("Payment")
        self.geometry("300x150")

        self.hotel_app = hotel_app
        self.room_number = room_number
        
        # Load and display background image
        bg_image = Image.open('bg.jpg')
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.payment_label = tk.Label(self, text="Select Mode of Payment:", font=("Helvetica", 14), bg="#8B4513", fg="white")
        self.payment_label.place(relx=0.5, rely=0.3, anchor="center")
        

        self.payment_var = tk.StringVar(self)
        self.payment_var.set("Cash")
        self.payment_options = ["Cash", "Online"]
        self.payment_menu = tk.OptionMenu(self, self.payment_var, *self.payment_options)
        self.payment_menu.place(relx=0.5, rely=0.4, anchor="center")

        self.proceed_button = tk.Button(self, text="Proceed", command=self.proceed_payment,font=("Helvetica", 14), bg="#8B4513", fg="white" )
        self.proceed_button.place(relx=0.5, rely=0.6, anchor="center")

    def proceed_payment(self):
        selected_payment = self.payment_var.get()
        if selected_payment == "Cash":
            messagebox.showinfo("Payment Accepted", "Payment completed in cash. Thank you!")
            self.hotel_app.complete_payment(self.room_number, "Cash")
            self.destroy()
        elif selected_payment == "Online":
            self.upi_window = UpiWindow(self, self.hotel_app)

class UpiWindow(tk.Toplevel):
    def __init__(self, parent, hotel_app):
        super().__init__(parent)
        self.title("Online Payment - UPI")
        self.geometry("300x200")

        self.hotel_app = hotel_app
        
        # Load and display background image
        bg_image = Image.open('bg.jpg')
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.upi_label = tk.Label(self, text="Enter UPI ID:")
        self.upi_label.grid(row=0, column=0, padx=10, pady=10)
        self.upi_entry = tk.Entry(self)
        self.upi_entry.grid(row=0, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_upi)
        self.submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def submit_upi(self):
        upi_id = self.upi_entry.get()
        if upi_id:
            messagebox.showinfo("Payment Accepted", "Payment completed online. Thank you!")
            self.hotel_app.complete_payment(self.room_number, "Online")
            self.destroy()
        else:
            messagebox.showwarning("Missing Information", "Please enter your UPI ID.")

class HotelManagementApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Hotel Management System")
        self.geometry("600x400")
        
         # Load and display background image
        bg_image = Image.open('bg.jpg')
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        
        # Create a canvas
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a frame inside the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        

        self.rooms = {}
        for i in range(101, 151):
            room_type = "AC" if i % 2 != 0 else "Non-AC"
            self.rooms[str(i)] = {"status": "available", "type": room_type, "guest_info": []}




        self.room_label = tk.Label(self.frame, text="Room Number:")
        self.room_label.grid(row=0, column=0, padx=10, pady=10)

        self.room_entry = tk.Entry(self.frame)
        self.room_entry.grid(row=0, column=1, padx=10, pady=10)

        self.check_button = tk.Button(self.frame, text="Check Availability", command=self.check_availability)
        self.check_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.accept_button = tk.Button(self.frame, text="Accept Guest", command=self.accept_guest)
        self.accept_button.grid(row=2, column=0, padx=10, pady=10)

        self.decline_button = tk.Button(self.frame, text="Decline Guest", command=self.decline_guest)
        self.decline_button.grid(row=2, column=1, padx=10, pady=10)

        self.ac_rooms_label = tk.Label(self.frame, text="")
        self.ac_rooms_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.non_ac_rooms_label = tk.Label(self.frame, text="")
        self.non_ac_rooms_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.total_guest_label = tk.Label(self.frame, text="")
        self.total_guest_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.available_rooms_label = tk.Label(self.frame, text="Available Rooms:")
        self.available_rooms_label.grid(row=6, column=0, padx=10, pady=10)

        self.available_rooms_listbox = tk.Listbox(self.frame, width=30, height=10)
        self.available_rooms_listbox.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

        self.update_room_status_listbox()

        self.display_button = tk.Button(self.frame, text="Display Alloted Rooms", command=self.display_alloted_rooms)
        self.display_button.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    def check_availability(self):
        room_number = self.room_entry.get()
        if room_number in self.rooms:
            status = self.rooms[room_number]["status"]
            room_type = self.rooms[room_number]["type"]
            self.result_label.config(text=f"Room {room_number} is {status}. Type: {room_type}")
        else:
            self.result_label.config(text=f"Room {room_number} does not exist.")

    def accept_guest(self):
        room_number = self.room_entry.get()
        if room_number in self.rooms and self.rooms[room_number]["status"] == "available":
            self.get_guest_information(room_number)
        else:
            messagebox.showwarning("Invalid Room", f"Room {room_number} is not available.")

    def accept_guest_internal(self, room_number, guest_info):
        if room_number in self.rooms and self.rooms[room_number]["status"] == "available":
            self.rooms[room_number]["status"] = "occupied"
            self.rooms[room_number]["guest_info"].append(guest_info)
            self.update_total_guests()
            self.update_available_rooms()
            self.update_room_status_listbox()

    def decline_guest(self):
        room_number = self.room_entry.get()
        if room_number in self.rooms and self.rooms[room_number]["status"] == "occupied":
            self.rooms[room_number]["status"] = "available"
            self.update_total_guests()
            self.update_available_rooms()
            self.update_room_status_listbox()
        else:
            messagebox.showwarning("Invalid Room", f"No guest in Room {room_number}.")

    def update_total_guests(self):
        total_guests = sum(len(room["guest_info"]) for room in self.rooms.values() if room["status"] == "occupied")
        self.total_guest_label.config(text=f"Total Guests: {total_guests}")

    def update_available_rooms(self):
        ac_rooms_count = sum(1 for room in self.rooms.values() if room["type"] == "AC" and room["status"] == "available")
        non_ac_rooms_count = sum(1 for room in self.rooms.values() if room["type"] == "Non-AC" and room["status"] == "available")
        self.ac_rooms_label.config(text=f"Available AC Rooms: {ac_rooms_count}")
        self.non_ac_rooms_label.config(text=f"Available Non-AC Rooms: {non_ac_rooms_count}")

    def update_room_status_listbox(self):
        self.available_rooms_listbox.delete(0, tk.END)
        for room_number, room_info in self.rooms.items():
            if room_info["status"] == "available":
                room_type = room_info["type"]
                self.available_rooms_listbox.insert(tk.END, f"Room {room_number} ({room_type})")

    def get_guest_information(self, room_number):
        GuestInfoWindow(self.master, room_number, self)

    def ask_payment_option(self, room_number):
        PaymentWindow(self.master, room_number, self)

    def complete_payment(self, room_number, payment_method):
        if payment_method == "Cash":
            messagebox.showinfo("Payment Accepted", "Payment completed in cash. Thank you!")
        else:
            messagebox.showinfo("Payment Accepted", "Payment completed online. Thank you!")

    def display_alloted_rooms(self):
        self.alloted_rooms_listbox = tk.Listbox(self.frame, width=40, height=10)
        self.alloted_rooms_listbox.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

        def show_guest_information(room_number):
            guest_info_list = self.rooms[room_number]["guest_info"]
            info_str = ""
            for guest_info in guest_info_list:
                info_str += f"Name: {guest_info['name']}\nAddress: {guest_info['address']}\nAadhar Number: {guest_info['aadhar_number']}\nPhone Number: {guest_info['phone_number']}\nExtra Number: {guest_info['extra_number']}\n\n"
            if info_str:
                messagebox.showinfo("Guest Information", info_str)
            else:
                messagebox.showinfo("Guest Information", "No guest information available for this room.")

        def create_button(room_number):
            return tk.Button(self.frame, text=f"Room {room_number}", command=lambda: show_guest_information(room_number))

        alloted_rooms = [room_number for room_number, room_info in self.rooms.items() if room_info["status"] == "occupied"]
        if alloted_rooms:
            for idx, room_number in enumerate(alloted_rooms):
                self.alloted_rooms_listbox.insert(tk.END, f"Room {room_number}")
                room_button = create_button(room_number)
                room_button.grid(row=10 + idx, column=0, columnspan=3, padx=10, pady=10)
        else:
            messagebox.showinfo("Alloted Rooms", "No rooms are currently alloted.")

def main():
    root = tk.Tk()
    app = HotelManagementApp(root)
    app.update_total_guests()
    app.update_available_rooms()
    root.mainloop()

if __name__ == "__main__":
    main()
