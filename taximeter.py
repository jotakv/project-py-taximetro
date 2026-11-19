from taxi import Taxi
# US-05: Importamos la función para consultar el histórico
from historial import mostrar_historial_hoy
# US-06: Importamos el logger de TaxiTech
from registro import logger


# Creamos nuestro objeto Taxi
taxi = Taxi()

# US-06: Registramos el inicio de TaxiTech
logger.info("aplicacion_iniciada")


# Mostramos el título de la aplicación
print("=============================")
print("          TAXITECH")
print("      TAXÍMETRO DIGITAL")
print("=============================")

# Mantenemos el programa funcionando
while True:

    # Opciones disponibles en TaxiTech
    print("\n--------- MENÚ ---------")
    print("1. Iniciar carrera / iniciar otra carrera")
    print("2. Taxi en movimiento")
    print("3. Taxi parado")
    print("4. Consultar importe")
    print("5. Finalizar carrera")
    print("6. Ver histórico de carreras de hoy")
    print("7. Salir")
    print("------------------------")


    # Leemos la opción introducida
    opcion = input("Selecciona una opción: ")

    # US-01: Iniciar carrera
    if opcion == "1":
        taxi.iniciar_carrera()

    # US-02: Cambiar a movimiento
    elif opcion == "2":
        taxi.iniciar_movimiento()

    # US-02: Cambiar a parado
    elif opcion == "3":
        taxi.detener_movimiento()

    # US-02: Consultar cuánto debemos cobrar
    elif opcion == "4":
        taxi.consultar_importe()
    
    # US-03: Finalizar la carrera
    elif opcion == "5":
        taxi.finalizar_carrera()
    
    # US-05: Consultar las carreras guardadas hoy
   
    # US-05 y US-06: Consultar el histórico
    elif opcion == "6":

        try:
            mostrar_historial_hoy()

            # Registramos la consulta realizada
            logger.info("historico_consultado")

        # Gestionamos errores de lectura o formato del CSV
        except (OSError, ValueError, KeyError) as error:
            print("Error al consultar el histórico:", error)

            # Guardamos los detalles técnicos
            logger.exception("error_consultando_historico")


    # Salir del programa
    elif opcion == "7":

        if taxi.carrera_activa:
            print("Primero debes finalizar la carrera.")

            # US-06: Intento de salida no permitido
            logger.warning(
                "salida_rechazada | motivo=carrera_activa"
            )

        else:
            print("Gracias por utilizar TaxiTech.")

            # US-06: Cierre normal de la aplicación
            logger.info("aplicacion_finalizada")

            break

    
    # Gestionar opciones incorrectas
    else:
        print("Opción incorrecta. Inténtalo de nuevo.")

        # US-06: Registramos la opción desconocida
        logger.warning(
            "opcion_invalida | valor=%s",
            opcion
        )

