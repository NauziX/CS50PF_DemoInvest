# NInvest – Aplicación de Inverción por consola

#### Video Demo:

## Descripción
NInvest es una aplicación de consola escrita en **Python** que simula una cuenta de inversión con dinero virtual. Permite crear un usuario, asignarle un saldo inicial y operar con acciones (o criptoactivos en el futuro) en tiempo real utilizando la API pública de Yahoo Finance a través de la librería **yfinance**. Todas las operaciones se guardan en un archivo `datos.json`, de modo que al reiniciar el programa se conserva el historial de compras, ventas y el balance.

La interfaz se basa en un menú interactivo que guía al usuario paso a paso.
## Instalación
```bash
# 1. Clonar el repositorio
$ git clone https://github.com/NauziX/CS50PF_DemoInvest

# 2. Instalar dependencias
$ pip install -r requirements.txt
```

## Uso rápido
```bash
# Lanzar la aplicación
$ python project.py
```
Verás el menú principal:
```
-------- NInvest --------
1. Create User
2. Delete User
3. Show User Information
4. Buy Shares
5. Show Portfolio
6. Sell Shares
7. Save Data
8. Load Data
9. Exit
```

1. **Create User** – introduce un nombre y un saldo inicial para abrir tu cuenta.
2. **Buy Shares** – escribe el *ticker* (p. ej. AAPL) y la cantidad de unidades a comprar. El precio se obtiene en ese instante mediante *yfinance*.
3. **Show Portfolio / Information** – muestra un resumen del valor actual de tus posiciones, beneficio/pérdida y saldo disponible.
4. **Sell Shares** – elige el *ticker* y las unidades a vender; la operación se liquida al precio de mercado actual.
5. **Save Data / Load Data** – persiste o restaura toda la información en `datos.json`.
6. **Exit** – cierra la sesión.

## Estructura del proyecto
| Archivo | Propósito |
|--------------|-----------|
| `project.py` | Contine las funciones y clases `User`, `Product`, `Shares`|
| `test_project.py` | Conjunto de pruebas unitarias (`pytest`) que verifican compras, representación de acciones y cálculos de valor. |
| `requirements.txt` | Lista de dependencias (`yfinance`) necesarias para ejecutar y probar el proyecto. |
| `datos.json` | Archivo generado automáticamente para guardar usuarios y carteras. |
| `README.md` | Este documento. |

## Diseño y decisiones técnicas
* **Escalabilidad** – se definió una jerarquía de clases (`Product` → `Shares`) para que añadir bonos, ETF o cripto sea tan simple como crear nuevas subclases.
* **Persistencia** – se eligió JSON por su sencillez y fácil lectura; en proyectos mayores se podría migrar a SQLite.
* **Datos de mercado** – *yfinance* permite obtener precios actuales sin claves de API, ideal para un proyecto académico.
* **Pruebas** – las funciones críticas están cubiertas por tests; se puede ejecutar `pytest -q` para ver un resumen rápido.

## Próximos pasos
- Añadir validación de entrada más robusta (manejo de `ValueError`, `FileNotFoundError`).
- Incluir soporte para criptomonedas usando la misma arquitectura.

- Exportar informes a CSV y gráficos de rendimiento con `matplotlib`.

## Licencia
MIT License – consulta el archivo `LICENSE` para más detalles.
