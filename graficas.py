import pandas as pd
import matplotlib.pyplot as plt


def generar_grafica():
    # 1. Leer los datos
    try:
        df = pd.read_csv("precios_steam.csv")
    except:
        print("❌ No se encuentra el archivo CSV. Ejecuta primero el tracker.")
        return

    # 2. Limpiar los precios (quitar el símbolo € y convertir a número)
    # Si dice 'Gratis', lo ponemos como 0
    def limpiar_precio(precio):
        if "Gratis" in str(precio):
            return 0.0
        # Quitamos €, puntos de miles y cambiamos coma por punto
        p = str(precio).replace("€", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(p)
        except:
            return 0.0

    df["Precio_Num"] = df["Precio"].apply(limpiar_precio)

    # 3. Crear la gráfica de los 10 más caros
    top_10 = df.sort_values(by="Precio_Num", ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_10["Juego"], top_10["Precio_Num"], color="skyblue")

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Precio en Euros (€)")
    plt.title("Top 10 Juegos más caros de mi lista")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Añadir el precio encima de cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval}€", ha="center")

    plt.tight_layout()

    # Guardar la imagen
    plt.savefig("grafica_precios.png")
    print("✅ Gráfica guardada como 'grafica_precios.png'")
    plt.show()


if __name__ == "__main__":
    generar_grafica()
