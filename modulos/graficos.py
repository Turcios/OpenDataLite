import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import filedialog

def generar_grafico_barras(x, y): 
    """Genera un gráfico de barras."""
    fig, ax = plt.subplots()
    ax.bar(x, y)
    return fig

def generar_grafico_lineas(x, y):
    """Genera un gráfico de líneas."""
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig

def generar_grafico_pastel(etiquetas, valores):
    """Genera un gráfico circular (pastel)."""
    fig, ax = plt.subplots()
    ax.pie(valores, labels=etiquetas, autopct="%1.1f%%")
    return fig

def mostrar_grafico(frame, fig):
    """Muestra un gráfico en un widget Tkinter."""
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas

def exportar_grafico_pdf(fig):
    """Exporta el gráfico a un archivo PDF."""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        with PdfPages(file_path) as pdf:
            pdf.savefig(fig)
            plt.close(fig)
