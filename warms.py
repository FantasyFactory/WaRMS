import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class WaterRocketSimulator:
    def __init__(self, root):
        self.root = root
        self.curves = []
        self.impulses = []
        
        # Sistema di internazionalizzazione
        self.translations = {
            'it': {
                'title': "WaRMS - Simulatore Motore Razzo ad Acqua",
                'motor_params': "Parametri Motore",
                'length': "Lunghezza",
                'diameter': "Diametro", 
                'bottle_mass': "Massa bottiglia",
                'operational_params': "Parametri Operativi",
                'pressure': "Pressione",
                'water_ratio': "Rapporto Acqua (%)",
                'nozzle_diameter': "Diametro Ugello",
                'bottle_volume': "Volume Bottiglia",
                'options': "Opzioni",
                'include_air_phase': "Includi fase ad aria",
                'unit_system': "Sistema unità:",
                'metric': "Metrico",
                'imperial': "Imperiale", 
                'language': "Lingua:",
                'calculate': "Calcola",
                'clear_all': "Cancella Tutto",
                'export_rasp': "Esporta RASP",
                'thrust_chart': "Curva di Spinta Razzo ad Acqua",
                'time_ms': "Tempo (ms)",
                'thrust_n': "Spinta (N)",
                'time_s': "Tempo (s)",
                'thrust_lbf': "Spinta (lbf)",
                'export_success': "File esportato con successo!",
                'no_data': "Nessun dato da esportare. Calcola prima una curva.",
                'water_phase': "Fase Acqua",
                'air_phase': "Fase Aria",
                'total': "Totale"
            },
            'en': {
                'title': "WaRMS - Water Rocket Motor Simulator",
                'motor_params': "Motor Parameters",
                'length': "Length",
                'diameter': "Diameter",
                'bottle_mass': "Bottle mass", 
                'operational_params': "Operational Parameters",
                'pressure': "Pressure",
                'water_ratio': "Water Ratio (%)",
                'nozzle_diameter': "Nozzle Diameter",
                'bottle_volume': "Bottle Volume",
                'options': "Options",
                'include_air_phase': "Include air phase",
                'unit_system': "Unit system:",
                'metric': "Metric",
                'imperial': "Imperial",
                'language': "Language:",
                'calculate': "Calculate", 
                'clear_all': "Clear All",
                'export_rasp': "Export RASP",
                'thrust_chart': "Water Rocket Thrust Curve",
                'time_ms': "Time (ms)",
                'thrust_n': "Thrust (N)",
                'time_s': "Time (s)", 
                'thrust_lbf': "Thrust (lbf)",
                'export_success': "File exported successfully!",
                'no_data': "No data to export. Calculate a curve first.",
                'water_phase': "Water Phase",
                'air_phase': "Air Phase", 
                'total': "Total"
            }
        }
        
        # Stato dell'applicazione
        self.current_language = 'it'
        self.current_units = 'metric'  # 'metric' o 'imperial'
        
        # Fattori di conversione
        self.unit_conversions = {
            'length': {'metric_to_imperial': 0.0393701, 'imperial_to_metric': 25.4},  # mm <-> inch
            'pressure': {'metric_to_imperial': 14.5038, 'imperial_to_metric': 0.0689476},  # bar <-> psi  
            'volume': {'metric_to_imperial': 0.264172, 'imperial_to_metric': 3.78541},  # L <-> gal
            'mass': {'metric_to_imperial': 0.035274, 'imperial_to_metric': 28.3495},  # g <-> oz
            'thrust': {'metric_to_imperial': 0.224809, 'imperial_to_metric': 4.44822}  # N <-> lbf
        }
        
        self.setup_ui()
        self.update_language()
        
        # Memorizza l'ultima curva calcolata per l'export
        self.last_time = None
        self.last_thrust = None
        self.last_water_time = None  # Tempo fine fase acqua
        
    def get_text(self, key):
        """Ottiene il testo tradotto per la lingua corrente"""
        return self.translations[self.current_language].get(key, key)
    
    def get_unit_label(self, param_type):
        """Ottiene l'etichetta dell'unità per il parametro specificato"""
        if self.current_units == 'metric':
            units = {
                'length': 'mm', 'pressure': 'bar', 'volume': 'L', 
                'mass': 'g', 'thrust': 'N', 'time': 'ms'
            }
        else:
            units = {
                'length': 'in', 'pressure': 'psi', 'volume': 'gal',
                'mass': 'oz', 'thrust': 'lbf', 'time': 'ms'  
            }
        return units.get(param_type, '')
    
    def convert_value(self, value, param_type, to_metric=True):
        """Converte un valore tra sistemi di unità"""
        if param_type not in self.unit_conversions:
            return value
            
        conv = self.unit_conversions[param_type]
        if to_metric:
            return value * conv['imperial_to_metric']
        else:
            return value * conv['metric_to_imperial']
    
    def setup_ui(self):
        self.root.title(self.get_text('title'))
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        # Configurazione layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Aggiustato per il layout modificato
        
        # Frame parametri motore
        self.motor_frame = ttk.LabelFrame(main_frame, text="Motor Parameters", padding="5")
        self.motor_frame.grid(row=0, column=0, sticky="EW", padx=5, pady=5)
        
        # Inizializza valori in unità metriche (default)
        self.length_var = tk.DoubleVar(value=330.0)
        self.diameter_var = tk.DoubleVar(value=110.0) 
        self.bottle_mass_var = tk.DoubleVar(value=100.0)
        
        # Frame parametri operativi
        self.params_frame = ttk.LabelFrame(main_frame, text="Operational Parameters", padding="5")
        self.params_frame.grid(row=1, column=0, sticky="EW", padx=5, pady=5)
        
        self.pressure_var = tk.DoubleVar(value=3.0)
        self.water_ratio_var = tk.DoubleVar(value=33.0)
        self.nozzle_diameter_var = tk.DoubleVar(value=8.0)
        self.bottle_volume_var = tk.DoubleVar(value=2.0)
        
        # Frame opzioni (ora include lingua e unità)
        self.options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        self.options_frame.grid(row=2, column=0, sticky="EW", padx=5, pady=5)
        
        self.include_air_phase_var = tk.BooleanVar(value=False)
        
        self.create_motor_params_widgets()
        self.create_operational_params_widgets() 
        self.create_options_widgets()
        self.create_buttons()
        self.create_plot()
        
    def create_motor_params_widgets(self):
        # Parametri bottiglia con Entry
        self.length_label = ttk.Label(self.motor_frame, text="Length (mm):")
        self.length_label.grid(row=0, column=0, sticky="W")
        self.length_entry = ttk.Entry(self.motor_frame, textvariable=self.length_var, width=10)
        self.length_entry.grid(row=0, column=1, padx=5, pady=2)
        
        self.diameter_label = ttk.Label(self.motor_frame, text="Diameter (mm):")
        self.diameter_label.grid(row=0, column=2, sticky="W")
        self.diameter_entry = ttk.Entry(self.motor_frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.grid(row=0, column=3, padx=5, pady=2)
        
        self.bottle_mass_label = ttk.Label(self.motor_frame, text="Bottle mass (g):")
        self.bottle_mass_label.grid(row=0, column=4, sticky="W")
        self.bottle_mass_entry = ttk.Entry(self.motor_frame, textvariable=self.bottle_mass_var, width=10)
        self.bottle_mass_entry.grid(row=0, column=5, padx=5, pady=2)
        
    def create_operational_params_widgets(self):
        # Slider per pressione
        self.pressure_label = ttk.Label(self.params_frame, text="Pressure (bar):")
        self.pressure_label.grid(row=0, column=0, sticky="W")
        self.pressure_value_label = ttk.Label(self.params_frame, text="3.0")
        self.pressure_value_label.grid(row=0, column=2, sticky="E")
        self.pressure_slider = ttk.Scale(self.params_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                      variable=self.pressure_var, command=self.update_pressure_label)
        self.pressure_slider.grid(row=0, column=1, sticky="EW", padx=5, pady=5)
        
        # Slider per rapporto acqua
        self.water_ratio_label = ttk.Label(self.params_frame, text="Water Ratio (%):")
        self.water_ratio_label.grid(row=0, column=4, sticky="W")
        self.water_ratio_value_label = ttk.Label(self.params_frame, text="33.0")
        self.water_ratio_value_label.grid(row=0, column=6, sticky="E")
        self.water_ratio_slider = ttk.Scale(self.params_frame, from_=10, to=90, orient=tk.HORIZONTAL,
                                         variable=self.water_ratio_var, command=self.update_water_ratio_label)
        self.water_ratio_slider.grid(row=0, column=5, sticky="EW", padx=5, pady=5)
        
        # Slider per diametro ugello
        self.nozzle_diameter_label = ttk.Label(self.params_frame, text="Nozzle Diameter (mm):")
        self.nozzle_diameter_label.grid(row=1, column=0, sticky="W")
        self.nozzle_diameter_value_label = ttk.Label(self.params_frame, text="8.0")
        self.nozzle_diameter_value_label.grid(row=1, column=2, sticky="E")
        self.nozzle_diameter_slider = ttk.Scale(self.params_frame, from_=4, to=12, orient=tk.HORIZONTAL,
                                             variable=self.nozzle_diameter_var, command=self.update_nozzle_diameter_label)
        self.nozzle_diameter_slider.grid(row=1, column=1, sticky="EW", padx=5, pady=5)
        
        # Slider per volume bottiglia
        self.bottle_volume_label = ttk.Label(self.params_frame, text="Bottle Volume (L):")
        self.bottle_volume_label.grid(row=1, column=4, sticky="W")
        self.bottle_volume_value_label = ttk.Label(self.params_frame, text="2.0")
        self.bottle_volume_value_label.grid(row=1, column=6, sticky="E")
        self.bottle_volume_slider = ttk.Scale(self.params_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL,
                                           variable=self.bottle_volume_var, command=self.update_bottle_volume_label)
        self.bottle_volume_slider.grid(row=1, column=5, sticky="EW", padx=5, pady=5)
        
        # Configurazione colonne elastiche
        self.params_frame.columnconfigure(1, weight=1)
        self.params_frame.columnconfigure(5, weight=1)
        
    def create_options_widgets(self):
        # Checkbox fase aria
        self.include_air_phase_check = ttk.Checkbutton(self.options_frame, text="Include air phase",
                                                     variable=self.include_air_phase_var)
        self.include_air_phase_check.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        
        # Selezione lingua
        self.language_label = ttk.Label(self.options_frame, text="Language:")
        self.language_label.grid(row=0, column=1, sticky="W", padx=(20,5))
        self.language_var = tk.StringVar(value='it')
        language_combo = ttk.Combobox(self.options_frame, textvariable=self.language_var, 
                                    values=['it', 'en'], width=8, state='readonly')
        language_combo.grid(row=0, column=2, padx=5)
        language_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Selezione unità
        self.units_label = ttk.Label(self.options_frame, text="Units:")
        self.units_label.grid(row=0, column=3, sticky="W", padx=(20,5))
        self.units_var = tk.StringVar(value='metric')
        units_combo = ttk.Combobox(self.options_frame, textvariable=self.units_var,
                                 values=['metric', 'imperial'], width=8, state='readonly')
        units_combo.grid(row=0, column=4, padx=5)
        units_combo.bind('<<ComboboxSelected>>', self.change_units)
        
    def create_buttons(self):
        # Frame pulsanti
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)
        
        self.calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate_curve)
        self.calculate_button.grid(row=0, column=0, padx=5)
        self.clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_curves)
        self.clear_button.grid(row=0, column=1, padx=5)
        self.export_button = ttk.Button(button_frame, text="Export RASP", command=self.export_rasp)
        self.export_button.grid(row=0, column=2, padx=5)
        
    def create_plot(self):
        # Setup grafico
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.grid(row=3, column=0, sticky="NSEW", padx=10, pady=5)
        self.root.rowconfigure(3, weight=1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.ax.set_xlabel('Time (ms)')
        self.ax.set_ylabel('Thrust (N)')
        self.ax.set_title('Water Rocket Thrust Curve')
        self.ax.grid(True)
        
    def change_language(self, event=None):
        """Cambia la lingua dell'interfaccia"""
        self.current_language = self.language_var.get()
        self.update_language()
        
    def change_units(self, event=None):
        """Cambia il sistema di unità"""
        new_units = self.units_var.get()
        if new_units != self.current_units:
            self.convert_all_values(new_units)
            self.current_units = new_units
            self.update_language()  # Aggiorna anche le etichette
            
    def convert_all_values(self, new_units):
        """Converte tutti i valori quando si cambia sistema di unità"""
        to_metric = (new_units == 'metric')
        
        # Converti valori delle entry
        self.length_var.set(self.convert_value(self.length_var.get(), 'length', to_metric))
        self.diameter_var.set(self.convert_value(self.diameter_var.get(), 'length', to_metric))
        self.bottle_mass_var.set(self.convert_value(self.bottle_mass_var.get(), 'mass', to_metric))
        
        # Converti valori degli slider
        self.pressure_var.set(self.convert_value(self.pressure_var.get(), 'pressure', to_metric))
        self.nozzle_diameter_var.set(self.convert_value(self.nozzle_diameter_var.get(), 'length', to_metric))
        self.bottle_volume_var.set(self.convert_value(self.bottle_volume_var.get(), 'volume', to_metric))
        
        # Aggiorna range degli slider per il nuovo sistema
        if new_units == 'metric':
            self.pressure_slider.config(from_=1, to=10)
            self.nozzle_diameter_slider.config(from_=4, to=12)
            self.bottle_volume_slider.config(from_=0.5, to=5.0)
        else:
            self.pressure_slider.config(from_=14.5, to=145)  # ~1-10 bar in psi
            self.nozzle_diameter_slider.config(from_=0.16, to=0.47)  # ~4-12mm in inch
            self.bottle_volume_slider.config(from_=0.13, to=1.32)  # ~0.5-5L in gal
            
    def update_language(self):
        """Aggiorna tutti i testi dell'interfaccia"""
        self.root.title(self.get_text('title'))
        
        # Aggiorna etichette frame
        self.motor_frame.config(text=self.get_text('motor_params'))
        self.params_frame.config(text=self.get_text('operational_params'))
        self.options_frame.config(text=self.get_text('options'))
        
        # Aggiorna etichette parametri motore
        self.length_label.config(text=f"{self.get_text('length')} ({self.get_unit_label('length')}):")
        self.diameter_label.config(text=f"{self.get_text('diameter')} ({self.get_unit_label('length')}):")
        self.bottle_mass_label.config(text=f"{self.get_text('bottle_mass')} ({self.get_unit_label('mass')}):")
        
        # Aggiorna etichette parametri operativi
        self.pressure_label.config(text=f"{self.get_text('pressure')} ({self.get_unit_label('pressure')}):")
        self.water_ratio_label.config(text=self.get_text('water_ratio'))
        self.nozzle_diameter_label.config(text=f"{self.get_text('nozzle_diameter')} ({self.get_unit_label('length')}):")
        self.bottle_volume_label.config(text=f"{self.get_text('bottle_volume')} ({self.get_unit_label('volume')}):")
        
        # Aggiorna opzioni
        self.include_air_phase_check.config(text=self.get_text('include_air_phase'))
        self.language_label.config(text=self.get_text('language'))
        self.units_label.config(text=self.get_text('unit_system'))
        
        # Aggiorna pulsanti
        self.calculate_button.config(text=self.get_text('calculate'))
        self.clear_button.config(text=self.get_text('clear_all'))
        self.export_button.config(text=self.get_text('export_rasp'))
        
        # Aggiorna grafico
        time_unit = self.get_text('time_ms') if self.current_units == 'metric' else self.get_text('time_s')
        thrust_unit = self.get_text('thrust_n') if self.current_units == 'metric' else self.get_text('thrust_lbf')
        
        self.ax.set_xlabel(time_unit)
        self.ax.set_ylabel(thrust_unit)
        self.ax.set_title(self.get_text('thrust_chart'))
        self.canvas.draw()
        
        # Aggiorna valori visualizzati
        self.update_all_labels()
        
    def update_all_labels(self):
        """Aggiorna tutti i label dei valori"""
        self.update_pressure_label(self.pressure_var.get())
        self.update_water_ratio_label(self.water_ratio_var.get())
        self.update_nozzle_diameter_label(self.nozzle_diameter_var.get())
        self.update_bottle_volume_label(self.bottle_volume_var.get())
        
    def update_pressure_label(self, value):
        self.pressure_value_label.config(text=f"{float(value):.1f}")
        
    def update_water_ratio_label(self, value):
        self.water_ratio_value_label.config(text=f"{float(value):.1f}")
        
    def update_nozzle_diameter_label(self, value):
        self.nozzle_diameter_value_label.config(text=f"{float(value):.2f}")
    
    def update_bottle_volume_label(self, value):
        self.bottle_volume_value_label.config(text=f"{float(value):.2f}")
        
    def get_metric_values(self):
        """Ottiene tutti i valori convertiti in unità metriche per i calcoli"""
        if self.current_units == 'metric':
            return {
                'bottle_volume': self.bottle_volume_var.get(),
                'pressure': self.pressure_var.get(), 
                'nozzle_diameter': self.nozzle_diameter_var.get(),
                'length': self.length_var.get(),
                'diameter': self.diameter_var.get(),
                'bottle_mass': self.bottle_mass_var.get()
            }
        else:
            return {
                'bottle_volume': self.convert_value(self.bottle_volume_var.get(), 'volume', True),
                'pressure': self.convert_value(self.pressure_var.get(), 'pressure', True),
                'nozzle_diameter': self.convert_value(self.nozzle_diameter_var.get(), 'length', True),
                'length': self.convert_value(self.length_var.get(), 'length', True),
                'diameter': self.convert_value(self.diameter_var.get(), 'length', True),
                'bottle_mass': self.convert_value(self.bottle_mass_var.get(), 'mass', True)
            }
        
    def calculate_thrust_curve(self, bottle_volume, water_ratio, pressure, nozzle_diameter, include_air_phase=False):
        """Calcola la curva di spinta includendo opzionalmente la fase ad aria"""
        # Conversione unità (assumendo input in unità metriche)
        water_volume = bottle_volume * water_ratio/100
        initial_pressure = pressure * 1e5 + 1e5  # bar -> Pa assoluti
        nozzle_area = np.pi * (nozzle_diameter/2000)**2  # mm -> m
        
        # Costanti
        gamma = 1.4  # Rapporto calore specifico aria
        rho_water = 1000  # kg/m³
        Cd = 0.95  # Coefficiente di scarico
        
        # FASE ACQUA: Calcolo tempo di esaurimento acqua
        water_time = 0.5 * water_volume / (Cd * nozzle_area * np.sqrt(2 * rho_water * (initial_pressure - 1e5)))
        
        # Genera punti temporali per fase acqua
        t_water = np.linspace(0, water_time, 500)
        thrust_water = np.zeros_like(t_water)
        
        for i, time in enumerate(t_water):
            # Calcola volume acqua rimanente
            water_remaining = max(0, water_volume * (1 - time/water_time))
            air_volume = bottle_volume - water_remaining
            initial_air_volume = bottle_volume - water_volume
            
            # Pressione corrente (espansione adiabatica dell'aria)
            if air_volume > 0 and initial_air_volume > 0:
                current_pressure = initial_pressure * (initial_air_volume/air_volume)**gamma
            else:
                current_pressure = initial_pressure
                
            if water_remaining > 0 and current_pressure > 1e5:
                # Velocità di uscita acqua
                exit_velocity = Cd * np.sqrt(2 * (current_pressure - 1e5) / rho_water)
                # Portata massica
                mass_flow = Cd * nozzle_area * np.sqrt(2 * rho_water * (current_pressure - 1e5))
                # Spinta
                thrust_water[i] = mass_flow * exit_velocity
        
        if not include_air_phase:
            return t_water * 1000, thrust_water, t_water[-1] * 1000  # tempo in ms
        
        # FASE ARIA: Continua con solo aria
        # Pressione all'inizio della fase aria
        air_start_pressure = initial_pressure * (initial_air_volume/bottle_volume)**gamma
        
        if air_start_pressure <= 1e5:  # Nessuna pressione residua
            return t_water * 1000, thrust_water, t_water[-1] * 1000
            
        # Stima tempo fase aria (più conservativo)
        # Tempo per espansione da pressione corrente a pressione atmosferica
        air_time_estimate = 0.1  # secondi stimati per fase aria
        
        t_air = np.linspace(0, air_time_estimate, 300)
        thrust_air = np.zeros_like(t_air)
        
        # Densità aria a pressione iniziale fase aria (approssimazione)
        rho_air_initial = 1.225 * (air_start_pressure / 1e5)  # kg/m³
        
        for i, time in enumerate(t_air):
            # Espansione adiabatica dell'aria nella bottiglia
            # Pressione diminuisce man mano che l'aria esce
            volume_ratio = 1 + time/air_time_estimate * 2  # Volume "virtuale" aumenta
            current_pressure = air_start_pressure * (1/volume_ratio)**gamma
            
            if current_pressure > 1e5:
                # Velocità di uscita aria (formula per flusso comprimibile)
                pressure_ratio = current_pressure / 1e5
                if pressure_ratio > 1.89:  # Flusso sonico critico
                    exit_velocity = np.sqrt(gamma * 287 * 288)  # Velocità sonica ~340 m/s
                else:
                    exit_velocity = np.sqrt(2 * gamma / (gamma-1) * 287 * 288 * 
                                          (1 - (1/pressure_ratio)**((gamma-1)/gamma)))
                
                # Densità aria all'uscita
                rho_air_exit = 1.225 * (current_pressure / 1e5)
                
                # Portata massica aria
                mass_flow = Cd * nozzle_area * rho_air_exit * exit_velocity
                
                # Spinta (con efficienza ridotta per fase aria)
                thrust_air[i] = mass_flow * exit_velocity * 0.7  # Fattore di efficienza
            else:
                break
                
        # Combina le due fasi
        t_total = np.concatenate([t_water, t_air + water_time])
        thrust_total = np.concatenate([thrust_water, thrust_air])
        
        return t_total * 1000, thrust_total, water_time * 1000  # tempo in ms
    
    def calculate_curve(self):
        """Calcola e visualizza la curva di spinta"""
        # Ottieni valori in unità metriche per i calcoli
        values = self.get_metric_values()
        
        t, thrust, water_end_time = self.calculate_thrust_curve(
            bottle_volume=values['bottle_volume'],
            water_ratio=self.water_ratio_var.get(),
            pressure=values['pressure'],
            nozzle_diameter=values['nozzle_diameter'],
            include_air_phase=self.include_air_phase_var.get()
        )
        
        # Converti unità per visualizzazione se necessario
        if self.current_units == 'imperial':
            thrust = self.convert_value(thrust, 'thrust', False)  # N -> lbf
            
        # Calcola l'impulso totale
        impulse = np.trapz(thrust, t/1000)  # Integrazione numerica
        
        # Trova gli impulsi delle due fasi se inclusa fase aria
        if self.include_air_phase_var.get():
            water_mask = t <= water_end_time
            water_impulse = np.trapz(thrust[water_mask], t[water_mask]/1000)
            air_impulse = impulse - water_impulse
        
        self.impulses.append(impulse)
        
        # Salva l'ultima curva calcolata (sempre in unità metriche per export)
        if self.current_units == 'imperial':
            self.last_thrust = self.convert_value(thrust, 'thrust', True)  # Riconverti per export
        else:
            self.last_thrust = thrust
        self.last_time = t
        self.last_water_time = water_end_time
        
        # Crea etichetta per legenda
        unit_labels = {
            'volume': self.get_unit_label('volume'),
            'pressure': self.get_unit_label('pressure'), 
            'length': self.get_unit_label('length'),
            'impulse': 'N⋅s' if self.current_units == 'metric' else 'lbf⋅s'
        }
        
        if self.include_air_phase_var.get():
            label = (f'V={self.bottle_volume_var.get():.1f}{unit_labels["volume"]}, '
                    f'P={self.pressure_var.get():.1f}{unit_labels["pressure"]}, '
                    f'W={self.water_ratio_var.get():.0f}%, '
                    f'D={self.nozzle_diameter_var.get():.1f}{unit_labels["length"]}, '
                    f'I={impulse:.2f}{unit_labels["impulse"]} '
                    f'(W:{water_impulse:.2f}+A:{air_impulse:.2f})')
        else:
            label = (f'V={self.bottle_volume_var.get():.1f}{unit_labels["volume"]}, '
                    f'P={self.pressure_var.get():.1f}{unit_labels["pressure"]}, '
                    f'W={self.water_ratio_var.get():.0f}%, '
                    f'D={self.nozzle_diameter_var.get():.1f}{unit_labels["length"]}, '
                    f'I={impulse:.2f}{unit_labels["impulse"]}')
        
        # Aggiungi la nuova curva
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'orange', 'purple', 'brown', 'pink']
        line_color = colors[len(self.curves) % len(colors)]
        
        # Disegna curva principale
        line, = self.ax.plot(t, thrust, color=line_color, linewidth=2, label=label)
        self.curves.append(line)
        
        # Se inclusa fase aria, evidenzia la transizione
        if self.include_air_phase_var.get():
            # Linea verticale al termine della fase acqua
            self.ax.axvline(x=water_end_time, color=line_color, linestyle='--', alpha=0.5)
            # Annotazione
            max_thrust = np.max(thrust)
            self.ax.annotate(f'{self.get_text("water_phase")}→{self.get_text("air_phase")}', 
                           xy=(water_end_time, max_thrust*0.8), 
                           xytext=(water_end_time + 50, max_thrust*0.9),
                           arrowprops=dict(arrowstyle='->', color=line_color, alpha=0.7),
                           fontsize=8, color=line_color)
        
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        self.canvas.draw()
        
    def clear_curves(self):
        """Cancella tutte le curve dal grafico"""
        for line in self.curves:
            line.remove()
        self.curves = []
        self.impulses = []
        
        # Rimuovi anche le annotazioni
        for annotation in self.ax.texts:
            annotation.remove()
        for line in self.ax.lines:
            if line.get_linestyle() == '--':  # Rimuovi linee tratteggiate
                line.remove()
                
        self.ax.legend()
        self.canvas.draw()
        
    def get_impulse_class(self, impulse):
        """Determina la classe di impulso NAR dato l'impulso totale in N⋅s"""
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
        """Esporta l'ultima curva calcolata in formato RASP"""
        if self.last_time is None or self.last_thrust is None:
            messagebox.showwarning("Warning", self.get_text('no_data'))
            return
            
        file_name = filedialog.asksaveasfilename(
            defaultextension=".eng",
            filetypes=[("RASP Engine Files", "*.eng"), ("All Files", "*.*")]
        )
        
        if not file_name:
            return
            
        try:
            # Ottieni valori in unità metriche per l'export
            values = self.get_metric_values()
            
            # Calcola parametri per il file RASP
            diameter_mm = values['diameter']
            length_mm = values['length']
            
            # Masse in kg
            propellant_mass_kg = values['bottle_volume'] * (self.water_ratio_var.get() / 100)
            total_mass_kg = propellant_mass_kg + values['bottle_mass'] / 1000
            
            # Calcola impulso totale e spinta media (sempre da dati in N)
            impulse = np.trapz(self.last_thrust, self.last_time/1000)
            burn_time = (self.last_time[-1] - self.last_time[0]) / 1000
            average_thrust = impulse / burn_time
            
            # Determina la classe di impulso
            motor_class = self.get_impulse_class(impulse)
            
            # Genera nome motore secondo standard
            motor_name = f"{motor_class}{int(average_thrust)}"
            
            with open(file_name, 'w') as f:
                # Header con informazioni
                f.write(f"; Water Rocket Motor File\n")
                f.write(f"; Generated by WaRMS on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"; Configuration:\n")
                f.write(f";   Volume: {values['bottle_volume']:.1f}L\n")
                f.write(f";   Pressure: {values['pressure']:.1f} bar\n")
                f.write(f";   Water ratio: {self.water_ratio_var.get():.1f}%\n")
                f.write(f";   Nozzle diameter: {values['nozzle_diameter']:.1f} mm\n")
                f.write(f";   Air phase included: {self.include_air_phase_var.get()}\n")
                f.write(f";   Total Impulse: {impulse:.2f} Ns\n")
                f.write(f";   Average Thrust: {average_thrust:.2f} N\n")
                f.write(f";   Burn Time: {burn_time:.3f} s\n\n")
                
                # RASP header line
                f.write(f"{motor_name} {diameter_mm:.1f} {length_mm:.1f} P {propellant_mass_kg:.4f} {total_mass_kg:.4f} WaRMS\n")
                
                # Dati curva di spinta (sempre in unità metriche: secondi e Newton)
                for time, thrust in zip(self.last_time/1000, self.last_thrust):
                    f.write(f"{time:.4f} {thrust:.4f}\n")
                
                # Fine dati
                f.write(";")
            
            messagebox.showinfo("Success", self.get_text('export_success'))
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = WaterRocketSimulator(root)
    root.mainloop()
