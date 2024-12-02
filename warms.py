import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class WaterRocketSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("WaRMS - Simulatore Motore Razzo ad Acqua")
        self.curves = []
        self.impulses = []
        
        # Frame principale
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="WENS")#(tk.W, tk.E, tk.N, tk.S))
        
        # Frame parametri motore
        motor_frame = ttk.LabelFrame(main_frame, text="Parametri Motore", padding="5")
        motor_frame.grid(row=0, column=0, sticky="WENS", padx=5, pady=5)
        
        # Parametri bottiglia
        ttk.Label(motor_frame, text="Lunghezza (mm):").grid(row=0, column=0, sticky="W")
        self.length_var = tk.DoubleVar(value=330.0)  # Tipica bottiglia da 2L
        ttk.Entry(motor_frame, textvariable=self.length_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(motor_frame, text="Diametro (mm):").grid(row=0, column=2, sticky="W")
        self.diameter_var = tk.DoubleVar(value=110.0)  # Tipica bottiglia da 2L
        ttk.Entry(motor_frame, textvariable=self.diameter_var, width=10).grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(motor_frame, text="Massa bottiglia (g):").grid(row=0, column=4, sticky="W")
        self.bottle_mass_var = tk.DoubleVar(value=100.0)  # Massa tipica bottiglia PET 2L
        ttk.Entry(motor_frame, textvariable=self.bottle_mass_var, width=10).grid(row=0, column=5, padx=5, pady=2)
        
        # Frame parametri operativi
        params_frame = ttk.LabelFrame(main_frame, text="Parametri Operativi", padding="5")
        params_frame.grid(row=1, column=0, sticky="WENS", padx=5, pady=5)
        
        # Slider e label per pressione
        ttk.Label(params_frame, text="Pressione (bar):").grid(row=0, column=0, sticky="W")
        self.pressure_var = tk.DoubleVar(value=3.0)
        self.pressure_label = ttk.Label(params_frame, text="3.0")
        self.pressure_label.grid(row=0, column=2, sticky="E")
        pressure_slider = ttk.Scale(params_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                  variable=self.pressure_var, command=self.update_pressure_label)
        pressure_slider.grid(row=0, column=1, sticky="WE", padx=5, pady=5)
        
        # Slider per rapporto acqua
        ttk.Label(params_frame, text="Rapporto Acqua (%):").grid(row=0, column=4, sticky="W")
        self.water_ratio_var = tk.DoubleVar(value=33.0)
        self.water_ratio_label = ttk.Label(params_frame, text="33.0")
        self.water_ratio_label.grid(row=0, column=6, sticky="E")
        water_ratio_slider = ttk.Scale(params_frame, from_=10, to=90, orient=tk.HORIZONTAL,
                                     variable=self.water_ratio_var, command=self.update_water_ratio_label)
        water_ratio_slider.grid(row=0, column=5, sticky="WE", padx=5, pady=5)
        
        # Slider per diametro ugello
        ttk.Label(params_frame, text="Diametro Ugello (mm):").grid(row=1, column=0, sticky="W")
        self.nozzle_diameter_var = tk.DoubleVar(value=8.0)
        self.nozzle_diameter_label = ttk.Label(params_frame, text="8.0")
        self.nozzle_diameter_label.grid(row=1, column=2, sticky="E")
        nozzle_diameter_slider = ttk.Scale(params_frame, from_=4, to=12, orient=tk.HORIZONTAL,
                                         variable=self.nozzle_diameter_var, command=self.update_nozzle_diameter_label)
        nozzle_diameter_slider.grid(row=1, column=1, sticky="WE", padx=5, pady=5)
        
        # Slider per volume bottiglia
        ttk.Label(params_frame, text="Volume Bottiglia (L):").grid(row=1, column=4, sticky="W")
        self.bottle_volume_var = tk.DoubleVar(value=2.0)
        self.bottle_volume_label = ttk.Label(params_frame, text="2.0")
        self.bottle_volume_label.grid(row=1, column=6, sticky="E")
        bottle_volume_slider = ttk.Scale(params_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL,
                                     variable=self.bottle_volume_var, command=self.update_bottle_volume_label)
        bottle_volume_slider.grid(row=1, column=5, sticky="WE", padx=5, pady=5)
        
        # Frame pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        ttk.Button(button_frame, text="Calcola", command=self.calculate_curve).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancella Tutto", command=self.clear_curves).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Esporta RASP", command=self.export_rasp).grid(row=0, column=2, padx=5)
        
        # Setup grafico
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, sticky="WENS")
        
        self.ax.set_xlabel('Tempo (ms)')
        self.ax.set_ylabel('Spinta (N)')
        self.ax.set_title('Curva di Spinta Razzo ad Acqua')
        self.ax.grid(True)
        
        # Memorizza l'ultima curva calcolata per l'export
        self.last_time = None
        self.last_thrust = None
        
    def update_pressure_label(self, value):
        self.pressure_label.config(text=f"{float(value):.1f}")
        
    def update_water_ratio_label(self, value):
        self.water_ratio_label.config(text=f"{float(value):.1f}")
        
    def update_nozzle_diameter_label(self, value):
        self.nozzle_diameter_label.config(text=f"{float(value):.1f}")
    
    def update_bottle_volume_label(self, value):
        self.bottle_volume_label.config(text=f"{float(value):.1f}")
        
    def calculate_thrust_curve(self, bottle_volume, water_ratio, pressure, nozzle_diameter):
        # Conversione unità
        water_volume = bottle_volume * water_ratio/100
        initial_pressure = pressure * 1e5 + 1e5
        nozzle_area = np.pi * (nozzle_diameter/2000)**2
        
        # Costanti
        gamma = 1.4
        rho_water = 1000
        Cd = 0.95
        
        # Stima del tempo totale
        estimated_time = 0.5 * water_volume / (Cd * nozzle_area * np.sqrt(2 * rho_water * (initial_pressure - 1e5)))
        
        # Genera punti temporali
        t = np.linspace(0, estimated_time, 1000)
        thrust = np.zeros_like(t)
        
        for i, time in enumerate(t):
            water_remaining = max(0, water_volume * (1 - time/estimated_time))
            air_volume = bottle_volume - water_remaining
            initial_air_volume = bottle_volume - water_volume
            
            current_pressure = initial_pressure * (initial_air_volume/air_volume)**gamma
            
            if water_remaining > 0:
                exit_velocity = Cd * np.sqrt(2 * (current_pressure - 1e5) / rho_water)
                mass_flow = Cd * nozzle_area * np.sqrt(2 * rho_water * (current_pressure - 1e5))
                thrust[i] = mass_flow * exit_velocity
        
        return t * 1000, thrust  # converti tempo in millisecondi
    
    def calculate_curve(self):
        t, thrust = self.calculate_thrust_curve(
            bottle_volume=self.bottle_volume_var.get(),  # Ora usa il volume dallo slider
            water_ratio=self.water_ratio_var.get(),
            pressure=self.pressure_var.get(),
            nozzle_diameter=self.nozzle_diameter_var.get()
        )
        
        # Calcola l'impulso totale (N⋅s)
        impulse = np.trapezoid(thrust, t/1000)  # dividi per 1000 per tornare ai secondi
        self.impulses.append(impulse)
        
        # Salva l'ultima curva calcolata
        self.last_time = t
        self.last_thrust = thrust
        
        # Aggiungi la nuova curva
        colors = ['b', 'g', 'r', 'c', 'm', 'y']
        line, = self.ax.plot(t, thrust, color=colors[len(self.curves) % len(colors)],
                            label=f'V={self.bottle_volume_var.get():.1f}L, P={self.pressure_var.get():.1f}bar, '
                                  f'W={self.water_ratio_var.get():.0f}%, D={self.nozzle_diameter_var.get():.1f}mm, '
                                  f'I={impulse:.2f}N⋅s')
        self.curves.append(line)
        
        self.ax.legend()#bbox_to_anchor=(1.05, 1), loc='upper left')
        self.canvas.draw()
        
    def clear_curves(self):
        for line in self.curves:
            line.remove()
        self.curves = []
        self.impulses = []
        self.ax.legend()
        self.canvas.draw()
        
    def get_impulse_class(self, impulse):
        """
        Determina la classe di impulso NAR dato l'impulso totale in N⋅s
        """
        class_boundaries = {
            0.625: '1/4A', 1.25: '1/2A', 2.5: 'A', 5.0: 'B',
            10.0: 'C', 20.0: 'D', 40.0: 'E', 80.0: 'F',
            160.0: 'G', 320.0: 'H', 640.0: 'I'
        }
        
        for boundary, class_name in class_boundaries.items():
            if impulse <= boundary:
                return class_name
        return 'I+'  # Per impulsi molto grandi        
        
    def export_rasp(self):
        if self.last_time is None or self.last_thrust is None:
            return
            
        file_name = filedialog.asksaveasfilename(
            defaultextension=".eng",
            filetypes=[("RASP Engine Files", "*.eng"), ("All Files", "*.*")]
        )
        
        if not file_name:
            return
            
        # Calcola parametri per il file RASP
        diameter_mm = self.diameter_var.get()
        length_mm = self.length_var.get()
        
        # Masse in kg
        propellant_mass_kg = self.bottle_volume_var.get() * (self.water_ratio_var.get() / 100)  # acqua in kg
        total_mass_kg = propellant_mass_kg + self.bottle_mass_var.get() / 1000  # bottiglia da g a kg
        
        # Calcola impulso totale e spinta media
        impulse = np.trapezoid(self.last_thrust, self.last_time/1000)
        burn_time = (self.last_time[-1] - self.last_time[0]) / 1000  # in secondi
        average_thrust = impulse / burn_time
        
        # Determina la classe di impulso
        motor_class = self.get_impulse_class(impulse)
        
        # Genera nome motore secondo standard
        # Formato: [CLASSE]-[SPINTA_MEDIA]
        motor_name = f"{motor_class}{int(average_thrust)}"
        
        with open(file_name, 'w') as f:
            # Header con informazioni aggiuntive
            f.write(f"; Water Rocket Motor File\n")
            f.write(f"; Generated by Water Rocket Motor Simulator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"; Configuration:\n")
            f.write(f";   Volume: {self.bottle_volume_var.get():.1f}L\n")
            f.write(f";   Pressure: {self.pressure_var.get():.1f} bar\n")
            f.write(f";   Water ratio: {self.water_ratio_var.get():.1f}%\n")
            f.write(f";   Nozzle diameter: {self.nozzle_diameter_var.get():.1f} mm\n")
            f.write(f";   Total Impulse: {impulse:.2f} Ns\n")
            f.write(f";   Average Thrust: {average_thrust:.2f} N\n")
            f.write(f";   Burn Time: {burn_time:.3f} s\n\n")
            
            # RASP header line secondo standard:
            # nome diametro_mm lunghezza_mm ritardo massa_propellente_kg massa_totale_kg produttore
            f.write(f"{motor_name} {diameter_mm:.1f} {length_mm:.1f} P {propellant_mass_kg:.4f} {total_mass_kg:.4f} WaRMS\n")
            
            # Dati curva di spinta
            for time, thrust in zip(self.last_time/1000, self.last_thrust):
                f.write(f"{time:.4f} {thrust:.4f}\n")
            
            # Fine dati
            f.write(";")
        
if __name__ == '__main__':
    root = tk.Tk()
    app = WaterRocketSimulator(root)
    root.mainloop()
