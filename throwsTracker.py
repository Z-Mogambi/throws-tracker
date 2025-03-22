import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class throwsTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Throwing Performance Tracker")
        self.root.geometry("800x600")

        # Data storage
        self.throws = self.load_data()

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Record Throw", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Event selection
        ttk.Label(input_frame, text="Event:").grid(row=0, column=0, sticky=tk.W)
        self.event_var = tk.StringVar(value="shotput")
        event_combo = ttk.Combobox(input_frame, textvariable=self.event_var, values=["shotput", "discus"], state="readonly")
        event_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        event_combo.bind('<<ComboboxSelected>>', lambda e: self.update_displays())

        # Throw type selection
        ttk.Label(input_frame, text="Throw Type:").grid(row=0, column=2, sticky=tk.W)
        self.throw_type_var = tk.StringVar(value="standing")
        throw_type_combo = ttk.Combobox(input_frame, textvariable=self.throw_type_var,
                                      values=["standing", "half", "full"], state="readonly")
        throw_type_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5)
        throw_type_combo.bind('<<ComboboxSelected>>', lambda e: self.update_displays())

        # Distance input
        ttk.Label(input_frame, text="Distance:").grid(row=1, column=0, sticky=tk.W)
        self.distance_var = tk.StringVar()
        distance_entry = ttk.Entry(input_frame, textvariable=self.distance_var)
        distance_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        # Unit selection
        self.unit_var = tk.StringVar(value="meters")
        ttk.Radiobutton(input_frame, text="Meters", variable=self.unit_var,
                       value="meters", command=self.update_displays).grid(row=1, column=2)
        ttk.Radiobutton(input_frame, text="Feet", variable=self.unit_var,
                       value="feet", command=self.update_displays).grid(row=1, column=3)

        # Record button
        record_btn = ttk.Button(input_frame, text="Record Throw", command=self.record_throw)
        record_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # Statistics section
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.stats_text = tk.Text(stats_frame, height=10, width=40)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Predictions section
        pred_frame = ttk.LabelFrame(main_frame, text="Predictions", padding="10")
        pred_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.pred_text = tk.Text(pred_frame, height=10, width=40)
        self.pred_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Update displays
        self.update_displays()

    def load_data(self):
        if os.path.exists('throws.json'):
            try:
                with open('throws.json', 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open('throws.json', 'w') as f:
            json.dump(self.throws, f)

    def convert_to_meters(self, distance, unit):
        return distance * 0.3048 if unit == "feet" else distance

    def convert_to_display_unit(self, distance_meters):
        return distance_meters * 3.28084 if self.unit_var.get() == "feet" else distance_meters

    def record_throw(self):
        try:
            distance = float(self.distance_var.get())
            if distance <= 0:
                raise ValueError("Distance must be positive")

            # Store all measurements in meters internally
            distance_meters = self.convert_to_meters(distance, self.unit_var.get())

            throw = {
                'event': self.event_var.get(),
                'type': self.throw_type_var.get(),
                'distance': distance_meters,  # Always store in meters
                'unit': 'meters',  # Always store in meters
                'date': datetime.now().isoformat()
            }

            self.throws.append(throw)
            self.save_data()
            self.distance_var.set("")  # Clear input
            self.update_displays()
            messagebox.showinfo("Success", "Throw recorded successfully!")

        except ValueError as e:
            messagebox.showerror("Error", "Please enter a valid positive number for distance.")
           def calculate_average(self, event_type, throw_type):
        relevant_throws = [t for t in self.throws
                         if t['event'] == event_type and t['type'] == throw_type]
        if not relevant_throws:
            return 0
        avg_meters = sum(t['distance'] for t in relevant_throws) / len(relevant_throws)
        return self.convert_to_display_unit(avg_meters)

    def calculate_predictions(self, event_type):
        standing_avg = self.calculate_average(event_type, 'standing')
        if standing_avg == 0:
            return None

        # Typical progression ratios
        half_prediction = standing_avg * 1.115
        full_prediction = half_prediction * 1.048

        return {
            'half': half_prediction,
            'full': full_prediction
        }

    def update_displays(self):
        # Update statistics
        self.stats_text.delete(1.0, tk.END)
        unit = self.unit_var.get()

        self.stats_text.insert(tk.END, f"Shot Put Averages ({unit}):\n")
        self.stats_text.insert(tk.END, f"Standing: {self.calculate_average('shotput', 'standing'):.2f}\n")
        self.stats_text.insert(tk.END, f"Half Turn: {self.calculate_average('shotput', 'half'):.2f}\n")
        self.stats_text.insert(tk.END, f"Full Turn: {self.calculate_average('shotput', 'full'):.2f}\n\n")

        self.stats_text.insert(tk.END, f"Discus Averages ({unit}):\n")
        self.stats_text.insert(tk.END, f"Standing: {self.calculate_average('discus', 'standing'):.2f}\n")
        self.stats_text.insert(tk.END, f"Half Turn: {self.calculate_average('discus', 'half'):.2f}\n")
        self.stats_text.insert(tk.END, f"Full Turn: {self.calculate_average('discus', 'full'):.2f}\n")

        # Update predictions
        self.pred_text.delete(1.0, tk.END)
        for event in ['shotput', 'discus']:
            predictions = self.calculate_predictions(event)
            self.pred_text.insert(tk.END, f"\n{event.title()} Predictions ({unit}):\n")
            if predictions:
                self.pred_text.insert(tk.END, f"Predicted Half Turn: {predictions['half']:.2f}\n")
                self.pred_text.insert(tk.END, f"Predicted Full Turn: {predictions['full']:.2f}\n")
            else:
                self.pred_text.insert(tk.END, "Need standing throws for predictions\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = throwsTracker(root)
    root.mainloop()
