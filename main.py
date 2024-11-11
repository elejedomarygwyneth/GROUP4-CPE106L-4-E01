import flet as ft
from UI.login_ui import open_login_form


def open_welcome_screen(page: ft.Page):
    page.controls.clear()  # Clear previous content
    page.title = "Welcome to EventSynch!"


    def get_started(e):
        open_login_form(page)


    welcome_content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to EventSynch!", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.FilledButton("Get Started", on_click=get_started)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20  # Adds spacing between elements
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(20),
        expand=True  # Ensures full height and width expansion for centering
    )
    page.add(welcome_content)
    page.update()


def main(page: ft.Page):
    open_welcome_screen(page)


ft.app(target=main)
