import tkinter as tk
from tkinter import filedialog, messagebox 
def leer_archivo(nombre_archivo):
    lineas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            lineas.append(linea)
    return lineas
def procesar_registro(lineas):
    registro = {}
    for linea in lineas:
        partes = linea.split(",",1)
        if len(partes) != 2:
            continue
        nombre = partes[0].strip()
        horas_t = partes[1].strip()
        try:
            horas = int(horas_t)
            if nombre in registro:
                registro[nombre] += horas
            else: registro[nombre] = horas
        except ValueError: continue
    return registro    
def kpis(registro):
    total = sum(registro.values())
    promedio = total / len(registro)
    MMax = max(registro, key=registro.get)
    return total, promedio, MMax
def rank(registro):
    return sorted(registro.items(), key=lambda x:x[1], reverse=True)
def porcentaje(registro):
    total = sum(registro.values())
    porcentajes = {}
    for equipo in registro:
        porcentajes[equipo] = (registro[equipo]/total) * 100
    return porcentajes 
def below_avg(registro, promedio):

    debajo = []
    for equipo, horas in registro.items():
        if horas < promedio:
            debajo.append(equipo)
    return debajo
ruta_archivo = ""
def seleccionar_archivo():
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(
        title = "Seleccionar archivo",
        filetypes =[("Archivos de texto", "*.txt*")]
    )
    if ruta_archivo:
        lbl_archivo.config(text = f"Archivo: {ruta_archivo.split('/')[-1]}")
        btn_procesar.config(state="normal")
def procesar_archivo():
    if not ruta_archivo:
        messagebox.showwarning("Aviso", "Seleccione un archivo primero")
    try:  
        resultado.delete(1.0, tk.END)
        lineas = leer_archivo(ruta_archivo)
        registro = procesar_registro(lineas)

        total, promedio, MMax = kpis(registro)
        ranking = rank(registro)
        prc = porcentaje(registro)
        equipos_b = below_avg(registro, promedio)

        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "KPIs\n\n")
        resultado.insert(tk.END, f"Total de horas: {total}\n")
        resultado.insert(tk.END, f"Promedio: {round(promedio, 2)}\n")
        resultado.insert(tk.END, f"Mayor uso: {MMax} ({registro[MMax]} hrs)\n\n")

        resultado.insert(tk.END, "Ranking: \n")
        for equipo, horas in ranking:
            resultado.insert(tk.END, f"- {equipo}: {horas}\n")
        
        resultado.insert(tk.END, "\nPorcentajes de uso: \n")
        for equipo, valor in prc.items():
            resultado.insert(tk.END, f"- {equipo}: {round(valor,2)}%\n")
        
        resultado.insert(tk.END, "\nDebajo del promedio\n")
        for equipo in equipos_b:
            resultado.insert(tk.END, f"- {equipo}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))
def limpiar():
    resultado.delete(1.0, tk.END)
    lbl_archivo.config(text="Archivo: ninguno")
    btn_procesar.config(state="disabled")
ventana = tk.Tk()
ventana.title("Análisis de KPIs por Equipo")
ventana.geometry("500x500")
ventana.config(bg = "#f4f6f8")

tk.Label(
    ventana,
    text = "Análisis de KPIs",
    font = ("Segoe UI", 16, "bold"),
    bg = "#f4f6f8",
    fg = "#5014ea"
).pack(pady=10)

frame_top = tk.Frame(ventana, bg = "#f4f6f8")
frame_top.pack(pady=5)


tk.Button(frame_top, text = "Seleccionar archivo", command=seleccionar_archivo).grid(row = 0, column = 0, padx = 5)
btn_procesar = tk.Button(frame_top, text = "Procesar", command=procesar_archivo, state = "disabled")
btn_procesar.grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="Limpiar", command=limpiar).grid(row=0, column=2, padx=5)

lbl_archivo = tk.Label(ventana, text = "Archivo: ninguno", bg = "#f4f6f8")
lbl_archivo.pack(pady=5)

frame_text = tk.Frame(ventana)
frame_text.pack(expand=True, fill="both", padx=10, pady=10)
scroll = tk.Scrollbar(frame_text)
scroll.pack(side="right", fill="y")

resultado = tk.Text(frame_text, yscrollcommand=scroll.set, font = ("Consolas", 10))
resultado.pack(expand=True, fill="both")
scroll.config(command=resultado.yview)

ventana.mainloop()