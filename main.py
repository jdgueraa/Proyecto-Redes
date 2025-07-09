import csv
import heapq
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Archivo con las conexiones de la red ISP
ARCHIVO_RED = "red_isp_peru.csv"
 # Permitir que el usuario pase su propio archivo CSV como argumento al ejecutar el script
if len(sys.argv) > 1:
    ARCHIVO_RED = sys.argv[1]

class RedISP:
    """Clase que representa la red de un ISP"""
    def __init__(self):
        self.grafo = {}  # diccionario para guardar las conexiones
        self.ciudades = []  # lista de ciudades disponibles
    
    def cargar_red_desde_archivo(self, archivo):
        """
        Carga la red ISP desde un archivo CSV
        Formato esperado: ciudad_origen,ciudad_destino,latencia_ms,costo_soles,ancho_banda_mbps
        """
        print("📡 Cargando red ISP desde archivo:", archivo)
        
        try:
            with open(archivo, newline="", encoding='utf-8') as archivo_csv:
                lector = csv.reader(archivo_csv)
                
                # saltar encabezado si existe
                primera_linea = next(lector)
                if not primera_linea[0].replace('.','').isdigit():
                    # es encabezado, continuar con la siguiente
                    pass
                else:
                    # no es encabezado, procesar esta linea
                    self._procesar_conexion(primera_linea)
                
                # procesar el resto de lineas
                for linea in lector:
                    self._procesar_conexion(linea)
                    
        except FileNotFoundError:
            print("❌ ERROR: No se encontró el archivo", archivo)
            print("💡 Por favor, crea el archivo CSV con las conexiones de la red.")
            print("📋 Formato esperado: ciudad_origen,ciudad_destino,latencia_ms,costo_soles,ancho_banda_mbps")
            sys.exit()
        
        # crear lista ordenada de ciudades
        self.ciudades = sorted(list(self.grafo.keys()))
        print(f"✅ Red cargada: {len(self.ciudades)} ciudades, {self._contar_conexiones()} conexiones")
    
    def _procesar_conexion(self, linea):
        """Procesa una línea del CSV y agrega la conexión al grafo"""
        ciudad_a = linea[0].strip()
        ciudad_b = linea[1].strip()
        latencia = float(linea[2])      # milisegundos
        costo = float(linea[3])         # soles por MB
        ancho_banda = float(linea[4])   # Mbps
        
        # crear conexiones bidireccionales
        if ciudad_a not in self.grafo:
            self.grafo[ciudad_a] = []
        if ciudad_b not in self.grafo:
            self.grafo[ciudad_b] = []
        
        # agregar conexión A -> B y B -> A con todas las métricas
        conexion_ab = {
            'destino': ciudad_b,
            'latencia': latencia,
            'costo': costo,
            'ancho_banda': ancho_banda
        }
        conexion_ba = {
            'destino': ciudad_a,
            'latencia': latencia,
            'costo': costo,
            'ancho_banda': ancho_banda
        }
        
        self.grafo[ciudad_a].append(conexion_ab)
        self.grafo[ciudad_b].append(conexion_ba)
    
    def _contar_conexiones(self):
        """Cuenta el total de conexiones únicas"""
        total = 0
        for ciudad in self.grafo:
            total += len(self.grafo[ciudad])
        return total // 2  # dividir por 2 porque son bidireccionales
    
    def dijkstra_optimizado(self, origen, criterio='latencia'):
        """
        Ejecuta Dijkstra optimizado para el criterio seleccionado
        Criterios: 'latencia', 'costo', 'ancho_banda', 'compuesto'
        """
        # inicializar distancias
        distancias = {}
        anteriores = {}
        
        for ciudad in self.grafo:
            distancias[ciudad] = float('inf')
        distancias[origen] = 0
        
        # cola de prioridad
        cola = [(0, origen)]
        
        print(f"🔍 Calculando rutas óptimas desde {origen} (criterio: {criterio})...")
        
        while cola:
            distancia_actual, ciudad_actual = heapq.heappop(cola)
            
            # si ya procesamos esta ciudad con mejor distancia, continuar
            if distancia_actual > distancias[ciudad_actual]:
                continue
            
            # revisar todas las conexiones de esta ciudad
            for conexion in self.grafo[ciudad_actual]:
                ciudad_vecina = conexion['destino']
                
                # calcular peso según el criterio
                if criterio == 'latencia':
                    peso = conexion['latencia']
                elif criterio == 'costo':
                    peso = conexion['costo'] * 100  # multiplicar para evitar números muy pequeños
                elif criterio == 'ancho_banda':
                    peso = 1000 - conexion['ancho_banda']  # invertir (mayor ancho = menor peso)
                elif criterio == 'compuesto':
                    # fórmula compuesta (puedes ajustar los factores)
                    peso = (conexion['latencia'] * 0.5 + 
                           conexion['costo'] * 50 + 
                           (1000 - conexion['ancho_banda']) * 0.3)
                else:
                    peso = conexion['latencia']  # default
                
                nueva_distancia = distancia_actual + peso
                
                # si encontramos mejor camino, actualizar
                if nueva_distancia < distancias[ciudad_vecina]:
                    distancias[ciudad_vecina] = nueva_distancia
                    anteriores[ciudad_vecina] = ciudad_actual
                    heapq.heappush(cola, (nueva_distancia, ciudad_vecina))
        
        return distancias, anteriores
    
    def reconstruir_ruta(self, anteriores, destino):
        """Reconstruye la ruta desde origen hasta destino"""
        ruta = []
        ciudad_actual = destino
        
        while ciudad_actual in anteriores:
            ruta.append(ciudad_actual)
            ciudad_actual = anteriores[ciudad_actual]
        ruta.append(ciudad_actual)
        
        return list(reversed(ruta))
    
    def obtener_metricas_ruta(self, ruta):
        """Calcula las métricas totales de una ruta"""
        if len(ruta) < 2:
            return None
        
        latencia_total = 0
        costo_total = 0
        ancho_banda_minimo = float('inf')
        
        for i in range(len(ruta) - 1):
            ciudad_actual = ruta[i]
            ciudad_siguiente = ruta[i + 1]
            
            # buscar la conexión
            for conexion in self.grafo[ciudad_actual]:
                if conexion['destino'] == ciudad_siguiente:
                    latencia_total += conexion['latencia']
                    costo_total += conexion['costo']
                    ancho_banda_minimo = min(ancho_banda_minimo, conexion['ancho_banda'])
                    break
        
        return {
            'latencia_total': latencia_total,
            'costo_total': costo_total,
            'ancho_banda_limitante': ancho_banda_minimo,
            'saltos': len(ruta) - 1
        }
    
    def mostrar_ciudades(self):
        """Muestra todas las ciudades disponibles"""
        print("🏙️  Ciudades disponibles en la red ISP:")
        print("-" * 40)
        for i, ciudad in enumerate(self.ciudades, 1):
            print(f"{i:2d}. {ciudad}")
        print("-" * 40)
    
    def crear_imagen_grafo(self, ruta_destacada=None, nombre_archivo="red_isp_grafo.png", 
                          criterio_visual='latencia', mostrar_etiquetas=True):
        """
        Crea una imagen visual del grafo de la red ISP con métricas
        ruta_destacada: lista de ciudades que forman una ruta a destacar
        criterio_visual: 'latencia', 'costo', 'ancho_banda' para colorear/dimensionar
        mostrar_etiquetas: si mostrar valores en las conexiones
        """
        print(f"📊 Generando imagen del grafo (criterio: {criterio_visual})...")
        
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            import matplotlib.cm as cm
            import numpy as np
            
            # Crear grafo de NetworkX
            G = nx.Graph()
            
            # Agregar nodos (ciudades)
            for ciudad in self.ciudades:
                G.add_node(ciudad)
            
            # Agregar aristas con pesos y recopilar valores para normalización
            aristas_agregadas = set()
            valores_criterio = []
            
            for ciudad_origen in self.grafo:
                for conexion in self.grafo[ciudad_origen]:
                    ciudad_destino = conexion['destino']
                    # Evitar duplicar aristas bidireccionales
                    arista = tuple(sorted([ciudad_origen, ciudad_destino]))
                    if arista not in aristas_agregadas:
                        G.add_edge(ciudad_origen, ciudad_destino, 
                                 latencia=conexion['latencia'],
                                 costo=conexion['costo'],
                                 ancho_banda=conexion['ancho_banda'])
                        aristas_agregadas.add(arista)
                        
                        # Recopilar valores para normalización
                        if criterio_visual == 'latencia':
                            valores_criterio.append(conexion['latencia'])
                        elif criterio_visual == 'costo':
                            valores_criterio.append(conexion['costo'])
                        elif criterio_visual == 'ancho_banda':
                            valores_criterio.append(conexion['ancho_banda'])
            
            # Configurar el layout del grafo
            plt.figure(figsize=(20, 14))
            pos = nx.spring_layout(G, k=4, iterations=100, seed=42)
            
            # Normalizar valores para colores y anchos
            if valores_criterio:
                min_val = min(valores_criterio)
                max_val = max(valores_criterio)
                
                # Crear mapas de colores y anchos para cada arista
                edge_colors = []
                edge_widths = []
                edge_labels = {}
                
                for edge in G.edges():
                    ciudad_a, ciudad_b = edge
                    edge_data = G[ciudad_a][ciudad_b]
                    
                    if criterio_visual == 'latencia':
                        valor = edge_data['latencia']
                        unidad = 'ms'
                    elif criterio_visual == 'costo':
                        valor = edge_data['costo']
                        unidad = 'S/'
                    elif criterio_visual == 'ancho_banda':
                        valor = edge_data['ancho_banda']
                        unidad = 'Mbps'
                    else:
                        valor = edge_data['latencia']
                        unidad = 'ms'
                    
                    # Normalizar valor (0-1)
                    if max_val > min_val:
                        valor_norm = (valor - min_val) / (max_val - min_val)
                    else:
                        valor_norm = 0.5
                    
                    # Para ancho de banda, invertir colores (mayor = mejor = verde)
                    if criterio_visual == 'ancho_banda':
                        color_norm = 1 - valor_norm
                        width = 1 + valor_norm * 4  # Más ancho = mejor ancho de banda
                    else:
                        color_norm = valor_norm
                        width = 1 + (1 - valor_norm) * 4  # Más ancho = mejor (menor latencia/costo)
                    
                    edge_colors.append(color_norm)
                    edge_widths.append(width)
                    
                    # Etiqueta con valor
                    if mostrar_etiquetas:
                        if criterio_visual == 'costo':
                            edge_labels[edge] = f"{valor:.3f}{unidad}"
                        else:
                            edge_labels[edge] = f"{valor:.1f}{unidad}"
                
                # Elegir mapa de colores según criterio
                if criterio_visual == 'latencia':
                    cmap = cm.Reds  # Rojo = alta latencia (malo)
                elif criterio_visual == 'costo':
                    cmap = cm.Oranges  # Naranja = alto costo (malo)
                elif criterio_visual == 'ancho_banda':
                    cmap = cm.Greens  # Verde = alto ancho de banda (bueno)
                else:
                    cmap = cm.Blues
                
                # Dibujar aristas con colores y anchos basados en criterio
                edges = nx.draw_networkx_edges(G, pos, 
                                             edge_color=edge_colors,
                                             edge_cmap=cmap,
                                             width=edge_widths,
                                             alpha=0.7)
                
                # Agregar barra de colores
                sm = plt.cm.ScalarMappable(cmap=cmap, 
                                         norm=plt.Normalize(vmin=min_val, vmax=max_val))
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.8)
                
                if criterio_visual == 'latencia':
                    cbar.set_label('Latencia (ms)', rotation=270, labelpad=20)
                elif criterio_visual == 'costo':
                    cbar.set_label('Costo (S/ por MB)', rotation=270, labelpad=20)
                elif criterio_visual == 'ancho_banda':
                    cbar.set_label('Ancho de Banda (Mbps)', rotation=270, labelpad=20)
                
                # Mostrar etiquetas de valores en las conexiones
                if mostrar_etiquetas and len(edge_labels) < 50:  # No mostrar si hay muchas conexiones
                    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, alpha=0.8)
            
            # Si hay una ruta destacada, dibujarla con estilo especial
            if ruta_destacada and len(ruta_destacada) > 1:
                aristas_ruta = []
                for i in range(len(ruta_destacada) - 1):
                    aristas_ruta.append((ruta_destacada[i], ruta_destacada[i + 1]))
                
                nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, 
                                     edge_color='purple', width=6, alpha=0.9,
                                     style='dashed')
            
            # Dibujar nodos (ciudades) con tamaños variables según conectividad
            node_sizes = []
            for ciudad in G.nodes():
                conexiones = len(self.grafo[ciudad])
                size = 1000 + conexiones * 200  # Tamaño base + factor de conectividad
                node_sizes.append(size)
            
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                                 node_size=node_sizes, alpha=0.9, edgecolors='black')
            
            # Destacar nodos de la ruta si existe
            if ruta_destacada:
                ruta_sizes = [1200 + len(self.grafo[ciudad]) * 200 for ciudad in ruta_destacada]
                nx.draw_networkx_nodes(G, pos, nodelist=ruta_destacada, 
                                     node_color='gold', node_size=ruta_sizes, 
                                     alpha=0.9, edgecolors='purple', linewidths=3)
            
            # Agregar etiquetas de las ciudades
            nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
            
            # Configurar el título
            criterio_nombres = {
                'latencia': 'Latencia (ms)',
                'costo': 'Costo (S/)',
                'ancho_banda': 'Ancho de Banda (Mbps)'
            }
            
            titulo = f"Red ISP - Perú\nVisualización por {criterio_nombres.get(criterio_visual, criterio_visual)}"
            titulo += f"\n{len(self.ciudades)} ciudades, {len(G.edges())} conexiones"
            
            if ruta_destacada:
                titulo += f"\nRuta destacada: {' → '.join(ruta_destacada)}"
            
            plt.title(titulo, fontsize=16, fontweight='bold', pad=20)
            
            # Agregar leyenda
            legend_elements = [
                plt.Line2D([0], [0], color='lightblue', marker='o', linestyle='None',
                          markersize=10, label='Ciudades (tamaño = conectividad)'),
                plt.Line2D([0], [0], color='gray', linewidth=2, alpha=0.7,
                          label=f'Conexiones (color/grosor = {criterio_visual})')
            ]
            
            if ruta_destacada:
                legend_elements.append(
                    plt.Line2D([0], [0], color='purple', linewidth=4, linestyle='--',
                              label='Ruta destacada')
                )
            
            plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98))
            
            plt.axis('off')
            plt.tight_layout()
            
            # Guardar la imagen
            import os

            # Crear carpeta de salida si no existe (por seguridad)
            os.makedirs("salidas", exist_ok=True)

            # Guardar dentro de la carpeta salidas/
            ruta_salida = os.path.join("salidas", nombre_archivo)
            plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')

            plt.show()
            
            print(f"✅ Imagen guardada como: {nombre_archivo}")
            print(f"📊 Criterio visualizado: {criterio_nombres.get(criterio_visual, criterio_visual)}")
            if valores_criterio:
                print(f"📈 Rango de valores: {min_val:.3f} - {max_val:.3f}")
            
        except ImportError:
            print("❌ Error: Se requieren las librerías matplotlib y networkx")
            print("💡 Instala con: pip install matplotlib networkx numpy")
        except Exception as e:
            print(f"❌ Error al crear imagen: {e}")

def pedir_entrada(mensaje):
    """Función auxiliar para pedir datos al usuario"""
    try:
        entrada = input(mensaje).strip()
        return entrada if entrada else None
    except:
        return None

def menu_principal():
    """Función principal del programa"""
    print("🌐" + "="*60)
    print("   SIMULADOR DE TRÁFICO EN RED ISP - PERÚ")
    print("   Optimización de rutas usando algoritmo de Dijkstra")
    print("="*60)
    
    # crear instancia de la red ISP
    red = RedISP()
    red.cargar_red_desde_archivo(ARCHIVO_RED)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1️⃣  Encontrar mejor ruta entre dos ciudades")
        print("2️⃣  Comparar rutas con diferentes criterios")
        print("3️⃣  Ver todas las rutas desde una ciudad")
        print("4️⃣  Mostrar estadísticas de la red")
        print("5️⃣  Crear imagen del grafo de la red")
        print("0️⃣  Salir del simulador")
        print("-" * 50)
        
        opcion = pedir_entrada("👉 Selecciona una opción: ")
        
        if opcion == "0":
            print("👋 Cerrando simulador. ¡Hasta luego!")
            break
        elif opcion == "1":
            simular_ruta_simple(red)
        elif opcion == "2":
            comparar_criterios(red)
        elif opcion == "3":
            rutas_desde_origen(red)
        elif opcion == "4":
            mostrar_estadisticas(red)
        elif opcion == "5":
            crear_imagen_grafo(red)
        else:
            print("❌ Opción no válida")
        
        input("\n📱 Presiona Enter para continuar...")

def simular_ruta_simple(red):
    """Simula una ruta simple entre dos ciudades"""
    print("\n🎯 SIMULACIÓN DE RUTA ENTRE DOS CIUDADES")
    red.mostrar_ciudades()
    
    origen = pedir_entrada("📍 Ciudad de origen: ")
    if not origen or origen not in red.ciudades:
        print("❌ Ciudad de origen no válida")
        return
    
    destino = pedir_entrada("🎯 Ciudad de destino: ")
    if not destino or destino not in red.ciudades:
        print("❌ Ciudad de destino no válida")
        return
    
    # seleccionar criterio
    print("\n📊 Criterios de optimización:")
    print("1. Latencia (menor tiempo)")
    print("2. Costo (menor precio)")
    print("3. Ancho de banda (mejor velocidad)")
    print("4. Compuesto (balance de todos)")
    
    criterio_num = pedir_entrada("Selecciona criterio (1-4): ")
    criterios = {'1': 'latencia', '2': 'costo', '3': 'ancho_banda', '4': 'compuesto'}
    criterio = criterios.get(criterio_num, 'latencia')
    
    # ejecutar Dijkstra
    distancias, anteriores = red.dijkstra_optimizado(origen, criterio)
    
    if distancias[destino] == float('inf'):
        print(f"❌ No hay conexión entre {origen} y {destino}")
        return
    
    # mostrar resultados
    ruta = red.reconstruir_ruta(anteriores, destino)
    metricas = red.obtener_metricas_ruta(ruta)
    
    print(f"\n✅ RUTA ÓPTIMA ENCONTRADA ({criterio.upper()})")
    print("="*50)
    print(f"🗺️  Ruta: {' → '.join(ruta)}")
    print(f"⏱️  Latencia total: {metricas['latencia_total']:.1f} ms")
    print(f"💰 Costo total: S/ {metricas['costo_total']:.4f} por MB")
    print(f"📶 Ancho de banda limitante: {metricas['ancho_banda_limitante']:.0f} Mbps")
    print(f"🔗 Número de saltos: {metricas['saltos']}")
    
    # Preguntar si quiere crear imagen con la ruta destacada
    crear_img = pedir_entrada("\n¿Crear imagen del grafo con esta ruta destacada? (s/n): ")
    if crear_img and crear_img.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n📊 Criterio visual para la imagen:")
        print("1. Latencia (ms)")
        print("2. Costo (S/)")
        print("3. Ancho de banda (Mbps)")
        
        criterio_visual_num = pedir_entrada("Selecciona criterio visual (1-3): ")
        criterios_visuales = {'1': 'latencia', '2': 'costo', '3': 'ancho_banda'}
        criterio_visual = criterios_visuales.get(criterio_visual_num, 'latencia')
        
        mostrar_etiquetas = pedir_entrada("¿Mostrar valores en las conexiones? (s/n): ")
        mostrar_vals = mostrar_etiquetas and mostrar_etiquetas.lower() in ['s', 'si', 'sí', 'y', 'yes']
        
        nombre_archivo = f"ruta_{origen}_{destino}_{criterio}_{criterio_visual}.png"
        red.crear_imagen_grafo(ruta_destacada=ruta, nombre_archivo=nombre_archivo, 
                              criterio_visual=criterio_visual, mostrar_etiquetas=mostrar_vals)

def comparar_criterios(red):
    """Compara rutas usando diferentes criterios"""
    print("\n🔄 COMPARACIÓN DE CRITERIOS DE OPTIMIZACIÓN")
    red.mostrar_ciudades()
    
    origen = pedir_entrada("📍 Ciudad de origen: ")
    if not origen or origen not in red.ciudades:
        print("❌ Ciudad de origen no válida")
        return
    
    destino = pedir_entrada("🎯 Ciudad de destino: ")
    if not destino or destino not in red.ciudades:
        print("❌ Ciudad de destino no válida")
        return
    
    criterios = ['latencia', 'costo', 'ancho_banda', 'compuesto']
    nombres_criterios = ['⏱️  Latencia', '💰 Costo', '📶 Ancho Banda', '⚖️  Compuesto']
    
    print(f"\n📊 COMPARACIÓN DE RUTAS: {origen} → {destino}")
    print("="*70)
    
    for i, criterio in enumerate(criterios):
        distancias, anteriores = red.dijkstra_optimizado(origen, criterio)
        
        if distancias[destino] == float('inf'):
            print(f"{nombres_criterios[i]}: Sin conexión")
            continue
        
        ruta = red.reconstruir_ruta(anteriores, destino)
        metricas = red.obtener_metricas_ruta(ruta)
        
        print(f"\n{nombres_criterios[i]}:")
        print(f"   Ruta: {' → '.join(ruta)}")
        print(f"   Latencia: {metricas['latencia_total']:.1f}ms | "
              f"Costo: S/{metricas['costo_total']:.4f}/MB | "
              f"Ancho: {metricas['ancho_banda_limitante']:.0f}Mbps")

def rutas_desde_origen(red):
    """Muestra todas las rutas desde una ciudad origen"""
    print("\n🗺️  RUTAS DESDE UNA CIUDAD A TODAS LAS DEMÁS")
    red.mostrar_ciudades()
    
    origen = pedir_entrada("📍 Ciudad de origen: ")
    if not origen or origen not in red.ciudades:
        print("❌ Ciudad de origen no válida")
        return
    
    distancias, anteriores = red.dijkstra_optimizado(origen, 'latencia')
    
    print(f"\n📡 RUTAS DESDE {origen.upper()}:")
    print("="*60)
    
    for ciudad in sorted(red.ciudades):
        if ciudad == origen:
            continue
        
        if distancias[ciudad] == float('inf'):
            print(f"❌ {ciudad}: Sin conexión")
        else:
            ruta = red.reconstruir_ruta(anteriores, ciudad)
            metricas = red.obtener_metricas_ruta(ruta)
            print(f"✅ {ciudad}: {' → '.join(ruta)} "
                  f"({metricas['latencia_total']:.1f}ms)")

def mostrar_estadisticas(red):
    """Muestra estadísticas de la red"""
    print("\n📈 ESTADÍSTICAS DE LA RED ISP")
    print("="*50)
    print(f"🏙️  Total de ciudades: {len(red.ciudades)}")
    print(f"🔗 Total de conexiones: {red._contar_conexiones()}")
    
    # calcular estadísticas de conectividad
    conexiones_por_ciudad = {}
    for ciudad in red.grafo:
        conexiones_por_ciudad[ciudad] = len(red.grafo[ciudad])
    
    ciudad_mas_conectada = max(conexiones_por_ciudad, key=conexiones_por_ciudad.get)
    max_conexiones = conexiones_por_ciudad[ciudad_mas_conectada]
    
    print(f"🌟 Ciudad más conectada: {ciudad_mas_conectada} ({max_conexiones} conexiones)")
    
    # mostrar todas las ciudades y sus conexiones
    print(f"\n🔗 CONEXIONES POR CIUDAD:")
    for ciudad in sorted(red.ciudades):
        print(f"   {ciudad}: {conexiones_por_ciudad[ciudad]} conexiones")

def crear_imagen_grafo(red):
    """Opción del menú para crear imagen del grafo"""
    print("\n🎨 CREAR IMAGEN DEL GRAFO DE LA RED")
    print("="*50)
    
    print("📊 Opciones de visualización:")
    print("1. Grafo completo de la red")
    print("2. Grafo con ruta específica destacada")
    
    opcion = pedir_entrada("Selecciona opción (1-2): ")
    
    # Seleccionar criterio visual
    print("\n🎨 Criterio visual para colorear/dimensionar conexiones:")
    print("1. Latencia (ms) - Rojo: alta latencia")
    print("2. Costo (S/) - Naranja: alto costo") 
    print("3. Ancho de banda (Mbps) - Verde: mayor ancho de banda")
    
    criterio_visual_num = pedir_entrada("Selecciona criterio visual (1-3): ")
    criterios_visuales = {'1': 'latencia', '2': 'costo', '3': 'ancho_banda'}
    criterio_visual = criterios_visuales.get(criterio_visual_num, 'latencia')
    
    # Preguntar si mostrar etiquetas con valores
    mostrar_etiquetas = pedir_entrada("¿Mostrar valores numéricos en las conexiones? (s/n): ")
    mostrar_vals = mostrar_etiquetas and mostrar_etiquetas.lower() in ['s', 'si', 'sí', 'y', 'yes']
    
    if opcion == "1":
        nombre_archivo = pedir_entrada("Nombre del archivo (sin extensión): ") or f"red_isp_{criterio_visual}"
        nombre_archivo += ".png"
        red.crear_imagen_grafo(nombre_archivo=nombre_archivo, criterio_visual=criterio_visual, 
                              mostrar_etiquetas=mostrar_vals)
    
    elif opcion == "2":
        red.mostrar_ciudades()
        
        origen = pedir_entrada("📍 Ciudad de origen para la ruta: ")
        if not origen or origen not in red.ciudades:
            print("❌ Ciudad de origen no válida")
            return
        
        destino = pedir_entrada("🎯 Ciudad de destino para la ruta: ")
        if not destino or destino not in red.ciudades:
            print("❌ Ciudad de destino no válida")
            return
        
        # Seleccionar criterio para calcular la ruta
        print("\n🎯 Criterio para calcular la ruta óptima:")
        print("1. Latencia (menor tiempo)")
        print("2. Costo (menor precio)")
        print("3. Ancho de banda (mejor velocidad)")
        print("4. Compuesto (balance)")
        
        criterio_ruta_num = pedir_entrada("Selecciona criterio para ruta (1-4): ")
        criterios_ruta = {'1': 'latencia', '2': 'costo', '3': 'ancho_banda', '4': 'compuesto'}
        criterio_ruta = criterios_ruta.get(criterio_ruta_num, 'latencia')
        
        # Calcular ruta óptima
        distancias, anteriores = red.dijkstra_optimizado(origen, criterio_ruta)
        
        if distancias[destino] == float('inf'):
            print(f"❌ No hay conexión entre {origen} y {destino}")
            return
        
        ruta = red.reconstruir_ruta(anteriores, destino)
        nombre_archivo = pedir_entrada("Nombre del archivo (sin extensión): ") or f"ruta_{origen}_{destino}_{criterio_visual}"
        nombre_archivo += ".png"
        
        red.crear_imagen_grafo(ruta_destacada=ruta, nombre_archivo=nombre_archivo, 
                              criterio_visual=criterio_visual, mostrar_etiquetas=mostrar_vals)
        
        # Mostrar información de la ruta
        metricas = red.obtener_metricas_ruta(ruta)
        print(f"\n📊 INFORMACIÓN DE LA RUTA:")
        print(f"🗺️  Ruta: {' → '.join(ruta)}")
        print(f"⏱️  Latencia total: {metricas['latencia_total']:.1f} ms")
        print(f"💰 Costo total: S/ {metricas['costo_total']:.4f} por MB")
        print(f"📶 Ancho de banda limitante: {metricas['ancho_banda_limitante']:.0f} Mbps")
    
    else:
        print("❌ Opción no válida")

# Ejecutar el programa
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        print("Contacta al administrador del sistema")
    finally:
        # Al cerrar el simulador, lanzar la galería
        print("\n🌐 Abriendo galería de imágenes...")
        import subprocess
        subprocess.run(["python", "gallery.py"])
