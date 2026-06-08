# hamming-sec-ded-simulatoru# Hamming SEC-DED Simulator

## Project Description

This project is a graphical simulation of the **Hamming SEC-DED (Single Error Correction, Double Error Detection)** algorithm developed using **Python** and **Tkinter**.

The simulator allows users to:

* Encode 8-bit, 16-bit, and 32-bit binary data using Hamming Code.
* Store the encoded data in simulated memory.
* Inject artificial bit errors into the stored data.
* Detect and correct single-bit errors.
* Detect double-bit errors and inform the user that they cannot be corrected.
* Visualize encoded data and error locations using a graphical interface.

---

## Features

### Encoding

* Supports 8-bit, 16-bit, and 32-bit binary inputs.
* Automatically calculates and inserts parity bits.
* Generates the Hamming SEC-DED code.

### Error Injection

* Users can select a bit position and flip its value.
* Simulates memory transmission/storage errors.

### Error Detection and Correction

* Detects single-bit errors.
* Corrects single-bit errors automatically.
* Detects double-bit errors.
* Reports double-bit errors as uncorrectable.

### Graphical Visualization

* Displays encoded data in a table format.
* Shows bit positions below the code word.
* Highlights erroneous bits in red.
* Highlights corrected bits in green.

---

## Technologies Used

* Python 3
* Tkinter GUI Library

---

## Project Structure

```text
hamming-sec-ded-simulator/
│
├── main.py
├── README.md
└── screenshots/
```

---

## How to Run

1. Install Python 3.
2. Download or clone the repository.

```bash
git clone https://github.com/your-username/hamming-sec-ded-simulator.git
```

3. Navigate to the project directory.

```bash
cd hamming-sec-ded-simulator
```

4. Run the program.

```bash
python main.py
```

---

## Example Usage

### Step 1: Encode Data

Input:

```text
1010101010101010
```

Output:

```text
1110010010101010010100
```

### Step 2: Inject Error

Example:

```text
Bit Position: 5
```

The selected bit is flipped and highlighted in red.

### Step 3: Detect and Correct

* Single-bit error → corrected automatically.
* Double-bit error → detected and reported as uncorrectable.

---

## Screenshots

### Figure 1 – Initial Program Interface

The simulator's initial state before any data is entered.

### Figure 2 – Hamming Code Generation

A 16-bit input encoded using Hamming SEC-DED.

### Figure 3 – Error Injection

A single-bit error injected into memory.

### Figure 4 – Error Detection and Correction

The simulator identifies and corrects the erroneous bit.

### Figure 5 – Double Error Detection

Two-bit error detected and reported as uncorrectable.

---

## Author

Fateme Mohammadi

Computer Engineering Student

---

## License

This project is developed for educational and academic purposes.
