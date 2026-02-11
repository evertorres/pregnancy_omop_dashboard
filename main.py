import flet as ft
from database.db_manager import DataManager
from ui.charts import create_sex_pie_chart, create_histogram_bar_chart, create_treemap_conditions

def main(page: ft.Page):
    page.title = "Dashboard OMOP CDM"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # 1. Instanciar gestor de datos
    data_manager = DataManager()
    
    # 2. Obtener datos (esto podría ser asíncrono en una app más compleja)
    df_sex = data_manager.get_sex()
    df_age = data_manager.get_age_at_first_seen()
    df_conditions = data_manager.get_conditions_per_person()

    #print(df_sex)

    # 3. Crear componentes de la UI
    header = ft.Row(
        [
            ft.Icon(ft.Icons.DASHBOARD, size=30),
            ft.Text("OMOP Dashboard", size=24, weight=ft.FontWeight.BOLD)
        ],
        alignment=ft.MainAxisAlignment.START
    )


    pie_chart_container = ft.Container(
    content=ft.Column(
        [
            # Header azul con título
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Sex Distribution",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.WHITE
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor=ft.Colors.BLUE_700,
                padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
                width=float("inf"),  # Forzar ancho infinito
            ),

            # Gráfico
            ft.Container(
                content=create_sex_pie_chart(df_sex),
                bgcolor=ft.Colors.WHITE,
                padding=5,
                expand=True,
                width=float("inf"),  # Forzar ancho infinito
            ),

            # Footer Container
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "10K Pregnant woman",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            "Gender distribution across the patient cohort.",
                            size=11,
                            color=ft.Colors.GREY_700
                        ),
                    ],
                    spacing=2,
                ),
                bgcolor=ft.Colors.GREY_200,
                padding=ft.Padding.only(left=15, right=15, top=10, bottom=10),
                width=float("inf"),  # Forzar ancho infinito
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # CLAVE: estirar horizontalmente
    ),
    shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=8,
        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        offset=ft.Offset(0, 2),
    ),
    border_radius=10,
    height=500,
    padding=0,
    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    histogram_container = ft.Container(
        content= ft.Column(
            [
                # Header azul con título
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "Year of Birth",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.WHITE
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=ft.Colors.BLUE_700,
                    padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
                    width=float("inf"),
                ),

                # Gráfico
                ft.Container(
                    content=create_histogram_bar_chart(df_age),
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.Padding.all(5),
                    expand=True,
                    width=float("inf"),
                ),

                # Footer Container
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "10K Pregnant woman",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800
                            ),
                            ft.Text(
                                "The age of the patient cohort at first seen.",
                                size=11,
                                color=ft.Colors.GREY_700
                            ),
                        ],
                        spacing=2,
                    ),
                    bgcolor=ft.Colors.GREY_200,
                    padding=ft.Padding.only(left=15, right=15, top=10, bottom=10),
                    width=float("inf"),
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    
            ),
            col={"sm": 12, "md": 12},
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            border_radius=10,
            height=450,
            padding=0,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            )
    
    treemap_container = ft.Container(
    content=ft.Column(
        [
            # Header azul con título
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Conditions",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.WHITE
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor=ft.Colors.BLUE_700,
                padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
            ),

            # Gráfico Treemap
            ft.Container(
                content=create_treemap_conditions(df_conditions),
                bgcolor=ft.Colors.WHITE,
                padding=ft.Padding.all(5),
                expand=True,
            ),

            # Footer gris con descripción
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "10K Pregnant woman",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            "Distribution of medical conditions across the patient cohort. Top 50 most common conditions.",
                            size=11,
                            color=ft.Colors.GREY_700
                        ),
                    ],
                    spacing=2,
                ),
                bgcolor=ft.Colors.GREY_200,
                padding=ft.Padding.only(left=15, right=15, top=10, bottom=10),
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    ),
    shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=8,
        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        offset=ft.Offset(0, 2),
    ),
    border_radius=10,
    height=500,
    padding=0,
    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    col={"sm": 12, "md": 12},
    )

    # 4. Layout Principal
    # Usamos ResponsiveRow para que se adapte a móviles y escritorio
    layout = ft.Column(
        [
            header,
            ft.Divider(),
            ft.ResponsiveRow(
                [
                    # Espacio vacío a la izquierda (50% en escritorio, oculto en móvil)
                    ft.Column(col={"sm": 0, "md": 6}),
                    # Gráfica a la derecha (50% en escritorio, 100% en móvil)
                    ft.Column([pie_chart_container], col={"sm": 12, "md": 6}), 
                ],
                columns=12,
            ),
            ft.ResponsiveRow(
                [
                    # Histograma ocupando el 100% del ancho
                    histogram_container, 
                    
                ],
                
            ),

            ft.ResponsiveRow(
                [
                    treemap_container,
                ],
            columns=12,
            ),

        ],
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO, 

    )

    page.add(layout)

if __name__ == "__main__":
    ft.run(main)
