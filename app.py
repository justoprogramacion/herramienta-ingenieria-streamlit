# 1. Importar los módulos necesarios
import streamlit as st
import pandas as pd
import os # Este módulo nos ayudará a verificar si un archivo existe

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Herramientas de Ingeniería",
    page_icon="🛠️",
    layout="wide"
)


# --- FUNCIONES PARA CADA ESPECIALIDAD ---

def calcular_concreto(largo, ancho, espesor):
    """Calcula el volumen de concreto en metros cúbicos."""
    if largo > 0 and ancho > 0 and espesor > 0:
        volumen = largo * ancho * espesor
        return round(volumen, 2)
    return None

def calcular_riego(area, lamina_riego):
    """Calcula el volumen de agua necesario para riego en metros cúbicos."""
    if area > 0 and lamina_riego > 0:
        # Convertir lámina de mm a metros (1 mm = 0.001 m)
        volumen_agua = area * (lamina_riego / 1000)
        return round(volumen_agua, 2)
    return None

# --- ESTRUCTURA PRINCIPAL DE LA APLICACIÓN ---

# Título principal de la aplicación
st.title('🛠️ Herramienta de Apoyo para Ingeniería V1.0')
st.write("Una aplicación para asistir en tareas de Ingeniería Agrícola, Civil y Agroindustrial.")

# --- BARRA LATERAL (SIDEBAR) PARA NAVEGACIÓN ---
st.sidebar.header('Seleccione su Especialidad')
opcion = st.sidebar.radio(
    'Menú de Navegación',
    ('Página Principal', 'Ingeniería Civil', 'Ingeniería Agrícola', 'Ingeniería Agroindustrial')
)

# --- LÓGICA PARA MOSTRAR LA PÁGINA SELECCIONADA ---

if opcion == 'Página Principal':
    st.header('Bienvenido/a a la Caja de Herramientas Digital')
    st.image('https://images.unsplash.com/photo-1581092921462-692004651e36?q=80&w=2070&auto=format&fit=crop',
             caption='Ingeniería y Tecnología al servicio del desarrollo.')
    st.markdown("""
    Esta aplicación ha sido desarrollada para apoyar a los estudiantes de **Programación de Computadoras con Python**.
    
    **Instrucciones:**
    1.  Utiliza el menú en la barra lateral izquierda para navegar entre las diferentes especialidades.
    2.  Ingresa los datos solicitados en cada sección.
    3.  Observa los resultados de los cálculos o el registro de la información.
    
    ¡Explora y aprende!
    """)

# --- MÓDULO DE INGENIERÍA CIVIL ---
elif opcion == 'Ingeniería Civil':
    st.header('Calculadora de Volumen de Concreto')
    st.subheader('Para una losa rectangular')

    col1, col2, col3 = st.columns(3)
    with col1:
        largo = st.number_input('Largo de la losa (metros)', min_value=0.1, value=5.0, step=0.1)
    with col2:
        ancho = st.number_input('Ancho de la losa (metros)', min_value=0.1, value=4.0, step=0.1)
    with col3:
        espesor = st.number_input('Espesor de la losa (metros)', min_value=0.05, value=0.15, step=0.01)

    if st.button('Calcular Volumen'):
        volumen = calcular_concreto(largo, ancho, espesor)
        if volumen:
            st.success(f'El volumen de concreto requerido es: **{volumen} m³**')
        else:
            st.error('Por favor, ingrese valores válidos y mayores a cero.')

# --- MÓDULO DE INGENIERÍA AGRÍCOLA ---
elif opcion == 'Ingeniería Agrícola':
    st.header('Estimador de Necesidad de Riego')
    st.subheader('Cálculo de volumen de agua')

    area_cultivo = st.number_input('Área del cultivo (metros cuadrados)', min_value=1.0, value=1000.0, step=10.0)
    lamina = st.number_input('Lámina de riego a aplicar (milímetros)', min_value=1.0, value=10.0, step=0.5)

    if st.button('Calcular Agua Requerida'):
        volumen_agua = calcular_riego(area_cultivo, lamina)
        if volumen_agua:
            st.success(f'El volumen de agua requerido es: **{volumen_agua} m³**')
        else:
            st.error('Por favor, ingrese valores válidos y mayores a cero.')

# --- MÓDULO DE INGENIERÍA AGROINDUSTRIAL ---
elif opcion == 'Ingeniería Agroindustrial':
    st.header('Registro de Control de Calidad (pH)')
    st.info("Esta sección guarda los datos en un archivo `control_calidad.csv`.")

    # Usamos un formulario para agrupar los inputs y tener un solo botón de envío
    with st.form(key='quality_form'):
        id_lote = st.text_input('ID del Lote de Producción', 'LOTE-001')
        valor_ph = st.number_input('Valor de pH medido', min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        submit_button = st.form_submit_button(label='Guardar Registro')

    if submit_button:
        # Crear un DataFrame con el nuevo dato
        nuevo_registro = pd.DataFrame({'id_lote': [id_lote], 'ph': [valor_ph]})
        
        # Nombre del archivo donde guardaremos los datos
        archivo_csv = 'control_calidad.csv'
        
        # Lógica para guardar el archivo
        if os.path.exists(archivo_csv):
            # Si el archivo ya existe, leemos los datos y añadimos el nuevo registro
            df_existente = pd.read_csv(archivo_csv)
            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        else:
            # Si el archivo no existe, el nuevo registro es nuestro DataFrame
            df_actualizado = nuevo_registro
        
        # Guardar el DataFrame actualizado en el archivo CSV
        df_actualizado.to_csv(archivo_csv, index=False)
        st.success(f"Registro para el lote **{id_lote}** guardado con éxito.")

    # Mostrar la tabla con todos los registros guardados
    st.subheader("Historial de Registros")
    if os.path.exists('control_calidad.csv'):
        df_registros = pd.read_csv('control_calidad.csv')
        st.dataframe(df_registros)
    else:
        st.warning("Aún no se ha guardado ningún registro.")