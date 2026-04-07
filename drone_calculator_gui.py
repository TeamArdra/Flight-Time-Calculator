import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DroneCalculatorApp(tk.Tk):
    """
    A GUI application for calculating drone flight time based on user-provided specs.
    """
    def __init__(self):
        super().__init__()

        self.title("Drone Flight Time Calculator")
        self.geometry("400x520")  # Adjusted window size
        self.resizable(False, False)

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TLabel", font=("Inter", 10))
        style.configure("TButton", font=("Inter", 11, "bold"), padding=10)
        style.configure("Header.TLabel", font=("Inter", 16, "bold"))
        style.configure("Result.TLabel", font=("Inter", 24, "bold"), foreground="#007bff")
        style.configure("Amp.TLabel", font=("Inter", 12, "bold"))  # New style for amp draw

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill="both")

        # --- Header ---
        header_label = ttk.Label(main_frame, text="Flight Time Estimator", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- Input Fields ---
        self.create_input_field(main_frame, "Battery Capacity (mAh):", 1)
        self.create_input_field(main_frame, "Total Weight (AUW in kg):", 2)
        self.create_input_field(main_frame, "Power Consumption (watts/kg):", 3)
        self.create_input_field(main_frame, "Battery Voltage (V):", 4)
        
        # --- Store entry widgets for easy access ---
        self.capacity_var = self.entries["Battery Capacity (mAh):"]
        self.weight_var = self.entries["Total Weight (AUW in kg):"]
        self.power_var = self.entries["Power Consumption (watts/kg):"]
        self.voltage_var = self.entries["Battery Voltage (V):"]

        # --- Calculate Button ---
        calculate_button = ttk.Button(main_frame, text="Calculate Flight Time", command=self.calculate)
        calculate_button.grid(row=5, column=0, columnspan=2, pady=20)

        # --- Result Display ---
        self.result_var = tk.StringVar(value="0.00")
        self.amp_draw_var = tk.StringVar(value="0.00")  # Variable for average amp draw

        result_label_prefix = ttk.Label(main_frame, text="Estimated Flight Time:")
        result_label_prefix.grid(row=6, column=0, columnspan=2, pady=(10, 5))

        result_display_frame = ttk.Frame(main_frame)
        result_display_frame.grid(row=7, column=0, columnspan=2)

        result_value_label = ttk.Label(result_display_frame, textvariable=self.result_var, style="Result.TLabel")
        result_value_label.pack(side="left")

        result_unit_label = ttk.Label(result_display_frame, text=" minutes", font=("Inter", 14))
        result_unit_label.pack(side="left", anchor="s", pady=4)

        # --- Average Ampere Draw (AAD) Display ---
        aad_label_prefix = ttk.Label(main_frame, text="Average Ampere Draw:")
        aad_label_prefix.grid(row=8, column=0, columnspan=2, pady=(10, 5))

        aad_display_frame = ttk.Frame(main_frame)
        aad_display_frame.grid(row=9, column=0, columnspan=2)

        aad_value_label = ttk.Label(aad_display_frame, textvariable=self.amp_draw_var, style="Result.TLabel")
        aad_value_label.pack(side="left")

        aad_unit_label = ttk.Label(aad_display_frame, text=" amps (A)", font=("Inter", 14))
        aad_unit_label.pack(side="left", anchor="s", pady=4)

    def create_input_field(self, parent, label_text, row):
        """Helper method to create a labeled entry field."""
        if not hasattr(self, 'entries'):
            self.entries = {}
        
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        
        entry_var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=entry_var, width=20, font=("Inter", 10))
        entry.grid(row=row, column=1, sticky="e", padx=5, pady=5)
        
        self.entries[label_text] = entry_var
        return entry_var

    def calculate(self):
        """Performs the flight time calculation and updates the GUI."""
        try:
            # --- Get values from input fields ---
            capacity = float(self.capacity_var.get())
            auw = float(self.weight_var.get())
            power = float(self.power_var.get())
            voltage = float(self.voltage_var.get())

            # --- Constants ---
            DISCHARGE_FACTOR = 80

            # --- Calculations based on standard formulas ---
            total_power_draw = auw * power  # Total power in watts
            aad = total_power_draw / voltage # Amps = Watts / Volts

            # Formula for Time
            # time (hours) = usable capacity (Ah) / amp draw (A)
            usable_capacity_ah = (capacity / 1000) * DISCHARGE_FACTOR
            time_minutes = usable_capacity_ah / aad

            self.result_var.set(f"{time_minutes:.2f}")
            self.amp_draw_var.set(f"{aad:.2f}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in all fields.")
        except ZeroDivisionError:
            messagebox.showerror("Calculation Error", "Voltage and Power Consumption cannot be zero. Please enter a valid number.")

# --- Run the Application ---
if __name__ == "__main__":
    app = DroneCalculatorApp()
    app.mainloop()