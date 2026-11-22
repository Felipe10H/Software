from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ
from excepciones import ErrorSoftwareFJ
from registro import eventos, errores


def ejecutar_pruebas():
    """Ejecuta más de 10 operaciones, incluidas operaciones que fallan."""
    sistema = SistemaSoftwareFJ()
    print("=" * 58)
    print("        SOFTWARE FJ - DEMOSTRACIÓN AUTOMÁTICA")
    print("=" * 58)

    operaciones = 0

    def probar(titulo, accion):
        nonlocal operaciones
        operaciones += 1
        print(f"\nOperación {operaciones}: {titulo}")
        try:
            resultado = accion()
        except Exception as exc:
            errores.exception("Falló la operación de demostración: %s", titulo)
            print(f"Error controlado: {exc}")
        else:
            print(f"Resultado: {resultado}")
        finally:
            print("La aplicación continúa ejecutándose.")

    # 1. Registro válido de cliente
    cliente1 = Cliente("C001", "Laura Pérez", "laura@email.com", "3001234567")
    probar("Registrar cliente válido", lambda: sistema.registrar_cliente(cliente1))

    # 2. Registro inválido: correo incorrecto
    probar("Registrar cliente con correo inválido",
           lambda: Cliente("C002", "Carlos", "correo-invalido", "3001234567"))

    # 3. Registro de otro cliente válido
    cliente2 = Cliente("C003", "Andrés Gómez", "andres@email.com", "3107654321")
    probar("Registrar segundo cliente válido", lambda: sistema.registrar_cliente(cliente2))

    # 4. Servicio de sala válido
    sala = ReservaSala("S001", "Sala principal", 50000, 12)
    probar("Crear servicio de sala", lambda: sistema.agregar_servicio(sala))

    # 5. Alquiler de equipo válido
    equipo = AlquilerEquipo("S002", "Portátil", 20000, 5)
    probar("Crear servicio de alquiler de equipos", lambda: sistema.agregar_servicio(equipo))

    # 6. Asesoría válida
    asesoria = AsesoriaEspecializada("S003", "Asesoría tecnológica", 80000, "software")
    probar("Crear servicio de asesoría", lambda: sistema.agregar_servicio(asesoria))

    # 7. Servicio inválido: tarifa negativa
    probar("Intentar crear servicio con tarifa negativa",
           lambda: ReservaSala("S004", "Sala inválida", -10, 8))

    # 8. Reserva correcta
    reserva1 = None
    def crear_reserva_correcta():
        nonlocal reserva1
        reserva1 = sistema.crear_reserva("R001", "C001", "S001", 2)
        reserva1.confirmar()
        return reserva1.describir()
    probar("Crear y confirmar reserva correcta", crear_reserva_correcta)

    # 9. Procesar costo con impuestos y descuento
    probar("Calcular costo con impuesto del 19% y descuento del 10%",
           lambda: f"${reserva1.procesar(impuesto=19, descuento=10):,.2f}")

    # 10. Reserva fallida: cliente inexistente
    probar("Crear reserva con cliente inexistente",
           lambda: sistema.crear_reserva("R002", "NO-EXISTE", "S001", 1))

    # 11. Reserva fallida: duración inválida
    probar("Crear reserva con duración cero",
           lambda: sistema.crear_reserva("R003", "C001", "S002", 0))

    # 12. Servicio no disponible
    no_disponible = ReservaSala("S005", "Sala ocupada", 40000, 6, disponible=False)
    probar("Intentar reservar un servicio no disponible",
           lambda: sistema.agregar_servicio(no_disponible))
    probar("Intentar crear reserva de servicio no disponible",
           lambda: sistema.crear_reserva("R004", "C001", "S005", 1))

    # 13. Intentar confirmar nuevamente una reserva confirmada (encadenamiento)
    probar("Intentar confirmar de nuevo una reserva confirmada", lambda: reserva1.confirmar())

    # 14. Cancelar reserva
    probar("Cancelar reserva", lambda: (reserva1.cancelar(), reserva1.estado)[1])

    # 15. Intentar procesar reserva cancelada
    probar("Intentar procesar una reserva cancelada", lambda: reserva1.procesar())

    print("\n" + "=" * 58)
    print(f"Demostración finalizada. Operaciones ejecutadas: {operaciones}")
    print("El programa terminó las pruebas sin detenerse por los errores.")
    print("Revisa logs/eventos.log y logs/errores.log para ver los registros.")
    print("=" * 58)
    sistema.mostrar_resumen()
    return sistema


def menu():
    sistema = SistemaSoftwareFJ()
    while True:
        print("\n===== SOFTWARE FJ =====")
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Listar información")
        print("5. Ejecutar demostración de 15 operaciones")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                cliente = Cliente(
                    input("ID del cliente: "),
                    input("Nombre: "),
                    input("Correo: "),
                    input("Teléfono: ")
                )
                sistema.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")
            elif opcion == "2":
                print("Tipo: 1) Sala  2) Equipo  3) Asesoría")
                tipo = input("Seleccione tipo: ").strip()
                identificador = input("ID del servicio: ")
                nombre = input("Nombre del servicio: ")
                tarifa = float(input("Tarifa por hora: "))
                if tipo == "1":
                    servicio = ReservaSala(identificador, nombre, tarifa, int(input("Capacidad: ")))
                elif tipo == "2":
                    servicio = AlquilerEquipo(identificador, nombre, tarifa, int(input("Unidades: ")))
                elif tipo == "3":
                    servicio = AsesoriaEspecializada(
                        identificador, nombre, tarifa, input("Especialidad: ")
                    )
                else:
                    raise ValueError("Tipo de servicio no válido.")
                sistema.agregar_servicio(servicio)
                print("Servicio registrado correctamente.")
            elif opcion == "3":
                reserva = sistema.crear_reserva(
                    input("ID de reserva: "),
                    input("ID del cliente: "),
                    input("ID del servicio: "),
                    float(input("Duración en horas: "))
                )
                print("Reserva creada:", reserva.describir())
                if input("¿Confirmar reserva? (s/n): ").strip().lower() == "s":
                    reserva.confirmar()
                    print("Reserva confirmada.")
            elif opcion == "4":
                sistema.mostrar_resumen()
            elif opcion == "5":
                ejecutar_pruebas()
            elif opcion == "0":
                eventos.info("El usuario cerró la aplicación.")
                print("Hasta luego.")
                break
            else:
                raise ValueError("Opción no válida.")
        except Exception as exc:
            errores.exception("Error controlado en el menú")
            print(f"No se pudo completar la operación: {exc}")
            print("Puedes intentarlo de nuevo; el programa sigue activo.")
        else:
            eventos.info("Opción del menú procesada correctamente: %s", opcion)
        finally:
            print("-" * 40)


if __name__ == "__main__":
    print("Software FJ: 1) Demostración automática  2) Menú interactivo")
    modo = input("Elige 1 o 2: ").strip()
    try:
        if modo == "1":
            ejecutar_pruebas()
        elif modo == "2":
            menu()
        else:
            print("Opción no reconocida. Se ejecutará la demostración.")
            ejecutar_pruebas()
    except Exception as exc:
        errores.exception("Error inesperado en el punto de entrada")
        print(f"Error general controlado: {exc}")
