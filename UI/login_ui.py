import flet as ft
from UI.dashboard_ui import open_dashboard
from PAL.login_pal import login_user


def open_login_form(page: ft.Page):
    page.controls.clear()  # Clear previous content
    page.title = "EventSynch - Login"


    def login(e):
        username = username_field.value
        password = password_field.value
        if login_user(username, password):
            open_dashboard(page, username)
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Invalid credentials. Please try again."))
            page.dialog.open = True
            page.update()


    username_field = ft.TextField(label="Username", autofocus=True, width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)


    login_content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login to EventSynch", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                username_field,
                password_field,
                ft.FilledButton("Login", on_click=login)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20  # Adds spacing between elements
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(20),
        expand=True  # Ensures full height and width expansion for centering
    )
    page.add(login_content)
    page.update()
