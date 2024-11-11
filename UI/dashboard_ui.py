import flet as ft
from BL.event_management import add_event, delete_event, get_all_events, update_event




# Simple in-memory storage for demonstration purposes
data_store = {
    "budget_data": {}
}




def open_welcome_screen(page: ft.Page):
    page.controls.clear()
    page.title = "Welcome to EventSynch!"




    def open_login_form(page: ft.Page):
        # Clear previous state to ensure consistency
        page.controls.clear()
        page.title = "Login to EventSynch"




        # Reset layout for the login form
        username_input = ft.TextField(label="Username")
        password_input = ft.TextField(label="Password", password=True)




        def login(e):
            # Example login logic (replace with actual authentication if needed)
            if username_input.value:
                open_dashboard(page, username_input.value)
            else:
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Please enter a username."),
                    actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page))]
                )
                page.dialog.open = True
                page.update()




        login_content = ft.Column(
            [
                ft.Text("Login to EventSynch", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                username_input,
                password_input,
                ft.FilledButton("Login", on_click=login)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
       
        page.add(login_content)
        page.dialog = None  # Clear any existing dialogs
        page.update()




    def close_dialog(page):
        if page.dialog:
            page.dialog.open = False
            page.update()




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
            spacing=20
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(20),
        expand=True
    )
    page.add(welcome_content)
    page.update()




def open_dashboard(page: ft.Page, username):
    page.controls.clear()
    page.title = f"EventSynch Dashboard - Welcome {username}"




    def logout(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Logout Confirmation"),
            content=ft.Text("Are you sure you want to logout?"),
            actions=[
                ft.TextButton("Yes", on_click=lambda e: perform_logout(page)),
                ft.TextButton("No", on_click=lambda e: close_dialog(page))
            ],
            open=True
        )
        page.update()




    def perform_logout(page):
        page.dialog.open = False
        page.update()
        open_welcome_screen(page)  # Reset and go back to the welcome screen




    def close_dialog(page):
        if page.dialog:
            page.dialog.open = False
            page.update()




    dashboard_content = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Welcome to EventSynch, {username}!",
                            size=24,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(text="Add Event", on_click=lambda e: open_add_event(page, username)),
                                ft.FilledButton(text="View All Events", on_click=lambda e: open_event_list(page, username))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20),
                expand=True
            ),
            ft.Container(
                content=ft.FilledButton("Logout", on_click=logout),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=30),
                padding=ft.padding.only(bottom=10)
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )




    page.add(dashboard_content)
    page.update()




def open_event_list(page, username):
    page.controls.clear()
    page.title = "All Events"




    events = get_all_events(username)
   
    if not events:
        event_list_content = ft.Text("No events found.", text_align=ft.TextAlign.CENTER)
    else:
        event_list_content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Event: {event['name']}\nDate: {event['date']}\nLocation: {event['location']}\nDescription: {event['description']}",
                                size=16,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Row(
                                controls=[
                                    ft.FilledButton(
                                        text="Edit",
                                        on_click=lambda e, event=event: open_edit_event(page, username, event)
                                    ),
                                    ft.FilledButton(
                                        text="Delete",
                                        on_click=lambda e, event=event: delete_event_confirmation(page, username, event)
                                    ),
                                    ft.FilledButton(
                                        text="Financial Budgeting",
                                        on_click=lambda e, event=event: open_financial_budgeting_page(page, username, event)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10),
                    margin=ft.margin.symmetric(vertical=5),
                    border=ft.border.all(1, ft.colors.BLACK12)
                )
                for event in events
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START
        )




    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Event List", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10)
                ),
                ft.Container(
                    content=event_list_content,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20),
                    expand=True
                ),
                ft.Container(
                    content=ft.FilledButton("Back", on_click=lambda e: open_dashboard(page, username)),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10)
                )
            ],
            expand=True
        )
    )
    page.update()




def open_add_event(page: ft.Page, username):
    event_name = ft.TextField(label="Event Name", width=300)
    event_date = ft.TextField(label="Event Date (MM-DD-YYYY)", width=300)
    event_location = ft.TextField(label="Location", width=300)
    event_description = ft.TextField(label="Description", width=300)




    def validate_date_format(date_str):
        import re
        pattern = r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\d{4}$"
        return re.match(pattern, date_str)




    def save_event(e):
        if not validate_date_format(event_date.value):
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Invalid date format. Please use MM-DD-YYYY."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page))],
                open=True
            )
            page.update()
            return




        add_event(
            event_name.value,
            event_date.value,
            event_location.value,
            event_description.value,
            username
        )
        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Event Added"),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog_and_return(page, username))],
            open=True
        )
        page.update()




    def close_dialog(page):
        if page.dialog:
            page.dialog.open = False
            page.update()




    def close_dialog_and_return(page, username):
        close_dialog(page)
        open_dashboard(page, username)




    add_event_content = ft.Column(
        [
            event_name,
            event_date,
            event_location,
            event_description,
            ft.Row(
                [
                    ft.FilledButton("Save", on_click=save_event),
                    ft.FilledButton("Cancel", on_click=lambda e: close_dialog_and_return(page, username))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )




    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add Event"),
        content=add_event_content,
        open=True
    )
    page.update()




def open_edit_event(page: ft.Page, username, event):
    event_name = ft.TextField(label="Event Name", value=event["name"], width=300)
    event_date = ft.TextField(label="Event Date (MM-DD-YYYY)", value=event["date"], width=300)
    event_location = ft.TextField(label="Location", value=event["location"], width=300)
    event_description = ft.TextField(label="Description", value=event["description"], width=300)




    def save_edited_event(e):
        updated_event = {
            "id": event["id"],
            "name": event_name.value,
            "date": event_date.value,
            "location": event_location.value,
            "description": event_description.value
        }
        update_event(updated_event)
        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Event Updated Successfully"),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog_and_return(page, username))]
        )
        page.dialog.open = True
        page.update()




    def close_dialog(page):
        if page.dialog:
            page.dialog.open = False
            page.update()




    def close_dialog_and_return(page, username):
        close_dialog(page)
        open_event_list(page, username)




    edit_event_content = ft.Column(
        [
            event_name,
            event_date,
            event_location,
            event_description,
            ft.Row(
                [
                    ft.FilledButton("Save", on_click=save_edited_event),
                    ft.FilledButton("Cancel", on_click=lambda e: close_dialog_and_return(page, username))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )




    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Event"),
        content=edit_event_content,
        open=True
    )
    page.update()




def delete_event_confirmation(page: ft.Page, username, event):
    def confirm_delete(response):
        if response == "yes":
            delete_event(event["id"])
            page.dialog.open = False
            page.update()
            open_event_list(page, username)
        else:
            page.dialog.open = False
            page.update()




    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Delete Confirmation"),
        content=ft.Text(f"Are you sure you want to delete the event '{event['name']}'?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: confirm_delete("yes")),
            ft.TextButton("No", on_click=lambda e: confirm_delete("no"))
        ],
        open=True
    )
    page.update()




def open_financial_budgeting_page(page: ft.Page, username, event):
    page.controls.clear()
    page.title = f"Financial Budgeting for {event['name']}"




    budget_input = ft.TextField(label="Total Budget (PHP)", width=300)
    expense_name = ft.TextField(label="Expense Name", width=200)
    expense_amount = ft.TextField(label="Expense Amount (PHP)", width=150)




    # Load existing data if available
    event_id = event["id"]
    expenses = data_store["budget_data"].get(event_id, {"budget": "", "expenses": []})["expenses"]
    budget_input.value = data_store["budget_data"].get(event_id, {"budget": ""})["budget"]




    def format_currency(amount):
        return f"₱{amount:,.2f}"




    def add_expense(e):
        if expense_name.value and expense_amount.value.replace('.', '', 1).isdigit():
            expenses.append({
                "name": expense_name.value,
                "amount": float(expense_amount.value)
            })
            refresh_expense_table()
            expense_name.value = ""
            expense_amount.value = ""
            page.update()




    def refresh_expense_table():
        total_expenses = sum(exp["amount"] for exp in expenses)
        remaining_budget = float(budget_input.value) - total_expenses if budget_input.value.replace('.', '', 1).isdigit() else 0




        expense_table.controls.clear()
        for exp in expenses:
            expense_table.controls.append(ft.Row(
                [
                    ft.Text(exp["name"], width=200),
                    ft.Text(format_currency(exp["amount"]), width=150),
                    ft.FilledButton("Edit", on_click=lambda e, exp=exp: edit_expense(exp)),
                    ft.FilledButton("Delete", on_click=lambda e, exp=exp: delete_expense(exp))
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ))
        total_text.value = f"Total Expenses: {format_currency(total_expenses)}"
        remaining_text.value = f"Remaining Budget: {format_currency(remaining_budget)}"
        page.update()




    def edit_expense(exp):
        expense_name.value = exp["name"]
        expense_amount.value = str(exp["amount"])
        expenses.remove(exp)
        refresh_expense_table()
        page.update()




    def delete_expense(exp):
        expenses.remove(exp)
        refresh_expense_table()
        page.update()




    def save_budgeting(e):
        # Save data to the in-memory data store
        data_store["budget_data"][event_id] = {
            "budget": budget_input.value,
            "expenses": expenses
        }
        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Financial details saved successfully."),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page))],
            open=True
        )
        page.update()




    def close_dialog(page):
        if page.dialog:
            page.dialog.open = False
            page.update()




    expense_table = ft.Column()
    total_text = ft.Text("Total Expenses: ₱0.00")
    remaining_text = ft.Text("Remaining Budget: ₱0.00")




    refresh_expense_table()  # Initialize the table with current data




    budgeting_content = ft.Column(
        [
            ft.Text(f"Financial Budgeting for {event['name']}", size=20, weight="bold"),
            budget_input,
            ft.Row(
                [expense_name, expense_amount, ft.FilledButton("Add Expense", on_click=add_expense)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            expense_table,
            total_text,
            remaining_text,
            ft.Row(
                [
                    ft.FilledButton("Save", on_click=save_budgeting),
                    ft.FilledButton("Back", on_click=lambda e: open_event_list(page, username))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )




    page.add(budgeting_content)
    page.update()

