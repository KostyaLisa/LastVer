import os
import flet as ft
from utils.Database import Database  # Database class for note handling
from utils.Validation import Validation  # Validation helper
from utils.style import *  # Style configuration


class PostPage:

    # Load environment variables for bot and channel link
    token_bot = os.getenv('TOKEN_BOT')
    channel_link = os.getenv('CHANNEL_LINK')
    validation = Validation()
    db = Database()  # Instance of Database class

    # Main view method
    def view(self, page: ft.Page):
        # Page configurations
        page.title = "Add post"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 900
        page.window.min_height = 400

        # Define fonts for the page
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

        # Style for sidebar menu buttons
        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.colors.WHITE,
                                           ft.ControlState.DEFAULT: menuColorFont},
                                    icon_size=14,
                                    overlay_color=hoverBqColor,
                                    shadow_color=hoverBqColor)

        # Sidebar with navigation options
        logotype = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(src='images/logo.png', width=45, height=32, fit=ft.ImageFit.FILL),
                    ft.Text('First Program', expand=True, color=defaultFontColor, font_family='muller-extrabold', size=16)
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text('Menu', color=menuColorFont, size=12),
                    ft.TextButton('Header', icon='space_dashboard_rounded', style=style_menu,
                                  on_click=lambda e: page.go('/dashboard')),
                    ft.TextButton('Send', icon='post_add', style=style_menu,
                                  on_click=lambda e: page.go('/posting')),
                    ft.TextButton('Test Button', icon='verified_user', style=style_menu),
                ]
            )
        )

        # Header
        header = ft.Container(content=ft.Row(controls=[
            ft.Text('Control Panel', color=defaultFontColor, size=20, font_family='muller-extrabold'),
            ft.Row(controls=[
                ft.CircleAvatar(foreground_image_src='images/avatar.png', content=ft.Text('Avatar')),
                ft.IconButton(icon=ft.icons.NOTIFICATIONS_ROUNDED, icon_size=20, hover_color=hoverBqColor,
                              icon_color=defaultFontColor)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        # Note input fields
        self.note_input = ft.TextField(
            hint_text="Write a new note...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True,
            bgcolor=secondaryBqColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor
        )

        self.priority_input = ft.Dropdown(
            options=[
                ft.dropdown.Option("1 - Low"),
                ft.dropdown.Option("2 - Medium"),
                ft.dropdown.Option("3 - High")
            ],
            hint_text="Select priority",
            bgcolor=secondaryBqColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor
        )

        # Search field and sorting dropdown
        search_field = ft.TextField(
            hint_text="Search notes...",
            bgcolor=secondaryBqColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
            on_change=self.update_notes_view
        )

        sort_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option("Priority"), ft.dropdown.Option("Date")],
            bgcolor=secondaryBqColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
            on_change=self.update_notes_view
        )

        # Save button to store notes
        save_button = ft.ElevatedButton(
            text="Save Note",
            on_click=self.save_note_handler
        )

        # Notes list section
        self.notes_list = ft.Column()
        notes_section = ft.Container(
            content=ft.Column([
                ft.Row(controls=[search_field, sort_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.notes_list
            ]),
            padding=ft.padding.all(10),
            expand=True
        )

        # New note section with input fields and save button
        new_note_section = ft.Container(
            content=ft.Column([
                ft.Row([self.note_input, self.priority_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                save_button
            ]),
            padding=ft.padding.all(10),
            expand=True
        )

        # Page layout with sidebar and content
        view = ft.View(
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Sidebar
                        ft.Container(
                            expand=1,
                            content=ft.Column(controls=[logotype, sidebar_menu]),
                            bgcolor=secondaryBqColor,
                        ),
                        # Main content area
                        ft.Container(
                            image_src="images/bg_login1.webp",
                            image_fit=ft.ImageFit.COVER,
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column([header, new_note_section, notes_section]),
                            bgcolor=secondaryBqColor
                        )
                    ]
                )
            ], bgcolor=defaultBqColor, padding=0
        )

        # Load notes on page load
        page.on_load = lambda e: self.load_notes()
        return view

    # Save note and reset fields
    def save_note_handler(self, e):
        note_text = self.note_input.value
        priority_text = self.priority_input.value

        if note_text and priority_text:
            priority = int(priority_text.split(" - ")[0])  # Extract priority as an integer
            user_id = 1  # Use a user ID placeholder; replace in production

            # Save note to database
            self.db.create_note(user_id, note_text, priority)

            # Clear input fields after saving
            self.note_input.value = ""
            self.priority_input.value = None

            # Reload notes view
            self.load_notes()
            self.note_input.update()
            self.priority_input.update()
            self.notes_list.update()

    # Load and display notes, with optional search and sorting
    def load_notes(self, search_query="", sort_by="priority"):
        self.notes_list.controls.clear()  # Clear the list before loading

        # Fetch notes from the database based on search and sorting
        notes = self.db.get_user_notes_sorted(search_query, sort_by)

        # Create a display for each note
        for note in notes:
            note_control = ft.Row(
                controls=[
                    ft.Text(note[2]),  # Note text
                    ft.Text(f"Priority: {note[3]}"),  # Priority
                    ft.IconButton(icon=ft.icons.DELETE,
                                  on_click=lambda e, note_id=note[0]: self.delete_note_handler(note_id))  # Delete button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.notes_list.controls.append(note_control)

        self.notes_list.update()

    # Update notes view on search or sort change
    def update_notes_view(self, e):
        search_query = e.control.parent.controls[0].value  # Get search input
        sort_by = e.control.parent.controls[1].value  # Get sorting preference
        self.load_notes(search_query, sort_by)

    # Delete a note and refresh the list
    def delete_note_handler(self, note_id):
        self.db.delete_note(note_id)  # Delete note from database
        self.load_notes()  # Reload notes after deletion
