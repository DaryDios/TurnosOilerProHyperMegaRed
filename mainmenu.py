import pandas as pd
from datetime import datetime, timedelta

# Definir el nombre del archivo donde se almacenarán los pacientes y citas
PACIENTES_FILE = "pacientes.csv"
CITAS_FILE = "citas.csv"
Administradores = {"admin": "123", "admin2": "pass2"}

# Función para agregar un paciente a la base de datos (archivo CSV)
def AgregarPaciente():
    # Verificar si el archivo de pacientes ya existe
    try:
        # Intentamos cargar el archivo de pacientes
        pacientes = pd.read_csv(PACIENTES_FILE)
    except FileNotFoundError:
        # Si no existe el archivo, creamos uno vacío con las columnas correspondientes
        pacientes = pd.DataFrame(columns=["nombre", "apellido", "cedula"])

    while True:
        print("\n--- Agregar Paciente ---")
        
        # Pedimos los datos del paciente
        nombre = input("Introduce el nombre del paciente: ")
        apellido = input("Introduce el apellido del paciente: ")
        cedula = input("Introduce la cédula del paciente: ")

        # Validación de cédula (si se desea)
        if not cedula.isdigit():
            print("La cédula debe ser un número. Intenta nuevamente.")
            continue

        # Crear un nuevo registro para el paciente
        nuevo_paciente = {"nombre": nombre, "apellido": apellido, "cedula": cedula}
        
        # Agregar el nuevo paciente al DataFrame
        pacientes = pd.concat([pacientes, pd.DataFrame([nuevo_paciente])], ignore_index=True)
        
        # Guardar el DataFrame actualizado en el archivo CSV
        pacientes.to_csv(PACIENTES_FILE, index=False)
        
        print(f"\nPaciente agregado exitosamente: {nombre} {apellido}, Cédula: {cedula}")

        # Preguntar si desea agregar otro paciente
        opcion = input("¿Quieres agregar otro paciente? (S/N): ").strip().lower()
        if opcion != 's':
            break

#####################################################################################################################

# Función para agregar una cita
def agregar_cita():
    
  

    # Cargar los pacientes desde el archivo CSV
    try:
        pacientes = pd.read_csv(PACIENTES_FILE)
    except FileNotFoundError:
        print("No se encontró el archivo de pacientes.")
        return

    # Asegurarse de que la columna 'cedula' es de tipo string
    pacientes['cedula'] = pacientes['cedula'].astype(str).str.strip()  # Eliminar espacios adicionales y asegurarse de que es str

    # Pedir la cédula del paciente
    cedula_buscar = input("Introduce la cédula del paciente: ").strip()

    # Buscar el paciente por la cédula
    paciente_encontrado = pacientes[pacientes['cedula'] == cedula_buscar]

    # Verificar si el paciente existe en el archivo
    if not paciente_encontrado.empty:
        print(f"Paciente encontrado: {paciente_encontrado.iloc[0]['nombre']} {paciente_encontrado.iloc[0]['apellido']}")

        # Obtener la fecha de hoy
        fecha_hoy = datetime.now().strftime("%Y %m %d")
        print(f"La fecha actual es: {fecha_hoy}")
        
        # Pedir la fecha de la cita
        while True:
            fecha = input("Introduce la fecha de la cita (YYYY MM DD): ").strip()
            if fecha == "":
                print("La fecha no puede estar vacía. Intenta nuevamente.")
            else:
                try:
                    datetime.strptime(fecha, "%Y %m %d")
                    break
                except ValueError:
                    print("Formato de fecha incorrecto. Debe ser YYYY MM DD.")

        # Pedir la hora de la cita (solo hora y minutos)
        while True:
            hora = input("Introduce la hora de la cita (HH MM): ").strip()
            if hora == "":
                print("La hora no puede estar vacía. Intenta nuevamente.")
            else:
                try:
                    datetime.strptime(hora, "%H %M")
                    break
                except ValueError:
                    print("Formato de hora incorrecto. Debe ser HH MM.")

        # Cargar las citas desde el archivo CSV
        try:
            citas = pd.read_csv(CITAS_FILE)
        except FileNotFoundError:
            citas = pd.DataFrame(columns=["cedula", "fecha", "hora"])

        # Verificar si ya existe una cita para esa fecha y hora
        cita_existente = citas[(citas['fecha'] == fecha) & (citas['hora'] == hora)]

        if not cita_existente.empty:
            print(f"Ya existe una cita para esa fecha y hora: {fecha} a las {hora}.")
            opcion = input("¿Quieres agregar otra hora para esa fecha? (S/N): ").strip().lower()
            if opcion == 's':
                nueva_hora = input("Introduce una nueva hora para la cita (HH MM): ").strip()
                citas = pd.concat([citas, pd.DataFrame([{"cedula": cedula_buscar, "fecha": fecha, "hora": nueva_hora}])], ignore_index=True)
                citas.to_csv(CITAS_FILE, index=False)
                print(f"Cita agregada exitosamente para el paciente {paciente_encontrado.iloc[0]['nombre']} el {fecha} a las {nueva_hora}.")
            else:
                print("No se agregó ninguna cita.")
        else:
            citas = pd.concat([citas, pd.DataFrame([{"cedula": cedula_buscar, "fecha": fecha, "hora": hora}])], ignore_index=True)
            citas.to_csv(CITAS_FILE, index=False)
            print(f"Cita agregada exitosamente para el paciente {paciente_encontrado.iloc[0]['nombre']} el {fecha} a las {hora}.")
               

    else:
        print("No se encontró un paciente con esa cédula.")

######################################################################################################################

def verificar_cita():
    print("\n--- Verificar Cita ---")
    cedula = input("Introduce la cédula del paciente para verificar su cita: ").strip()

    try:
        # Leer los archivos CSV
        citas_df = pd.read_csv(CITAS_FILE)
        pacientes_df = pd.read_csv(PACIENTES_FILE)

        # Asegurar que la columna 'cedula' es de tipo string
        citas_df['cedula'] = citas_df['cedula'].astype(str)
        pacientes_df['cedula'] = pacientes_df['cedula'].astype(str)

        # Buscar la cita por cédula
        cita = citas_df[citas_df['cedula'] == cedula]

        if not cita.empty:
            # Buscar el nombre del paciente en el archivo de pacientes
            paciente = pacientes_df[pacientes_df['cedula'] == cedula]

            if not paciente.empty:
                nombre_paciente = paciente.iloc[0]['nombre']  # Asumiendo que hay una columna 'nombre' en pacientes.csv
                fecha = cita.iloc[0]['fecha']
                hora = cita.iloc[0]['hora']
                
                # Mostrar los detalles de la cita
                print(f"\nEl paciente {nombre_paciente} tiene una cita el día {fecha} a las {hora}.")
                
                # Preguntar si desea verificar más detalles de la cita
                verificar = input("¿Desea verificar la cita? (s/n): ").strip().lower()
                if verificar == 's':
                    print("Su cita se verificó correctamente.")
                else:
                    print("si desea cancelar de 4 en el siguiente menu gracias ")

                              
            else:
                print("No se encontró el nombre del paciente con esa cédula.")
        else:
            print("No se encontró una cita para esta cédula.")

    except FileNotFoundError:
        print("Uno o más archivos necesarios no se encuentran.")

#####################################################################################################################

def cancelar_cita():
    print("\n--- Cancelar Cita ---")
    cedula = input("Introduce la cédula del paciente para cancelar su cita: ").strip()

    try:
        # Leer los archivos CSV
        citas_df = pd.read_csv(CITAS_FILE)
        pacientes_df = pd.read_csv(PACIENTES_FILE)

        # Asegurar que la columna 'cedula' es de tipo string
        citas_df['cedula'] = citas_df['cedula'].astype(str)
        pacientes_df['cedula'] = pacientes_df['cedula'].astype(str)

        # Buscar todas las citas por cédula
        citas = citas_df[citas_df['cedula'] == cedula]

        if not citas.empty:
            # Buscar el nombre del paciente en el archivo de pacientes
            paciente = pacientes_df[pacientes_df['cedula'] == cedula]

            if not paciente.empty:
                nombre_paciente = paciente.iloc[0]['nombre']  # Asumiendo que hay una columna 'nombre' en pacientes.csv
                
                print(f"\nLas citas del paciente {nombre_paciente} son las siguientes:")
                
                # Numerar las citas de forma consecutiva
                cita_num = 1  # Empezamos la numeración desde 1
                for index, row in citas.iterrows():
                    print(f"{cita_num}: Fecha: {row['fecha']} - Hora: {row['hora']}")
                    cita_num += 1  # Incrementar el número de cita

                # Solicitar al usuario que elija cuál cita desea cancelar
                cita_num = input(f"\nIntroduce el número de la cita que deseas cancelar (1-{len(citas)}): ").strip()
                
                if cita_num.isdigit() and 1 <= int(cita_num) <= len(citas):
                    cita_index = int(cita_num) - 1  # Ajustar el índice de la cita

                    # Eliminar la cita seleccionada
                    cita_a_eliminar = citas.iloc[cita_index]
                    citas_df = citas_df.drop(cita_a_eliminar.name)  # Eliminar la fila de la cita seleccionada

                    # Guardar los cambios en el archivo CSV
                    citas_df.to_csv(CITAS_FILE, index=False)

                    print(f"La cita del paciente {nombre_paciente} para el día {cita_a_eliminar['fecha']} a las {cita_a_eliminar['hora']} ha sido cancelada correctamente.")
                else:
                    print("Opción inválida. No se canceló ninguna cita.")
            else:
                print("No se encontró el nombre del paciente con esa cédula.")
        else:
            print("No se encontró una cita para esta cédula.")

    except FileNotFoundError:
        print("Uno o más archivos necesarios no se encuentran.")
        
#############################################################################################################################

def generar_reportes():
    while True:
        print("\n--- Menú de Reportes ---")
        print("1. Buscar citas por cédula")
        print("2. Buscar citas por fecha específica")
        print("3. Mostrar reportes de los próximos 7 días")
        print("4. Salir al menú anterior")
        print("5. Salir del sistema")
        
        opcion = input("Introduce tu opción: ").strip()

        try:
            citas_df = pd.read_csv(CITAS_FILE)
            pacientes_df = pd.read_csv(PACIENTES_FILE)
            
            # Asegurar que las cédulas son cadenas
            citas_df['cedula'] = citas_df['cedula'].astype(str)
            pacientes_df['cedula'] = pacientes_df['cedula'].astype(str)
        except FileNotFoundError:
            print("No se encontraron los archivos necesarios.")
            return

        if opcion == "1":
            # Buscar citas por cédula
            cedula = input("Introduce la cédula del paciente: ").strip()
            citas_paciente = citas_df[citas_df['cedula'] == cedula]

            if citas_paciente.empty:
                print(f"No se encontraron citas para la cédula: {cedula}.")
            else:
                paciente = pacientes_df[pacientes_df['cedula'] == cedula]
                nombre_paciente = paciente.iloc[0]['nombre'] if not paciente.empty else "Desconocido"
                print(f"\nCitas para el paciente {nombre_paciente} (Cédula: {cedula}):")
                for idx, cita in citas_paciente.iterrows():
                    print(f"{idx + 1}: Fecha: {cita['fecha']} - Hora: {cita['hora']}")

        elif opcion == "2":
            # Buscar citas por fecha específica
            fecha_input = input("Introduce la fecha (YYYY MM DD): ").strip()
            try:
                fecha_especifica = datetime.strptime(fecha_input, "%Y %m %d")
                citas_fecha = citas_df[citas_df['fecha'] == fecha_especifica.strftime("%Y %m %d")]

                if citas_fecha.empty:
                    print(f"No se encontraron citas para la fecha: {fecha_especifica.strftime('%Y-%m-%d')}.")
                else:
                    print(f"\nCitas para el día {fecha_especifica.strftime('%Y-%m-%d')}:")
                    for idx, cita in citas_fecha.iterrows():
                        paciente = pacientes_df[pacientes_df['cedula'] == cita['cedula']]
                        nombre_paciente = paciente.iloc[0]['nombre'] if not paciente.empty else "Desconocido"
                        print(f"{idx + 1}: Paciente: {nombre_paciente} - Cédula: {cita['cedula']} - Hora: {cita['hora']}")
            except ValueError:
                print("Formato de fecha incorrecto. Debe ser YYYY MM DD.")

        elif opcion == "3":
            # Reporte de los próximos 7 días
            fecha_actual = datetime.now()
            fecha_limite = fecha_actual + timedelta(days=7)
            
            citas_df['fecha'] = pd.to_datetime(citas_df['fecha'], format='%Y %m %d')
            citas_proximas = citas_df[(citas_df['fecha'] > fecha_actual) & (citas_df['fecha'] <= fecha_limite)]

            if citas_proximas.empty:
                print("No hay citas programadas para los próximos 7 días.")
            else:
                print("Citas programadas para los próximos 7 días:\n")
                citas_proximas = citas_proximas.sort_values(by=['cedula', 'fecha'])

                for cedula, citas in citas_proximas.groupby('cedula'):
                    paciente = pacientes_df[pacientes_df['cedula'] == cedula]
                    nombre_paciente = paciente.iloc[0]['nombre'] if not paciente.empty else "Desconocido"
                    print(f"\nPaciente: {nombre_paciente} (Cédula: {cedula})")
                    for idx, cita in citas.iterrows():
                        print(f"  - Fecha: {cita['fecha'].strftime('%Y-%m-%d')} - Hora: {cita['hora']}")

        elif opcion == "4":
            # Salir al menú anterior
            print("Volviendo al menú anterior...")
            break

        elif opcion == "5":
            # Salir del sistema
            print("Saliendo del sistema... Hasta luego.")
            exit()

        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


############################################# PROGRAMA PRINCIPAL  ###################################################
# Menú principal
while True:
    print("\nBienvenido a Turnos OilerPro Hyper Mega Red")
    print("1. Escoge si eres Administrador")
    print("2. Escoge si eres usuario regular")
    print("3. Salir del sistema")
    opcion = input("Introduce tu opción: ")

    if opcion == "1":  # Opción para Administrador
        nombre = input("Introduce tu nombre de usuario: ")
        contrasena = input("Introduce tu contraseña: ")

        # Verificación de usuario y contraseña
        if Administradores.get(nombre) == contrasena:
            print("Has accedido como Administrador.")
            while True:
                print("\n--- Menú Administrador ---")
                print("1. Agregar Paciente")
                print("2. Agregar Cita")
                print("3. Verificar Cita")
                print("4. Cancelar una Cita")
                print("5. Mostrar Reportes")
                print("6. Volver al Menú Principal")
                print("7. Salir del sistema")

                admin_opcion = input("Introduce tu opción: ")

                if admin_opcion == "1":
                    AgregarPaciente()
                elif admin_opcion == "2":
                    agregar_cita()                    
                elif admin_opcion == "3":
                    verificar_cita()
                elif admin_opcion == "4":
                    cancelar_cita()                
                elif admin_opcion == "5":
                    generar_reportes()
                elif admin_opcion == "6":
                    print("Volviendo al Menú Principal...")
                    break  # Vuelve al menú principal
                elif admin_opcion == "7":
                    print("Saliendo del sistema... Hasta luego.")
                    exit()  # Termina el programa
                else:
                    print("Opción no válida. Por favor, elige una opción válida.")
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            # Regresa al menú principal si la autenticación falla
            continue  # Vuelve a pedir la opción del menú principal

    elif opcion == "2":  # Opción para Paciente Regular
        print("Has elegido ser Usuario regular.")
        while True:
            print("\n--- Menú Usuario Regular ---")
            print("1. Agregar Paciente")
            print("2. Agregar Cita")
            print("3. Mostrar Reportes")
            print("4. Volver al Menú Principal")
            print("5. Salir del sistema")

            patient_opcion = input("Introduce tu opción: ")

            if patient_opcion == "1":
                AgregarPaciente()
                # Aquí deberías agregar la lógica para agregar pacientes.
            elif patient_opcion == "2":
                agregar_cita()
                # Aquí deberías agregar la lógica para agregar citas.
            elif patient_opcion == "3":
                generar_reportes()
                # Aquí deberías agregar la lógica para mostrar reportes.
            elif patient_opcion == "4":
                print("Volviendo al Menú Principal...")
                break  # Regresa al menú principal
            elif patient_opcion == "5":
                print("Saliendo del sistema... Hasta luego.")
                exit()  # Termina el programa
            else:
                print("Opción no válida. Por favor, elige una opción válida.")

    elif opcion == "3":
        print("Saliendo... Hasta luego.")
        break  # Salir del sistema
    else:
        print("Opción no válida. Por favor, elige una opción correcta.")
