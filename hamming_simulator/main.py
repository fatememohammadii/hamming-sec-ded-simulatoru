import tkinter as tk
from tkinter import messagebox

# Parity bitlerini hesaplayan fonksiyon
def calculate_parity_bits(data_bits):
    m = len(data_bits)
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1

    total_length = m + r + 1  # +1 overall parity için
    code = ['0'] * total_length

    j = 0
    for i in range(1, total_length):
        if (i & (i - 1)) == 0:
            continue
        code[i - 1] = data_bits[j]
        j += 1

    # Parity bitleri
    for i in range(r):
        parity_pos = (2 ** i) - 1
        parity = 0
        for j in range(parity_pos + 1, total_length):
            if j & (parity_pos + 1):
                parity ^= int(code[j - 1])
        code[parity_pos] = str(parity)

    # Genel parite (overall parity)
    overall_parity = sum(int(b) for b in code[:-1]) % 2
    code[-1] = str(overall_parity)

    return ''.join(code)

# Hatalı biti bulan ve düzelten fonksiyon (SEC-DED)
def detect_and_correct_error(encoded_bits):
    n = len(encoded_bits)
    r = 0
    while (2 ** r) < n:
        r += 1

    syndrome = 0
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n):
            if j & parity_pos:
                parity ^= int(encoded_bits[j - 1])
        if parity != 0:
            syndrome += parity_pos

    overall_parity = sum(int(b) for b in encoded_bits[:-1]) % 2
    expected_overall = int(encoded_bits[-1])

    if syndrome == 0 and overall_parity == expected_overall:
        return 0, encoded_bits, "no_error"
    elif syndrome != 0 and overall_parity != expected_overall:
        corrected_bits = list(encoded_bits)
        if syndrome <= len(encoded_bits) - 1:
            corrected_bits[syndrome - 1] = '1' if encoded_bits[syndrome - 1] == '0' else '0'
            return syndrome, ''.join(corrected_bits), "single_error"
        else:
            return syndrome, encoded_bits, "uncorrectable"
    elif syndrome == 0 and overall_parity != expected_overall:
        return 0, encoded_bits, "double_error"
    else:
        return syndrome, encoded_bits, "uncorrectable"

# Tabloyu güncelleyen fonksiyon
def update_hamming_table(bits, error_pos=None, corrected_pos=None):
    for widget in hamming_frame.winfo_children():
        widget.destroy()

    total_len = len(bits)
    for idx, bit in enumerate(bits):
        pos = idx + 1
        if error_pos is not None and pos == error_pos:
            bg_color = "red"
        elif corrected_pos is not None and pos == corrected_pos:
            bg_color = "lightgreen"
        else:
            bg_color = "white"

        lbl = tk.Label(
            hamming_frame, text=bit, borderwidth=1, relief="solid",
            width=2, height=1, bg=bg_color, fg="black", font=('Arial', 12)
        )
        lbl.grid(row=0, column=idx, padx=1)

    for idx in range(total_len):
        tk.Label(hamming_frame, text=str(total_len - idx), width=2, font=('Arial', 10)).grid(row=1, column=idx)

# Encode butonu
def encode_data():
    data_bits = data_entry.get()
    if not all(bit in '01' for bit in data_bits):
        messagebox.showerror("Hata", "Sadece 0 ve 1 girmelisiniz.")
        return

    if len(data_bits) not in [8, 16, 32]:
        messagebox.showerror("Hata", "Sadece 8, 16 veya 32 bit veri girebilirsiniz.")
        return

    encoded = calculate_parity_bits(data_bits)
    encoded_var.set(encoded)
    memory_var.set(encoded)
    corrected_var.set("")
    error_position_var.set("")
    update_hamming_table(encoded)

# Hata oluştur butonu
def inject_error():
    bit_pos = error_entry.get()
    encoded = memory_var.get()
    if not encoded:
        messagebox.showerror("Hata", "Önce veri kodlanmalı.")
        return

    if not bit_pos.isdigit() or not (1 <= int(bit_pos) <= len(encoded)):
        messagebox.showerror("Hata", f"1 ile {len(encoded)} arasında bir bit pozisyonu girin.")
        return

    bit_pos = int(bit_pos)
    modified = list(encoded)
    modified[bit_pos - 1] = '1' if modified[bit_pos - 1] == '0' else '0'
    memory_var.set(''.join(modified))
    corrected_var.set("")
    error_position_var.set("")
    update_hamming_table(modified, error_pos=bit_pos)

# Hata kontrolü butonu
def check_and_correct():
    memory_bits = memory_var.get()
    if not memory_bits:
        messagebox.showerror("Hata", "Bellekte veri yok.")
        return

    syndrome, corrected, status = detect_and_correct_error(memory_bits)

    if status == "no_error":
        messagebox.showinfo("Sonuç", "Hata yok.")
        error_position_var.set("0 (Hata yok)")
        update_hamming_table(corrected)
    elif status == "single_error":
        messagebox.showinfo("Sonuç", f"Tek hata bulundu ve düzeltildi! Bit pozisyonu: {syndrome}")
        error_position_var.set(str(syndrome))
        update_hamming_table(corrected, corrected_pos=syndrome)
    elif status == "double_error":
        messagebox.showwarning("Sonuç", "Çift hata tespit edildi! Düzeltilemez.")
        error_position_var.set("Çift hata")
        update_hamming_table(memory_bits)
    else:
        messagebox.showerror("Sonuç", "Hata tespit edildi ancak düzeltilemedi.")
        error_position_var.set("Düzeltilemedi")
        update_hamming_table(memory_bits)

    corrected_var.set(corrected if status == "single_error" else memory_bits)

# GUI başlat
root = tk.Tk()
root.title("Hamming SEC-DED Simülatörü")

tk.Label(root, text="Girdi (8, 16, 32 bit):").grid(row=0, column=0, sticky="e")
data_entry = tk.Entry(root, width=40)
data_entry.grid(row=0, column=1, columnspan=2)

tk.Button(root, text="Encode", command=encode_data).grid(row=1, column=1, pady=5)

tk.Label(root, text="Kodlanmış Veri:").grid(row=2, column=0, sticky="e")
encoded_var = tk.StringVar()
tk.Entry(root, textvariable=encoded_var, width=50, state="readonly").grid(row=2, column=1, columnspan=2)

tk.Label(root, text="Bellekteki Veri:").grid(row=3, column=0, sticky="e")
memory_var = tk.StringVar()
tk.Entry(root, textvariable=memory_var, width=50, state="readonly").grid(row=3, column=1, columnspan=2)

tk.Label(root, text="Hatalı Bit Pozisyonu:").grid(row=4, column=0, sticky="e")
error_entry = tk.Entry(root, width=10)
error_entry.grid(row=4, column=1, sticky="w")
tk.Button(root, text="Hata Oluştur", command=inject_error).grid(row=4, column=2)

tk.Button(root, text="Kontrol Et & Düzelt", command=check_and_correct).grid(row=5, column=1, pady=5)

tk.Label(root, text="Düzeltilmiş Veri:").grid(row=6, column=0, sticky="e")
corrected_var = tk.StringVar()
tk.Entry(root, textvariable=corrected_var, width=50, state="readonly").grid(row=6, column=1, columnspan=2)

tk.Label(root, text="Hata Pozisyonu:").grid(row=7, column=0, sticky="e")
error_position_var = tk.StringVar()
tk.Entry(root, textvariable=error_position_var, width=20, state="readonly").grid(row=7, column=1, sticky="w")

hamming_frame = tk.Frame(root)
hamming_frame.grid(row=8, column=0, columnspan=3, pady=10)

root.mainloop()
