import plotly.express as px
import plotly.graph_objects as go


def create_big_number(df):
    if df.empty:
        return None
    
    # Obtener el valor (asumiendo primera fila, primera columna)
    value = df.iloc[0, 0]

    # Crear indicador (Big Number)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        number = {'font': {'size': 80, 'color': '#1976D2'}}, # Azul corporativo
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    # Personalizar Layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=250, # Altura ajustada para centrado vertical
    )
    
    return fig
        

def create_sex_pie_chart(df):
    if df.empty:
        return None

    # Crear gráfico con Plotly Express
    fig = px.pie(
        df, 
        values='total',
        names='concept_name', 
        template="plotly_white" # Tema oscuro para coincidir con Flet por defecto
    )
    
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    # Personalizar un poco el layout de Plotly  
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="black"
    )

    # Retornar figura de Plotly
    return fig

def create_histogram_bar_chart(df):
    if df.empty:
        return None

    # Crear gráfica en Plotly
    fig = px.histogram(
        df, 
        x='age_in_years'
    )

    # Personalizar Layout histogram
    fig.update_layout(
        margin=dict(l=40, r=20, t=20, b=50),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="black",
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor='rgba(200,200,200,0.3)',
        ),
        yaxis=dict(
            title="Count",
            showgrid=True,
            gridcolor='rgba(200,200,200,0.3)',
        ),
    )
    
    # Color de las barras
    fig.update_traces(marker_color='rgb(108, 142, 168)')

    # Retornar figura de Plotly
    return fig

def create_treemap_conditions(df):
    if df.empty:
        return None

    # Crear treemap con Plotly Express
    fig = px.treemap(
        df,
        path=[px.Constant("All Conditions"), 'concept_name'],  # Jerarquía
        values='cnt',  # Tamaño de cada bloque
        color='cnt',  # Color basado en el conteo
        color_continuous_scale='Blues',  # Escala de colores
        hover_data={'cnt': ':,'},  # Formato del hover
    )

    # Personalizar layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="black",
    )

    # Personalizar las etiquetas del treemap
    fig.update_traces(
        textposition="middle center",
        textfont_size=12,
        marker=dict(
            line=dict(width=2, color='white')  # Borde blanco entre bloques
        )
    )

    # Retornar figura de Plotly
    return fig