import psycopg2
from psycopg2 import Error
from datetime import datetime, timedelta
import random
import csv
import os

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
    (15, 'Don Pancho', 'Mariscos', 'Av. Hidalgo 90', 'Oaxaca', 'OAX', '9511111015', 'rest015@gmail.com', 8.9, 'Activo'),
    (16, 'Mar y Tierra', 'Mariscos', 'Calle Morelos 145', 'Oaxaca', 'OAX', '9511111016', 'rest016@gmail.com', 8.8, 'Activo'),
    (17, 'La Toscana', 'Italiana', 'Av. Niños Héroes 230', 'Oaxaca', 'OAX', '9511111017', 'rest017@gmail.com', 9.0, 'Activo'),
    (18, 'Wok Express', 'Asiática', 'Calle Valerio Trujano 312', 'Oaxaca', 'OAX', '9511111018', 'rest018@gmail.com', 8.3, 'Activo'),
    (19, 'Antojitos Lupita', 'Mexicana', 'Calle Murguía 67', 'Oaxaca', 'OAX', '9511111019', 'rest019@gmail.com', 8.6, 'Activo'),
    (20, 'La Parrilla Norteña', 'Carnes', 'Av. Símbolos Patrios 520', 'Oaxaca', 'OAX', '9511111020', 'rest020@gmail.com', 8.9, 'Activo'),
    (21, 'Sabor Istmeño', 'Oaxaqueña', 'Calle Zaragoza 189', 'Oaxaca', 'OAX', '9511111021', 'rest021@gmail.com', 9.1, 'Activo'),
    (22, 'Bistro Central', 'Internacional', 'Calle Constitución 140', 'Oaxaca', 'OAX', '9511111022', 'rest022@gmail.com', 8.4, 'Activo'),
    (23, 'Ramen House', 'Japonesa', 'Av. Juárez 410', 'Oaxaca', 'OAX', '9511111023', 'rest023@gmail.com', 8.7, 'Activo'),
    (24, 'El Patio Verde', 'Vegetariana', 'Calle Abasolo 98', 'Oaxaca', 'OAX', '9511111024', 'rest024@gmail.com', 8.5, 'Activo'),
    (25, 'Taquería Don Chuy', 'Mexicana', 'Calle Rayón 255', 'Oaxaca', 'OAX', '9511111025', 'rest025@gmail.com', 8.2, 'Activo'),
    (26, 'Pasta e Vino', 'Italiana', 'Av. Universidad 670', 'Oaxaca', 'OAX', '9511111026', 'rest026@gmail.com', 8.9, 'Activo'),
    (27, 'La Cabaña Grill', 'Americana', 'Blvd. Eduardo Vasconcelos 880', 'Oaxaca', 'OAX', '9511111027', 'rest027@gmail.com', 8.1, 'Activo'),
    (28, 'Cocina del Valle', 'Oaxaqueña', 'Calle Allende 175', 'Oaxaca', 'OAX', '9511111028', 'rest028@gmail.com', 9.2, 'Activo'),
    (29, 'Deli Sandwich', 'Americana', 'Av. Heroico Colegio Militar 333', 'Oaxaca', 'OAX', '9511111029', 'rest029@gmail.com', 7.9, 'Activo'),
    (30, 'Dulce Aroma Café', 'Cafetería', 'Calle Reforma 260', 'Oaxaca', 'OAX', '9511111030', 'rest030@gmail.com', 8.6, 'Activo'),
    (31, 'Casa Mezquite', 'Mexicana', 'Calle Xicoténcatl 142', 'Oaxaca', 'OAX', '9511111031', 'rest031@gmail.com', 8.8, 'Activo'),
    (32, 'Trattoria Nonna', 'Italiana', 'Av. Benito Juárez 512', 'Oaxaca', 'OAX', '9511111032', 'rest032@gmail.com', 9.1, 'Activo'),
    (33, 'Pacific Roll', 'Japonesa', 'Calle Manuel Doblado 77', 'Oaxaca', 'OAX', '9511111033', 'rest033@gmail.com', 8.6, 'Activo'),
    (34, 'Parrilla del Centro', 'Carnes', 'Av. Morelos 610', 'Oaxaca', 'OAX', '9511111034', 'rest034@gmail.com', 8.7, 'Activo'),
    (35, 'La Esquina del Taco', 'Mexicana', 'Calle Armenta y López 33', 'Oaxaca', 'OAX', '9511111035', 'rest035@gmail.com', 8.4, 'Activo'),
    (36, 'Green Bowl', 'Vegetariana', 'Calle Independencia 204', 'Oaxaca', 'OAX', '9511111036', 'rest036@gmail.com', 8.9, 'Activo'),
    (37, 'Café Monte Albán', 'Cafetería', 'Av. Hidalgo 370', 'Oaxaca', 'OAX', '9511111037', 'rest037@gmail.com', 8.5, 'Activo'),
    (38, 'Costa Azul', 'Mariscos', 'Blvd. Guadalupe Hinojosa 120', 'Oaxaca', 'OAX', '9511111038', 'rest038@gmail.com', 9.0, 'Activo'),
    (39, 'Burger House', 'Americana', 'Calle Las Casas 158', 'Oaxaca', 'OAX', '9511111039', 'rest039@gmail.com', 8.0, 'Activo'),
    (40, 'Sabores del Istmo', 'Oaxaqueña', 'Calle Matamoros 219', 'Oaxaca', 'OAX', '9511111040', 'rest040@gmail.com', 9.2, 'Activo'),
    (41, 'Wok & Noodles', 'Asiática', 'Av. Universidad 455', 'Oaxaca', 'OAX', '9511111041', 'rest041@gmail.com', 8.3, 'Activo'),
    (42, 'La Terraza Bistro', 'Internacional', 'Calle García Vigil 620', 'Oaxaca', 'OAX', '9511111042', 'rest042@gmail.com', 8.6, 'Activo'),
    (43, 'Antojo Criollo', 'Mexicana', 'Calle Crespo 96', 'Oaxaca', 'OAX', '9511111043', 'rest043@gmail.com', 8.7, 'Activo'),
    (44, 'Río Grill', 'Carnes', 'Av. Símbolos Patrios 745', 'Oaxaca', 'OAX', '9511111044', 'rest044@gmail.com', 8.8, 'Activo'),
    (45, 'Dolce Caffè', 'Cafetería', 'Calle Constitución 288', 'Oaxaca', 'OAX', '9511111045', 'rest045@gmail.com', 8.9, 'Activo'),
    (46, 'La Ruta del Sabor', 'Mexicana', 'Av. Independencia 715', 'Oaxaca', 'OAX', '9511111046', 'rest046@gmail.com', 8.7, 'Activo'),
    (47, 'Casa del Mar', 'Mariscos', 'Calle Morelos 88', 'Oaxaca', 'OAX', '9511111047', 'rest047@gmail.com', 9.0, 'Activo'),
    (48, 'Forno Italiano', 'Italiana', 'Av. Juárez 520', 'Oaxaca', 'OAX', '9511111048', 'rest048@gmail.com', 8.8, 'Activo'),
    (49, 'Taquitos El Compa', 'Mexicana', 'Calle Mina 210', 'Oaxaca', 'OAX', '9511111049', 'rest049@gmail.com', 8.3, 'Activo'),
    (50, 'Nori Sushi Bar', 'Japonesa', 'Calle Abasolo 330', 'Oaxaca', 'OAX', '9511111050', 'rest050@gmail.com', 8.9, 'Activo'),
    (51, 'Brasa Norte', 'Carnes', 'Av. Universidad 910', 'Oaxaca', 'OAX', '9511111051', 'rest051@gmail.com', 8.6, 'Activo'),
    (52, 'Bowl Garden', 'Vegetariana', 'Calle Reforma 187', 'Oaxaca', 'OAX', '9511111052', 'rest052@gmail.com', 8.5, 'Activo'),
    (53, 'Café Alameda', 'Cafetería', 'Av. Hidalgo 490', 'Oaxaca', 'OAX', '9511111053', 'rest053@gmail.com', 8.4, 'Activo'),
    (54, 'La Olla Oaxaqueña', 'Oaxaqueña', 'Calle Allende 260', 'Oaxaca', 'OAX', '9511111054', 'rest054@gmail.com', 9.1, 'Activo'),
    (55, 'Urban Burgers', 'Americana', 'Blvd. Vasconcelos 410', 'Oaxaca', 'OAX', '9511111055', 'rest055@gmail.com', 8.0, 'Activo'),
    (56, 'Sazón del Barrio', 'Mexicana', 'Calle Crespo 141', 'Oaxaca', 'OAX', '9511111056', 'rest056@gmail.com', 8.8, 'Activo'),
    (57, 'Marea Alta', 'Mariscos', 'Av. Símbolos Patrios 620', 'Oaxaca', 'OAX', '9511111057', 'rest057@gmail.com', 8.7, 'Activo'),
    (58, 'Pizzería Vesubio', 'Italiana', 'Calle Rayón 305', 'Oaxaca', 'OAX', '9511111058', 'rest058@gmail.com', 8.6, 'Activo'),
    (59, 'Rincón del Ramen', 'Japonesa', 'Av. Benito Juárez 705', 'Oaxaca', 'OAX', '9511111059', 'rest059@gmail.com', 8.8, 'Activo'),
    (60, 'Parrilla 57', 'Carnes', 'Calle Murguía 280', 'Oaxaca', 'OAX', '9511111060', 'rest060@gmail.com', 8.9, 'Activo'),
    (61, 'Verde Vivo', 'Vegetariana', 'Calle Porfirio Díaz 420', 'Oaxaca', 'OAX', '9511111061', 'rest061@gmail.com', 8.7, 'Activo'),
    (62, 'Coffee Lab Oaxaca', 'Cafetería', 'Av. Independencia 845', 'Oaxaca', 'OAX', '9511111062', 'rest062@gmail.com', 8.5, 'Activo'),
    (63, 'El Comal Istmeño', 'Oaxaqueña', 'Calle Zaragoza 244', 'Oaxaca', 'OAX', '9511111063', 'rest063@gmail.com', 9.2, 'Activo'),
    (64, 'Grill House 24', 'Americana', 'Av. Universidad 1020', 'Oaxaca', 'OAX', '9511111064', 'rest064@gmail.com', 8.1, 'Activo'),
    (65, 'Antojitos del Sur', 'Mexicana', 'Calle Las Casas 299', 'Oaxaca', 'OAX', '9511111065', 'rest065@gmail.com', 8.4, 'Activo'),
    (66, 'Puerto Fresco', 'Mariscos', 'Av. Ferrocarril 330', 'Oaxaca', 'OAX', '9511111066', 'rest066@gmail.com', 8.8, 'Activo'),
    (67, 'Trattoria Venezia', 'Italiana', 'Calle Constitución 512', 'Oaxaca', 'OAX', '9511111067', 'rest067@gmail.com', 9.0, 'Activo'),
    (68, 'Sakura Roll', 'Japonesa', 'Calle García Vigil 715', 'Oaxaca', 'OAX', '9511111068', 'rest068@gmail.com', 8.7, 'Activo'),
    (69, 'Fuego y Carbón', 'Carnes', 'Blvd. Tecnológico 980', 'Oaxaca', 'OAX', '9511111069', 'rest069@gmail.com', 8.9, 'Activo'),
    (70, 'Huerto Urbano', 'Vegetariana', 'Calle Xicoténcatl 188', 'Oaxaca', 'OAX', '9511111070', 'rest070@gmail.com', 8.6, 'Activo'),
    (71, 'Café Nativo', 'Cafetería', 'Av. Juárez 640', 'Oaxaca', 'OAX', '9511111071', 'rest071@gmail.com', 8.8, 'Activo'),
    (72, 'Moles y Sabores', 'Oaxaqueña', 'Calle Matamoros 378', 'Oaxaca', 'OAX', '9511111072', 'rest072@gmail.com', 9.3, 'Activo'),
    (73, 'Route 66 Burgers', 'Americana', 'Av. Heroico Colegio Militar 520', 'Oaxaca', 'OAX', '9511111073', 'rest073@gmail.com', 7.9, 'Activo'),
    (74, 'La Casa del Taco', 'Mexicana', 'Calle Armenta y López 120', 'Oaxaca', 'OAX', '9511111074', 'rest074@gmail.com', 8.5, 'Activo'),
    (75, 'Bahía Azul', 'Mariscos', 'Av. Morelos 845', 'Oaxaca', 'OAX', '9511111075', 'rest075@gmail.com', 9.0, 'Activo'),
    (76, 'Pasta Toscana', 'Italiana', 'Calle Reforma 640', 'Oaxaca', 'OAX', '9511111076', 'rest076@gmail.com', 8.7, 'Activo'),
    (77, 'Tokyo Street', 'Japonesa', 'Calle Manuel Doblado 204', 'Oaxaca', 'OAX', '9511111077', 'rest077@gmail.com', 8.6, 'Activo'),
    (78, 'Asador del Valle', 'Carnes', 'Av. Hidalgo 910', 'Oaxaca', 'OAX', '9511111078', 'rest078@gmail.com', 8.8, 'Activo'),
    (79, 'Raíz Verde', 'Vegetariana', 'Calle Independencia 299', 'Oaxaca', 'OAX', '9511111079', 'rest079@gmail.com', 8.9, 'Activo'),
    (80, 'Tostado Café', 'Cafetería', 'Av. Benito Juárez 780', 'Oaxaca', 'OAX', '9511111080', 'rest080@gmail.com', 8.4, 'Activo'),
    (81, 'Tradición del Istmo', 'Oaxaqueña', 'Calle Crespo 265', 'Oaxaca', 'OAX', '9511111081', 'rest081@gmail.com', 9.1, 'Activo'),
    (82, 'Big Bites', 'Americana', 'Blvd. Guadalupe Hinojosa 330', 'Oaxaca', 'OAX', '9511111082', 'rest082@gmail.com', 8.0, 'Activo'),
    (83, 'El Fogoncito Mixteco', 'Mexicana', 'Calle Abasolo 410', 'Oaxaca', 'OAX', '9511111083', 'rest083@gmail.com', 8.6, 'Activo'),
    (84, 'Costa Dorada', 'Mariscos', 'Av. Universidad 1180', 'Oaxaca', 'OAX', '9511111084', 'rest084@gmail.com', 8.9, 'Activo'),
    (85, 'Nonna Mia', 'Italiana', 'Calle Rayón 402', 'Oaxaca', 'OAX', '9511111085', 'rest085@gmail.com', 9.0, 'Activo'),
    (86, 'Nippon Express', 'Japonesa', 'Calle Mina 366', 'Oaxaca', 'OAX', '9511111086', 'rest086@gmail.com', 8.5, 'Activo'),
    (87, 'La Estancia Grill', 'Carnes', 'Av. Símbolos Patrios 890', 'Oaxaca', 'OAX', '9511111087', 'rest087@gmail.com', 8.7, 'Activo'),
    (88, 'Semilla Kitchen', 'Vegetariana', 'Calle Constitución 366', 'Oaxaca', 'OAX', '9511111088', 'rest088@gmail.com', 8.8, 'Activo'),
    (89, 'Origen Café', 'Cafetería', 'Av. Independencia 980', 'Oaxaca', 'OAX', '9511111089', 'rest089@gmail.com', 8.6, 'Activo'),
    (90, 'Cocina Zapoteca', 'Oaxaqueña', 'Calle Morelos 520', 'Oaxaca', 'OAX', '9511111090', 'rest090@gmail.com', 9.2, 'Activo'),

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
    (90, 15, 'Agua de Coco', 'Bebida', 45, 'Disponible'),
    (91, 16, 'Camarones Empanizados', 'Principal', 210, 'Disponible'),
    (92, 16, 'Pulpo a las Brasas', 'Principal', 245, 'Disponible'),
    (93, 16, 'Filete al Ajo', 'Principal', 195, 'Disponible'),
    (94, 16, 'Tostadas de Atún', 'Entrada', 125, 'Disponible'),
    (95, 16, 'Caldo de Mariscos', 'Entrada', 140, 'Disponible'),
    (96, 16, 'Limonada Mineral', 'Bebida', 45, 'Disponible'),
    (97, 17, 'Fettuccine Alfredo', 'Principal', 165, 'Disponible'),
    (98, 17, 'Ravioles de Ricotta', 'Principal', 175, 'Disponible'),
    (99, 17, 'Pizza Cuatro Quesos', 'Principal', 155, 'Disponible'),
    (100, 17, 'Bruschettas', 'Entrada', 95, 'Disponible'),
    (101, 17, 'Minestrone', 'Entrada', 85, 'Disponible'),
    (102, 17, 'Panna Cotta', 'Postre', 80, 'Disponible'),
    (103, 18, 'Pollo Teriyaki', 'Principal', 150, 'Disponible'),
    (104, 18, 'Arroz Frito Especial', 'Principal', 140, 'Disponible'),
    (105, 18, 'Noodles con Res', 'Principal', 155, 'Disponible'),
    (106, 18, 'Rollitos Primavera', 'Entrada', 90, 'Disponible'),
    (107, 18, 'Dumplings al Vapor', 'Entrada', 95, 'Disponible'),
    (108, 18, 'Té Jazmín', 'Bebida', 35, 'Disponible'),
    (109, 19, 'Enchiladas Suizas', 'Principal', 125, 'Disponible'),
    (110, 19, 'Flautas de Pollo', 'Principal', 115, 'Disponible'),
    (111, 19, 'Pozole Rojo', 'Principal', 135, 'Disponible'),
    (112, 19, 'Guacamole con Totopos', 'Entrada', 85, 'Disponible'),
    (113, 19, 'Sopes Sencillos', 'Entrada', 70, 'Disponible'),
    (114, 19, 'Agua de Tamarindo', 'Bebida', 30, 'Disponible'),
    (115, 20, 'Rib Eye 350g', 'Principal', 320, 'Disponible'),
    (116, 20, 'Picaña', 'Principal', 290, 'Disponible'),
    (117, 20, 'Brochetas Mixtas', 'Principal', 210, 'Disponible'),
    (118, 20, 'Chistorra Asada', 'Entrada', 110, 'Disponible'),
    (119, 20, 'Papas Gajo', 'Entrada', 75, 'Disponible'),
    (120, 20, 'Naranjada', 'Bebida', 40, 'Disponible'),
    (121, 21, 'Mole Coloradito', 'Principal', 190, 'Disponible'),
    (122, 21, 'Tasajo Encebollado', 'Principal', 210, 'Disponible'),
    (123, 21, 'Empanadas de Amarillo', 'Principal', 145, 'Disponible'),
    (124, 21, 'Sopa de Guías', 'Entrada', 95, 'Disponible'),
    (125, 21, 'Quesillo Asado', 'Entrada', 85, 'Disponible'),
    (126, 21, 'Atole de Maíz', 'Bebida', 45, 'Disponible'),
    (127, 22, 'Salmón a la Plancha', 'Principal', 240, 'Disponible'),
    (128, 22, 'Pechuga Rellena', 'Principal', 210, 'Disponible'),
    (129, 22, 'Risotto de Hongos', 'Principal', 185, 'Disponible'),
    (130, 22, 'Carpaccio', 'Entrada', 130, 'Disponible'),
    (131, 22, 'Sopa del Día', 'Entrada', 85, 'Disponible'),
    (132, 22, 'Limonada de Pepino', 'Bebida', 50, 'Disponible'),
    (133, 23, 'Ramen Tonkotsu', 'Principal', 185, 'Disponible'),
    (134, 23, 'Katsu Curry', 'Principal', 170, 'Disponible'),
    (135, 23, 'Yakimeshi', 'Principal', 140, 'Disponible'),
    (136, 23, 'Takoyaki', 'Entrada', 120, 'Disponible'),
    (137, 23, 'Tempura Mixta', 'Entrada', 135, 'Disponible'),
    (138, 23, 'Ramune', 'Bebida', 55, 'Disponible'),
    (139, 24, 'Bowl Mediterráneo', 'Principal', 135, 'Disponible'),
    (140, 24, 'Tacos de Coliflor', 'Principal', 115, 'Disponible'),
    (141, 24, 'Lasaña Vegetal', 'Principal', 145, 'Disponible'),
    (142, 24, 'Hummus con Pita', 'Entrada', 95, 'Disponible'),
    (143, 24, 'Crema de Calabaza', 'Entrada', 80, 'Disponible'),
    (144, 24, 'Kombucha', 'Bebida', 65, 'Disponible'),

    (145, 25, 'Taco al Pastor', 'Principal', 32, 'Disponible'),
    (146, 25, 'Taco de Suadero', 'Principal', 34, 'Disponible'),
    (147, 25, 'Gringa', 'Principal', 65, 'Disponible'),
    (148, 25, 'Volcán de Pastor', 'Entrada', 58, 'Disponible'),
    (149, 25, 'Frijoles Charros', 'Entrada', 50, 'Disponible'),
    (150, 25, 'Agua de Limón con Chía', 'Bebida', 28, 'Disponible'),
    (151, 26, 'Spaghetti Bolognesa', 'Principal', 160, 'Disponible'),
    (152, 26, 'Gnocchi al Pesto', 'Principal', 170, 'Disponible'),
    (153, 26, 'Pizza Prosciutto', 'Principal', 180, 'Disponible'),
    (154, 26, 'Caprese', 'Entrada', 110, 'Disponible'),
    (155, 26, 'Focaccia', 'Entrada', 70, 'Disponible'),
    (156, 26, 'Cannoli', 'Postre', 85, 'Disponible'),
    (157, 27, 'Cheeseburger Doble', 'Principal', 145, 'Disponible'),
    (158, 27, 'BBQ Bacon Burger', 'Principal', 155, 'Disponible'),
    (159, 27, 'Chicken Sandwich', 'Principal', 130, 'Disponible'),
    (160, 27, 'Aros de Cebolla', 'Entrada', 75, 'Disponible'),
    (161, 27, 'Mac & Cheese Bites', 'Entrada', 85, 'Disponible'),
    (162, 27, 'Malteada Vainilla', 'Bebida', 70, 'Disponible'),
    (163, 28, 'Mole Amarillo', 'Principal', 185, 'Disponible'),
    (164, 28, 'Chileajo de Cerdo', 'Principal', 195, 'Disponible'),
    (165, 28, 'Tamales Oaxaqueños', 'Principal', 120, 'Disponible'),
    (166, 28, 'Tetelas', 'Entrada', 90, 'Disponible'),
    (167, 28, 'Quesadillas de Flor', 'Entrada', 85, 'Disponible'),
    (168, 28, 'Tejate', 'Bebida', 50, 'Disponible'),
    (169, 29, 'Club Sandwich', 'Principal', 120, 'Disponible'),
    (170, 29, 'Panini de Pavo', 'Principal', 115, 'Disponible'),
    (171, 29, 'Wrap César', 'Principal', 110, 'Disponible'),
    (172, 29, 'Papas a la Francesa', 'Entrada', 60, 'Disponible'),
    (173, 29, 'Ensalada de Atún', 'Entrada', 95, 'Disponible'),
    (174, 29, 'Té Helado', 'Bebida', 35, 'Disponible'),
    (175, 30, 'Espresso Doble', 'Bebida', 48, 'Disponible'),
    (176, 30, 'Moka', 'Bebida', 78, 'Disponible'),
    (177, 30, 'Chai Latte', 'Bebida', 72, 'Disponible'),
    (178, 30, 'Bagel de Queso', 'Entrada', 62, 'Disponible'),
    (179, 30, 'Cheesecake de Frutos Rojos', 'Postre', 92, 'Disponible'),
    (180, 30, 'Galleta de Avena', 'Postre', 38, 'Disponible')
]


ruta_csv = "datos_csv/"


def csv_generador( ruta, datos ):
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos)


def usuarios_generador():
    nombres = [
        'Fernanda', 'Valentina', 'Adriana', 'Ana', 'Carlos', 'Andres', 'Patricia',
        'Juan', 'Karla', 'Sofia', 'Mario', 'Elena', 'Gabriela', 'Diego', 'Miguel',
        'Daniel', 'Rosa', 'Ricardo', 'Paola', 'Eduardo',
        'Camila', 'Jose', 'Mariana', 'Luis', 'Andrea', 'Fernando', 'Ximena',
        'Sebastian', 'Alejandra', 'Raul', 'Natalia', 'Hugo', 'Daniela', 'Javier',
        'Monica', 'Alberto', 'Renata', 'Oscar', 'Lucia', 'Tomas'
    ]
    apellidos = [
        'Jimenez', 'Gonzalez', 'Reyes', 'Guerrero', 'Lopez', 'Vega', 'Diaz',
        'Morales', 'Rodriguez', 'Flores', 'Mendoza', 'Torres', 'Sanchez',
        'Ruiz', 'Castillo', 'Ortega', 'Salinas', 'Rivera', 'Ramos', 'Cruz',
        'Hernandez', 'Navarro', 'Aguilar', 'Pineda', 'Vazquez', 'Campos', 'Delgado',
        'Rojas', 'Cabrera', 'Mejia', 'Nunez', 'Ibarra', 'Fuentes', 'Solis',
        'Molina', 'Acosta', 'Escobar', 'Cortes', 'Padilla', 'Espinoza'
    ]
    fecha_base = datetime(2023, 1, 1, 8, 0, 0)
    usuarios = []
    usuarios.append([
        "id_usuario",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "telefono",
        "email",
        "direccion",
        "fecha_registro",
        "calificacion_promedio",
    ])

    for i in range(1, nombres.__len__() * apellidos.__len__() * apellidos.__len__() + 1):
        idx = i - 1
        bloque_apellidos = len(apellidos) * len(apellidos)

        nombre = nombres[(idx // bloque_apellidos) % len(nombres)]
        resto = idx % bloque_apellidos
        apellido_paterno = apellidos[resto // len(apellidos)]
        apellido_materno = apellidos[resto % len(apellidos)]
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

def conductores_generador():
    nombres = [
        'Fernanda', 'Valentina', 'Adriana', 'Ana', 'Carlos', 'Andres', 'Patricia',
        'Juan', 'Karla', 'Sofia', 'Mario', 'Elena', 'Gabriela', 'Diego', 'Miguel',
        'Daniel', 'Rosa', 'Ricardo', 'Paola', 'Eduardo',
        'Camila', 'Jose', 'Mariana', 'Luis', 'Andrea', 'Fernando', 'Ximena',
        'Sebastian', 'Alejandra', 'Raul', 'Natalia', 'Hugo', 'Daniela', 'Javier',
        'Monica', 'Alberto', 'Renata', 'Oscar', 'Lucia', 'Tomas'
    ]
    apellidos = [
        'Jimenez', 'Gonzalez', 'Reyes', 'Guerrero', 'Lopez', 'Vega', 'Diaz',
        'Morales', 'Rodriguez', 'Flores', 'Mendoza', 'Torres', 'Sanchez',
        'Ruiz', 'Castillo', 'Ortega', 'Salinas', 'Rivera', 'Ramos', 'Cruz',
        'Hernandez', 'Navarro', 'Aguilar', 'Pineda', 'Vazquez', 'Campos',
        # Conductores pueden tener apellidos repetidos
    ]
    fecha_base = datetime(2023, 1, 1, 8, 0, 0)
    conductores = []
    conductores.append([
        "id_conductor",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "telefono",
        "email",
        "tipo_vehiculo",
        "placa",
        "calificacion_promedio",
        "estatus",
        "fecha_ingreso",
    ])

    tipos_vehiculo = ['Sedan', 'SUV', 'Hatchback', 'Pickup', 'Van','Motocicleta']
    estatus_opciones = ['Activo', 'Inactivo', 'Sancionado']

    for i in range(1, nombres.__len__() * apellidos.__len__() * apellidos.__len__() + 1):
        idx = i - 1
        bloque_apellidos = len(apellidos) * len(apellidos)

        nombre = nombres[(idx // bloque_apellidos) % len(nombres)]
        resto = idx % bloque_apellidos
        apellido_paterno = apellidos[resto // len(apellidos)]
        apellido_materno = apellidos[resto % len(apellidos)]
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

def pedidos_generador( cantidad):
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
    
    fecha_base = datetime(2021, 1, 1, 9, 0, 0)
    fecha_hoy = datetime.now()
    pedidos = []
    pedidos.append([
        "id_pedido",
        "id_usuario",
        "restaurante",
        "id_conductor",
        "estatus_pedido",
        "metodo_pago",
        "fecha_pedido",
        "hora_recogida",
        "hora_entrega",
        "subtotal",
        "costo_envio",
        "total",
        "tiempo_entrega_min",
    ])
    random.seed(126)

    for i in range(1, cantidad + 1):
        id_usuario = random.randint(1, 40 * 40 * 40)  
        id_restaurante = random.randint(1, RESTAURANTES.__len__())
        id_conductor = random.randint(1, 20*20*20)
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

        # metodo_pago = random.choice(metodos_pago_ids)
        subtotal = round(random.uniform(90, 650), 2)
        costo_envio = round(random.uniform(15, 65), 2)
        total = round(subtotal + costo_envio, 2)

        estatus_valor = next(nombre for _id, nombre, _desc in ESTATUS if _id == id_estatus)
        metodo_pago_valor = random.choice([nombre for _id, nombre, _desc in METODOS_PAGO])

        pedidos.append(
            [
            i,
            id_usuario,
            RESTAURANTES[id_restaurante-1][1],
            id_conductor,
            estatus_valor,
            metodo_pago_valor,
            fecha_pedido,
            hora_recogida,
            hora_entrega,
            subtotal,
            costo_envio,
            total,
            tiempo_entrega_min,
            ]
        )

    return pedidos

def restaurantes_generador():
    
    restaurantes = []
    restaurantes.append([
        "id_restaurante",
        "nombre",
        "direccion",
        "telefono",
        "calificacion_promedio",
    ])

    for restaurante in RESTAURANTES:
        id_restaurante, nombre, _tipo, direccion, _ciudad, _estado, telefono, _email, calificacion_promedio, _estatus = restaurante
        restaurantes.append([
            id_restaurante,
            nombre,
            direccion,
            telefono,
            calificacion_promedio,
        ])

    return restaurantes

def productos_generador():
    
    productos = []
    productos.append([
        "id_producto",
        "restaurante",
        "nombre",
        "categoria",
        "precio",
        "estatus",
    ])

    for producto in PRODUCTOS:
        id_producto, id_restaurante, nombre, categoria, precio, estatus = producto
        productos.append([
            id_producto,
            RESTAURANTES[id_restaurante][1],
            nombre,
            categoria,
            precio,
            estatus,
        ])

    return productos

if __name__ == "__main__":
    # Generar CSV de usuarios
    csv_generador(ruta_csv + "usuarios.csv", usuarios_generador())
    # Generar CSV de conductores
    csv_generador(ruta_csv + "conductores.csv", conductores_generador())
    # Generar CSV de restaurantes
    csv_generador(ruta_csv + "restaurantes.csv", restaurantes_generador())
    #Generar CSV de productos
    csv_generador(ruta_csv + "productos.csv", productos_generador())
    # Generar CSV de pedidos
    csv_generador(ruta_csv + "pedidos.csv", pedidos_generador(1000000))