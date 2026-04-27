import psycopg2
from psycopg2 import Error
from datetime import datetime, timedelta
import random

# Datos reales de restaurantes y productos para poblar la base de datos
RESTAURANTES = [
    (1, 'Terranova', 'Italiana', 'Calle Macedonio Alcalá 100', 'Oaxaca', 'OAX', '9511111001', 'rest001@gmail.com', 9.2, 'Activo'),
    (2, 'El Asador', 'Carnes', 'Av. Independencia 305', 'Oaxaca', 'OAX', '9511111002', 'rest002@gmail.com', 8.8, 'Activo'),
    (3, 'Sushi Yuki', 'Japonesa', 'Calle Cinco de Mayo 220', 'Oaxaca', 'OAX', '9511111003', 'rest003@gmail.com', 9.0, 'Activo'),
    (4, 'La Biznaga', 'Mexicana', 'Calle García Vigil 512', 'Oaxaca', 'OAX', '9511111004', 'rest004@gmail.com', 9.4, 'Activo'),
    (5, 'Taco Loco', 'Mexicana', 'Av. Juárez 78', 'Oaxaca', 'OAX', '9511111005', 'rest005@gmail.com', 8.5, 'Activo'),
    (6, 'Pizza Roma', 'Italiana', 'Blvd. Tecnológico 450', 'Oaxaca', 'OAX', '9511111006', 'rest006@gmail.com', 8.2, 'Activo'),
    (7, 'Burger King', 'Americana', 'Periférico 1200', 'Oaxaca', 'OAX', '9511111007', 'rest007@gmail.com', 7.9, 'Activo'),
    (8, 'KFC Oaxaca', 'Americana', 'Av. Universidad 300', 'Oaxaca', 'OAX', '9511111008', 'rest008@gmail.com', 7.8, 'Activo'),
    (9, 'El Fogón', 'Oaxaqueña', 'Calle Mina 88', 'Oaxaca', 'OAX', '9511111009', 'rest009@gmail.com', 9.1, 'Activo'),
    (10, 'Café Brújula', 'Cafetería', 'Calle Alcalá 104', 'Oaxaca', 'OAX', '9511111010', 'rest010@gmail.com', 8.7, 'Activo'),
    (11, 'Pollo Feliz', 'Pollo', 'Av. Ferrocarril 210', 'Oaxaca', 'OAX', '9511111011', 'rest011@gmail.com', 8.0, 'Activo'),
    (12, 'Vegetalia', 'Vegetariana', 'Calle Reforma 55', 'Oaxaca', 'OAX', '9511111012', 'rest012@gmail.com', 8.6, 'Activo'),
    (13, 'Los Comales', 'Mexicana', 'Mercado 20 de Nov 1', 'Oaxaca', 'OAX', '9511111013', 'rest013@gmail.com', 9.3, 'Activo'),
    (14, 'Subway Oaxaca', 'Americana', 'Calle Porfirio Díaz 200', 'Oaxaca', 'OAX', '9511111014', 'rest014@gmail.com', 7.5, 'Activo'),
    (15, 'Don Pancho', 'Mariscos', 'Av. Hidalgo 90', 'Oaxaca', 'OAX', '9511111015', 'rest015@gmail.com', 8.9, 'Activo')
]
PRODUCTOS = [
    (1, 1, 'Pizza Margherita', 'Principal', 120, 'Disponible'),
    (2, 1, 'Pasta Carbonara', 'Principal', 145, 'Disponible'),
    (3, 1, 'Lasagna', 'Principal', 160, 'Disponible'),
    (4, 1, 'Tiramisú', 'Postre', 75, 'Disponible'),
    (5, 1, 'Ensalada César', 'Entrada', 90, 'Disponible'),
    (6, 1, 'Pan de Ajo', 'Entrada', 45, 'Disponible'),
    (7, 2, 'Chuletón 300g', 'Principal', 280, 'Disponible'),
    (8, 2, 'Arrachera', 'Principal', 240, 'Disponible'),
    (9, 2, 'Costilla BBQ', 'Principal', 260, 'Disponible'),
    (10, 2, 'Ensalada Mixta', 'Entrada', 95, 'Disponible'),
    (11, 2, 'Papas Fritas', 'Entrada', 65, 'Disponible'),
    (12, 2, 'Agua de Horchata', 'Bebida', 35, 'Disponible'),
    (13, 3, 'Sushi Roll California', 'Principal', 185, 'Disponible'),
    (14, 3, 'Nigiri Salmón', 'Principal', 95, 'Disponible'),
    (15, 3, 'Ramen', 'Principal', 175, 'Disponible'),
    (16, 3, 'Gyozas', 'Entrada', 110, 'Disponible'),
    (17, 3, 'Edamame', 'Entrada', 55, 'Disponible'),
    (18, 3, 'Té Verde', 'Bebida', 30, 'Disponible'),
    (19, 4, 'Tlayuda con Tasajo', 'Principal', 180, 'Disponible'),
    (20, 4, 'Mole Negro', 'Principal', 200, 'Disponible'),
    (21, 4, 'Memelas', 'Entrada', 85, 'Disponible'),
    (22, 4, 'Chapulines', 'Entrada', 60, 'Disponible'),
    (23, 4, 'Chocolate Oaxaqueño', 'Bebida', 45, 'Disponible'),
    (24, 4, 'Mezcal Shot', 'Bebida', 70, 'Disponible'),
    (25, 5, 'Taco de Barbacoa', 'Principal', 35, 'Disponible'),
    (26, 5, 'Taco de Carnitas', 'Principal', 35, 'Disponible'),
    (27, 5, 'Quesadilla', 'Principal', 55, 'Disponible'),
    (28, 5, 'Gordita', 'Principal', 50, 'Disponible'),
    (29, 5, 'Agua Fresca', 'Bebida', 25, 'Disponible'),
    (30, 5, 'Tostada', 'Entrada', 40, 'Disponible'),
    (31, 6, 'Pizza Pepperoni', 'Principal', 135, 'Disponible'),
    (32, 6, 'Pizza Hawaiana', 'Principal', 130, 'Disponible'),
    (33, 6, 'Calzone', 'Principal', 125, 'Disponible'),
    (34, 6, 'Pan de Ajo Especial', 'Entrada', 40, 'Disponible'),
    (35, 6, 'Refresco', 'Bebida', 30, 'Disponible'),
    (36, 6, 'Alitas', 'Entrada', 110, 'Disponible'),
    (37, 7, 'Whopper', 'Principal', 105, 'Disponible'),
    (38, 7, 'Double Whopper', 'Principal', 135, 'Disponible'),
    (39, 7, 'Nuggets x10', 'Principal', 95, 'Disponible'),
    (40, 7, 'Papas Medianas', 'Entrada', 45, 'Disponible'),
    (41, 7, 'Refresco BK', 'Bebida', 30, 'Disponible'),
    (42, 7, 'Sundae', 'Postre', 40, 'Disponible'),
    (43, 8, 'Bucket Original', 'Principal', 189, 'Disponible'),
    (44, 8, 'Box Combo', 'Principal', 155, 'Disponible'),
    (45, 8, 'Sandwich KFC', 'Principal', 110, 'Disponible'),
    (46, 8, 'Coleslaw', 'Entrada', 45, 'Disponible'),
    (47, 8, 'Puré KFC', 'Entrada', 40, 'Disponible'),
    (48, 8, 'Refresco KFC', 'Bebida', 30, 'Disponible'),
    (49, 9, 'Tlayuda Negra', 'Principal', 195, 'Disponible'),
    (50, 9, 'Estofado', 'Principal', 185, 'Disponible'),
    (51, 9, 'Tasajo Asado', 'Principal', 230, 'Disponible'),
    (52, 9, 'Sopa de Fideo', 'Entrada', 75, 'Disponible'),
    (53, 9, 'Chocolate Caliente', 'Bebida', 50, 'Disponible'),
    (54, 9, 'Mezcal Artesanal', 'Bebida', 80, 'Disponible'),
    (55, 10, 'Café Americano', 'Bebida', 55, 'Disponible'),
    (56, 10, 'Cappuccino', 'Bebida', 70, 'Disponible'),
    (57, 10, 'Latte', 'Bebida', 75, 'Disponible'),
    (58, 10, 'Croissant', 'Entrada', 55, 'Disponible'),
    (59, 10, 'Pay de Queso', 'Postre', 85, 'Disponible'),
    (60, 10, 'Brownie', 'Postre', 65, 'Disponible'),
    (61, 11, 'Pollo Entero', 'Principal', 185, 'Disponible'),
    (62, 11, 'Medio Pollo', 'Principal', 100, 'Disponible'),
    (63, 11, 'Cuarto Pollo', 'Principal', 60, 'Disponible'),
    (64, 11, 'Papas Extras', 'Entrada', 35, 'Disponible'),
    (65, 11, 'Ensalada', 'Entrada', 45, 'Disponible'),
    (66, 11, 'Refresco PF', 'Bebida', 30, 'Disponible'),
    (67, 12, 'Bowl Quinoa', 'Principal', 110, 'Disponible'),
    (68, 12, 'Hamburguesa Vegana', 'Principal', 130, 'Disponible'),
    (69, 12, 'Wrap Vegetal', 'Principal', 105, 'Disponible'),
    (70, 12, 'Smoothie Verde', 'Bebida', 75, 'Disponible'),
    (71, 12, 'Ensalada Tofu', 'Principal', 120, 'Disponible'),
    (72, 12, 'Jugo Natural', 'Bebida', 55, 'Disponible'),
    (73, 13, 'Comida Corrida', 'Principal', 90, 'Disponible'),
    (74, 13, 'Enchiladas Verdes', 'Principal', 95, 'Disponible'),
    (75, 13, 'Chiles Rellenos', 'Principal', 110, 'Disponible'),
    (76, 13, 'Sopa de Lima', 'Entrada', 70, 'Disponible'),
    (77, 13, 'Arroz con Leche', 'Postre', 50, 'Disponible'),
    (78, 13, 'Agua de Jamaica', 'Bebida', 25, 'Disponible'),
    (79, 14, 'Sub Italiano', 'Principal', 95, 'Disponible'),
    (80, 14, 'Sub Pollo', 'Principal', 90, 'Disponible'),
    (81, 14, 'Sub Vegetariano', 'Principal', 85, 'Disponible'),
    (82, 14, 'Cookie', 'Postre', 30, 'Disponible'),
    (83, 14, 'Refresco SW', 'Bebida', 30, 'Disponible'),
    (84, 14, 'Papas Kettle', 'Entrada', 45, 'Disponible'),
    (85, 15, 'Ceviche', 'Principal', 165, 'Disponible'),
    (86, 15, 'Camarones al Mojo', 'Principal', 220, 'Disponible'),
    (87, 15, 'Filete de Pescado', 'Principal', 195, 'Disponible'),
    (88, 15, 'Aguachile', 'Principal', 175, 'Disponible'),
    (89, 15, 'Michelada', 'Bebida', 85, 'Disponible'),
    (90, 15, 'Agua de Coco', 'Bebida', 45, 'Disponible')
]
ESTATUS = [
    (1, 'Pendiente','El pedido ha sido recibido pero aún no se ha confirmado.'),
    (2, 'Confirmado','El pedido ha sido confirmado por el restaurante.'),
    (3, 'En preparación','El pedido está siendo preparado por el restaurante.'),
    (4, 'Listo para recoger','El pedido está listo para ser recogido por el cliente.'),
    (5, 'En camino','El pedido está en camino hacia el cliente.'),
    (6, 'Entregado','El pedido ha sido entregado al cliente.'),
    (7, 'Cancelado por el cliente', 'El cliente ha cancelado el pedido antes de que fuera confirmado.'),
    (8, 'Cancelado por el restaurante', 'El restaurante ha cancelado el pedido.'),
    (9, 'Cancelado por el conductor', 'El conductor ha cancelado el pedido.')
]
METODOS_PAGO = [
    (1, 'Efectivo', 'Pago realizado en efectivo al momento de la entrega.'),
    (2, 'Tarjeta', 'Pago realizado con tarjeta de crédito o débito a través de la plataforma.'),
    (3, 'Transferencia', 'Pago realizado mediante transferencia bancaria a la cuenta del restaurante antes de la entrega.')
]

# Función para generar usuarios de forma aleatoria
def factory_usuarios(cantidad):
    nombres = [
        'Fernanda', 'Valentina', 'Adriana', 'Ana', 'Carlos', 'Andres', 'Patricia',
        'Juan', 'Karla', 'Sofia', 'Mario', 'Elena', 'Gabriela', 'Diego', 'Miguel',
        'Daniel', 'Rosa', 'Ricardo', 'Paola', 'Eduardo'
    ]
    apellidos = [
        'Jimenez', 'Gonzalez', 'Reyes', 'Guerrero', 'Lopez', 'Vega', 'Diaz',
        'Morales', 'Rodriguez', 'Flores', 'Mendoza', 'Torres', 'Sanchez',
        'Ruiz', 'Castillo', 'Ortega', 'Salinas', 'Rivera', 'Ramos', 'Cruz'
    ]

    random.seed(42)
    fecha_base = datetime(2023, 1, 1, 8, 0, 0)
    usuarios = []

    for i in range(1, cantidad + 1):
        nombre = random.choice(nombres)
        apellido_paterno = random.choice(apellidos)
        apellido_materno = random.choice(apellidos)
        telefono = f"951{random.randint(1000000, 9999999)}"
        email = f"usr{i:04d}@gmail.com"
        direccion = f"Calle {random.randint(1, 200)} #{random.randint(1, 999)}, Col. Centro, Oaxaca"
        fecha_registro = fecha_base + timedelta(days=random.randint(0, 800), minutes=random.randint(0, 1440))
        calificacion_promedio = round(random.uniform(3.5, 5.0), 1)

        usuarios.append(
            (
                i,
                nombre,
                apellido_paterno,
                apellido_materno,
                telefono,
                email,
                direccion,
                fecha_registro,
                calificacion_promedio,
            )
        )

    return usuarios

def factory_conductores(cantidad):
    nombres = [
        'Fernando', 'Lucia', 'Adrian', 'Mariana', 'Jorge', 'Alejandra', 'Pedro',
        'Daniela', 'Oscar', 'Monica', 'Ivan', 'Andrea', 'Hector', 'Vanessa',
        'Saul', 'Rocio', 'Tomas', 'Karen', 'Ruben', 'Erika'
    ]
    apellidos = [
        'Jimenez', 'Gonzalez', 'Reyes', 'Guerrero', 'Lopez', 'Vega', 'Diaz',
        'Morales', 'Rodriguez', 'Flores', 'Mendoza', 'Torres', 'Sanchez',
        'Ruiz', 'Castillo', 'Ortega', 'Salinas', 'Rivera', 'Ramos', 'Cruz'
    ]
    tipos_vehiculo = ['Moto', 'Auto', 'Bicicleta']
    estatus_opciones = ['Activo', 'Inactivo', 'Suspendido']

    random.seed(84)
    fecha_base = datetime(2022, 1, 1, 7, 0, 0)
    conductores = []

    for i in range(1, cantidad + 1):
        nombre = random.choice(nombres)
        apellido_paterno = random.choice(apellidos)
        apellido_materno = random.choice(apellidos)
        telefono = f"951{random.randint(1000000, 9999999)}"
        email = f"drv{i:04d}@gmail.com"
        tipo_vehiculo = random.choice(tipos_vehiculo)
        placa = f"OXA-{i:03d}-{random.randint(100, 999)}"
        calificacion_promedio = round(random.uniform(3.5, 5.0), 1)
        estatus = random.choices(estatus_opciones, weights=[80, 15, 5], k=1)[0]
        fecha_ingreso = fecha_base + timedelta(days=random.randint(0, 1400), minutes=random.randint(0, 1440))

        conductores.append(
            (
                i,
                nombre,
                apellido_paterno,
                apellido_materno,
                telefono,
                email,
                tipo_vehiculo,
                placa,
                calificacion_promedio,
                estatus,
                fecha_ingreso,
            )
        )

    return conductores

def factory_pedidos(cantidad):
    metodos_pago_ids = [1, 2, 3]
    fecha_base = datetime(2021, 1, 1, 9, 0, 0)
    fecha_hoy = datetime.now()
    pedidos = []

    random.seed(126)

    for i in range(1, cantidad + 1):
        id_usuario = random.randint(1, 300)
        id_restaurante = random.randint(1, 15)
        id_conductor = random.randint(1, 120)
        id_estatus = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9], weights=[8, 12, 14, 10, 16, 30, 4, 3, 3], k=1)[0]

        fecha_pedido = fecha_base + timedelta(days=random.randint(0, (fecha_hoy - fecha_base).days), minutes=random.randint(0, 1440))

        hora_recogida = None
        hora_entrega = None
        tiempo_entrega_min = None

        if id_estatus in [4, 5, 6]:
            hora_recogida = fecha_pedido + timedelta(minutes=random.randint(15, 45))

        if id_estatus == 6:
            tiempo_entrega_min = random.randint(20, 75)
            hora_entrega = fecha_pedido + timedelta(minutes=tiempo_entrega_min)

        metodo_pago = random.choice(metodos_pago_ids)
        subtotal = round(random.uniform(90, 650), 2)
        costo_envio = round(random.uniform(15, 65), 2)
        total = round(subtotal + costo_envio, 2)

        pedidos.append(
            (
                i,
                id_usuario,
                id_restaurante,
                id_conductor,
                id_estatus,
                metodo_pago,
                fecha_pedido,
                hora_recogida,
                hora_entrega,
                subtotal,
                costo_envio,
                total,
                tiempo_entrega_min,
            )
        )

    return pedidos

def factory_detalle_pedido(cantidad_pedidos):
    # Mapeo de precios de productos para cálculos realistas
    precios_productos = {p[0]: p[4] for p in PRODUCTOS}
    
    random.seed(127)
    detalle_pedido = []
    id_detalle = 1
    
    for id_pedido in range(1, cantidad_pedidos + 1):
        # Generar 1-5 items por pedido
        cantidad_items = random.randint(1, 5)
        
        for _ in range(cantidad_items):
            id_producto = random.randint(1, 90)
            cantidad = random.randint(1, 3)
            precio_unitario = float(precios_productos.get(id_producto, 100))
            subtotal_linea = round(cantidad * precio_unitario, 2)
            
            detalle_pedido.append(
                (
                    id_detalle,
                    id_pedido,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal_linea,
                )
            )
            id_detalle += 1
    
    return detalle_pedido

def factory_resenias_restaurante(cantidad):
    comentarios = [
        'Excelente comida y buen servicio',
        'Muy delicioso, lo recomiendo',
        'Fue una experiencia fantástica',
        'Comida fresca y de calidad',
        'Atención rápida y eficiente',
        'Precio justo para la porción',
        'Regresaré con mi familia',
        'No me gustó mucho',
        'Pudieron mejorar la presentación',
        'Espera un poco larga'
    ]
    
    random.seed(128)
    fecha_base = datetime(2024, 1, 1, 10, 0, 0)
    resenias = []
    
    for i in range(1, cantidad + 1):
        id_usuario = random.randint(1, 300)
        id_restaurante = random.randint(1, 15)
        calificacion = random.randint(1, 5)
        comentario = random.choice(comentarios)
        fecha = fecha_base + timedelta(days=random.randint(0, 450), minutes=random.randint(0, 1440))
        
        resenias.append(
            (
                i,
                id_usuario,
                id_restaurante,
                calificacion,
                comentario,
                fecha,
            )
        )
    
    return resenias

def factory_resenias_conductor(cantidad):
    comentarios = [
        'Conductor muy profesional',
        'Entrega rápida y segura',
        'Buen trato y cortesía',
        'Llegó a la hora exacta',
        'Excelente servicio',
        'Pedido bien cuidado',
        'Debería mejorar la comunicación',
        'Llegó tarde',
        'El conductor fue desatento',
        'Recomendado'
    ]
    
    random.seed(129)
    fecha_base = datetime(2024, 1, 1, 10, 0, 0)
    resenias = []
    
    for i in range(1, cantidad + 1):
        id_usuario = random.randint(1, 300)
        id_conductor = random.randint(1, 120)
        calificacion = random.randint(1, 5)
        comentario = random.choice(comentarios)
        fecha = fecha_base + timedelta(days=random.randint(0, 450), minutes=random.randint(0, 1440))
        
        resenias.append(
            (
                i,
                id_usuario,
                id_conductor,
                calificacion,
                comentario,
                fecha,
            )
        )
    
    return resenias

def factory_estados_conductor(cantidad_conductores):
    estados = ['Disponible', 'En entrega', 'Inactivo', 'Activo', 'Tomando descanso']
    
    random.seed(130)
    fecha_base = datetime(2024, 1, 1, 8, 0, 0)
    estados_log = []
    id_log = 1
    
    for id_conductor in range(1, cantidad_conductores + 1):
        # Generar 2-8 cambios de estado por conductor
        cantidad_cambios = random.randint(2, 8)
        
        for _ in range(cantidad_cambios):
            estado = random.choice(estados)
            timestamp_registro = fecha_base + timedelta(days=random.randint(0, 450), minutes=random.randint(0, 1440))
            
            estados_log.append(
                (
                    id_log,
                    id_conductor,
                    estado,
                    timestamp_registro,
                )
            )
            id_log += 1
    
    return estados_log





# Insertar datos en la base de datos PostgreSQL
def insertar_restaurantes(cursor):
    consulta_insercion = '''
            INSERT INTO restaurantes (id_restaurante, nombre, categoria, direccion, ciudad, estado, telefono, email, calificacion_promedio, estatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
    cursor.executemany(consulta_insercion, RESTAURANTES)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'restaurantes'.")

def insertar_productos(cursor):
    consulta_insercion = '''
            INSERT INTO productos (id_producto, id_restaurante, nombre_producto, categoria_producto, precio, disponibilidad)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''
        
    cursor.executemany(consulta_insercion, PRODUCTOS)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'productos'.")

def insertar_usuarios(cursor):
    consulta_insercion = '''
            INSERT INTO usuarios (id_usuario, nombre, apellido_paterno, apellido_materno, telefono, email, direccion, fecha_registro, calificacion_promedio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    usuarios = factory_usuarios(cantidad=300)
    cursor.executemany(consulta_insercion, usuarios)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'usuarios'.")

def insertar_conductores(cursor):
    consulta_insercion = '''
            INSERT INTO conductores (id_conductor, nombre, apellido_paterno, apellido_materno, telefono, email, tipo_vehiculo, placa, calificacion_promedio, estatus, fecha_ingreso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    conductores = factory_conductores(cantidad=120)
    cursor.executemany(consulta_insercion, conductores)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'conductores'.")

def insertar_estatus(cursor):
    consulta_insercion = '''
            INSERT INTO estatus_pedido (id_estatus, estatus, descripcion)
            VALUES (%s, %s, %s);
        '''
        
    cursor.executemany(consulta_insercion, ESTATUS)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'estatus'.")

def insertar_metodos_pago(cursor):
    consulta_insercion = '''
            INSERT INTO metodos_pago (id_metodo, metodo, descripcion)
            VALUES (%s, %s, %s);
        '''
        
    cursor.executemany(consulta_insercion, METODOS_PAGO)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'metodos_pago'.")

def insertar_pedidos(cursor):
    consulta_insercion = '''
            INSERT INTO pedidos (id_pedido, id_usuario, id_restaurante, id_conductor, id_estatus, metodo_pago, fecha_pedido, hora_recogida, hora_entrega, subtotal, costo_envio, total, tiempo_entrega_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    pedidos = factory_pedidos(cantidad=100000)
    cursor.executemany(consulta_insercion, pedidos)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'pedidos'.")


def insertar_detalle_pedido(cursor):
    consulta_insercion = '''
            INSERT INTO detalle_pedido (id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal_linea)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

    detalle = factory_detalle_pedido(cantidad_pedidos=100000)
    cursor.executemany(consulta_insercion, detalle)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'detalle_pedido'.")


def insertar_resenias_restaurante(cursor):
    consulta_insercion = '''
            INSERT INTO resenias_restaurante (id_resenia, id_usuario, id_restaurante, calificacion, comentario, fecha)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

    resenias = factory_resenias_restaurante(cantidad=2000)
    cursor.executemany(consulta_insercion, resenias)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'resenias_restaurante'.")


def insertar_resenias_conductor(cursor):
    consulta_insercion = '''
            INSERT INTO resenias_conductor (id_resenia, id_usuario, id_conductor, calificacion, comentario, fecha)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

    resenias = factory_resenias_conductor(cantidad=16000)
    cursor.executemany(consulta_insercion, resenias)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'resenias_conductor'.")


def insertar_estados_conductor(cursor):
    consulta_insercion = '''
            INSERT INTO estados_conductor (id_log, id_conductor, estado, timestamp_registro)
            VALUES (%s, %s, %s, %s);
        '''

    estados = factory_estados_conductor(cantidad_conductores=120)
    cursor.executemany(consulta_insercion, estados)
    print(f"Éxito: Se han insertado {cursor.rowcount} registros en la tabla 'estados_conductor'.")

def limpiar_tablas(cursor):
    cursor.execute('TRUNCATE TABLE resenias_restaurante, resenias_conductor, estados_conductor, detalle_pedido, productos, pedidos, restaurantes, conductores, usuarios, estatus_pedido, metodos_pago RESTART IDENTITY CASCADE;')
    print("Tablas limpiadas correctamente.\n\n")



def poblar_base_datos_postgres():
    conexion = None
    try:
        # Reemplaza estos valores con tus credenciales de PostgreSQL
        conexion = psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            database="didifood",
            user="postgres",
            password="5691323"
        )

        cursor = conexion.cursor()

        limpiar_tablas(cursor)

        insertar_usuarios(cursor)
        insertar_conductores(cursor)
        insertar_estatus(cursor)
        insertar_metodos_pago(cursor)
        insertar_restaurantes(cursor)
        insertar_productos(cursor)
        insertar_pedidos(cursor)
        insertar_detalle_pedido(cursor)
        insertar_resenias_restaurante(cursor)
        insertar_resenias_conductor(cursor)
        insertar_estados_conductor(cursor)
        

        conexion.commit()


    except Error as e:
        print(f"Error al interactuar con PostgreSQL: {e}")
        
    finally:
        # Asegurarse de cerrar la conexión siempre
        if conexion:
            cursor.close()
            conexion.close()
            print("Conexión a PostgreSQL cerrada.")

if __name__ == '__main__':
    poblar_base_datos_postgres()

