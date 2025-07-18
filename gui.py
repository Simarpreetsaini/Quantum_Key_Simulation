import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import os
from datetime import datetime

class QKDSatelliteSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Key Simulation")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.config(bg="#272B33")
        
        # Set application icon
        try:
            # This would be replaced with an actual icon file in a real app
            self.create_dummy_icon()
            self.root.iconphoto(True, ImageTk.PhotoImage(Image.open("temp_icon.png")))
        except Exception:
            pass
        
        # Global variables
        self.simulate_interception = False
        self.security_states = []
        self.animation_running = False
        self.animation_thread = None
        
        # Create styles
        self.create_styles()
        
        # Create main frames
        self.create_frames()
        
        # Create notebook tabs
        self.create_notebook()
        
        # Initialize application widgets
        self.init_input_frame()
        self.init_output_frame()
        self.init_visualization_frame()
        self.init_log_frame()
        self.init_status_bar()
        
        # Create menu
        self.create_menu()
        
        # Start system status indicator
        self.update_system_status()

    def create_dummy_icon(self):
        """Create a temporary icon for the application"""
        img = Image.new('RGB', (48, 48), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 10, 38, 38), fill=(236, 240, 241))
        draw.ellipse((16, 16, 32, 32), fill=(52, 152, 219))
        img.save("temp_icon.png")
        
    def create_styles(self):
        """Create ttk styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure("TFrame", background="#272B33")
        self.style.configure("TNotebook", background="#272B33", tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", background="#1E2129", foreground="#FFFFFF", 
                            padding=[20, 10], font=('Helvetica', 11))
        self.style.map("TNotebook.Tab", background=[("selected", "#3498DB")])
        
        self.style.configure("TLabel", background="#272B33", foreground="#FFFFFF", font=('Helvetica', 11))
        self.style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'))
        self.style.configure("Status.TLabel", background="#1E2129", foreground="#AAAAAA", font=('Helvetica', 10))
        
        self.style.configure("TButton", background="#3498DB", foreground="#FFFFFF", 
                            font=('Helvetica', 11), padding=8)
        self.style.map("TButton", background=[("active", "#2980B9")])
        
        self.style.configure("Danger.TButton", background="#E74C3C", foreground="#FFFFFF")
        self.style.map("Danger.TButton", background=[("active", "#C0392B")])
        
        self.style.configure("TEntry", padding=8, font=('Helvetica', 11))
        self.style.configure("TCheckbutton", background="#272B33", foreground="#FFFFFF", font=('Helvetica', 11))
        self.style.map("TCheckbutton", background=[("active", "#272B33")])
        
        # Status indicators
        self.style.configure("Green.TLabel", background="#272B33", foreground="#2ECC71", font=('Helvetica', 11))
        self.style.configure("Red.TLabel", background="#272B33", foreground="#E74C3C", font=('Helvetica', 11))
        
    def create_frames(self):
        """Create the main application frames"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame with logo and title
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a simple logo
        self.logo_canvas = tk.Canvas(self.header_frame, width=50, height=50, bg="#272B33", 
                                    highlightthickness=0)
        self.logo_canvas.pack(side=tk.LEFT, padx=(0, 10))
        self.logo_canvas.create_oval(5, 5, 45, 45, fill="#3498DB", outline="#3498DB")
        self.logo_canvas.create_oval(15, 15, 35, 35, fill="#ECF0F1", outline="#ECF0F1")
        
        # Application title
        title_label = ttk.Label(self.header_frame, text="Quantum Key Simulation", 
                                style="Header.TLabel", font=('Helvetica', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # System status indicator
        self.status_frame = ttk.Frame(self.header_frame)
        self.status_frame.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(self.status_frame, text="System Status: ", style="TLabel")
        self.status_label.pack(side=tk.LEFT)
        
        self.status_indicator = ttk.Label(self.status_frame, text="Operational", style="Green.TLabel")
        self.status_indicator.pack(side=tk.LEFT)
        
        # Content frame
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.statusbar_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.statusbar_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def create_notebook(self):
        """Create the notebook with tabs"""
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.simulation_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        self.log_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.simulation_tab, text="Simulation")
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.notebook.add(self.log_tab, text="System Log")
        
        # Setup frames within the simulation tab
        self.input_frame = ttk.LabelFrame(self.simulation_tab, text="Input Parameters", padding=10)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.output_frame = ttk.LabelFrame(self.simulation_tab, text="Simulation Results", padding=10)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def init_input_frame(self):
        """Initialize the input parameters frame"""
        # Input frame with grid layout
        input_grid = ttk.Frame(self.input_frame)
        input_grid.pack(fill=tk.X, expand=True)
        
        # Message input
        ttk.Label(input_grid, text="Message to encrypt:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.message_entry = ttk.Entry(input_grid, width=50)
        self.message_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.message_entry.insert(0, "Hello Quantum World!")
        
        # Interception simulation
        ttk.Label(input_grid, text="Simulation options:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        options_frame = ttk.Frame(input_grid)
        options_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.interception_var = tk.BooleanVar(value=False)
        interception_check = ttk.Checkbutton(options_frame, text="Simulate interception", 
                                            variable=self.interception_var)
        interception_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Buttons frame
        button_frame = ttk.Frame(self.input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Run simulation button
        self.run_button = ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = ttk.Button(button_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
    def init_output_frame(self):
        """Initialize the output results frame"""
        # Create a notebook for output results
        self.results_notebook = ttk.Notebook(self.output_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tab frames
        self.results_summary_frame = ttk.Frame(self.results_notebook)
        self.results_details_frame = ttk.Frame(self.results_notebook)
        self.security_frame = ttk.Frame(self.results_notebook)
        
        self.results_notebook.add(self.results_summary_frame, text="Summary")
        self.results_notebook.add(self.results_details_frame, text="Details")
        self.results_notebook.add(self.security_frame, text="Security")
        
        # Summary results
        self.summary_text = scrolledtext.ScrolledText(self.results_summary_frame, wrap=tk.WORD, 
                                                    background="#1E2129", foreground="#FFFFFF",
                                                    font=('Consolas', 11), padx=10, pady=10)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.configure(state='disabled')
        
        # Detailed results
        self.details_text = scrolledtext.ScrolledText(self.results_details_frame, wrap=tk.WORD, 
                                                    background="#1E2129", foreground="#FFFFFF",
                                                    font=('Consolas', 11), padx=10, pady=10)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.configure(state='disabled')
        
        # Security results
        self.security_text = scrolledtext.ScrolledText(self.security_frame, wrap=tk.WORD, 
                                                    background="#1E2129", foreground="#FFFFFF",
                                                    font=('Consolas', 11), padx=10, pady=10)
        self.security_text.pack(fill=tk.BOTH, expand=True)
        self.security_text.configure(state='disabled')
        
    def init_visualization_frame(self):
        """Initialize the visualization frame"""
        # Split visualization tab into two parts
        viz_top_frame = ttk.Frame(self.visualization_tab)
        viz_top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(viz_top_frame, text="Quantum Key Distribution Visualization", 
                style="Header.TLabel").pack(side=tk.LEFT)
        
        # Canvas for visualization
        viz_content_frame = ttk.Frame(self.visualization_tab)
        viz_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.viz_canvas = tk.Canvas(viz_content_frame, bg="#1E2129", highlightthickness=0)
        self.viz_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animation controls
        viz_controls_frame = ttk.Frame(self.visualization_tab)
        viz_controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_animation_btn = ttk.Button(viz_controls_frame, text="Start Animation", 
                                            command=self.toggle_animation)
        self.start_animation_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(viz_controls_frame, text="Reset", command=self.reset_visualization).pack(
            side=tk.LEFT, padx=5)
        
    def init_log_frame(self):
        """Initialize the system log frame"""
        log_top_frame = ttk.Frame(self.log_tab)
        log_top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(log_top_frame, text="System Log", style="Header.TLabel").pack(side=tk.LEFT)
        
        ttk.Button(log_top_frame, text="Clear Log", command=self.clear_log).pack(side=tk.RIGHT)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(self.log_tab, wrap=tk.WORD, 
                                                background="#1E2129", foreground="#AAAAAA",
                                                font=('Consolas', 10), padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.configure(state='disabled')
        
        # Add initial log entries
        self.add_log_entry("System initialized")
        self.add_log_entry("Quantum key distribution modules loaded")
        self.add_log_entry("Satellite communication protocol initialized")
        self.add_log_entry("System ready for simulation")
        
    def init_status_bar(self):
        """Initialize the status bar"""
        self.status_message = ttk.Label(self.statusbar_frame, text="Ready", style="Status.TLabel")
        self.status_message.pack(side=tk.LEFT, padx=5)
        
        self.time_label = ttk.Label(self.statusbar_frame, text="", style="Status.TLabel")
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
        # Start time update
        self.update_time()
        
    def create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Simulation", command=self.clear_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Simulation menu
        simulation_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Simulation", menu=simulation_menu)
        simulation_menu.add_command(label="Run", command=self.run_simulation)
        simulation_menu.add_command(label="Stop", command=self.stop_simulation)
        simulation_menu.add_separator()
        simulation_menu.add_checkbutton(label="Simulate Interception", 
                                      variable=self.interception_var)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Simulation", 
                            command=lambda: self.notebook.select(self.simulation_tab))
        view_menu.add_command(label="Visualization", 
                            command=lambda: self.notebook.select(self.visualization_tab))
        view_menu.add_command(label="System Log", 
                            command=lambda: self.notebook.select(self.log_tab))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
    
    def update_time(self):
        """Update the time in the status bar"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_system_status(self):
        """Update system status indicator randomly for effect"""
        states = [
            ("Operational", "Green.TLabel"),
            ("Processing", "TLabel"),
            ("Standby", "TLabel"),
        ]
        
        if not self.animation_running:
            # Only show operational most of the time when not animating
            rand = np.random.randint(0, 10)
            if rand < 8:  # 80% chance of operational
                state, style = states[0]
            else:
                state, style = states[np.random.randint(1, len(states))]
        else:
            # More varied states during animation
            state, style = states[np.random.randint(0, len(states))]
            
        self.status_indicator.config(text=state, style=style)
        
        # Schedule next update (faster during animation)
        update_time = 2000 if not self.animation_running else 800
        self.root.after(update_time, self.update_system_status)
    
    def add_log_entry(self, message):
        """Add entry to system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
    
    def clear_log(self):
        """Clear the system log"""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.add_log_entry("Log cleared")
    
    def set_status(self, message):
        """Set status bar message"""
        self.status_message.config(text=message)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Quantum Key Distribution Satellite System
        Version 1.0
        
        This application simulates quantum key distribution 
        through satellite communications.
        
        © 2025 Quantum Security Labs
        """
        messagebox.showinfo("About", about_text)
    
    def show_documentation(self):
        """Show documentation dialog"""
        doc_text = """
        Quantum Key Distribution (QKD) Satellite System
        
        This system simulates:
        
        1. Quantum key generation using entangled photon pairs
        2. Quantum key distribution from satellite to ground station
        3. Error correction and privacy amplification
        4. Data encryption using quantum keys
        5. Transmission over satellite communication channel
        6. Data reception and decryption
        7. Security validation
        
        For detailed documentation, please refer to the
        user manual or visit our website.
        """
        messagebox.showinfo("Documentation", doc_text)
    
    def clear_results(self):
        """Clear all result fields"""
        # Clear text areas
        for text_widget in [self.summary_text, self.details_text, self.security_text]:
            text_widget.configure(state='normal')
            text_widget.delete(1.0, tk.END)
            text_widget.configure(state='disabled')
        
        # Reset visualization
        self.reset_visualization()
        
        # Log the action
        self.add_log_entry("Results cleared")
        self.set_status("Results cleared")
    
    def stop_simulation(self):
        """Stop the current simulation"""
        if self.animation_running:
            self.toggle_animation()
        self.add_log_entry("Simulation stopped")
        self.set_status("Simulation stopped")
    
    def reset_visualization(self):
        """Reset the visualization canvas"""
        self.viz_canvas.delete("all")
        self.viz_canvas.create_text(
            self.viz_canvas.winfo_width() // 2, 
            self.viz_canvas.winfo_height() // 2,
            text="Run a simulation to see visualization",
            fill="#AAAAAA",
            font=('Helvetica', 12)
        )
        
        if self.animation_running:
            self.toggle_animation()
            
        self.add_log_entry("Visualization reset")
    
    def toggle_animation(self):
        """Toggle animation state"""
        if self.animation_running:
            self.animation_running = False
            self.start_animation_btn.config(text="Start Animation")
            self.add_log_entry("Animation stopped")
        else:
            self.animation_running = True
            self.start_animation_btn.config(text="Stop Animation")
            self.add_log_entry("Animation started")
            
            # Start animation in a separate thread
            if self.animation_thread is None or not self.animation_thread.is_alive():
                self.animation_thread = threading.Thread(target=self.run_animation)
                self.animation_thread.daemon = True
                self.animation_thread.start()
    
    def run_animation(self):
        """Run a more accurate visualization animation of QKD protocol"""
        self.viz_canvas.delete("all")
        
        # Draw satellite and ground station
        canvas_width = self.viz_canvas.winfo_width()
        canvas_height = self.viz_canvas.winfo_height()
        
        # If canvas not yet realized, set default dimensions
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        # Draw satellite
        satellite_x = canvas_width // 2
        satellite_y = 80
        satellite = self.viz_canvas.create_oval(
            satellite_x - 25, satellite_y - 25, 
            satellite_x + 25, satellite_y + 25, 
            fill="#3498DB", outline="#ECF0F1", width=2
        )
        self.viz_canvas.create_text(
            satellite_x, satellite_y - 40, 
            text="Quantum Satellite", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        # Solar panels
        self.viz_canvas.create_rectangle(
            satellite_x - 60, satellite_y - 10, 
            satellite_x - 30, satellite_y + 10, 
            fill="#2C3E50", outline="#ECF0F1"
        )
        self.viz_canvas.create_rectangle(
            satellite_x + 30, satellite_y - 10, 
            satellite_x + 60, satellite_y + 10, 
            fill="#2C3E50", outline="#ECF0F1"
        )
        
        # Ground stations - Left is Alice (sender), Right is Bob (receiver)
        alice_x = canvas_width // 4
        alice_y = canvas_height - 80
        self.viz_canvas.create_rectangle(
            alice_x - 40, alice_y - 30, 
            alice_x + 40, alice_y + 30, 
            fill="#E74C3C", outline="#ECF0F1", width=2
        )
        self.viz_canvas.create_polygon(
            alice_x - 20, alice_y - 30, 
            alice_x, alice_y - 60, 
            alice_x + 20, alice_y - 30, 
            fill="#E74C3C", outline="#ECF0F1", width=2
        )
        self.viz_canvas.create_text(
            alice_x, alice_y + 50, 
            text="Alice (Sender)", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        # Bob (Receiver)
        bob_x = canvas_width * 3 // 4
        bob_y = canvas_height - 80
        self.viz_canvas.create_rectangle(
            bob_x - 40, bob_y - 30, 
            bob_x + 40, bob_y + 30, 
            fill="#2ECC71", outline="#ECF0F1", width=2
        )
        self.viz_canvas.create_polygon(
            bob_x - 20, bob_y - 30, 
            bob_x, bob_y - 60, 
            bob_x + 20, bob_y - 30, 
            fill="#2ECC71", outline="#ECF0F1", width=2
        )
        self.viz_canvas.create_text(
            bob_x, bob_y + 50, 
            text="Bob (Receiver)", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        # Add an interceptor if interception is on (Eve)
        interceptor_x = None
        if self.interception_var.get():
            interceptor_x = (alice_x + bob_x) // 2
            interceptor_y = canvas_height - 150
            self.viz_canvas.create_rectangle(
                interceptor_x - 30, interceptor_y - 20, 
                interceptor_x + 30, interceptor_y + 20, 
                fill="#F39C12", outline="#E67E22", width=2
            )
            self.viz_canvas.create_text(
                interceptor_x, interceptor_y + 35, 
                text="Eve (Interceptor)", fill="#F39C12", font=('Helvetica', 10)
            )
        
        # Add explanatory text
        info_x = 20
        info_y = 30
        self.viz_canvas.create_text(
            info_x, info_y, 
            text="QKD Protocol Animation", 
            fill="#FFFFFF", font=('Helvetica', 12, 'bold'),
            anchor=tk.W
        )
        
        # Protocol phases
        phase_texts = {
            1: "Phase 1: Quantum state distribution",
            2: "Phase 2: Measurement & basis selection",
            3: "Phase 3: Basis reconciliation",
            4: "Phase 4: Error detection & privacy amplification",
            5: "Phase 5: Secure key established"
        }
        
        phase_indicator = self.viz_canvas.create_text(
            info_x, info_y + 25, 
            text=phase_texts[1], 
            fill="#3498DB", font=('Helvetica', 11),
            anchor=tk.W
        )
        
        # Animation counters
        photon_count = 0
        phase = 1
        matched_bases = 0
        error_bits = 0
        
        # Create basis and bit value displays for Alice and Bob
        alice_basis_text = self.viz_canvas.create_text(
            alice_x, alice_y - 80, 
            text="Basis: ", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        bob_basis_text = self.viz_canvas.create_text(
            bob_x, bob_y - 80, 
            text="Basis: ", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        alice_bit_text = self.viz_canvas.create_text(
            alice_x, alice_y - 100, 
            text="Bit: ", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        bob_bit_text = self.viz_canvas.create_text(
            bob_x, bob_y - 100, 
            text="Bit: ", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        # Status text
        status_text = self.viz_canvas.create_text(
            canvas_width // 2, canvas_height - 20,
            text="", fill="#FFFFFF", font=('Helvetica', 10)
        )
        
        # Define BB84 simulation parameters
        total_photons = 20
        total_phases = 5
        basis_options = ["Rectilinear (H/V)", "Diagonal (D/A)"]
        bit_values = ["0", "1"]
        
        # Phase 1: Quantum state distribution (satellite to both stations)
        while self.animation_running and phase == 1 and photon_count < total_photons:
            # Update phase text
            self.viz_canvas.itemconfig(phase_indicator, text=phase_texts[phase])
            self.viz_canvas.itemconfig(status_text, text=f"Sending photon {photon_count+1}/{total_photons}")
            
            # Alice and Bob select random bases and bits
            alice_basis = np.random.choice(basis_options)
            bob_basis = np.random.choice(basis_options)
            alice_bit = np.random.choice(bit_values)
            
            # Update basis and bit displays
            self.viz_canvas.itemconfig(alice_basis_text, text=f"Basis: {alice_basis}")
            self.viz_canvas.itemconfig(alice_bit_text, text=f"Bit: {alice_bit}")
            
            # Satellite sends entangled photons to both Alice and Bob
            # Photon color indicates polarization state
            colors = {
                "0_Rectilinear (H/V)": "#3498DB",     # Horizontal (blue)
                "1_Rectilinear (H/V)": "#2980B9",     # Vertical (dark blue)
                "0_Diagonal (D/A)": "#9B59B6",         # Diagonal (purple) 
                "1_Diagonal (D/A)": "#8E44AD"          # Anti-diagonal (dark purple)
            }
            photon_color = colors[f"{alice_bit}_{alice_basis}"]
            
            # Create entangled photon pair
            photon_alice = self.viz_canvas.create_oval(
                satellite_x - 3, satellite_y - 3,
                satellite_x + 3, satellite_y + 3,
                fill=photon_color, outline="#FFFFFF"
            )
            
            photon_bob = self.viz_canvas.create_oval(
                satellite_x - 3, satellite_y - 3,
                satellite_x + 3, satellite_y + 3,
                fill=photon_color, outline="#FFFFFF"
            )
            
            # Animate photons moving to Alice and Bob
            steps = 20
            for i in range(steps):
                if not self.animation_running:
                    break
                    
                # Progress for each photon path
                progress = i / steps
                
                # Alice's photon position
                alice_photon_x = satellite_x + (alice_x - satellite_x) * progress
                alice_photon_y = satellite_y + (alice_y - satellite_y) * progress
                
                # Bob's photon position
                bob_photon_x = satellite_x + (bob_x - satellite_x) * progress
                bob_photon_y = satellite_y + (bob_y - satellite_y) * progress
                
                # Interception simulation
                if self.interception_var.get() and progress > 0.4 and progress < 0.6:
                    # Eve intercepts Bob's photon
                    if progress == 0.5:
                        # Eve measures with random basis
                        eve_basis = np.random.choice(basis_options)
                        if eve_basis != alice_basis:
                            # If Eve uses wrong basis, the quantum state changes
                            photon_color = np.random.choice(list(colors.values()))
                            self.viz_canvas.itemconfig(photon_bob, fill=photon_color)
                    
                    # Route through the interceptor
                    if progress <= 0.5:
                        bob_photon_x = satellite_x + (interceptor_x - satellite_x) * (progress * 2)
                        bob_photon_y = satellite_y + (interceptor_y - satellite_y) * (progress * 2)
                    else:
                        # Continue from interceptor to Bob
                        adjusted_progress = (progress - 0.5) * 2
                        bob_photon_x = interceptor_x + (bob_x - interceptor_x) * adjusted_progress  
                        bob_photon_y = interceptor_y + (bob_y - bob_y) * adjusted_progress
                
                # Update photon positions
                self.viz_canvas.coords(photon_alice, 
                                    alice_photon_x - 3, alice_photon_y - 3, 
                                    alice_photon_x + 3, alice_photon_y + 3)
                
                self.viz_canvas.coords(photon_bob, 
                                    bob_photon_x - 3, bob_photon_y - 3, 
                                    bob_photon_x + 3, bob_photon_y + 3)
                
                self.viz_canvas.update()
                time.sleep(0.03)
            
            # Bob measures with his chosen basis
            bob_measured_bit = alice_bit if bob_basis == alice_basis else np.random.choice(bit_values)
            self.viz_canvas.itemconfig(bob_basis_text, text=f"Basis: {bob_basis}")
            self.viz_canvas.itemconfig(bob_bit_text, text=f"Bit: {bob_measured_bit if bob_basis == alice_basis else '?'}")
            
            # Delete photons after arrival
            self.viz_canvas.delete(photon_alice)
            self.viz_canvas.delete(photon_bob)
            
            # Count matching bases
            if bob_basis == alice_basis:
                matched_bases += 1
                # With interception, some errors may occur even with matching bases
                if self.interception_var.get() and np.random.random() < 0.3:
                    error_bits += 1
            
            photon_count += 1
            time.sleep(0.3)
        
        # Move to Phase 2: Measurement results
        if self.animation_running:
            phase = 2
            photon_count = 0
            self.viz_canvas.itemconfig(phase_indicator, text=phase_texts[phase])
            self.viz_canvas.itemconfig(status_text, text="Measuring quantum states...")
            time.sleep(1.5)
        
        # Phase 3: Basis reconciliation over classical channel
        if self.animation_running:
            phase = 3
            self.viz_canvas.itemconfig(phase_indicator, text=phase_texts[phase])
            self.viz_canvas.itemconfig(status_text, text="Exchanging basis information over classical channel...")
            
            # Animate classical communication
            steps = 15
            for i in range(steps):
                if not self.animation_running:
                    break
                
                # Create classical communication packet
                if i % 3 == 0:
                    # Alice to Bob
                    packet = self.viz_canvas.create_rectangle(
                        alice_x - 5, alice_y - 5,
                        alice_x + 5, alice_y + 5,
                        fill="#3498DB", outline="#FFFFFF"
                    )
                    
                    # Animate packet
                    for j in range(10):
                        if not self.animation_running:
                            break
                        
                        progress = j / 10
                        packet_x = alice_x + (bob_x - alice_x) * progress
                        packet_y = alice_y
                        
                        self.viz_canvas.coords(packet, 
                                            packet_x - 5, packet_y - 5,
                                            packet_x + 5, packet_y + 5)
                        self.viz_canvas.update()
                        time.sleep(0.03)
                        
                    self.viz_canvas.delete(packet)
                else:
                    # Bob to Alice
                    packet = self.viz_canvas.create_rectangle(
                        bob_x - 5, bob_y - 5,
                        bob_x + 5, bob_y + 5,
                        fill="#2ECC71", outline="#FFFFFF"
                    )
                    
                    # Animate packet
                    for j in range(10):
                        if not self.animation_running:
                            break
                        
                        progress = j / 10
                        packet_x = bob_x - (bob_x - alice_x) * progress
                        packet_y = bob_y
                        
                        self.viz_canvas.coords(packet, 
                                            packet_x - 5, packet_y - 5,
                                            packet_x + 5, packet_y + 5)
                        self.viz_canvas.update()
                        time.sleep(0.03)
                        
                    self.viz_canvas.delete(packet)
                
                time.sleep(0.1)
        
        # Phase 4: Error detection & privacy amplification
        if self.animation_running:
            phase = 4
            self.viz_canvas.itemconfig(phase_indicator, text=phase_texts[phase])
            
            # Show security statistics
            match_percentage = (matched_bases / total_photons) * 100
            error_percentage = (error_bits / max(matched_bases, 1)) * 100
            
            error_status = "Error rate above threshold!" if error_percentage > 10 else "Error rate acceptable"
            status_color = "#E74C3C" if error_percentage > 10 else "#2ECC71"
            
            self.viz_canvas.itemconfig(status_text, 
                                    text=f"Matching bases: {matched_bases}/{total_photons} ({match_percentage:.1f}%) | " +
                                        f"Error rate: {error_percentage:.1f}% | {error_status}")
            self.viz_canvas.itemconfig(status_text, fill=status_color)
            
            # Show error correction and privacy amplification
            time.sleep(1.5)
        
        # Phase 5: Secure key established (or aborted)
        if self.animation_running:
            phase = 5
            self.viz_canvas.itemconfig(phase_indicator, text=phase_texts[phase])
            
            # Key establishment result
            secure_key = error_percentage <= 10
            if secure_key:
                # Secure key - show key transfer animation
                self.viz_canvas.itemconfig(status_text, 
                                        text="Secure key established! Encrypted communication enabled.",
                                        fill="#2ECC71")
                
                # Animate data transfer using the key
                for i in range(10):
                    if not self.animation_running:
                        break
                    
                    # Encrypted data packet
                    packet = self.viz_canvas.create_rectangle(
                        alice_x - 8, alice_y - 8,
                        alice_x + 8, alice_y + 8,
                        fill="#27AE60", outline="#FFFFFF", width=2
                    )
                    
                    # Animate packet
                    for j in range(15):
                        if not self.animation_running:
                            break
                        
                        progress = j / 15
                        packet_x = alice_x + (bob_x - alice_x) * progress
                        packet_y = alice_y
                        
                        self.viz_canvas.coords(packet, 
                                            packet_x - 8, packet_y - 8,
                                            packet_x + 8, packet_y + 8)
                        self.viz_canvas.update()
                        time.sleep(0.04)
                        
                    self.viz_canvas.delete(packet)
                    time.sleep(0.1)
            else:
                # Aborted due to interception
                self.viz_canvas.itemconfig(status_text, 
                                        text="Security breach detected! Key exchange aborted.",
                                        fill="#E74C3C")
            
        # Reset animation state at end
        if not self.animation_running:
            self.start_animation_btn.config(text="Start Animation")
    
    def run_simulation(self):
        """Run the quantum key distribution simulation"""
        # Get data from input fields
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message to encrypt")
            return
        
        # Get interception setting
        simulate_interception = self.interception_var.get()
        
        # Update UI
        self.set_status("Running simulation...")
        self.add_log_entry(f"Starting simulation with message: '{message}'")
        if simulate_interception:
            self.add_log_entry("Interception simulation enabled")
        
        # Run simulation
        results = self.simulate_qkd_satellite(message, simulate_interception)
        
        # Display results
        self.display_results(results)
        
    def display_results(self, results):
        """Display the simulation results in the appropriate text areas"""
        # Update summary text
        self.summary_text.configure(state='normal')
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, f"Simulation Results Summary\n")
        self.summary_text.insert(tk.END, f"=========================\n\n")
        self.summary_text.insert(tk.END, f"Original Message: {results['original_message']}\n")
        self.summary_text.insert(tk.END, f"Encrypted Message: {results['encrypted_message'][:50]}...\n")
        self.summary_text.insert(tk.END, f"Decrypted Message: {results['decrypted_message']}\n\n")
        self.summary_text.insert(tk.END, f"Key Generation:\n")
        self.summary_text.insert(tk.END, f"  - Raw Key Size: {results['raw_key_size']} bits\n")
        self.summary_text.insert(tk.END, f"  - Final Key Size: {results['final_key_size']} bits\n")
        self.summary_text.insert(tk.END, f"  - QBER: {results['qber']:.2f}%\n\n")
        self.summary_text.insert(tk.END, f"Security Status: {results['security_status']}\n")
        self.summary_text.configure(state='disabled')
        
        # Update details text
        self.details_text.configure(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, "Quantum Key Distribution Details\n")
        self.details_text.insert(tk.END, "================================\n\n")
        self.details_text.insert(tk.END, f"Quantum Protocol: BB84\n")
        self.details_text.insert(tk.END, f"Channel Type: Satellite-to-Ground\n\n")
        self.details_text.insert(tk.END, f"Basis Reconciliation:\n")
        self.details_text.insert(tk.END, f"  - Alice's Bases: {results['alice_bases'][:20]}...\n")
        self.details_text.insert(tk.END, f"  - Bob's Bases: {results['bob_bases'][:20]}...\n")
        self.details_text.insert(tk.END, f"  - Matching Bases: {results['matching_bases']} ({results['matching_percentage']:.1f}%)\n\n")
        self.details_text.insert(tk.END, f"Key Sample (first 64 bits):\n")
        self.details_text.insert(tk.END, f"  - Raw Key: {results['raw_key'][:64]}...\n")
        self.details_text.insert(tk.END, f"  - Final Key: {results['final_key'][:64]}...\n")
        self.details_text.configure(state='disabled')
        
        # Update security text
        self.security_text.configure(state='normal')
        self.security_text.delete(1.0, tk.END)
        self.security_text.insert(tk.END, "Security Analysis\n")
        self.security_text.insert(tk.END, "================\n\n")
        
        # Display different security information based on interception status
        if results['intercept_detected']:
            self.security_text.insert(tk.END, "⚠️ SECURITY ALERT: Possible intercept detected ⚠️\n\n")
            self.security_text.insert(tk.END, f"QBER Analysis:\n")
            self.security_text.insert(tk.END, f"  - Measured QBER: {results['qber']:.2f}%\n")
            self.security_text.insert(tk.END, f"  - Threshold QBER: {results['qber_threshold']:.2f}%\n")
            self.security_text.insert(tk.END, f"  - Status: Above threshold (potential eavesdropping)\n\n")
            self.security_text.insert(tk.END, f"Interception Assessment:\n")
            self.security_text.insert(tk.END, f"  - Estimated data compromised: {results['compromise_estimate']:.1f}%\n")
            self.security_text.insert(tk.END, f"  - Confidence level: {results['confidence_level']:.1f}%\n\n")
            self.security_text.insert(tk.END, f"Security Recommendation:\n")
            self.security_text.insert(tk.END, f"  - Abort key and restart QKD with new parameters\n")
            self.security_text.insert(tk.END, f"  - Investigate potential security breach\n")
        else:
            self.security_text.insert(tk.END, "✓ Secure Communication Channel ✓\n\n")
            self.security_text.insert(tk.END, f"QBER Analysis:\n")
            self.security_text.insert(tk.END, f"  - Measured QBER: {results['qber']:.2f}%\n")
            self.security_text.insert(tk.END, f"  - Threshold QBER: {results['qber_threshold']:.2f}%\n")
            self.security_text.insert(tk.END, f"  - Status: Below threshold (no evidence of eavesdropping)\n\n")
            self.security_text.insert(tk.END, f"Privacy Amplification:\n")
            self.security_text.insert(tk.END, f"  - Estimated entropy reduction: {results['entropy_reduction']:.1f}%\n")
            self.security_text.insert(tk.END, f"  - Security parameter: {results['security_parameter']} bits\n\n")
            self.security_text.insert(tk.END, f"Information Leakage Estimate:\n")
            self.security_text.insert(tk.END, f"  - Maximum leakage: < {results['max_leakage']:.8f} bits\n")
            self.security_text.insert(tk.END, f"  - Channel security: {results['channel_security']}\n")
        
        self.security_text.configure(state='disabled')
        
        # Store security states for animation
        self.security_states = results['security_timeline']
        
        # Log the completion
        self.add_log_entry("Simulation completed successfully")
        self.set_status("Simulation complete")
        
        # Switch to visualization tab if not already there
        self.notebook.select(self.visualization_tab)
        
        # Start animation automatically
        if not self.animation_running:
            self.toggle_animation()
    
    def simulate_qkd_satellite(self, message, simulate_interception=False):
        """
        Simulate the quantum key distribution process using a satellite
        
        Args:
            message (str): The message to encrypt
            simulate_interception (bool): Whether to simulate an interception
            
        Returns:
            dict: Simulation results
        """
        # Show a progress bar during simulation
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Simulation in Progress")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Set window position
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        progress_window.geometry(f"+{x}+{y}")
        
        # Progress bar and label
        ttk.Label(progress_window, text="Running Quantum Key Distribution Simulation...", 
                  font=('Helvetica', 11)).pack(pady=(20, 10))
        
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=350, mode="determinate")
        progress.pack(pady=10, padx=20)
        
        status_label = ttk.Label(progress_window, text="Initializing...", font=('Helvetica', 10))
        status_label.pack(pady=10)
        
        # Simulation steps
        steps = [
            "Generating entangled photon pairs...",
            "Distributing quantum states...",
            "Measuring quantum states...",
            "Performing basis reconciliation...",
            "Estimating quantum bit error rate...",
            "Error correction in progress...",
            "Privacy amplification...",
            "Generating final key...",
            "Encrypting message...",
            "Transmitting data...",
            "Decrypting message...",
            "Verifying security...",
            "Finalizing results..."
        ]
        
        # Simulate the process with delays
        for i, step in enumerate(steps):
            progress["value"] = (i / len(steps)) * 100
            status_label.config(text=step)
            progress_window.update()
            time.sleep(0.3)  # Simulated delay
        
        progress["value"] = 100
        status_label.config(text="Completed!")
        progress_window.update()
        time.sleep(0.5)
        
        # Close progress window
        progress_window.destroy()
        
        # Simulate actual QKD
        # Generate random bit sequence for Alice and Bob's bases
        sequence_length = 1024
        alice_bases = ''.join(np.random.choice(['0', '1'], size=sequence_length).tolist())
        bob_bases = ''.join(np.random.choice(['0', '1'], size=sequence_length).tolist())
        
        # Generate raw quantum bits
        raw_bits = ''.join(np.random.choice(['0', '1'], size=sequence_length).tolist())
        
        # Calculate matching bases
        matching_indices = [i for i in range(sequence_length) if alice_bases[i] == bob_bases[i]]
        matching_bases = len(matching_indices)
        matching_percentage = (matching_bases / sequence_length) * 100
        
        # Extract raw key from matching bases
        raw_key = ''.join([raw_bits[i] for i in matching_indices])
        raw_key_size = len(raw_key)
        
        # Calculate QBER (Quantum Bit Error Rate)
        if simulate_interception:
            # Higher QBER if interception is simulated
            qber = np.random.uniform(15.0, 25.0)  # 15-25% error rate with interception
            intercept_detected = True
        else:
            # Normal QBER range
            qber = np.random.uniform(2.0, 8.0)  # 2-8% error rate without interception
            intercept_detected = qber > 11.0  # Threshold for detecting interception
        
        # Error correction and privacy amplification
        # Simulate by reducing key length
        error_correction_reduction = int(raw_key_size * 0.2)  # 20% reduction for error correction
        privacy_amplification_reduction = int(raw_key_size * 0.1)  # 10% reduction for privacy
        
        final_key_size = raw_key_size - error_correction_reduction - privacy_amplification_reduction
        
        # Ensure we have a key, even if it's very short
        final_key_size = max(final_key_size, 16)
        
        # Generate final key (simulated)
        final_key = ''.join(np.random.choice(['0', '1'], size=final_key_size).tolist())
        
        # Convert binary key to bytes (for encryption)
        key_bytes = bytes([int(final_key[i:i+8], 2) for i in range(0, len(final_key), 8)])
        
        # Simple encryption (XOR with key)
        message_bytes = message.encode('utf-8')
        key_repeated = key_bytes * (len(message_bytes) // len(key_bytes) + 1)
        encrypted_message = bytes([a ^ b for a, b in zip(message_bytes, key_repeated[:len(message_bytes)])])
        
        # Encrypted message as hex
        encrypted_hex = encrypted_message.hex()
        
        # Decrypt (same operation as encryption with XOR)
        decrypted_message = bytes([a ^ b for a, b in zip(encrypted_message, key_repeated[:len(encrypted_message)])])
        decrypted_text = decrypted_message.decode('utf-8')
        
        # Security parameters
        qber_threshold = 10.0
        entropy_reduction = np.random.uniform(10.0, 20.0)
        security_parameter = np.random.randint(50, 200)
        max_leakage = 2 ** (-security_parameter / 8)
        
        # Determine security status
        if intercept_detected:
            security_status = "COMPROMISED"
            channel_security = "INSECURE"
            compromise_estimate = np.random.uniform(20.0, 60.0)
            confidence_level = np.random.uniform(70.0, 99.0)
        else:
            security_status = "SECURE"
            channel_security = "SECURE"
            compromise_estimate = 0.0
            confidence_level = 99.9
        
        # Generate a timeline of security states for animation
        security_timeline = []
        for _ in range(20):
            if intercept_detected:
                # More fluctuations and higher error rates
                security_timeline.append({
                    'qber': np.random.uniform(12.0, 25.0),
                    'status': 'WARNING' if np.random.random() < 0.7 else 'ALERT'
                })
            else:
                # Lower, stable error rates
                security_timeline.append({
                    'qber': np.random.uniform(1.0, 8.0),
                    'status': 'SECURE' if np.random.random() < 0.9 else 'CHECK'
                })
        
        # Return simulation results
        return {
            'original_message': message,
            'encrypted_message': encrypted_hex,
            'decrypted_message': decrypted_text,
            'alice_bases': alice_bases,
            'bob_bases': bob_bases,
            'matching_bases': matching_bases,
            'matching_percentage': matching_percentage,
            'raw_key': raw_key,
            'raw_key_size': raw_key_size,
            'final_key': final_key,
            'final_key_size': final_key_size,
            'qber': qber,
            'qber_threshold': qber_threshold,
            'intercept_detected': intercept_detected,
            'security_status': security_status,
            'security_timeline': security_timeline,
            'entropy_reduction': entropy_reduction,
            'security_parameter': security_parameter,
            'max_leakage': max_leakage,
            'channel_security': channel_security,
            'compromise_estimate': compromise_estimate,
            'confidence_level': confidence_level
        }

if __name__ == "__main__":
    root = tk.Tk()
    app = QKDSatelliteSystem(root)
    root.mainloop()
    
    # Clean up temporary files
    try:
        if os.path.exists("temp_icon.png"):
            os.remove("temp_icon.png")
    except:
        pass