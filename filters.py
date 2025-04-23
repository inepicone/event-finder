# filters.py
from datetime import datetime

def get_filters():
    print("Ingrese los filtros para buscar actividades:\n")

    # Fecha (semana o rango personalizado)
    start_date_str = input("Fecha de inicio (YYYY-MM-DD): ")
    end_date_str = input("Fecha de fin (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️ Formato de fecha incorrecto. Usar YYYY-MM-DD.")
        return None

    # Edad
    try:
        age = int(input("Edad de tus hijos (solo un número por ahora): "))
    except ValueError:
        print("⚠️ La edad debe ser un número.")
        return None

    # Presupuesto
    try:
        budget = float(input("Presupuesto máximo (en euros): "))
    except ValueError:
        print("⚠️ El presupuesto debe ser un número.")
        return None

    # Localidad
    city = input("Ciudad (helsinki / espoo / vantaa): ").strip().lower()
    if city not in ["helsinki", "espoo", "vantaa"]:
        print("⚠️ Ciudad no reconocida.")
        return None

    return {
        "start_date": start_date,
        "end_date": end_date,
        "age": age,
        "budget": budget,
        "city": city
    }

# Test rápido
if __name__ == "__main__":
    filters = get_filters()
    if filters:
        print("\n✅ Filtros seleccionados:")
        for key, value in filters.items():
            print(f"{key}: {value}")
