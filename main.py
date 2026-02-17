import streamlit as st
from database.db_manager import DataManager
from ui.charts import create_sex_pie_chart, create_histogram_bar_chart, create_treemap_conditions, create_big_number


# Configuración de la página (debe ser lo primero)
st.set_page_config(
    page_title="Dashboard OMOP CDM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar estilos CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('ui/style.css')

# Función auxiliar para renderizar tarjetas con estilo
def render_card(title, fig, footer_title, footer_desc):
    # 1. Header HTML
    st.markdown(f'<div class="card-header">{title}</div>', unsafe_allow_html=True)
    
    # 2. Gráfico Plotly
    if fig:
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    else:
        st.warning("No hay datos disponibles")
        
    # 3. Footer HTML
    st.markdown(f'''
        <div class="card-footer">
            <strong>{footer_title}</strong>
            {footer_desc}
        </div>
    ''', unsafe_allow_html=True)

def main():
    # 1. Instanciar gestor de datos
    data_manager = DataManager()
    
    # 2. Obtener datos (ahora con caché)
    with st.spinner('Cargando datos...'):
        df_patients = data_manager.get_count_patients()
        df_sex = data_manager.get_sex()
        df_age = data_manager.get_age_at_first_seen()
        df_conditions = data_manager.get_conditions_per_person()

    # 3. Header Principal
    st.title("📊 OMOP Dashboard")
    st.markdown("---")

    # 4. Layout Principal
    
    # Fila 1: Espacio vacío (izquierda) y Gráfico de Sexo (derecha)
    # En Streamlit usamos columnas. 
    col1, col2 = st.columns([1, 1]) # 50% y 50%
    
    with col1:
        render_card(
            title="Total Patiets",
            fig=create_big_number(df_patients),
            footer_title="10K Pregnant woman",
            footer_desc="Number of patients in the cohort"
        )
        
    with col2:
        render_card(
            title="Sex Distribution",
            fig=create_sex_pie_chart(df_sex),
            footer_title="10K Pregnant woman",
            footer_desc="Gender distribution across the patient cohort."
        )

    st.write("###") # Espaciador

    # Fila 2: Histograma (Ancho completo)
    render_card(
        title="Year of Birth",
        fig=create_histogram_bar_chart(df_age),
        footer_title="10K Pregnant woman",
        footer_desc="The age of the patient cohort at first seen."
    )

    st.write("###") # Espaciador

    # Fila 3: Treemap (Ancho completo)
    render_card(
        title="Conditions",
        fig=create_treemap_conditions(df_conditions),
        footer_title="10K Pregnant woman",
        footer_desc="Distribution of medical conditions across the patient cohort. Top 50 most common conditions."
    )

if __name__ == "__main__":
    main()