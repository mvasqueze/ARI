
# README para Configuración y Ejecución del Cuaderno de Jupyter

Este README proporciona las instrucciones necesarias para configurar y ejecutar el cuaderno de Jupyter incluido en este proyecto.

---

## Clonación del Repositorio

1. Clona el repositorio desde GitHub asegurándote de estar en la rama `main`. Ejecuta el siguiente comando en tu terminal:

   ```bash
   git clone -b main https://github.com/mvasqueze/ARI.git
   ```

2. Accede a la carpeta principal del proyecto:

   ```bash
   cd ARI
   ```

3. Ingresa a la carpeta `Proyecto integrador`:

   ```bash
   cd "Proyecto integrador"
   ```

---

## Configuración del Entorno de Python

1. Crea un entorno virtual para Python:

   ```bash
   python -m venv myenv
   ```

2. Activa el entorno virtual:

   - **En Windows**:
     ```bash
     myenv\Scripts\activate
     ```

   - **En macOS/Linux**:
     ```bash
     source myenv/bin/activate
     ```

3. Instala las dependencias necesarias desde el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Preparación de los Datos

1. Asegúrate de contar con un archivo `.zip` llamado `datasets`, que contiene tres archivos `.csv`.
2. Copia este archivo `.zip` en la carpeta `prep-data` del repositorio.
3. Descomprime el archivo en la carpeta `prep-data`. Luego de hacerlo, la estructura del directorio debería lucir así:

   ```
   ARI/
   ├── Proyecto integrador/
       ├── prep-data/
           ├── datasets/
               ├── pcd_1211.csv
               ├── sampled_file.csv
   ```

---

## Ejecución del Cuaderno de Jupyter

1. Abre el cuaderno en **Visual Studio Code** o cualquier entorno compatible con Jupyter.
2. Ejecuta el cuaderno, ya sea:

   - Corriéndolo completamente de una vez, o
   - Celda por celda, según prefieras.

---

¡Listo! Ahora deberías poder trabajar con el cuaderno y realizar las tareas necesarias.
