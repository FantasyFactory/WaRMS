# WaRMS
Water Rocket Motor Simulator

![screenshot](screenshot.png)

Un simulatore avanzato per "motori razzo" ad acqua con interfaccia multilingua;
calcola il grafico della spinta nel tempo, tenendo conto di:

## 🚀 Parametri Fisici
* **Pressione iniziale** - controllo tramite slider (1-10 bar)
* **Rapporto aria/acqua** - percentuale di riempimento (10-90%)
* **Diametro ugello** - dimensione dell'apertura di scarico (4-12 mm)
* **Volume totale** - capacità della bottiglia (0.5-5 L)
* **Dimensioni bottiglia** - lunghezza e diametro per calcoli accurati
* **Massa bottiglia** - peso a vuoto per calcolo impulso specifico

## ✨ Funzionalità Avanzate

### 🌍 **Interfaccia Multilingua**
- **Italiano** e **Inglese** completamente supportati
- Cambio lingua istantaneo tramite dropdown
- Tutte le etichette, grafici e messaggi tradotti

### 🌪️ **Simulazione Bifase**
- **Fase Acqua**: Spinta principale durante l'espulsione del propellente liquido
- **Fase Aria**: Spinta residua dall'espansione dell'aria compressa (opzionale)
- Transizione visualizzata graficamente con annotazioni
- Calcolo separato degli impulsi per ogni fase

### 📏 **Sistema Unità Flessibile**
- **Metrico**: mm, bar, L, g, N
- **Imperiale**: inch, psi, galloni, once, lbf
- Conversione automatica di tutti i parametri
- Calcoli interni sempre coerenti

### 📊 **Analisi Prestazioni**
- **Impulso totale** calcolato per classificazione NAR
- **Tempo di combustione** e spinta media
- **Curva di spinta** ad alta risoluzione (1000+ punti)
- **Legenda dettagliata** con tutti i parametri significativi

## 🎮 Controlli Interfaccia

La **legenda del grafico** mostra questi valori in formato compatto:
- **V** = Volume bottiglia
- **P** = Pressione iniziale  
- **W** = Rapporto acqua (%)
- **D** = Diametro ugello
- **I** = Impulso totale
- **W:X+A:Y** = Impulsi separati acqua+aria (se fase aria attiva)

### Pulsanti Principali
- **[Calcola]** → Genera nuova curva e la aggiunge al grafico
- **[Cancella Tutto]** → Rimuove tutte le curve e reset del grafico  
- **[Esporta RASP]** → Salva l'ultima curva in formato standard per simulatori

## 🔧 Compatibilità Software

L'**export RASP** genera file `.eng` compatibili con:
- **[OpenRocket](https://openrocket.info/)** - Simulatore razzi open source
- **RockSim** - Software commerciale Apogee Components
- **Altri simulatori** che supportano il formato RASP standard

I file includono:
- Header con configurazione completa del motore
- Metadati di generazione e parametri usati
- Curva spinta temporizzata in formato standard
- Classificazione automatica NAR (A, B, C, D, E...)

## 🛠️ Requisiti Tecnici

Il software è sviluppato in **Python 3.7+** e utilizza:

* **[tkinter](https://docs.python.org/3/library/tkinter.html)** - Interfaccia grafica nativa
* **[numpy](https://numpy.org/)** - Calcoli numerici e integrazione
* **[matplotlib](https://matplotlib.org/)** - Grafici e visualizzazione

### Installazione Dipendenze
```bash
pip install numpy matplotlib
# tkinter è incluso nella maggior parte delle distribuzioni Python
```

## 🔬 Fisica Implementata

### Modello Matematico
- **Espansione adiabatica** dell'aria compressa (γ = 1.4)
- **Equazione di Bernoulli** per velocità di scarico
- **Conservazione della massa** per portata
- **Fluidodinamica comprimibile** per fase aria

### Approssimazioni
- Coefficiente di scarico Cd = 0.95
- Densità acqua costante (1000 kg/m³)
- Temperatura aria ambiente costante
- Perdite di carico trascurabili

## 🏆 Crediti

Questo software è **open source** (licenza CC0) ed è sviluppato da **[Italian Rocketry Society](https://www.rocketry.it)**, 
un'associazione italiana di missilistica amatoriale.

### Contributi
- Design originale e implementazione fisica
- Sistema multilingua e conversioni unità
- Algoritmo bifase acqua/aria
- Compatibilità RASP estesa

---

*Per bug report, suggerimenti o contributi, contattare Italian Rocketry Society o aprire una issue nel repository.*
