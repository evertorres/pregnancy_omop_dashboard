import streamlit as st
from database.db_manager import DataManager
from ui.charts import create_pie_chart, create_histogram_bar_chart, create_treemap_conditions, create_big_number, create_line_chart_time, create_box_plot



# Configuración de la página (debe ser lo primero)
st.set_page_config(
    page_title="Dashboard OMOP CDM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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

def view_dashboard():
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
            fig=create_pie_chart(df_sex),
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

def view_data_density():
    st.title("📂 Data Density")
    st.markdown("---")

    with st.spinner('Cargando datos...'):
        df_data_density = data_manager.get_data_density_total_rows()
        df_data_avg_records = data_manager.get_avg_records_per_person_per_month()
        df_data_records_domain = data_manager.get_records_per_person_per_domain()

    # Fila 1: densidad de datos
    render_card(
        title="Data density - Records",
        fig= create_line_chart_time(df_data_density),
        footer_title="10K Pregnant woman",
        footer_desc="Number of records of each domain per month."
    )
    
    st.write("###") # Espaciador

    # Fila 2: Promedio de records por mes por persona
    render_card(
        title="Data density - Records",
        fig= create_line_chart_time(df_data_avg_records),
        footer_title="10K Pregnant woman",
        footer_desc="Number of average records per person of each domain per month."
    )

    st.write("###") # Espaciador

    # Fila 3: Boxplots de records por persona

    render_card(
        title="Data density - Concepts",
        fig= create_box_plot(df_data_records_domain),
        footer_title="10K Pregnant woman",
        footer_desc="Boxplot of records per person of each domain"
    )

def view_person():
    st.title("🧑‍🤝‍🧑 Person")
    st.markdown("---")

    with st.spinner('Cargando datos...'):
        df_data_age_years = data_manager.get_year_of_birth_patients()
        df_sex = data_manager.get_sex()
        df_race = data_manager.get_race()
        df_ethnicity = data_manager.get_ethnicity()

    
    # Fila 2: Histograma (Ancho completo)
    render_card(
        title="Year of Birth",
        fig=create_histogram_bar_chart(df_data_age_years),
        footer_title="10K Pregnant woman",
        footer_desc="The number of people in this cohort shown with respect to their year of birth."
    )


    st.write("###") # Espaciador

    col1, col2, col3 = st.columns([1, 1, 1]) # 50% y 50%
    
    with col1:
        render_card(
            title="Sex Distribution",
            fig=create_pie_chart(df_sex),
            footer_title="10K Pregnant woman",
            footer_desc="Gender distribution across the patient cohort."
        )
        
    with col2:
        render_card(
            title="Race Distribution",
            fig=create_pie_chart(df_race),
            footer_title="10K Pregnant woman",
            footer_desc="Race distribution across the patient cohort."
        )
    with col3:
        render_card(
            title="Ethnicity Distribution",
            fig=create_pie_chart(df_ethnicity),
            footer_title="10K Pregnant woman",
            footer_desc="Ethnicity distribution across the patient cohort."
        )

     

def view_placeholder(title):
    st.title(f"📂 {title}")
    st.markdown("---")
    st.info(f"La sección **{title}** está en construcción. Aquí se cargarán las gráficas correspondientes.")

def main():
    st.sidebar.title("Navegación")
    
    page = st.sidebar.radio(
        "Seleccione una vista:",
        [
            "Dashboard",
            "Data density",
            "Person",
            "Visit",
            "Condition Ocurrence",
            "Procedure",
            "Drug Exposure",
            "Measurement",
            "Observation",
            "Death"
        ]
    )

    if page == "Dashboard":
        view_dashboard()
    elif page == "Data density":
        view_data_density()
    elif page == "Person":
        view_person()
    else:
        view_placeholder(page)

if __name__ == "__main__":
    # 1. Instanciar gestor de datos
    data_manager = DataManager()
    main()