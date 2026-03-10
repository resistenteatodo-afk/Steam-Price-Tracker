import requests
import csv
import time
from datetime import datetime


def rastrear_50_juegos():
    archivo_csv = "precios_steam.csv"
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Leer los IDs con filtro especial para Windows (utf-8-sig)
    try:
        with open("juegos.txt", "r", encoding="utf-8-sig") as f:
            ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ No encuentro el archivo juegos.txt")
        return

    print(f"🚀 Empezando el rastreo de {len(ids)} juegos...")

    # 2. Abrir o crear el CSV
    with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Fecha", "ID", "Juego", "Precio"])

        # 3. Bucle de consulta
        for i, appid in enumerate(ids, 1):
            # Limpiamos el ID por si acaso se coló algún carácter extraño
            appid_limpio = "".join(filter(str.isdigit, appid))

            url = f"https://store.steampowered.com/api/appdetails?appids={appid_limpio}&cc=es&l=spanish"
            try:
                res = requests.get(url).json()
                if res and res[str(appid_limpio)]["success"]:
                    data = res[str(appid_limpio)]["data"]
                    nombre = data["name"]
                    # Si el juego es gratis, Steam no manda 'price_overview'
                    precio = data.get("price_overview", {}).get(
                        "final_formatted", "Gratis / Sin precio"
                    )

                    writer.writerow([fecha, appid_limpio, nombre, precio])
                    print(f"[{i}/{len(ids)}] ✅ {nombre} -> {precio}")
                else:
                    print(f"[{i}/{len(ids)}] ⚠️ ID {appid_limpio} no válido")

                # Pausa de seguridad para que Steam no nos bloquee
                time.sleep(1.2)

            except Exception as e:
                print(f"❌ Error procesando ID {appid_limpio}: {e}")

    print("\n✨ ¡Misión cumplida! Todo guardado en precios_steam.csv")


if __name__ == "__main__":
    rastrear_50_juegos()
