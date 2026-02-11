import plotly.express as px
import flet as ft
import flet_charts as fch

def create_sex_pie_chart(df):
    if df.empty:
        return ft.Text("No hay datos disponibles")

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

    # Retornar el control de Flet
    return fch.PlotlyChart(figure=fig, expand=True)

def create_histogram_bar_chart(df):
    if df.empty:
        return ft.Text("No hay datos disponibles")

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

    # Retornar PlotlyChart con las propiedades correctas
    return fch.PlotlyChart(
        figure=fig,
        expand=True,
    )

def create_treemap_conditions(df):
    if df.empty:
        return ft.Text("No hay datos disponibles")

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

    # Retornar PlotlyChart
    return fch.PlotlyChart(
        figure=fig,
        expand=True,
    )