import os
from tkinter import filedialog
import random
import re
import tkinter as tk
from tkinter import ttk, messagebox
from Railway_Management_Backend import RailwayManagementSystem
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from tkcalendar import DateEntry

class RailwayGUI:
    print("RUNNING GUI FILE:", __file__)
    def __init__(self, root):
        self.root = root
        self.root.title("Project - Ayush's Railway Management System")
        self.root.geometry("1250x780")
        self.root.minsize(1050, 680)
        self.root.configure(bg="#F4F7FC")

        # Existing backend connection
        self.railway = RailwayManagementSystem()
        self.logged_in_admin_id = None

        # Modern Railway Theme
        self.bg_color = "#F4F7FC"
        self.sidebar_color = "#FFFFFF"
        self.primary_color = "#1769AA"
        self.dark_color = "#123456"
        self.card_color = "#FFFFFF"
        self.text_color = "#1E293B"
        self.secondary_color = "#718096"
        self.border_color = "#E2E8F0"
        self.mode = "User"
        self.nav_buttons = {}
        self.setup_style()
        self.create_layout()
        self.show_dashboard()
        self.from_station_codes = {}
        self.to_station_codes = {}
        self.api_trains = []

    # ---------------------------------
    # STYLE
    # ---------------------------------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground=self.text_color,
            fieldbackground="white",
            rowheight=34,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#EAF2FA",
            foreground=self.dark_color,
            font=("Arial", 10, "bold"),
            padding=9
        )

        style.configure(
            "TEntry",
            padding=8
        )

        style.configure(
            "TCombobox",
            padding=8
        )

    # ---------------------------------
    # MAIN LAYOUT
    # ---------------------------------
    def create_layout(self):
        # Top Navigation Bar
        self.topbar = tk.Frame(
            self.root,
            bg="white",
            height=75,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        tk.Label(
            self.topbar,
            text="🚆 RAILWAY PROJECT",
            bg="white",
            fg=self.primary_color,
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=25)

        # Portal buttons
        self.user_btn = tk.Button(
            self.topbar,
            text="User Portal",
            command=lambda: self.change_portal("User"),
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=9,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.user_btn.pack(side="right", padx=(5, 20))

        self.admin_btn = tk.Button(
            self.topbar,
            text="Admin Portal",
            command=lambda: self.change_portal("Admin"),
            bg="#EAF2FA",
            fg=self.dark_color,
            activebackground="#D9E8F7",
            relief="flat",
            padx=18,
            pady=9,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.admin_btn.pack(side="right", padx=5)

        # Main body
        self.body = tk.Frame(
            self.root,
            bg=self.bg_color
        )
        self.body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(
            self.body,
            bg=self.sidebar_color,
            width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar heading
        self.sidebar_heading = tk.Label(
            self.sidebar,
            text="USER MENU",
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 9, "bold"),
            anchor="w"
        )

        self.sidebar_heading.pack(
            fill="x",
            padx=22,
            pady=(25, 15)
        )

        self.menu_area = tk.Frame(
            self.sidebar,
            bg="white"
        )
        self.menu_area.pack(fill="both", expand=True)

        tk.Label(
            self.sidebar,
            text="Railway Management System\nVersion 1.0",
            bg="white",
            fg="#94A3B8",
            font=("Arial", 8),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=20)

        # Main content
        self.content = tk.Frame(
            self.body,
            bg=self.bg_color
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )
        self.create_sidebar_menu()

    # ---------------------------------
    # PORTAL NAVIGATION
    # ---------------------------------
    def change_portal(self, mode):
        # Prevent switching to User Portal while Admin is logged in
        if mode == "User" and getattr(self, "logged_in_admin_id", None):
            messagebox.showwarning(
                "Admin Account Active",
                "Please logout your admin account to access the User Portal."
            )
            return
        self.mode = mode

        if mode == "User":
            self.user_btn.configure(
                bg=self.primary_color,
                fg="white"
            )

            self.admin_btn.configure(
                bg="#EAF2FA",
                fg=self.dark_color
            )

            # Show sidebar for User Portal
            self.sidebar.pack(
                side="left",
                fill="y",
                before=self.content
            )

            self.sidebar_heading.configure(
                text="USER MENU"
            )
            self.create_sidebar_menu()
            self.show_dashboard()

        else:
            self.admin_btn.configure(
                bg=self.primary_color,
                fg="white"
            )

            self.user_btn.configure(
                bg="#EAF2FA",
                fg=self.dark_color
            )

            # Hide sidebar for Admin Portal
            self.sidebar.pack_forget()

            # Open Admin Options screen
            self.show_screen("Admin Options")

    def create_sidebar_menu(self):
        for widget in self.menu_area.winfo_children():
            widget.destroy()
        self.nav_buttons = {}

        if self.mode == "User":
            self.sidebar_heading.configure(
                text="USER MENU"
            )

            options = [
                "Dashboard",
                "Train Details",
                "Available Trains",
                "Check Seat Availability",
                "Book Tickets",
                "Cancel Tickets",
                "View Booked Tickets",
                "Ticket Details"
            ]

        else:
            self.sidebar_heading.configure(
                text="ADMIN MENU"
            )

            options = [
                "Dashboard",
                "Admin Login",
                "Add Train",
                "Update Train",
                "Remove Train",
                "View All Bookings"
            ]

        for name in options:
            button = tk.Button(
                self.menu_area,
                text="   " + name,
                command=(
                    self.show_dashboard
                    if name == "Dashboard"
                    else lambda n=name: self.show_screen(n)
                ),
                bg="white",
                fg=self.text_color,
                activebackground="#EAF2FA",
                activeforeground=self.primary_color,
                relief="flat",
                bd=0,
                anchor="w",
                padx=12,
                pady=11,
                font=("Arial", 10),
                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2
            )
            self.nav_buttons[name] = button

    # ---------------------------------
    # COMMON FUNCTIONS
    # ---------------------------------
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_active(self, name):
        for button_name, button in self.nav_buttons.items():
            if button_name == name:
                button.configure(
                    bg="#EAF2FA",
                    fg=self.primary_color,
                    font=("Arial", 10, "bold")
                )

            else:
                button.configure(
                    bg="white",
                    fg=self.text_color,
                    font=("Arial", 10)
                )

    def create_header(self, title, description):
        tk.Label(
            self.content,
            text=title,
            bg=self.bg_color,
            fg=self.dark_color,
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        tk.Label(
            self.content,
            text=description,
            bg=self.bg_color,
            fg=self.secondary_color,
            font=("Arial", 10)
        ).pack(anchor="w", padx=30, pady=(0, 18))

    def create_service_card(self, parent, title, description, command):

        card = tk.Frame(
            parent,
            bg=self.card_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        tk.Label(
            card,
            text="●",
            bg="white",
            fg=self.primary_color,
            font=("Arial", 17)
        ).pack(anchor="w", padx=18, pady=(13, 3))

        tk.Label(
            card,
            text=title,
            bg="white",
            fg=self.dark_color,
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=18, pady=4)

        tk.Label(
            card,
            text=description,
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 9)
        ).pack(anchor="w", padx=18, pady=(0, 10))

        tk.Button(
            card,
            text="Explore  →",
            command=command,
            bg="#EAF2FA",
            fg=self.primary_color,
            activebackground="#D9E8F7",
            relief="flat",
            padx=13,
            pady=6,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(anchor="w", padx=18, pady=(0, 15))
        return card

    # ---------------------------------
    # DASHBOARD
    # ---------------------------------
    def show_dashboard(self):
        self.clear_content()
        self.set_active("Dashboard")

        if self.mode == "User":
            self.create_header(
                "Welcome to Railway Services",
                "Plan your journey and manage your train reservations."
            )

            # Welcome banner
            banner = tk.Frame(
                self.content,
                bg=self.dark_color,
                height=145
            )

            banner.pack(
                fill="x",
                padx=30,
                pady=(0, 20)
            )
            banner.pack_propagate(False)

            tk.Label(
                banner,
                text="Your Journey Starts Here!",
                bg=self.dark_color,
                fg="white",
                font=("Arial", 21, "bold")
            ).pack(anchor="w", padx=25, pady=(24, 7))

            tk.Label(
                banner,
                text="Discover trains, check seats and book your tickets easily.",
                bg=self.dark_color,
                fg="#D5E7FA",
                font=("Arial", 10)
            ).pack(anchor="w", padx=25, pady=(0, 12))

            tk.Button(
                banner,
                text="Explore Available Trains  →",
                command=lambda: self.show_screen("Available Trains"),
                bg="#FFFFFF",
                fg=self.primary_color,
                activebackground="#EAF2FA",
                relief="flat",
                padx=15,
                pady=7,
                font=("Arial", 9, "bold"),
                cursor="hand2"
            ).pack(anchor="w", padx=25)

            cards = [
                ("Train Details", "Explore registered trains."),
                ("Available Trains", "Find trains for your journey."),
                ("Seat Availability", "Check remaining train seats."),
                ("Book Tickets", "Reserve your train tickets."),
                ("Cancel Tickets", "Manage your existing booking."),
                ("My Bookings", "Review your booked tickets.")
            ]

        else:
            self.create_header(
                "Administration Dashboard",
                "Manage railway operations and reservations."
            )

            banner = tk.Frame(
                self.content,
                bg=self.dark_color,
                height=145
            )

            banner.pack(
                fill="x",
                padx=30,
                pady=(0, 20)
            )
            banner.pack_propagate(False)

            tk.Label(
                banner,
                text="Railway Administration",
                bg=self.dark_color,
                fg="white",
                font=("Arial", 21, "bold")
            ).pack(anchor="w", padx=25, pady=(28, 7))

            tk.Label(
                banner,
                text="Manage trains, schedules and passenger bookings.",
                bg=self.dark_color,
                fg="#D5E7FA",
                font=("Arial", 10)
            ).pack(anchor="w", padx=25)

            cards = [
                ("Admin Login", "Access administrator authentication."),
                ("Add Train", "Register a new train."),
                ("Update Train", "Modify train information."),
                ("Remove Train", "Remove a registered train."),
                ("View All Bookings", "Review passenger reservations.")
            ]

        # Service cards
        card_area = tk.Frame(
            self.content,
            bg=self.bg_color
        )

        card_area.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=0
        )

        for index, (title, description) in enumerate(cards):
            row = index // 2
            column = index % 2
            card = self.create_service_card(
                card_area,
                title,
                description,
                lambda n=title: self.open_card(n)
            )

            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=8,
                pady=7
            )
        card_area.columnconfigure(0, weight=1)
        card_area.columnconfigure(1, weight=1)
        for row in range((len(cards) + 1) // 2):
            card_area.rowconfigure(row, weight=1)

    def open_card(self, title):
        screen_names = {
            "Seat Availability": "Check Seat Availability",
            "My Bookings": "View Booked Tickets"
        }

        self.show_screen(
            screen_names.get(title, title)
        )

    # ---------------------------------
    # OTHER SCREENS
    # ---------------------------------
    def show_screen(self, screen_name):
        self.clear_content()
        self.set_active(screen_name)
        descriptions = {
            "Train Details":
                "Explore all registered railway trains.",

            "Available Trains":
                "Find trains available for your journey.",

            "Check Seat Availability":
                "Search for available seats.",

            "Book Tickets":
                "Enter journey and passenger information.",

            "Cancel Tickets":
                "Manage your existing reservations.",

            "View Booked Tickets":
                "Review your booking information.",

            "Ticket Details":
                "View your railway ticket information.",

            "Admin Login":
                "Administrator authentication.",

            "Add Trains":
                "Register new railway trains.",

            "Update Trains":
                "Search and update existing train information.",

            "Remove Trains":
                "Remove a train from the system.",

            "View All Bookings":
                "Review all passenger bookings.",

            "Delete Admin Account":
                "Delete your administrator account."
        }

        self.create_header(
            screen_name,
            descriptions.get(screen_name, "")
        )

        back_screens = {
            # User Screens
            "Train Details": "Dashboard",
            "Available Trains": "Dashboard",
            "Check Seat Availability": "Dashboard",
            "Book Tickets": "Dashboard",
            "Cancel Tickets": "Dashboard",
            "Cancel Ticket": "Dashboard",
            "View Booked Tickets": "Dashboard",
            "Ticket Details": "Dashboard",

            # Admin Screens
            "Admin Login": "Admin Options",
            "Admin Create Account": "Admin Options",
            "Add Trains": "Admin Dashboard",
            "Update Trains": "Admin Dashboard",
            "Remove Trains": "Admin Dashboard",
            "View All Bookings": "Admin Dashboard",
            "Delete Admin Account": "Admin Dashboard"
        }

        if screen_name in back_screens:
            back_frame = tk.Frame(
                self.content,
                bg="#F4F7FC"
            )

            back_frame.pack(
                fill="x",
                padx=30,
                pady=(0, 10)
            )

            tk.Button(
                back_frame,
                text="← BACK",
                font=("Segoe UI", 9, "bold"),
                bg="white",
                fg=self.primary_color,
                cursor="hand2",
                relief="solid",
                bd=1,
                command=lambda: self.show_dashboard() 
                if back_screens[screen_name] == "Dashboard" 
                else self.show_screen(back_screens[screen_name]
                )
            ).pack(
                side="left",
                ipadx=12,
                ipady=5
            )

        if screen_name == "Train Details":
            self.show_train_details()
            return

        if screen_name == "Available Trains":
            self.show_available_trains()
            return

        if screen_name == "Check Seat Availability":
            self.show_seat_availability()
            return

        if screen_name == "Book Tickets":
            self.show_book_tickets()
            return

        if screen_name == "Cancel Tickets":
            self.show_cancel_tickets()
            return

        if screen_name == "View Booked Tickets":
            self.show_booked_tickets()
            return

        if screen_name == "Ticket Details":
            self.show_ticket_details()
            return

        if screen_name == "Admin Options":
            self.show_admin_options()
            return

        if screen_name == "Admin Login":
            self.show_admin_login()
            return

        if screen_name == "Admin Dashboard":
            self.show_admin_dashboard()
            return

        if screen_name == "Admin Create Account":
            self.show_admin_create_account()
            return

        if screen_name == "Add Trains":
            self.show_add_train_screen()
            return

        if screen_name == "Update Trains":
            self.show_update_train_screen()
            return

        if screen_name == "Remove Trains":
            self.show_remove_train_screen()
            return

        if screen_name == "View All Bookings":
            self.show_all_bookings_screen()
            return

        if screen_name == "Delete Admin Account":
            self.show_delete_admin_screen()
            return

        # Temporary placeholder for other screens
        panel = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        tk.Label(
            panel,
            text=screen_name,
            bg="white",
            fg=self.dark_color,
            font=("Arial", 20, "bold")
        ).pack(pady=(65, 12))

    def show_train_details(self):
        # Main container
        table_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        # Table heading
        heading_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        heading_frame.pack(
            fill="x",
            padx=20,
            pady=18
        )

        tk.Label(
            heading_frame,
            text="Registered Train Information",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 15, "bold")
        ).pack(side="left")

        # Refresh button
        tk.Button(
            heading_frame,
            text="↻ Refresh",
            command=lambda: self.show_screen("Train Details"),
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            relief="flat",
            padx=15,
            pady=7,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(side="right")

        # Table container
        tree_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columns = (
            "Train Name",
            "Train Number",
            "Platform",
            "From",
            "To",
            "Departure",
            "Arrival",
            "Available Seats"
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        # Column headings and widths
        for column in columns:
            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120,
                minwidth=100,
                anchor="center"
            )
        tree.column("Train Name", width=150)

        # Scrollbars
        vertical_scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        print("Total Registered Trains:", len(self.railway.Trains))

        # Display backend train records
        if self.railway.Trains:
            for train in self.railway.Trains:
                tree.insert(
                    "",
                    "end",
                    values=(
                        train[0],
                        train[1],
                        train[2],
                        train[3],
                        train[4],
                        train[5],
                        train[6],
                        train[7]
                    )
                )

        else:
            messagebox.showinfo(
                "Train Details",
                "No registered trains found."
            )

    def get_api_availability_count(self, train):
        """
        Read availability from the train-search response. This prevents
        repeated class-wise seat API requests and treats unknown data as N/A.
        """
        summary = train.get("availability_summary") or []

        if isinstance(summary, dict):
            summary = list(summary.values())

        if not isinstance(summary, (list, tuple)) or not summary:
            return "N/A"

        available_counts = []
        all_confirmed_unavailable = True
        expected_classes = {
            str(class_code).strip().upper()
            for class_code in (train.get("classes") or [])
            if str(class_code).strip()
        }
        summarized_classes = set()

        for item in summary:
            if not isinstance(item, dict):
                all_confirmed_unavailable = False
                continue

            class_code = str(item.get("class_code", "")).strip().upper()
            if class_code:
                summarized_classes.add(class_code)

            status = str(item.get("status", "")).strip().upper()
            text_value = str(item.get("text", "")).strip().upper()
            count = item.get("available_count")

            if isinstance(count, int) and not isinstance(count, bool):
                if count > 0:
                    available_counts.append(count)
                elif count == 0 and status in ("AVAILABLE", "AVL", "WAITLIST", "WL", "REGRET", "CLOSED"):
                    continue
                else:
                    all_confirmed_unavailable = False
                continue

            if status in ("AVAILABLE", "AVL"):
                match = re.search(r"(?:AVAILABLE|AVL)[\s-]*(\d+)", text_value)
                if match:
                    available_counts.append(int(match.group(1)))
                else:
                    all_confirmed_unavailable = False
            elif status in ("WAITLIST", "WL", "REGRET", "CLOSED"):
                continue
            else:
                all_confirmed_unavailable = False

        if available_counts:
            return max(available_counts)
        # Return zero only when every advertised class has a known
        # unavailable status. Missing class summaries must remain N/A.
        if (
            all_confirmed_unavailable
            and expected_classes
            and expected_classes.issubset(summarized_classes)
        ):
            return 0
        return "N/A"

    def show_available_trains(self):
        # Main container
        table_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        # Table heading
        heading_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        heading_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            heading_frame,
            text="Available Train Information",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 15, "bold")
        ).pack(side="left")

        # Station Search Section
        search_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        # Search Stations Button
        tk.Button(
            search_frame,
            text="Search Trains",
            command=self.search_api_trains,
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            relief="flat",
            padx=15,
            pady=7,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(side="left")

        # Station Selection Section
        station_selection_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        station_selection_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # From Station Results
        tk.Label(
            station_selection_frame,
            text="Select From Station",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        self.from_station_list = ttk.Combobox(
            station_selection_frame,
            state="normal",
            width=25,
            font=("Arial", 9)
        )
        self.from_station_list.pack(side="left", padx=(0, 25))

        # Journey Date
        tk.Label(
            station_selection_frame,
            text="Journey Date",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        self.journey_date = DateEntry(
            station_selection_frame,
            width=12,
            background=self.primary_color,
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 9)
        )

        self.journey_date.pack(side="left", padx=(0, 20))

        if hasattr(self, "selected_journey_date"):
            self.journey_date.set_date(self.selected_journey_date)

        # To Station Results
        tk.Label(
            station_selection_frame,
            text="Select To Station",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        self.to_station_list = ttk.Combobox(
            station_selection_frame,
            state="normal",
            width=25,
            font=("Arial", 9)
        )
        self.to_station_list.pack(side="left")

        # Refresh button
        tk.Button(
            heading_frame,
            text="↻ Refresh",
            command=lambda: self.show_screen("Available Trains"),
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            relief="flat",
            padx=15,
            pady=7,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(side="right")

        print("TABLE SECTION REACHED")

        # Table container
        tree_frame = tk.Frame(
            table_frame,
            bg="white"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        columns = (
            "Train Name",
            "Train Number",
            "Platform",
            "From",
            "To",
            "Departure",
            "Arrival",
            "Available Seats",
            "Source"
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        # Column headings and widths
        for column in columns:
            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120,
                minwidth=100,
                anchor="center"
            )
        tree.column("Train Name", width=150)

        # Scrollbars
        vertical_scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Filter local trains by selected route
        available_trains = []
        if hasattr(self, "selected_from_code") and hasattr(self, "selected_to_code"):
            selected_from = next(
                (station for station in self.from_station_data
                if station["station_code"] == self.selected_from_code),
                None
            )

            selected_to = next(
                (station for station in self.to_station_data
                if station["station_code"] == self.selected_to_code),
                None
            )

            if selected_from and selected_to:
                from_names = [
                    selected_from.get("station_name", ""),
                    selected_from.get("display_name", ""),
                    selected_from.get("city", "")
                ] + selected_from.get("aliases", [])

                to_names = [
                    selected_to.get("station_name", ""),
                    selected_to.get("display_name", ""),
                    selected_to.get("city", "")
                ] + selected_to.get("aliases", [])

                from_names = [name.strip().casefold() for name in from_names if name]
                to_names = [name.strip().casefold() for name in to_names if name]

                available_trains = [
                    train for train in self.railway.Trains
                    if train[7] > 0
                    and train[3].strip().casefold() in from_names
                    and train[4].strip().casefold() in to_names
                ]
        print("Matching Local Trains:", len(available_trains))

        # Display available train records
        if available_trains:
            for train in available_trains:
                tree.insert(
                    "",
                    "end",
                    values=(
                        train[0],
                        train[1],
                        train[2],
                        train[3],
                        train[4],
                        train[5],
                        train[6],
                        train[7],
                        "Local"
                    )
                )
        
        # API Result Caching
        if not hasattr(self, "platform_cache"):
            self.platform_cache = {}

        if not hasattr(self, "seat_cache"):
            self.seat_cache = {}

        # Display API train records
        if hasattr(self, "api_trains") and self.api_trains:
            journey_date = self.journey_date.get_date().strftime("%Y-%m-%d")
            for train in self.api_trains:
                train_number = train.get("train_number")
                from_code = train.get("from_station_code")
                to_code = train.get("to_station_code")

                # Platform Cache
                platform_key = (train_number, from_code)

                if platform_key not in self.platform_cache:
                    success_platform, platform = self.railway.get_train_platform_from_api(
                        train_number,
                        from_code
                    )

                    self.platform_cache[platform_key] = (
                        platform if success_platform else "N/A"
                    )

                platform_number = self.platform_cache[platform_key]

                # Use the summary already returned by train search.
                # No repeated class-wise seat API requests are made here.
                seat_key = (
                    train_number,
                    from_code,
                    to_code,
                    journey_date
                )

                if seat_key not in self.seat_cache:
                    self.seat_cache[seat_key] = self.get_api_availability_count(train)

                seat_count = self.seat_cache[seat_key]

                tree.insert(
                    "",
                    "end",
                    values=(
                        train.get("train_name", "N/A"),
                        train_number,
                        platform_number,
                        train.get("from_station_name", "N/A"),
                        train.get("to_station_name", "N/A"),
                        train.get("departure_time", "N/A"),
                        train.get("arrival_time", "N/A"),
                        seat_count,
                        "API"
                    )
                )

    def search_api_trains(self):
        from_station = self.from_station_list.get().strip()
        to_station = self.to_station_list.get().strip()

        # Preserve entered station names
        entered_from = from_station
        entered_to = to_station

        if not from_station or not to_station:
            messagebox.showwarning(
                "Missing Stations",
                "Please enter both From and To stations."
            )
            return

        # Check whether stations are selected from API dropdowns
        from_code = self.from_station_codes.get(from_station)
        to_code = self.to_station_codes.get(to_station)

        # If both stations are selected, fetch trains
        if from_code and to_code:
            self.selected_from_code = from_code
            self.selected_to_code = to_code
            journey_date = self.journey_date.get_date().strftime("%Y-%m-%d")
            self.selected_journey_date = journey_date
            success, trains = self.railway.search_trains_from_api(
                from_code,
                to_code,
                journey_date
            )

            if not success:
                messagebox.showerror("Train Search Error", trains)
                return

            print("API TRAIN RESULTS:", trains)

            if trains:
                success_platform, platform = self.railway.get_train_platform_from_api(
                    trains[0].get("train_number"),
                    from_code
                )
                print("PLATFORM API RESULT:", success_platform, platform)

            if trains:
                print("FIRST API TRAIN DETAILS:", trains[0])

            # Store API train results for displaying in the table
            self.api_trains = trains
            messagebox.showinfo(
                "Train Search",
                f"API returned {len(trains)} trains."
            )

            # Refresh Available Trains table
            self.show_screen("Available Trains")
            return

        # Search From station
        success_from, from_results = self.railway.search_stations_from_api(
            from_station
        )

        if not success_from:
            messagebox.showerror("Station Search Error", from_results)
            return

        # Search To station
        success_to, to_results = self.railway.search_stations_from_api(
            to_station
        )

        if not success_to:
            messagebox.showerror("Station Search Error", to_results)
            return

        # Store station results
        self.from_station_data = from_results
        self.to_station_data = to_results

        # Populate From dropdown
        self.from_station_list["values"] = [
            f"{station['display_name']} ({station['station_code']})"
            for station in from_results
        ]

        # Populate To dropdown
        self.to_station_list["values"] = [
            f"{station['display_name']} ({station['station_code']})"
            for station in to_results
        ]

        # Store station code mapping
        self.from_station_codes = {
            f"{station['display_name']} ({station['station_code']})":
            station["station_code"]
            for station in from_results
        }

        self.to_station_codes = {
            f"{station['display_name']} ({station['station_code']})":
            station["station_code"]
            for station in to_results
        }

        # Debug dropdown options
        print("FROM DROPDOWN:", self.from_station_list["values"])
        print("TO DROPDOWN:", self.to_station_list["values"])

        # Clear text so user can select an API result
        self.from_station_list.set("")
        self.to_station_list.set("")

        messagebox.showinfo(
            "Station Search",
            "Station options loaded. Please select your stations."
        )

    def show_seat_availability(self):
        # Scrollable Main Area
        scroll_container = tk.Frame(
            self.content,
            bg=self.bg_color
        )

        scroll_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        canvas = tk.Canvas(
            scroll_container,
            bg=self.bg_color,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = tk.Frame(
            canvas,
            bg=self.bg_color
        )

        window_id = canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )

        scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                window_id,
                width=event.width
            )
        )

        # Mouse Wheel Scrolling
        canvas.bind(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        # Main Container
        search_frame = tk.Frame(
            scrollable_frame,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        search_frame.pack(
            fill="x",
            expand=True
        )

        # Search Heading
        tk.Label(
            search_frame,
            text="Find Your Train Seats",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 15, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            search_frame,
            text="Enter your train number to check current seat availability.",
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # Search Form
        form_frame = tk.Frame(
            search_frame,
            bg="white"
        )

        form_frame.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        tk.Label(
            form_frame,
            text="Train Number",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        train_number_entry = ttk.Entry(
            form_frame,
            width=35,
            font=("Arial", 11)
        )

        train_number_entry.pack(
            pady=10,
            ipady=6
        )

        # Result Card
        result_frame = tk.Frame(
            search_frame,
            bg="#F4F7FC",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        result_frame.pack(
            fill="x",
            padx=25,
            pady=8
        )

        tk.Label(
            result_frame,
            text="Train Availability Result",
            bg="#F4F7FC",
            fg=self.dark_color,
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 5)
        )

        details_frame = tk.Frame(
            result_frame,
            bg="#F4F7FC"
        )

        details_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 5)
        )

        train_name_label = tk.Label(
            details_frame,
            text="Train Name: --",
            bg="#F4F7FC",
            fg=self.dark_color,
            font=("Arial", 11)
        )
        train_name_label.pack(anchor="w", pady=5)
        train_number_label = tk.Label(
            details_frame,
            text="Train Number: --",
            bg="#F4F7FC",
            fg=self.dark_color,
            font=("Arial", 11)
        )
        train_number_label.pack(anchor="w", pady=5)

        # Available Seats Display
        seats_frame = tk.Frame(
            result_frame,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        seats_frame.pack(
            fill="x",
            padx=20,
            pady=8,
            ipady=12
        )

        tk.Label(
            seats_frame,
            text="AVAILABLE SEATS",
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 10, "bold")
        ).pack(pady=(8, 3))

        seats_label = tk.Label(
            seats_frame,
            text="--",
            bg="white",
            fg="black",
            font=("Arial", 32, "bold")
        )
        seats_label.pack(pady=(0, 8))
        status_label = tk.Label(
            details_frame,
            text="Search a train to check availability.",
            bg="#F4F7FC",
            fg=self.secondary_color,
            font=("Arial", 10, "bold")
        )
        status_label.pack(anchor="w", pady=5)

        # Search Function
        def search_train():
            print("SEARCH TRAIN BUTTON CLICKED")
            train_number = train_number_entry.get().strip()
            # Reset Previous Result
            train_name_label.config(text="Train Name: --")
            train_number_label.config(text="Train Number: --")
            seats_label.config(text="--")
            status_label.config(
                text="Search a train to check availability.",
                fg=self.secondary_color
            )

            # Validate Empty Input
            if not train_number:
                messagebox.showwarning(
                    "Input Required",
                    "Please enter a Train Number."
                )
                return

            # Validate Digits
            if not train_number.isdigit():
                messagebox.showerror(
                    "Invalid Input",
                    "Train Number must contain digits only."
                )
                return

            # Search Train
            found_train = None

            for train in self.railway.Trains:
                if train[1] == int(train_number):
                    found_train = train
                    break

            # Search API Trains if Local Train Not Found
            if found_train is None:
                print("SEARCHING API TRAINS...")
                print("API TRAINS COUNT:", len(getattr(self, "api_trains", [])))
                for train in getattr(self, "api_trains", []):
                    if str(train.get("train_number", "")) == train_number:
                        found_train = train
                        break

            # If Train Not Found
            if found_train is None:
                status_label.config(
                    text="No matching train found.",
                    fg="#DC2626"
                )

                messagebox.showerror(
                    "Train Not Found",
                    "No train found with this Train Number."
                )
                return

            # Display Local Train Details
            if isinstance(found_train, tuple):

                train_name = found_train[0]
                train_number = found_train[1]
                available_seats = found_train[7]

            # Display API Train Details
            else:
                train_name = found_train.get("train_name", "N/A")
                train_number = found_train.get("train_number", "N/A")

                # Use cached train-search summary instead of another seat API call.
                if not hasattr(self, "seat_cache"):
                    self.seat_cache = {}

                seat_key = (
                    found_train.get("train_number"),
                    found_train.get("from_station_code"),
                    found_train.get("to_station_code"),
                    self.selected_journey_date
                )

                if seat_key not in self.seat_cache:
                    self.seat_cache[seat_key] = self.get_api_availability_count(found_train)

                available_seats = self.seat_cache[seat_key]

            # Display Train Name
            train_name_label.config(
                text=f"Train Name: {train_name}"
            )

            # Display Train Number
            train_number_label.config(
                text=f"Train Number: {train_number}"
            )

            # Display Available Seats
            seats_label.config(
                text=str(available_seats)
            )

            # Display Seat Availability Status
            if isinstance(available_seats, int) and available_seats > 0:
                status_label.config(
                    text="✓ Seats Available",
                    fg="#15803D"
                )
            elif available_seats == 0:
                status_label.config(
                    text="✗ No Seats Available",
                    fg="#DC2626"
                )
            else:
                status_label.config(
                    text="Train found. Seat availability needs API check.",
                    fg=self.secondary_color
                )

        # Search Button
        tk.Button(
            form_frame,
            text="Search Train",
            command=search_train,
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=9,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(
            anchor="w",
            pady=3
        )
        train_number_entry.focus_set()

    def show_cancel_tickets(self):
        # Main container
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        # Heading
        tk.Label(
            main_frame,
            text="Cancel Your Reservation",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            main_frame,
            text="Enter your Booking ID to find your reservation.",
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # Booking ID input
        form_frame = tk.Frame(
            main_frame,
            bg="white"
        )

        form_frame.pack(
            anchor="w",
            padx=25
        )

        tk.Label(
            form_frame,
            text="Booking ID",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        # Booking ID and Search Button Row
        search_row = tk.Frame(
            form_frame,
            bg="white"
        )
        search_row.pack(anchor="w", pady=10)
        self.cancel_booking_id_entry = ttk.Entry(
            search_row,
            width=35,
            font=("Arial", 11)
        )

        self.cancel_booking_id_entry.pack(
            side="left",
            ipady=6,
            padx=(0, 15)
        )

        # Scrollable Search Result
        result_container = tk.Frame(
            main_frame,
            bg="white"
        )

        result_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        result_canvas = tk.Canvas(
            result_container,
            bg="#F4F7FC",
            highlightthickness=0
        )

        result_scrollbar = ttk.Scrollbar(
            result_container,
            orient="vertical",
            command=result_canvas.yview
        )

        result_canvas.configure(
            yscrollcommand=result_scrollbar.set
        )

        result_scrollbar.pack(
            side="right",
            fill="y"
        )

        result_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.cancel_result_frame = tk.Frame(
            result_canvas,
            bg="#F4F7FC"
        )

        result_window = result_canvas.create_window(
            (0, 0),
            window=self.cancel_result_frame,
            anchor="nw"
        )

        def update_cancel_scroll(event=None):
            result_canvas.configure(
                scrollregion=result_canvas.bbox("all")
            )

        self.cancel_result_frame.bind(
            "<Configure>",
            update_cancel_scroll
        )

        result_canvas.bind(
            "<Configure>",
            lambda event: result_canvas.itemconfig(
                result_window,
                width=event.width
            )
        )

        def on_cancel_mousewheel(event):
            result_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        result_canvas.bind(
            "<MouseWheel>",
            on_cancel_mousewheel
        )

        self.cancel_status_label = tk.Label(
            self.cancel_result_frame,
            text="Search a Booking ID to view reservation details.",
            bg="#F4F7FC",
            fg=self.secondary_color,
            font=("Arial", 10, "bold")
        )

        self.cancel_status_label.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # Search function
        def search_booking():
            booking_id = self.cancel_booking_id_entry.get().strip()
            self.cancel_status_label.config(
                text="",
                fg=self.secondary_color
            )

            for widget in self.cancel_result_frame.winfo_children():
                widget.destroy()

            if not booking_id:
                messagebox.showwarning(
                    "Input Required",
                    "Please enter your Booking ID."
                )
                return

            if not booking_id.isdigit():
                messagebox.showerror(
                    "Invalid Booking ID",
                    "Booking ID must contain digits only."
                )
                return
            booking_id = int(booking_id)

            matched_passengers = [
                passenger
                for passenger in self.railway.passengers
                if passenger["Booking ID"] == booking_id
            ]

            if not matched_passengers:
                self.cancel_status_label = tk.Label(
                    self.cancel_result_frame,
                    text="Booking ID not found.",
                    bg="#F4F7FC",
                    fg="#DC2626",
                    font=("Arial", 11, "bold")
                )

                self.cancel_status_label.pack(
                    anchor="w",
                    padx=20,
                    pady=15
                )
                return

            # Display booking information
            first_passenger = matched_passengers[0]

            tk.Label(
                self.cancel_result_frame,
                text="Booking Details",
                bg="#F4F7FC",
                fg=self.dark_color,
                font=("Arial", 13, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(15, 10)
            )

            details = [
                f"Booking ID: {booking_id}",
                f"Train Name: {first_passenger['Train Name']}",
                f"Train Number: {first_passenger['Train Number']}",
                f"Journey: {first_passenger['From']} to {first_passenger['To']}",
                f"Total Passengers: {len(matched_passengers)}"
            ]

            for detail in details:
                tk.Label(
                    self.cancel_result_frame,
                    text=detail,
                    bg="#F4F7FC",
                    fg=self.dark_color,
                    font=("Arial", 10)
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=4
                )

            # View Passenger Details Button
            tk.Button(
                self.cancel_result_frame,
                text="VIEW PASSENGER DETAILS",
                command=self.show_cancel_passenger_details,
                bg=self.primary_color,
                fg="white",
                relief="flat",
                padx=25,
                pady=10,
                font=("Arial", 10, "bold"),
                cursor="hand2"
            ).pack(
                anchor="w",
                padx=20,
                pady=10
            )

            self.cancel_status_label = tk.Label(
                self.cancel_result_frame,
                text="Booking found successfully.",
                bg="#F4F7FC",
                fg="#15803D",
                font=("Arial", 10, "bold")
            )

            self.cancel_status_label.pack(
                anchor="w",
                padx=20,
                pady=15
            )
            self.cancel_matched_passengers = matched_passengers
            self.cancel_selected_booking_id = booking_id

        # Search button
        tk.Button(
            form_frame,
            text="SEARCH BOOKING",
            command=search_booking,
            bg=self.primary_color,
            fg="white",
            activebackground="#12558B",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=9,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(
            in_=search_row,
            side="left",
            padx=(0, 10),
            pady=0
        )
        self.cancel_booking_id_entry.focus_set()

    def show_cancel_passenger_details(self):
        self.clear_content()
        self.create_header(
            "Passenger Details",
            "View all passengers associated with this booking."
        )

        # Main Container
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Booking Information
        first_passenger = self.cancel_matched_passengers[0]
        booking_info = tk.Label(
            main_frame,
            text=(
                f"Booking ID: {self.cancel_selected_booking_id}\n"
                f"Train: {first_passenger['Train Name']} "
                f"({first_passenger['Train Number']})\n"
                f"Journey: {first_passenger['From']} to "
                f"{first_passenger['To']}"
            ),
            bg="white",
            fg=self.dark_color,
            font=("Arial", 11, "bold"),
            justify="left"
        )
        booking_info.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # Bottom Button Container
        button_frame = tk.Frame(
            main_frame,
            bg="white"
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=10
        )

        # Cancel Entire Booking Button
        tk.Button(
            button_frame,
            text="CANCEL ENTIRE BOOKING",
            command=lambda: self.cancel_entire_booking(),
            bg="#DC2626",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # Back Button
        tk.Button(
            button_frame,
            text="BACK TO CANCEL TICKETS",
            command=lambda: self.show_screen("Cancel Tickets"),
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(
            side="left"
        )

        # Scrollable Passenger Details
        details_container = tk.Frame(
            main_frame,
            bg="white"
        )
        details_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        canvas = tk.Canvas(
            details_container,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            details_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        passenger_frame = tk.Frame(
            canvas,
            bg="white"
        )

        window = canvas.create_window(
            (0, 0),
            window=passenger_frame,
            anchor="nw"
        )

        def update_scroll(event):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        passenger_frame.bind(
            "<Configure>",
            update_scroll
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                window,
                width=event.width
            )
        )

        # Display Passenger Cards
        for index, passenger in enumerate(
            self.cancel_matched_passengers,
            start=1
        ):

            passenger_card = tk.Frame(
                passenger_frame,
                bg="#F4F7FC",
                highlightbackground="#E2E8F0",
                highlightthickness=1
            )
            passenger_card.pack(
                fill="x",
                padx=5,
                pady=8
            )

            tk.Label(
                passenger_card,
                text=f"Passenger {index}",
                bg="#F4F7FC",
                fg=self.primary_color,
                font=("Arial", 12, "bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(12, 8)
            )

            passenger_details = [
                f"Name: {passenger['Name']}",
                f"Email: {passenger['Email']}",
                f"Mobile: {passenger['Mobile']}"
            ]

            for detail in passenger_details:
                tk.Label(
                    passenger_card,
                    text=detail,
                    bg="#F4F7FC",
                    fg=self.dark_color,
                    font=("Arial", 10)
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=4
                )

            tk.Frame(
                passenger_card,
                bg="#F4F7FC",
                height=8
            ).pack()

            # Cancel Individual Passenger Button
            tk.Button(
                passenger_card,
                text="CANCEL PASSENGER",
                command=lambda p=passenger: self.cancel_single_passenger(p),
                bg="#DC2626",
                fg="white",
                relief="flat",
                padx=20,
                pady=8,
                font=("Arial", 9, "bold"),
                cursor="hand2"
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 12)
            )

    def cancel_entire_booking(self):
        booking_id = self.cancel_selected_booking_id
        matched_passengers = [
            passenger
            for passenger in self.railway.passengers
            if str(passenger["Booking ID"]) == str(booking_id)
        ]

        if not matched_passengers:
            messagebox.showerror(
                "Booking Not Found",
                "No passengers found for this Booking ID."
            )
            return

        passenger_count = len(matched_passengers)
        confirm = messagebox.askyesno(
            "Cancel Entire Booking",
            f"Are you sure you want to cancel the entire booking?\n\n"
            f"Booking ID: {booking_id}\n"
            f"Total Passengers: {passenger_count}\n\n"
            f"All {passenger_count} passenger tickets will be cancelled."
        )
        if not confirm:
            return

        # Restore seats only for Local bookings. API bookings are local demo
        # records and must never be written into trains.txt.
        seat_restore_counts = {}
        for passenger in matched_passengers:
            source = passenger.get("Train Source", "Local")
            if source == "API":
                continue
            train_number = str(passenger["Train Number"])
            seat_restore_counts[train_number] = (
                seat_restore_counts.get(train_number, 0) + 1
            )

        for train_number in seat_restore_counts:
            if not any(
                str(train[1]) == train_number
                for train in self.railway.Trains
            ):
                messagebox.showerror(
                    "Train Not Found",
                    f"Local train {train_number} was not found.\n"
                    "Booking cancellation could not be completed."
                )
                return

        updated_trains = []
        for train in self.railway.Trains:
            train_number = str(train[1])
            if train_number in seat_restore_counts:
                train_list = list(train)
                train_list[7] += seat_restore_counts[train_number]
                train = tuple(train_list)
            updated_trains.append(train)
        self.railway.Trains = updated_trains

        self.railway.passengers = [
            passenger for passenger in self.railway.passengers
            if str(passenger["Booking ID"]) != str(booking_id)
        ]
        self.railway.all_booked_tickets = [
            booking for booking in self.railway.all_booked_tickets
            if str(booking["Booking ID"]) != str(booking_id)
        ]

        # Release the in-session API demo seat count when available.
        for passenger in matched_passengers:
            if passenger.get("Train Source") == "API":
                key = (
                    str(passenger.get("Train Number")),
                    passenger.get("From Code"),
                    passenger.get("To Code"),
                    passenger.get("Journey Date")
                )
                if key in getattr(self, "api_booking_seat_counts", {}):
                    self.api_booking_seat_counts[key] += 1

        self.railway.save_trains()
        self.railway.save_passengers()
        self.railway.save_bookings()
        self.cancel_matched_passengers = []

        messagebox.showinfo(
            "Booking Cancelled",
            f"Entire booking cancelled successfully!\n\n"
            f"Booking ID: {booking_id}\n"
            f"Passengers Cancelled: {passenger_count}\n"
            f"Local Seats Restored: {sum(seat_restore_counts.values())}"
        )
        self.show_screen("Cancel Tickets")

    def cancel_single_passenger(self, passenger):
        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Are you sure you want to cancel the ticket for "
            f"{passenger['Name']}?"
        )
        if not confirm:
            return

        booking_id = passenger["Booking ID"]
        matched_passenger = next(
            (p for p in self.railway.passengers if p == passenger),
            None
        )

        if matched_passenger is None:
            messagebox.showerror(
                "Cancellation Failed",
                "Passenger record not found."
            )
            return

        # Restore a seat only when this is a Local train booking.
        if passenger.get("Train Source", "Local") != "API":
            for index, train in enumerate(self.railway.Trains):
                if train[1] == passenger["Train Number"]:
                    temp = list(train)
                    temp[7] += 1
                    self.railway.Trains[index] = tuple(temp)
                    break
        else:
            key = (
                str(passenger.get("Train Number")),
                passenger.get("From Code"),
                passenger.get("To Code"),
                passenger.get("Journey Date")
            )
            if key in getattr(self, "api_booking_seat_counts", {}):
                self.api_booking_seat_counts[key] += 1

        self.railway.passengers.remove(matched_passenger)
        self.railway.all_booked_tickets = [
            booking for booking in self.railway.all_booked_tickets
            if booking != passenger
        ]

        self.railway.save_trains()
        self.railway.save_passengers()
        self.railway.save_bookings()

        messagebox.showinfo(
            "Cancellation Successful",
            f"Ticket for {passenger['Name']} has been cancelled successfully."
        )

        remaining_passengers = [
            p for p in self.railway.passengers
            if str(p["Booking ID"]) == str(booking_id)
        ]

        if remaining_passengers:
            self.cancel_matched_passengers = remaining_passengers
            self.show_cancel_passenger_details()
        else:
            messagebox.showinfo(
                "Booking Completed",
                "All passengers under this Booking ID have been cancelled."
            )
            self.show_screen("Cancel Tickets")

    def show_book_tickets(self):

        # Main Scrollable Container
        scroll_container = tk.Frame(self.content, bg="#F4F7FC")
        scroll_container.pack(fill="both", expand=True, padx=25, pady=20)

        canvas = tk.Canvas(scroll_container, bg="#F4F7FC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        main_frame = tk.Frame(canvas, bg="#F4F7FC")
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        main_frame.bind("<Configure>", update_scroll_region)
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(canvas_window, width=event.width)
        )

        def on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)

        booking_card = tk.Frame(
            main_frame, bg="white",
            highlightbackground="#DCE3ED", highlightthickness=1
        )
        booking_card.pack(fill="x", padx=10, pady=10)

        tk.Label(
            booking_card, text="Book Your Tickets",
            font=("Segoe UI", 18, "bold"), bg="white", fg="#123456"
        ).pack(anchor="w", padx=25, pady=(25, 5))

        tk.Label(
            booking_card,
            text="Select your train and enter passenger count.",
            font=("Segoe UI", 10), bg="white", fg="#64748B"
        ).pack(anchor="w", padx=25, pady=(0, 25))

        tk.Label(
            booking_card, text="Select Train",
            font=("Segoe UI", 11, "bold"), bg="white", fg="#1E293B"
        ).pack(anchor="w", padx=25, pady=(5, 8))

        # Keep an exact option-to-record mapping so duplicate train numbers
        # from Local and API sources cannot select the wrong train.
        self.booking_train_lookup = {}
        train_options = []

        for train in self.railway.Trains:
            if isinstance(train[7], (int, float)) and train[7] > 0:
                option = (
                    f"{train[1]} - {train[0]} | {train[3]} to {train[4]} "
                    f"| Seats: {train[7]} [Local]"
                )
                train_options.append(option)
                self.booking_train_lookup[option] = {
                    "source": "Local",
                    "train": train
                }

        if not hasattr(self, "api_booking_seat_counts"):
            self.api_booking_seat_counts = {}

        if not hasattr(self, "platform_cache"):
            self.platform_cache = {}

        if hasattr(self, "api_trains") and self.api_trains:
            journey_date = getattr(self, "selected_journey_date", "")
            for api_train in self.api_trains:
                seat_count = self.get_api_availability_count(api_train)
                seat_key = (
                    str(api_train.get("train_number")),
                    api_train.get("from_station_code"),
                    api_train.get("to_station_code"),
                    journey_date
                )
                seat_count = self.api_booking_seat_counts.get(seat_key, seat_count)

                # Unknown, zero, and non-numeric availability cannot be booked.
                if not isinstance(seat_count, int) or isinstance(seat_count, bool) or seat_count <= 0:
                    continue

                train_number = api_train.get("train_number")
                train_name = api_train.get("train_name", "N/A")
                from_name = api_train.get("from_station_name", "N/A")
                to_name = api_train.get("to_station_name", "N/A")
                option = (
                    f"{train_number} - {train_name} | {from_name} to {to_name} "
                    f"| Seats: {seat_count} [API]"
                )
                train_options.append(option)
                self.booking_train_lookup[option] = {
                    "source": "API",
                    "train": api_train,
                    "seat_count": seat_count,
                    "seat_key": seat_key,
                    "journey_date": journey_date
                }

        self.booking_train_var = tk.StringVar()
        self.booking_train_combo = ttk.Combobox(
            booking_card,
            textvariable=self.booking_train_var,
            values=train_options,
            state="readonly",
            font=("Segoe UI", 10),
            width=65
        )
        self.booking_train_combo.pack(
            anchor="w", padx=25, pady=(0, 20), ipady=5
        )

        tk.Label(
            booking_card, text="Number of Passengers",
            font=("Segoe UI", 11, "bold"), bg="white", fg="#1E293B"
        ).pack(anchor="w", padx=25, pady=(5, 8))

        self.booking_count_var = tk.StringVar(value="1")
        ttk.Entry(
            booking_card, textvariable=self.booking_count_var,
            font=("Segoe UI", 10), width=20
        ).pack(anchor="w", padx=25, pady=(0, 25))

        tk.Button(
            booking_card, text="Continue",
            font=("Segoe UI", 10, "bold"),
            bg="#1769AA", fg="white",
            activebackground="#123456", activeforeground="white",
            relief="flat", cursor="hand2", padx=30, pady=10,
            command=self.validate_booking_selection
        ).pack(anchor="w", padx=25, pady=(0, 25))

    def validate_booking_selection(self):
        selected_option = self.booking_train_var.get()
        passenger_count = self.booking_count_var.get()

        if not selected_option:
            messagebox.showwarning("Select Train", "Please select a train first.")
            return

        if not passenger_count.isdigit() or int(passenger_count) <= 0:
            messagebox.showwarning(
                "Invalid Passenger Count",
                "Please enter a valid number of passengers."
            )
            return

        selected_record = self.booking_train_lookup.get(selected_option)
        if not selected_record:
            messagebox.showerror(
                "Train Not Found",
                "The selected train details could not be found. Please reopen Book Tickets."
            )
            return

        passenger_count = int(passenger_count)
        source = selected_record["source"]

        if source == "Local":
            train = selected_record["train"]
            available_seats = train[7]
            normalized_train = train
        else:
            api_train = selected_record["train"]
            available_seats = selected_record["seat_count"]
            platform_key = (
                api_train.get("train_number"),
                api_train.get("from_station_code")
            )
            platform = getattr(self, "platform_cache", {}).get(platform_key, "N/A")
            normalized_train = (
                api_train.get("train_name", "N/A"),
                api_train.get("train_number"),
                platform,
                api_train.get("from_station_name", "N/A"),
                api_train.get("to_station_name", "N/A"),
                api_train.get("departure_time", "N/A"),
                api_train.get("arrival_time", "N/A"),
                available_seats
            )

        if passenger_count > available_seats:
            messagebox.showwarning(
                "Seats Unavailable",
                f"Only {available_seats} seats are available."
            )
            return

        self.selected_train_for_booking = normalized_train
        self.selected_train_source = source
        self.selected_api_train = (
            selected_record if source == "API" else None
        )
        self.booking_passenger_count = passenger_count
        self.show_passenger_details()

    def show_passenger_details(self):
        self.clear_content()
        self.create_header(
            "Passenger Details",
            "Enter the details of each passenger."
        )

        # Main container
        main_frame = tk.Frame(
            self.content,
            bg=self.bg_color
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        # Back Button
        tk.Button(
            main_frame,
            text="← Back",
            command=lambda: self.show_screen("Book Tickets"),
            bg=self.primary_color,
            fg="white",
            activebackground="#123456",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        # Scrollable Canvas
        canvas = tk.Canvas(
            main_frame,
            bg=self.bg_color,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Inner frame
        form_frame = tk.Frame(
            canvas,
            bg=self.bg_color
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=form_frame,
            anchor="nw"
        )

        def update_scroll_region(event=None):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        form_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        def on_mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            on_mousewheel
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                canvas_window,
                width=event.width
            )
        )

        # Selected train information
        train = self.selected_train_for_booking

        tk.Label(
            form_frame,
            text=f"{train[0]} | Train No: {train[1]} | "
                 f"{train[3]} to {train[4]}",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        ).pack(fill="x", pady=(0, 15))

        # Passenger forms container
        self.passenger_entries = []
        print("Passenger forms section started")

        for i in range(self.booking_passenger_count):
            print("Passenger form created:", i + 1)
            passenger_frame = tk.LabelFrame(
                form_frame,
                text=f"Passenger {i + 1}",
                bg="white",
                fg=self.primary_color,
                font=("Arial", 11, "bold"),
                padx=15,
                pady=12
            )

            passenger_frame.pack(
                fill="x",
                pady=8
            )
            fields = {}

            for field in ["Name", "Email", "Mobile Number"]:
                tk.Label(
                    passenger_frame,
                    text=field,
                    bg="white",
                    fg=self.dark_color,
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(5, 3))

                entry = ttk.Entry(
                    passenger_frame,
                    font=("Arial", 10)
                )

                entry.pack(
                    fill="x",
                    pady=(0, 8)
                )
                fields[field] = entry
            self.passenger_entries.append(fields)
        print("Reached Confirm Booking button section")

        # Confirm Booking Button
        confirm_button = tk.Button(
            form_frame,
            text="CONFIRM BOOKING",
            font=("Arial", 12, "bold"),
            bg="#1769AA",
            fg="white",
            relief="flat",
            padx=30,
            pady=12,
            command=self.confirm_booking
        )

        confirm_button.pack(
            fill="x",
            padx=10,
            pady=15
        )

        confirm_button.lift()
        print("Confirm Booking button created successfully")

    def confirm_booking(self):
        # Validate all passenger details first.
        new_passengers = []

        for i, fields in enumerate(self.passenger_entries):
            Name = fields["Name"].get().strip()
            Email = fields["Email"].get().strip()
            Mobile_Number = fields["Mobile Number"].get().strip()

            if not Name:
                messagebox.showwarning(
                    "Missing Name",
                    f"Please enter the name of Passenger {i + 1}."
                )
                return

            if not re.match(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                Email
            ):
                messagebox.showwarning(
                    "Invalid Email",
                    f"Please enter a valid email for Passenger {i + 1}."
                )
                return

            if not re.match(r"^[6-9]\d{9}$", Mobile_Number):
                messagebox.showwarning(
                    "Invalid Mobile Number",
                    f"Please enter a valid 10-digit mobile number for Passenger {i + 1}."
                )
                return

            new_passengers.append({
                "Name": Name,
                "Email": Email,
                "Mobile": int(Mobile_Number)
            })

        source = getattr(self, "selected_train_source", "Local")
        selected_train = self.selected_train_for_booking
        train_number = selected_train[1]
        passenger_count = len(new_passengers)

        if source == "Local":
            train_index = next(
                (
                    i for i, train in enumerate(self.railway.Trains)
                    if train[1] == train_number
                ),
                None
            )

            if train_index is None:
                messagebox.showerror(
                    "Train Not Found",
                    "The selected train is no longer available."
                )
                return

            current_train = self.railway.Trains[train_index]
            available_seats = current_train[7]
        else:
            api_selection = self.selected_api_train
            api_train = api_selection["train"]
            current_train = selected_train
            train_index = None
            seat_key = api_selection["seat_key"]
            available_seats = self.api_booking_seat_counts.get(
                seat_key, api_selection["seat_count"]
            )

        if passenger_count > available_seats:
            messagebox.showwarning(
                "Seats Unavailable",
                f"Only {available_seats} seats are currently available."
            )
            return

        # Generate one unique 5-digit Booking ID for the whole group.
        existing_ids = {
            str(booking["Booking ID"])
            for booking in self.railway.all_booked_tickets
        }

        while True:
            Booking_id = random.randint(10000, 99999)
            if str(Booking_id) not in existing_ids:
                break

        # Preserve the common record structure used by all ticket screens.
        for passenger in new_passengers:
            booking_record = {
                "Booking ID": Booking_id,
                "Name": passenger["Name"],
                "Email": passenger["Email"],
                "Mobile": passenger["Mobile"],
                "Train Name": current_train[0],
                "Train Number": current_train[1],
                "Platform": current_train[2],
                "From": current_train[3],
                "To": current_train[4],
                "Departure": current_train[5],
                "Arrival": current_train[6],
                "Train Source": source
            }

            if source == "API":
                booking_record.update({
                    "Journey Date": api_selection.get("journey_date", ""),
                    "From Code": api_train.get("from_station_code", ""),
                    "To Code": api_train.get("to_station_code", "")
                })

            self.railway.passengers.append(booking_record)
            self.railway.all_booked_tickets.append(booking_record)

        if source == "Local":
            self.railway.Trains[train_index] = (
                current_train[:7] +
                (current_train[7] - passenger_count,)
            )
            self.railway.save_trains()
        else:
            # Keep API availability updated for this app session only.
            self.api_booking_seat_counts[seat_key] = (
                available_seats - passenger_count
            )

        # Save both local and API demo bookings in the existing TXT files.
        self.railway.save_passengers()
        self.railway.save_bookings()

        messagebox.showinfo(
            "Booking Successful",
            f"Your tickets have been booked successfully!\n\n"
            f"Booking ID: {Booking_id}\n"
            f"Passengers: {passenger_count}\n"
            f"Train: {current_train[0]}"
        )

        self.show_screen("Book Tickets")

    def show_booked_tickets(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Search Heading
        tk.Label(
            main_frame,
            text="Find Your Booking",
            bg="white",
            fg=self.dark_color,
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            main_frame,
            text="Enter your Booking ID to view complete reservation details.",
            bg="white",
            fg=self.secondary_color,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        # Search Container
        search_frame = tk.Frame(
            main_frame,
            bg="#F4F7FC"
        )
        search_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.booked_booking_id_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="flat",
            bg="white"
        )
        self.booked_booking_id_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=12,
            pady=12,
            ipady=9
        )

        self.booked_booking_id_entry.insert(
            0,
            "Enter Booking ID"
        )

        def search_booked_booking():
            booking_id = self.booked_booking_id_entry.get().strip()
            # Clear previous results
            for widget in self.booked_result_frame.winfo_children():
                widget.destroy()

            if not booking_id:
                messagebox.showwarning(
                    "Missing Booking ID",
                    "Please enter your Booking ID."
                )
                return

            if not booking_id.isdigit():
                messagebox.showwarning(
                    "Invalid Booking ID",
                    "Booking ID must contain digits only."
                )
                return

            # Find passengers using Booking ID
            matched_passengers = [
                passenger
                for passenger in self.railway.passengers
                if str(passenger["Booking ID"]) == booking_id
            ]

            if not matched_passengers:
                tk.Label(
                    self.booked_result_frame,
                    text="No booking found for this Booking ID.",
                    bg="white",
                    fg="#DC2626",
                    font=("Arial", 11, "bold")
                ).pack(pady=30)
                return

            # Store matching records
            self.booked_matched_passengers = matched_passengers

            # Booking Summary Block
            first_passenger = matched_passengers[0]
            summary_frame = tk.Frame(
                self.booked_result_frame,
                bg="#EFF6FF",
                highlightbackground="#BFDBFE",
                highlightthickness=1
            )
            summary_frame.pack(
                fill="x",
                pady=(5, 15)
            )

            tk.Label(
                summary_frame,
                text="BOOKING SUMMARY",
                bg="#EFF6FF",
                fg=self.primary_color,
                font=("Arial", 11, "bold")
            ).pack(
                anchor="w",
                padx=18,
                pady=(15, 8)
            )

            summary_details = tk.Frame(
                summary_frame,
                bg="#EFF6FF"
            )
            summary_details.pack(
                fill="x",
                padx=18,
                pady=(0, 15)
            )

            # Booking ID Block
            booking_id_card = tk.Frame(
                summary_details,
                bg="white"
            )
            booking_id_card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(0, 8)
            )

            tk.Label(
                booking_id_card,
                text="BOOKING ID",
                bg="white",
                fg=self.secondary_color,
                font=("Arial", 9, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(12, 4)
            )

            tk.Label(
                booking_id_card,
                text=booking_id,
                bg="white",
                fg=self.dark_color,
                font=("Arial", 16, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(0, 12)
            )

            # Passenger Count Block
            passenger_count_card = tk.Frame(
                summary_details,
                bg="white"
            )
            passenger_count_card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(8, 0)
            )

            tk.Label(
                passenger_count_card,
                text="TOTAL PASSENGERS",
                bg="white",
                fg=self.secondary_color,
                font=("Arial", 9, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(12, 4)
            )

            tk.Label(
                passenger_count_card,
                text=str(len(matched_passengers)),
                bg="white",
                fg=self.dark_color,
                font=("Arial", 16, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(0, 12)
            )

            # Modern Train Journey Card
            train_frame = tk.Frame(
                self.booked_result_frame,
                bg="white",
                highlightbackground="#BFDBFE",
                highlightthickness=1
            )
            train_frame.pack(
                fill="x",
                pady=(0, 18)
            )

            # Top Section
            train_top = tk.Frame(
                train_frame,
                bg="white"
            )
            train_top.pack(
                fill="x",
                padx=20,
                pady=(15, 10)
            )

            tk.Label(
                train_top,
                text="TRAIN JOURNEY",
                bg="white",
                fg=self.primary_color,
                font=("Arial", 11, "bold")
            ).pack(side="left")

            tk.Label(
                train_top,
                text="BOOKING CONFIRMED",
                bg="#DCFCE7",
                fg="#15803D",
                font=("Arial", 9, "bold"),
                padx=10,
                pady=5
            ).pack(side="right")

            # Train Name and Number
            tk.Label(
                train_frame,
                text=(
                    f"{first_passenger['Train Name']}  |  "
                    f"Train No. {first_passenger['Train Number']}"
                ),
                bg="white",
                fg=self.dark_color,
                font=("Arial", 14, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(5, 2)
            )

            tk.Label(
                train_frame,
                text=f"Platform: {first_passenger['Platform']}",
                bg="white",
                fg=self.secondary_color,
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

            # Journey Route
            route_frame = tk.Frame(
                train_frame,
                bg="#EFF6FF"
            )
            route_frame.pack(
                fill="x",
                padx=15,
                pady=(0, 15)
            )

            # Departure
            departure_frame = tk.Frame(
                route_frame,
                bg="#EFF6FF"
            )
            departure_frame.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=15
            )

            tk.Label(
                departure_frame,
                text=first_passenger["Departure"],
                bg="#EFF6FF",
                fg=self.dark_color,
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            tk.Label(
                departure_frame,
                text=first_passenger["From"],
                bg="#EFF6FF",
                fg=self.primary_color,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", pady=4)

            tk.Label(
                departure_frame,
                text="DEPARTURE",
                bg="#EFF6FF",
                fg=self.secondary_color,
                font=("Arial", 8, "bold")
            ).pack(anchor="w")

            # Route Arrow
            tk.Label(
                route_frame,
                text="➜",
                bg="#EFF6FF",
                fg=self.primary_color,
                font=("Arial", 22, "bold")
            ).pack(
                side="left",
                padx=5
            )

            # Arrival
            arrival_frame = tk.Frame(
                route_frame,
                bg="#EFF6FF"
            )
            arrival_frame.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=15
            )

            tk.Label(
                arrival_frame,
                text=first_passenger["Arrival"],
                bg="#EFF6FF",
                fg=self.dark_color,
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            tk.Label(
                arrival_frame,
                text=first_passenger["To"],
                bg="#EFF6FF",
                fg=self.primary_color,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", pady=4)

            tk.Label(
                arrival_frame,
                text="ARRIVAL",
                bg="#EFF6FF",
                fg=self.secondary_color,
                font=("Arial", 8, "bold")
            ).pack(anchor="w")

            # Passenger Information Heading
            tk.Label(
                self.booked_result_frame,
                text="PASSENGER INFORMATION",
                bg="white",
                fg=self.primary_color,
                font=("Arial", 12, "bold")
            ).pack(
                anchor="w",
                pady=(5, 10)
            )

            # Individual Passenger Blocks
            for index, passenger in enumerate(matched_passengers, start=1):
                passenger_card = tk.Frame(
                    self.booked_result_frame,
                    bg="#F8FAFC",
                    highlightbackground="#E2E8F0",
                    highlightthickness=1
                )
                passenger_card.pack(
                    fill="x",
                    pady=6
                )

                tk.Label(
                    passenger_card,
                    text=f"PASSENGER {index}",
                    bg="#F8FAFC",
                    fg=self.primary_color,
                    font=("Arial", 10, "bold")
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(12, 6)
                )

                for detail in [
                    f"Name: {passenger['Name']}",
                    f"Email: {passenger['Email']}",
                    f"Mobile: {passenger['Mobile']}"
                ]:

                    tk.Label(
                        passenger_card,
                        text=detail,
                        bg="#F8FAFC",
                        fg=self.dark_color,
                        font=("Arial", 10)
                    ).pack(
                        anchor="w",
                        padx=15,
                        pady=3
                    )

                tk.Frame(
                    passenger_card,
                    bg="#F8FAFC",
                    height=8
                ).pack()


        # Search Button
        tk.Button(
            search_frame,
            text="SEARCH BOOKING",
            command=search_booked_booking,
            bg=self.primary_color,
            fg="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        ).pack(
            side="right",
            padx=12
        )

        # Scrollable Booking Results Container
        result_container = tk.Frame(
            main_frame,
            bg="white"
        )
        result_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # Canvas
        self.booked_result_canvas = tk.Canvas(
            result_container,
            bg="white",
            highlightthickness=0
        )
        self.booked_result_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Vertical Scrollbar
        booked_scrollbar = ttk.Scrollbar(
            result_container,
            orient="vertical",
            command=self.booked_result_canvas.yview
        )
        booked_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.booked_result_canvas.configure(
            yscrollcommand=booked_scrollbar.set
        )

        # Inner Frame
        self.booked_result_frame = tk.Frame(
            self.booked_result_canvas,
            bg="white"
        )

        booked_window = self.booked_result_canvas.create_window(
            (0, 0),
            window=self.booked_result_frame,
            anchor="nw"
        )

        # Update Scroll Region
        def update_booked_scroll(event):
            self.booked_result_canvas.configure(
                scrollregion=self.booked_result_canvas.bbox("all")
            )

        self.booked_result_frame.bind(
            "<Configure>",
            update_booked_scroll
        )

        # Match Inner Frame Width with Canvas
        self.booked_result_canvas.bind(
            "<Configure>",
            lambda event: self.booked_result_canvas.itemconfig(
                booked_window,
                width=event.width
            )
        )

        def on_booked_mousewheel(event):
            self.booked_result_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        self.booked_result_canvas.bind(
            "<Enter>",
            lambda event: self.booked_result_canvas.bind_all(
                "<MouseWheel>",
                on_booked_mousewheel
            )
        )

        self.booked_result_canvas.bind(
            "<Leave>",
            lambda event: self.booked_result_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

    def show_ticket_details(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            main_frame,
            text="Generated Ticket Details",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(
            main_frame,
            text="View all confirmed passenger tickets.",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(anchor="w", padx=20)
        search_frame = tk.Frame(main_frame, bg="white")
        search_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(
            search_frame,
            text="Enter Booking ID",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(side="left", padx=(0, 10))

        self.ticket_booking_id_entry = ttk.Entry(
            search_frame,
            width=25
        )
        self.ticket_booking_id_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="SEARCH TICKET",
            command=self.search_ticket_details,
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=15,
            pady=9
        ).pack(side="left", padx=10)

        # Scrollable Ticket Result Area
        result_container = tk.Frame(main_frame, bg="white")
        result_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        ticket_canvas = tk.Canvas(
            result_container,
            bg="white",
            highlightthickness=0
        )
        ticket_canvas.pack(side="left", fill="both", expand=True)

        ticket_scrollbar = ttk.Scrollbar(
            result_container,
            orient="vertical",
            command=ticket_canvas.yview
        )
        ticket_scrollbar.pack(side="right", fill="y")

        ticket_canvas.configure(
            yscrollcommand=ticket_scrollbar.set
        )

        self.ticket_result_frame = tk.Frame(
            ticket_canvas,
            bg="white"
        )

        ticket_window = ticket_canvas.create_window(
            (0, 0),
            window=self.ticket_result_frame,
            anchor="nw"
        )

        def update_ticket_scroll(event):
            ticket_canvas.configure(
                scrollregion=ticket_canvas.bbox("all")
            )

        self.ticket_result_frame.bind(
            "<Configure>",
            update_ticket_scroll
        )

        ticket_canvas.bind(
            "<Configure>",
            lambda event: ticket_canvas.itemconfig(
                ticket_window,
                width=event.width
            )
        )

        def on_ticket_mousewheel(event):
            ticket_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        ticket_canvas.bind(
            "<Enter>",
            lambda event: ticket_canvas.bind_all(
                "<MouseWheel>",
                on_ticket_mousewheel
            )
        )

        ticket_canvas.bind(
            "<Leave>",
            lambda event: ticket_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

        if not self.railway.passengers:
            tk.Label(
                self.ticket_result_frame,
                text="There are no booked tickets.",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="red"
            ).pack(pady=30)
            return

    def search_ticket_details(self):
        booking_id = self.ticket_booking_id_entry.get().strip()

        for widget in self.ticket_result_frame.winfo_children():
            widget.destroy()

        if not booking_id:
            messagebox.showwarning(
                "Missing Booking ID",
                "Please enter a Booking ID."
            )
            return

        if not booking_id.isdigit():
            messagebox.showwarning(
                "Invalid Booking ID",
                "Booking ID must contain only digits."
            )
            return

        matched_passengers = [
            passenger
            for passenger in self.railway.passengers
            if str(passenger["Booking ID"]) == booking_id
        ]
        print("Booking ID:", booking_id)
        print("Matched Passengers:", len(matched_passengers))

        for passenger in matched_passengers:
            print(passenger["Name"])

        if not matched_passengers:
            tk.Label(
                self.ticket_result_frame,
                text="No ticket found for this Booking ID.",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="red"
            ).pack(pady=30)
            return

        self.ticket_print_button = tk.Button(
            self.ticket_result_frame,
            text="🖨 PRINT TICKET",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.print_ticket_details
        )
        self.ticket_print_button.pack(anchor="e", pady=10)
        self.ticket_matched_passengers = matched_passengers

        for index, passenger in enumerate(matched_passengers, start=1):
            print("Creating ticket card:", index, passenger["Name"])
            ticket_card = tk.Frame(
                self.ticket_result_frame,
                bg="#F8FAFC",
                highlightbackground=self.border_color,
                highlightthickness=1
            )
            ticket_card.pack(fill="x", pady=10)

            tk.Label(
                ticket_card,
                text=f"TICKET {index}",
                font=("Segoe UI", 13, "bold"),
                bg="#1769AA",
                fg="white",
                padx=15,
                pady=10
            ).pack(fill="x")

            details = [
                ("Booking ID", passenger["Booking ID"]),
                ("Passenger Name", passenger["Name"]),
                ("Email", passenger["Email"]),
                ("Mobile Number", passenger["Mobile"]),
                ("Train Name", passenger["Train Name"]),
                ("Train Number", passenger["Train Number"]),
                ("Platform", passenger["Platform"]),
                ("From", passenger["From"]),
                ("To", passenger["To"]),
                ("Departure", passenger["Departure"]),
                ("Arrival", passenger["Arrival"]),
                ("Seats Booked", 1)
            ]

            for label_text, value in details:
                row = tk.Frame(ticket_card, bg="#F8FAFC")
                row.pack(fill="x", padx=15, pady=4)

                tk.Label(
                    row,
                    text=label_text,
                    font=("Segoe UI", 10, "bold"),
                    bg="#F8FAFC",
                    fg=self.dark_color,
                    width=18,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    row,
                    text=str(value),
                    font=("Segoe UI", 10),
                    bg="#F8FAFC",
                    fg=self.dark_color
                ).pack(side="left")

    
    def print_ticket_details(self):
        if not hasattr(self, "ticket_matched_passengers"):
            messagebox.showwarning(
                "No Ticket",
                "Please search a Booking ID first."
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"Railway_Ticket_{self.ticket_matched_passengers[0]['Booking ID']}.pdf"
        )

        if not file_path:
            return

        try:
            pdf = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "TicketTitle",
                parent=styles["Title"],
                fontSize=20,
                textColor=colors.HexColor("#1769AA"),
                alignment=TA_CENTER,
                spaceAfter=10
            )
            story = []
            passengers = self.ticket_matched_passengers
            first_passenger = passengers[0]

            story.append(Paragraph(
                "RAILWAY MANAGEMENT SYSTEM",
                title_style
            ))

            story.append(Paragraph(
                "CONFIRMED JOURNEY TICKET",
                styles["Heading2"]
            ))
            story.append(Spacer(1, 15))

            journey_data = [
                ["BOOKING ID", str(first_passenger["Booking ID"])],
                ["TRAIN NAME", str(first_passenger["Train Name"])],
                ["TRAIN NUMBER", str(first_passenger["Train Number"])],
                ["PLATFORM", str(first_passenger["Platform"])],
                ["FROM", str(first_passenger["From"])],
                ["TO", str(first_passenger["To"])],
                ["DEPARTURE", str(first_passenger["Departure"])],
                ["ARRIVAL", str(first_passenger["Arrival"])],
                ["TOTAL PASSENGERS", str(len(passengers))]
            ]

            journey_table = Table(
                journey_data,
                colWidths=[160, 300]
            )

            journey_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#123456")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey)
            ]))
            story.append(journey_table)
            story.append(Spacer(1, 20))
            story.append(Paragraph(
                "PASSENGER DETAILS",
                styles["Heading2"]
            ))

            for index, passenger in enumerate(passengers, start=1):
                passenger_data = [
                    ["Passenger", f"TICKET {index}"],
                    ["Name", str(passenger["Name"])],
                    ["Email", str(passenger["Email"])],
                    ["Mobile", str(passenger["Mobile"])],
                    ["Seats Booked", "1"]
                ]

                passenger_table = Table(
                    passenger_data,
                    colWidths=[160, 300]
                )

                passenger_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1769AA")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("PADDING", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey)
                ]))
                story.append(passenger_table)
                story.append(Spacer(1, 12))
            story.append(Spacer(1, 15))
            story.append(Paragraph(
                "Thank you for choosing Railway Management System.",
                ParagraphStyle(
                    "Footer",
                    parent=styles["Normal"],
                    alignment=TA_CENTER,
                    textColor=colors.grey
                )
            ))
            pdf.build(story)
            messagebox.showinfo(
                "Ticket Generated",
                f"PDF ticket saved successfully:\n{file_path}"
            )
            os.startfile(file_path)

        except Exception as e:
            messagebox.showerror(
                "PDF Error",
                f"Unable to generate ticket:\n{e}"
            )

    def show_admin_options(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        tk.Label(
            main_frame,
            text="WELCOME TO ADMIN PORTAL",
            font=("Segoe UI", 23, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(70, 10))

        tk.Label(
            main_frame,
            text="Create a new account or login to continue",
            font=("Segoe UI", 11),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 40))

        options_frame = tk.Frame(
            main_frame,
            bg="white"
        )
        options_frame.pack()

        # Create Account Button
        create_frame = tk.Frame(
            options_frame,
            bg="#F4F7FC",
            width=260,
            height=190,
            highlightbackground="#DCE4EF",
            highlightthickness=1
        )
        create_frame.pack(side="left", padx=20)
        create_frame.pack_propagate(False)

        tk.Label(
            create_frame,
            text="👤",
            font=("Segoe UI Emoji", 35),
            bg="#F4F7FC"
        ).pack(pady=(20, 5))

        tk.Label(
            create_frame,
            text="Create Account",
            font=("Segoe UI", 14, "bold"),
            bg="#F4F7FC",
            fg=self.dark_color
        ).pack(pady=5)

        tk.Button(
            create_frame,
            text="CREATE ACCOUNT",
            bg=self.primary_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.show_screen("Admin Create Account")
        ).pack(pady=12)

        # Login Account Button
        login_frame = tk.Frame(
            options_frame,
            bg="#F4F7FC",
            width=260,
            height=190,
            highlightbackground="#DCE4EF",
            highlightthickness=1
        )
        login_frame.pack(side="left", padx=20)
        login_frame.pack_propagate(False)

        tk.Label(
            login_frame,
            text="🔐",
            font=("Segoe UI Emoji", 35),
            bg="#F4F7FC"
        ).pack(pady=(20, 5))

        tk.Label(
            login_frame,
            text="Login Account",
            font=("Segoe UI", 14, "bold"),
            bg="#F4F7FC",
            fg=self.dark_color
        ).pack(pady=5)

        tk.Button(
            login_frame,
            text="LOGIN ACCOUNT",
            bg=self.primary_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.show_screen("Admin Login")
        ).pack(pady=12)

    def show_admin_login(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        login_card = tk.Frame(
            main_frame,
            bg="white"
        )
        login_card.place(
            relx=0.5,
            rely=0.45,
            anchor="center"
        )

        tk.Label(
            login_card,
            text="ADMIN LOGIN",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(10, 5))

        tk.Label(
            login_card,
            text="Sign in to access the Admin Portal",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 25))

        tk.Label(
            login_card,
            text="Admin ID",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w")

        self.admin_id_entry = ttk.Entry(
            login_card,
            width=38
        )
        self.admin_id_entry.pack(pady=(7, 18), ipady=5)

        tk.Label(
            login_card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w")

         # Password Frame
        password_frame = tk.Frame(
            login_card,
            bg="white"
        )
        password_frame.pack(
            fill="x",
            pady=(7, 22)
        )

        self.admin_password_entry = ttk.Entry(
            password_frame,
            width=30,
            show="*"
        )
        self.admin_password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5
        )

        self.admin_login_toggle = tk.Button(
            password_frame,
            text="Show",
            bg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.toggle_password_visibility(
                self.admin_password_entry,
                self.admin_login_toggle
            )
        )
        self.admin_login_toggle.pack(side="right", padx=5)

        tk.Button(
            login_card,
            text="LOGIN",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10,
            command=self.verify_admin_login
        ).pack(fill="x")

    def verify_admin_login(self):
        admin_id = self.admin_id_entry.get().strip()
        password = self.admin_password_entry.get().strip()
        # Validate empty fields
        if not admin_id or not password:
            messagebox.showwarning(
                "Missing Details",
                "Please enter Admin ID and Password."
            )
            return

        # Validate Admin ID
        if not admin_id.isdigit() or len(admin_id) != 5:
            messagebox.showwarning(
                "Invalid Admin ID",
                "Admin ID must contain exactly 5 digits."
            )
            return

        # Check admin account details
        for admin in self.railway.admin_account_details:
            if str(admin["Admin ID"]) == admin_id:
                if admin["Password"] == password:
                    self.logged_in_admin_id = admin_id
                    self.logged_in_admin_name = admin["User Name"]

                    messagebox.showinfo(
                        "Login Successful",
                        f"Welcome, {self.logged_in_admin_name}!"
                    )
                    self.show_screen("Admin Dashboard")
                    return

                else:
                    messagebox.showerror(
                        "Login Failed",
                        "Incorrect Password."
                    )
                    return

        messagebox.showerror(
            "Login Failed",
            "Admin Account does not exist."
        )

    def show_admin_dashboard(self):
        # Security check
        if self.logged_in_admin_id is None:
            messagebox.showerror(
                "Access Denied",
                "Please login as Admin first."
            )
            self.show_screen("Admin Login")
            return

        dashboard_frame = tk.Frame(
            self.content,
            bg="#F4F7FC"
        )
        dashboard_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        admin_options = [
            ("🚆", "Add Trains", "Register new trains"),
            ("✏️", "Update Trains", "Modify train details"),
            ("🗑️", "Remove Trains", "Remove registered trains"),
            ("📋", "View All Bookings", "Manage passenger bookings"),
            ("👤", "Delete Admin Account", "Delete your admin account"),
            ("🚪", "Logout", "End your admin session")
        ]

        for index, (icon, title, description) in enumerate(admin_options):
            row = index // 2
            column = index % 2
            card = tk.Frame(
                dashboard_frame,
                bg="white",
                highlightbackground="#DCE4EF",
                highlightthickness=1,
                cursor="hand2"
            )

            card.grid(
                row=row,
                column=column,
                padx=12,
                pady=12,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=icon,
                font=("Segoe UI Emoji", 23),
                bg="white"
            ).pack(anchor="w", padx=20, pady=(10, 2))

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 13, "bold"),
                bg="white",
                fg=self.dark_color
            ).pack(anchor="w", padx=20, pady=(0, 2))

            tk.Label(
                card,
                text=description,
                font=("Segoe UI", 9),
                bg="white",
                fg=self.secondary_color
            ).pack(anchor="w", padx=20, pady=(2, 10))

            # Card click actions
            card.bind(
                "<Button-1>",
                lambda event, name=title: self.admin_dashboard_action(name)
            )

            for widget in card.winfo_children():
                widget.bind(
                    "<Button-1>",
                    lambda event, name=title: self.admin_dashboard_action(name)
                )
        dashboard_frame.grid_columnconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(1, weight=1)
        dashboard_frame.grid_rowconfigure(0, weight=1)
        dashboard_frame.grid_rowconfigure(1, weight=1)
        dashboard_frame.grid_rowconfigure(2, weight=1)

    def admin_dashboard_action(self, action):
        # Check admin login
        if self.logged_in_admin_id is None:
            messagebox.showerror(
                "Access Denied",
                "Please login as Admin first."
            )
            self.show_screen("Admin Login")
            return

        if action == "Logout":
            self.logout_admin()

        elif action == "Add Trains":
            self.show_screen("Add Trains")

        elif action == "Update Trains":
            self.show_screen("Update Trains")

        elif action == "Remove Trains":
            self.show_screen("Remove Trains")

        elif action == "View All Bookings":
            self.show_screen("View All Bookings")

        elif action == "Delete Admin Account":
            self.show_screen("Delete Admin Account")

        else:
            messagebox.showinfo(
                "Admin Section",
                f"{action} will be connected next."
            )

    def logout_admin(self):
        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?"
        )

        if confirm:
            self.logged_in_admin_id = None
            self.logged_in_admin_name = None
            messagebox.showinfo(
                "Logout Successful",
                "You have been logged out successfully."
            )
            self.show_screen("Admin Login")

    def show_admin_create_account(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Fixed Create Account Button
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=15
        )

        tk.Button(
            button_frame,
            text="CREATE ACCOUNT",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=self.register_admin_account
        ).pack()

        # Scrollable registration form
        form_container = tk.Frame(main_frame, bg="white")
        form_container.pack(
            side="top",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        form_canvas = tk.Canvas(
            form_container,
            bg="white",
            highlightthickness=0
        )

        form_scrollbar = ttk.Scrollbar(
            form_container,
            orient="vertical",
            command=form_canvas.yview
        )

        form_canvas.configure(
            yscrollcommand=form_scrollbar.set
        )

        form_scrollbar.pack(side="right", fill="y")
        form_canvas.pack(side="left", fill="both", expand=True)
        form = tk.Frame(form_canvas, bg="white")
        form_window = form_canvas.create_window(
            (0, 10),
            window=form,
            anchor="nw",
            width=650
        )

        # Form heading
        tk.Label(
            form,
            text="CREATE ADMIN ACCOUNT",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(5, 5))

        tk.Label(
            form,
            text="Register as a Railway Administrator",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 20))

        # Registration fields
        self.admin_name_entry = self.create_admin_field(
            form, "Full Name"
        )

        self.admin_email_entry = self.create_admin_field(
            form, "Email Address"
        )

        self.admin_mobile_entry = self.create_admin_field(
            form, "Mobile Number"
        )

        self.admin_new_password_entry = self.create_admin_field(
            form, "Password", show="*"
        )

        self.admin_confirm_password_entry = self.create_admin_field(
            form, "Confirm Password", show="*"
        )

        # Update scroll area whenever form size changes
        def update_form_scroll(event=None):
            form_canvas.configure(
                scrollregion=form_canvas.bbox("all")
            )
        form.bind("<Configure>", update_form_scroll)

        # Keep form centered
        def center_form(event):
            form_width = min(650, event.width - 40)
            x_position = (event.width - form_width) // 2
            form_canvas.coords(
                form_window,
                x_position,
                10
            )

            form_canvas.itemconfigure(
                form_window,
                width=form_width
            )
        form_canvas.bind("<Configure>", center_form)

        # Update form dimensions and scrolling
        form.update_idletasks()
        form_canvas.update_idletasks()
        update_form_scroll()
        form_canvas.yview_moveto(0)

        # Mouse-wheel scrolling
        def scroll_admin_form(event):

            # Check whether canvas still exists
            if not form_canvas.winfo_exists():
                return "break"
            if event.delta > 0:
                form_canvas.yview_scroll(-2, "units")
            else:
                form_canvas.yview_scroll(2, "units")
            return "break"

        form_canvas.bind_all(
            "<MouseWheel>",
            scroll_admin_form
        )

        form_canvas.bind_all(
            "<Button-4>",
            lambda event: form_canvas.yview_scroll(-2, "units")
        )

        form_canvas.bind_all(
            "<Button-5>",
            lambda event: form_canvas.yview_scroll(2, "units")
        )

    def create_admin_field(self, parent, label, show=None):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w", pady=(5, 2))

        if show:
            password_frame = tk.Frame(parent, bg="white")
            password_frame.pack(fill="x", pady=(2, 8))

            entry = ttk.Entry(
                password_frame,
                width=55,
                show=show
            )
            entry.pack(
                side="left",
                fill="x",
                expand=True,
                ipady=5
            )

            toggle_button = tk.Button(
                password_frame,
                text="Show",
                bg="white",
                relief="flat",
                cursor="hand2",
                command=lambda: self.toggle_password_visibility(
                    entry, toggle_button
                )
            )
            toggle_button.pack(side="right", padx=5)

        else:
            entry = ttk.Entry(parent, width=55)
            entry.pack(fill="x", pady=(2, 8), ipady=5)
        return entry

    def toggle_password_visibility(self, entry, button):
        if entry.cget("show") == "*":
            entry.config(show="")
            button.config(text="Hide")
        else:
            entry.config(show="*")
            button.config(text="Show")
    
    def register_admin_account(self):
        import re
        import random

        # Get entered details
        name = self.admin_name_entry.get().strip()
        email = self.admin_email_entry.get().strip()
        mobile = self.admin_mobile_entry.get().strip()
        password = self.admin_new_password_entry.get()
        confirm_password = self.admin_confirm_password_entry.get()

        # Empty field validation
        if not all([name, email, mobile, password, confirm_password]):
            messagebox.showwarning(
                "Missing Details",
                "Please fill in all the fields."
            )
            return

        # Name validation
        if not name.replace(" ", "").isalpha():
            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid name."
            )
            return

        # Email validation
        if not re.match(r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        # Mobile validation
        if not re.match(r"^[6-9]\d{9}$", mobile):
            messagebox.showerror(
                "Invalid Mobile Number",
                "Enter a valid 10-digit mobile number."
            )
            return

        # Password validation
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[^A-Za-z0-9]", password)
        ):
            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number and one special character."
            )
            return

        # Confirm password
        if password != confirm_password:
            messagebox.showerror(
                "Password Mismatch",
                "Password and Confirm Password do not match."
            )
            return

        # Check duplicate email and mobile
        for admin in self.railway.admin_account_details:
            if admin["E-mail"].lower() == email.lower():
                messagebox.showerror(
                    "Duplicate Email",
                    "This email is already registered."
                )
                return

            if str(admin["Mobile"]) == mobile:
                messagebox.showerror(
                    "Duplicate Mobile",
                    "This mobile number is already registered."
                )
                return

        # Generate unique 5-digit Admin ID
        while True:
            admin_id = random.randint(10000, 99999)
            if not any(
                str(admin["Admin ID"]) == str(admin_id)
                for admin in self.railway.admin_account_details
            ):
                break

        # Create admin account
        admin_details = {
            "Admin ID": admin_id,
            "User Name": name,
            "E-mail": email,
            "Mobile": mobile,
            "Password": password
        }
        self.railway.admin_account_details.append(admin_details)

        # Save account in admins.txt
        self.railway.save_admins()
        messagebox.showinfo(
            "Account Created Successfully",
            f"Your Admin Account has been created successfully!\n\n"
            f"Admin ID: {admin_id}\n"
            f"Name: {name}"
        )

        go_to_dashboard = messagebox.askyesno(
            "Go to Dashboard",
            "Your account has been created.\n\n"
            "Do you want to go to the Dashboard?"
        )

        if go_to_dashboard:
            self.logged_in_admin_id = str(admin_id)
            self.logged_in_admin_name = name
            self.show_screen("Admin Dashboard")
        else:
            self.logged_in_admin_id = None
            self.logged_in_admin_name = None
            self.show_screen("Admin Options")

    def show_add_train_screen(self):
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Heading
        tk.Label(
            main_frame,
            text="ADD NEW TRAIN",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(20, 5))

        tk.Label(
            main_frame,
            text="Enter the details to register a new train",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 20))

        # Buttons
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(
            side="bottom",
            pady=(10, 20)
        )

        tk.Button(
            button_frame,
            text="ADD TRAIN",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=35,
            pady=12,
            command=self.register_new_train
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="CLEAR FORM",
            bg="#EAF2FA",
            fg=self.dark_color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=35,
            pady=12,
            command=self.clear_add_train_form
        ).pack(side="left", padx=10)

        # Scrollable Form Container
        scroll_container = tk.Frame(main_frame, bg="white")
        scroll_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        # Canvas
        form_canvas = tk.Canvas(
            scroll_container,
            bg="white",
            highlightthickness=0
        )

        form_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollbar
        form_scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=form_canvas.yview
        )

        form_scrollbar.pack(
            side="right",
            fill="y"
        )

        form_canvas.configure(
            yscrollcommand=form_scrollbar.set
        )

        # Inner Form Frame
        form_frame = tk.Frame(
            form_canvas,
            bg="white"
        )

        form_window = form_canvas.create_window(
            (0, 0),
            window=form_frame,
            anchor="nw"
        )

        # Update scroll region
        def update_scroll_region(event):
            form_canvas.configure(
                scrollregion=form_canvas.bbox("all")
            )

        form_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        # Keep form width equal to canvas width
        form_canvas.bind(
            "<Configure>",
            lambda event: form_canvas.itemconfig(
                form_window,
                width=event.width
            )
        )

        # Mouse Wheel Scrolling
        def mouse_scroll(event):
            form_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        form_canvas.bind_all(
            "<MouseWheel>",
            mouse_scroll
        )

        # Two columns
        left_frame = tk.Frame(form_frame, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=15)
        right_frame = tk.Frame(form_frame, bg="white")
        right_frame.pack(side="left", fill="both", expand=True, padx=15)

        # Left column
        self.add_train_name_entry = self.create_admin_field(
            left_frame, "Train Name"
        )

        self.add_train_number_entry = self.create_admin_field(
            left_frame, "Train Number"
        )

        self.add_train_platform_entry = self.create_admin_field(
            left_frame, "Platform Number"
        )

        self.add_train_from_entry = self.create_admin_field(
            left_frame, "From Station"
        )

        # Right column
        self.add_train_to_entry = self.create_admin_field(
            right_frame, "To Station"
        )

        self.add_train_departure_entry = self.create_admin_field(
            right_frame, "Departure Time"
        )

        self.add_train_arrival_entry = self.create_admin_field(
            right_frame, "Arrival Time"
        )

        self.add_train_seats_entry = self.create_admin_field(
            right_frame, "Available Seats"
        )

    def show_update_train_screen(self):
        # Main Container
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Scrollable Main Container
        scroll_container = tk.Frame(main_frame, bg="white")
        scroll_container.pack(fill="both", expand=True)

        # Canvas
        canvas = tk.Canvas(
            scroll_container,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner Frame
        content_frame = tk.Frame(canvas, bg="white")
        content_window = canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )

        # Update Scroll Region
        content_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Maintain Canvas Width
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                content_window,
                width=event.width
            )
        )

        # Heading
        tk.Label(
            content_frame,
            text="UPDATE TRAIN DETAILS",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(20, 5))

        tk.Label(
            content_frame,
            text="Search a train or select a train to edit its details",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 20))

        # Search Section
        search_frame = tk.Frame(content_frame, bg="white")
        search_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.update_train_search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=30
        )

        self.update_train_search_entry.pack(
            side="left",
            ipady=9,
            padx=(0, 10)
        )

        tk.Button(
            search_frame,
            text="SEARCH TRAIN",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.search_update_train
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="SHOW ALL TRAINS",
            bg="#EAF2FA",
            fg=self.dark_color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.display_update_train_list
        ).pack(side="left", padx=5)

        # Train List Heading
        tk.Label(
            content_frame,
            text="ALL REGISTERED TRAINS",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 10)
        )

        # Train List Container
        self.update_train_list_frame = tk.Frame(
            content_frame,
            bg="white"
        )

        self.update_train_list_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        # Mouse Wheel Scrolling
        def mouse_scroll(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        canvas.bind_all("<MouseWheel>", mouse_scroll)

        # Display All Trains
        self.display_update_train_list()
    
    def show_remove_train_screen(self):
        # Main Container
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Scrollable Container
        scroll_container = tk.Frame(main_frame, bg="white")
        scroll_container.pack(fill="both", expand=True)

        # Canvas
        canvas = tk.Canvas(
            scroll_container,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner Frame
        content_frame = tk.Frame(canvas, bg="white")
        content_window = canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )

        content_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                content_window,
                width=event.width
            )
        )

        # Heading
        tk.Label(
            content_frame,
            text="REMOVE TRAINS",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(20, 5))

        tk.Label(
            content_frame,
            text="Search or select a train to remove it from the system",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 20))

        # Search Section
        search_frame = tk.Frame(content_frame, bg="white")
        search_frame.pack(fill="x", padx=30, pady=10)
        self.remove_train_search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=30
        )

        self.remove_train_search_entry.pack(
            side="left",
            ipady=9,
            padx=(0, 10)
        )

        tk.Button(
            search_frame,
            text="SEARCH TRAIN",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.search_remove_train
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="SHOW ALL TRAINS",
            bg="#EAF2FA",
            fg=self.dark_color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.display_remove_train_list
        ).pack(side="left", padx=5)

        # Train List Heading
        tk.Label(
            content_frame,
            text="ALL REGISTERED TRAINS",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w", padx=30, pady=(20, 10))

        # Train List Container
        self.remove_train_list_frame = tk.Frame(
            content_frame,
            bg="white"
        )

        self.remove_train_list_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        # Mouse Wheel Scrolling
        def mouse_scroll(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        canvas.bind_all("<MouseWheel>", mouse_scroll)

        # Display All Trains
        self.display_remove_train_list()


    def display_remove_train_list(self, trains=None):
        # Clear Previous Records
        for widget in self.remove_train_list_frame.winfo_children():
            widget.destroy()

        if trains is None:
            trains = self.railway.Trains

        if not trains:
            tk.Label(
                self.remove_train_list_frame,
                text="No trains found.",
                font=("Segoe UI", 12),
                bg="white",
                fg=self.secondary_color
            ).pack(pady=30)

            return

        for train in trains:
            train_frame = tk.Frame(
                self.remove_train_list_frame,
                bg="#F4F7FB",
                highlightbackground=self.border_color,
                highlightthickness=1
            )

            train_frame.pack(
                fill="x",
                pady=6,
                padx=5
            )

            # Train Name
            tk.Label(
                train_frame,
                text=train[0],
                font=("Segoe UI", 12, "bold"),
                bg="#F4F7FB",
                fg=self.dark_color,
                width=22,
                anchor="w"
            ).pack(side="left", padx=15, pady=15)

            # Train Number
            tk.Label(
                train_frame,
                text=f"Train No: {train[1]}",
                font=("Segoe UI", 10),
                bg="#F4F7FB",
                fg=self.secondary_color
            ).pack(side="left", padx=10)

            # Remove Button
            tk.Button(
                train_frame,
                text="REMOVE",
                bg="#DC3545",
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=7,
                command=lambda t=train: self.remove_train_record(t)
            ).pack(side="right", padx=15)


    def search_remove_train(self):
        train_number = self.remove_train_search_entry.get().strip()
        if not train_number.isdigit():
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid Train Number."
            )
            return

        found_trains = [
            train for train in self.railway.Trains
            if str(train[1]) == train_number
        ]
        self.display_remove_train_list(found_trains)

    def remove_train_record(self, train):
        # Confirmation Dialog
        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove this train?\n\n"
            f"Train Name: {train[0]}\n"
            f"Train Number: {train[1]}"
        )

        if not confirm:
            return

        # Check Train Exists
        if train not in self.railway.Trains:
            messagebox.showerror(
                "Error",
                "Train not found. It may have already been removed."
            )
            self.display_remove_train_list()
            return

        # Remove Train
        self.railway.Trains.remove(train)

        # Save Changes
        self.railway.save_trains()

        # Success Message
        messagebox.showinfo(
            "Success",
            f"{train[0]} has been removed successfully!"
        )

        # Refresh Train List
        self.display_remove_train_list()

    def edit_train_record(self, train):
        # Store Selected Train
        self.editing_train = train

        # Clear Previous Screen
        self.clear_content()

        self.create_header(
            "Edit Train",
            "Modify the selected train information."
        )

        # Main Container
        main_frame = tk.Frame(
            self.content,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Scrollable Container
        scroll_container = tk.Frame(main_frame, bg="white")
        scroll_container.pack(fill="both", expand=True)

        # Canvas
        canvas = tk.Canvas(
            scroll_container,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner Frame
        content_frame = tk.Frame(canvas, bg="white")
        content_window = canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )

        # Update Scroll Region
        content_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Maintain Canvas Width
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                content_window,
                width=event.width
            )
        )

        # Heading
        tk.Label(
            content_frame,
            text="EDIT TRAIN DETAILS",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=(20, 5))

        tk.Label(
            content_frame,
            text=f"Editing Train Number: {train[1]}",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=(0, 20))

        # Form Container
        form_frame = tk.Frame(content_frame, bg="white")
        form_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        # Two Columns
        left_frame = tk.Frame(form_frame, bg="white")
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15
        )
        right_frame = tk.Frame(form_frame, bg="white")
        right_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15
        )

        # Left Column
        self.edit_train_name_entry = self.create_admin_field(
            left_frame, "Train Name"
        )

        self.edit_train_number_entry = self.create_admin_field(
            left_frame, "Train Number"
        )

        self.edit_train_platform_entry = self.create_admin_field(
            left_frame, "Platform Number"
        )

        self.edit_train_from_entry = self.create_admin_field(
            left_frame, "From Station"
        )

        # Right Column
        self.edit_train_to_entry = self.create_admin_field(
            right_frame, "To Station"
        )

        self.edit_train_departure_entry = self.create_admin_field(
            right_frame, "Departure Time"
        )

        self.edit_train_arrival_entry = self.create_admin_field(
            right_frame, "Arrival Time"
        )

        self.edit_train_seats_entry = self.create_admin_field(
            right_frame, "Available Seats"
        )

        # Insert Existing Train Details
        entries = [
            self.edit_train_name_entry,
            self.edit_train_number_entry,
            self.edit_train_platform_entry,
            self.edit_train_from_entry,
            self.edit_train_to_entry,
            self.edit_train_departure_entry,
            self.edit_train_arrival_entry,
            self.edit_train_seats_entry
        ]

        for entry, value in zip(entries, train):
            entry.insert(0, str(value))

        # Buttons
        button_frame = tk.Frame(content_frame, bg="white")
        button_frame.pack(pady=(15, 25))

        tk.Button(
            button_frame,
            text="UPDATE TRAIN",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=35,
            pady=12,
            command=self.save_updated_train
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="CANCEL",
            bg="#EAF2FA",
            fg=self.dark_color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=35,
            pady=12,
            command=lambda: self.show_screen("Update Trains")
        ).pack(side="left", padx=10)

        # Mouse Wheel Scrolling
        def mouse_scroll(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        canvas.bind_all("<MouseWheel>", mouse_scroll)

    def save_updated_train(self):
        # Get Updated Values
        train_name = self.edit_train_name_entry.get().strip()
        train_number = self.edit_train_number_entry.get().strip()
        platform = self.edit_train_platform_entry.get().strip()
        from_station = self.edit_train_from_entry.get().strip()
        to_station = self.edit_train_to_entry.get().strip()
        departure = self.edit_train_departure_entry.get().strip()
        arrival = self.edit_train_arrival_entry.get().strip()
        seats = self.edit_train_seats_entry.get().strip()

        # Check Empty Fields
        if not all([
            train_name, train_number, platform,
            from_station, to_station, departure,
            arrival, seats
        ]):
            messagebox.showerror(
                "Missing Details",
                "Please fill in all train details."
            )
            return

        # Validate Numeric Fields
        if not train_number.isdigit() or not platform.isdigit() or not seats.isdigit():
            messagebox.showerror(
                "Invalid Details",
                "Train Number, Platform Number and Available Seats must be numeric."
            )
            return
        train_number = int(train_number)
        platform = int(platform)
        seats = int(seats)

        # Validate Values
        if platform <= 0 or seats < 0:
            messagebox.showerror(
                "Invalid Details",
                "Platform Number must be greater than 0 and seats cannot be negative."
            )
            return

        if from_station.lower() == to_station.lower():
            messagebox.showerror(
                "Invalid Route",
                "From Station and To Station cannot be the same."
            )
            return

        # Check Duplicate Train Number
        for existing_train in self.railway.Trains:
            if (
                existing_train[1] == train_number
                and existing_train != self.editing_train
            ):
                messagebox.showerror(
                    "Duplicate Train Number",
                    "This Train Number already exists."
                )
                return

        # Create Updated Train Tuple
        updated_train = (
            train_name,
            train_number,
            platform,
            from_station,
            to_station,
            departure,
            arrival,
            seats
        )

        # Update Train List
        index = self.railway.Trains.index(self.editing_train)
        self.railway.Trains[index] = updated_train

        # Save Changes
        self.railway.save_trains()
        messagebox.showinfo(
            "Success",
            "Train details updated successfully!"
        )

        # Return to Update Trains Screen
        self.show_screen("Update Trains")

    def display_update_train_list(self, trains=None):
        # Clear Previous Records
        for widget in self.update_train_list_frame.winfo_children():
            widget.destroy()

        if trains is None:
            trains = self.railway.Trains

        if not trains:
            tk.Label(
                self.update_train_list_frame,
                text="No trains found.",
                font=("Segoe UI", 12),
                bg="white",
                fg=self.secondary_color
            ).pack(pady=30)

            return

        for train in trains:
            train_frame = tk.Frame(
                self.update_train_list_frame,
                bg="#F4F7FB",
                highlightbackground=self.border_color,
                highlightthickness=1
            )

            train_frame.pack(
                fill="x",
                pady=6,
                padx=5
            )

            # Train Name
            tk.Label(
                train_frame,
                text=train[0],
                font=("Segoe UI", 12, "bold"),
                bg="#F4F7FB",
                fg=self.dark_color,
                width=22,
                anchor="w"
            ).pack(side="left", padx=15, pady=15)

            # Train Number
            tk.Label(
                train_frame,
                text=f"Train No: {train[1]}",
                font=("Segoe UI", 10),
                bg="#F4F7FB",
                fg=self.secondary_color
            ).pack(side="left", padx=10)

            # Edit Button
            tk.Button(
                train_frame,
                text="EDIT",
                bg=self.primary_color,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=7,
                command=lambda t=train: self.edit_train_record(t)
            ).pack(side="right", padx=15)

    def search_update_train(self):
        train_number = self.update_train_search_entry.get().strip()

        if not train_number.isdigit():
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid Train Number."
            )
            return

        found_trains = [
            train for train in self.railway.Trains
            if str(train[1]) == train_number
        ]
        self.display_update_train_list(found_trains)

    def register_new_train(self):
        import re
        # Get form values
        train_name = self.add_train_name_entry.get().strip()
        train_number = self.add_train_number_entry.get().strip()
        platform = self.add_train_platform_entry.get().strip()
        from_station = self.add_train_from_entry.get().strip()
        to_station = self.add_train_to_entry.get().strip()
        departure = self.add_train_departure_entry.get().strip()
        arrival = self.add_train_arrival_entry.get().strip()
        available_seats = self.add_train_seats_entry.get().strip()

        # Check empty fields
        if not all([
            train_name, train_number, platform,
            from_station, to_station, departure,
            arrival, available_seats
        ]):
            messagebox.showwarning(
                "Missing Details",
                "Please fill in all train details."
            )
            return

        # Train name validation
        if not any(char.isalpha() for char in train_name):
            messagebox.showerror(
                "Invalid Train Name",
                "Please enter a valid train name."
            )
            return

        # Train number validation
        if not train_number.isdigit() or not 4 <= len(train_number) <= 5:
            messagebox.showerror(
                "Invalid Train Number",
                "Train number must contain 4 or 5 digits."
            )
            return

        # Duplicate train number check
        for train in self.railway.Trains:
            if str(train[1]) == train_number:
                messagebox.showerror(
                    "Duplicate Train",
                    "This train number already exists."
                )
                return

        # Platform validation
        if not platform.isdigit() or int(platform) <= 0:
            messagebox.showerror(
                "Invalid Platform",
                "Enter a valid platform number."
            )
            return

        # Station validation
        if from_station.lower() == to_station.lower():
            messagebox.showerror(
                "Invalid Route",
                "From and To stations cannot be the same."
            )
            return

        # Available seats validation
        if not available_seats.isdigit() or int(available_seats) <= 0:
            messagebox.showerror(
                "Invalid Seats",
                "Enter a valid number of available seats."
            )
            return

        # Add train to backend list
        new_train = (
            train_name,
            int(train_number),
            int(platform),
            from_station,
            to_station,
            departure,
            arrival,
            int(available_seats)
        )
        self.railway.Trains.append(new_train)

        # Save train details
        self.railway.save_trains()
        messagebox.showinfo(
            "Success",
            f"Train {train_name} has been added successfully!"
        )
        self.clear_add_train_form()

    def clear_add_train_form(self):
        self.add_train_name_entry.delete(0, tk.END)
        self.add_train_number_entry.delete(0, tk.END)
        self.add_train_platform_entry.delete(0, tk.END)
        self.add_train_from_entry.delete(0, tk.END)
        self.add_train_to_entry.delete(0, tk.END)
        self.add_train_departure_entry.delete(0, tk.END)
        self.add_train_arrival_entry.delete(0, tk.END)
        self.add_train_seats_entry.delete(0, tk.END)
        self.add_train_name_entry.focus_set()

    def show_all_bookings_screen(self):
        # Main container
        main_frame = tk.Frame(
            self.content,
            bg="#F4F7FC"
        )
        main_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Search section
        search_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        search_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            search_frame,
            text="Search Bookings",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w", padx=18, pady=(12, 8))
        search_row = tk.Frame(search_frame, bg="white")
        search_row.pack(fill="x", padx=18, pady=(0, 15))

        self.booking_search_entry = ttk.Entry(
            search_row,
            font=("Segoe UI", 11)
        )
        self.booking_search_entry.pack(
            side="left", fill="x", expand=True, ipady=6
        )

        ttk.Button(
            search_row,
            text="SEARCH",
            command=self.search_admin_bookings
        ).pack(side="left", padx=(10, 5))

        ttk.Button(
            search_row,
            text="SHOW ALL",
            command=self.display_admin_bookings
        ).pack(side="left")

        # Bookings table container
        table_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="All Passenger Bookings",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(anchor="w", padx=18, pady=15)

        columns = (
            "Booking ID",
            "Passenger Name",
            "Train Number",
            "From",
            "To",
            "Mobile",
            "Departure",
            "Arrival"
        )

        self.admin_booking_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.admin_booking_tree.heading(
                column,
                text=column
            )

            self.admin_booking_tree.column(
                column,
                width=130,
                minwidth=100,
                anchor="center"
            )

        self.admin_booking_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(12, 0),
            pady=(0, 12)
        )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.admin_booking_tree.yview
        )
        scrollbar.pack(side="right", fill="y", pady=(0, 12), padx=(0, 12))

        self.admin_booking_tree.configure(
            yscrollcommand=scrollbar.set
        )

        # Horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(
            main_frame,
            orient="horizontal",
            command=self.admin_booking_tree.xview
        )
        horizontal_scrollbar.pack(fill="x")

        self.admin_booking_tree.configure(
            xscrollcommand=horizontal_scrollbar.set
        )
        # Load all bookings
        self.display_admin_bookings()

    def search_admin_bookings(self):
        search_value = self.booking_search_entry.get().strip()
        if search_value == "":
            messagebox.showwarning(
                "Input Required",
                "Please enter Booking ID or Train Number."
            )
            return
        matching_bookings = []

        for booking in self.railway.all_booked_tickets:
            if (
                search_value.lower() == str(booking["Booking ID"]).lower()
                or search_value.lower() == str(booking["Train Number"]).lower()
            ):
                matching_bookings.append(booking)
        self.display_admin_bookings(matching_bookings)
        if not matching_bookings:
            messagebox.showinfo(
                "No Results",
                "No bookings found with the entered Booking ID or Train Number."
            )

    def display_admin_bookings(self, bookings=None):
        # Clear previous records
        for item in self.admin_booking_tree.get_children():
            self.admin_booking_tree.delete(item)

        # Use all bookings if no filtered list is provided
        if bookings is None:
            bookings = self.railway.all_booked_tickets

        # Display booking records
        for booking in bookings:
            self.admin_booking_tree.insert(
                "",
                "end",
                values=(
                    booking["Booking ID"],
                    booking["Name"],
                    booking["Train Number"],
                    booking["From"],
                    booking["To"],
                    booking["Mobile"],
                    booking["Departure"],
                    booking["Arrival"]
                )
            )

    def show_delete_admin_screen(self):
        main_frame = tk.Frame(
            self.content,
            bg="#F4F7FC"
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        delete_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        delete_frame.pack(
            fill="x",
            padx=100,
            pady=15
        )

        tk.Label(
            delete_frame,
            text="⚠️",
            font=("Segoe UI Emoji", 25),
            bg="white"
        ).pack(pady=(12, 2))

        tk.Label(
            delete_frame,
            text="Delete Admin Account",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=3)

        tk.Label(
            delete_frame,
            text="This action will permanently delete your admin account.",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.secondary_color
        ).pack(pady=3)

        tk.Label(
            delete_frame,
            text=f"Admin ID: {self.logged_in_admin_id}",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=6)

        # OTP Label and Input Row
        otp_frame = tk.Frame(
            delete_frame,
            bg="white"
        )
        otp_frame.pack(
            fill="x",
            padx=40,
            pady=12
        )

        # OTP Label
        tk.Label(
            otp_frame,
            text="Enter OTP:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(
            side="left",
            padx=(0, 20)
        )

        # OTP Input
        self.delete_otp_entry = ttk.Entry(
            otp_frame,
            font=("Segoe UI", 10),
            justify="center"
        )
        self.delete_otp_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        tk.Button(
            delete_frame,
            text="GENERATE OTP",
            font=("Segoe UI", 9, "bold"),
            bg=self.primary_color,
            fg="white",
            cursor="hand2",
            relief="flat",
            command=self.generate_delete_admin_otp
        ).pack(pady=5, ipadx=15, ipady=5)

        tk.Button(
            delete_frame,
            text="VERIFY OTP & DELETE ACCOUNT",
            font=("Segoe UI", 9, "bold"),
            bg="#DC2626",
            fg="white",
            cursor="hand2",
            relief="flat",
            command=self.verify_delete_admin_otp
        ).pack(pady=(3, 15), ipadx=15, ipady=5)

        self.delete_otp_status = tk.Label(
            delete_frame,
            text="",
            font=("Segoe UI", 9),
            bg="white"
        )
        self.delete_otp_status.pack(pady=3)

    def generate_delete_admin_otp(self):
        import random
        confirm = messagebox.askyesno(
            "Confirm Account Deletion",
            "Are you sure you want to delete your admin account?"
        )

        if not confirm:
            return
        # Generate unique OTP
        otp = random.randint(10000, 99999)

        while otp in self.railway.OTP:
            otp = random.randint(10000, 99999)

        # Save OTP in existing OTP file
        self.railway.OTP.append(otp)
        self.railway.save_otp()
        self.delete_account_otp = otp

        # Update screen without popup
        self.delete_otp_status.config(
            text="OTP generated successfully! Check your OTP file.",
            fg="green"
        )

    def verify_delete_admin_otp(self):
        entered_otp = self.delete_otp_entry.get().strip()
        if not entered_otp.isdigit():
            messagebox.showerror(
                "Invalid OTP",
                "Please enter a valid numeric OTP."
            )
            return

        if not hasattr(self, "delete_account_otp"):
            messagebox.showwarning(
                "OTP Required",
                "Please generate OTP first."
            )
            return

        if int(entered_otp) != self.delete_account_otp:
            messagebox.showerror(
                "Incorrect OTP",
                "The OTP you entered is incorrect."
            )
            return

        # Find logged-in admin account
        admin_found = None
        for admin in self.railway.admin_account_details:
            if str(admin["Admin ID"]) == str(self.logged_in_admin_id):
                admin_found = admin
                break

        if admin_found is None:
            messagebox.showerror(
                "Error",
                "Admin account not found."
            )
            return

        # Remove OTP
        self.railway.OTP.remove(self.delete_account_otp)
        self.railway.save_otp()

        # Delete admin account
        self.railway.admin_account_details.remove(admin_found)
        self.railway.save_admins()

        # Clear login session
        self.logged_in_admin_id = None
        del self.delete_account_otp

        messagebox.showinfo(
            "Account Deleted",
            "Your admin account has been deleted successfully!"
        )
        self.show_screen("Admin Login")

# ---------------------------------
# RUN APPLICATION
# ---------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayGUI(root)
    root.mainloop()
