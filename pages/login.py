import flet as ft  # Importing Flet for UI components

from utils.style import *  # Importing styling variables
from utils.Database import Database  # Importing the Database class for user management
from utils.function import hesh_password  # Importing function for password hashing


class LoginPage:
    # Initialize UI components of the login page
    def __init__(self):
        # Email input field wrapped in a container
        self.email_input = ft.Container(
            content=ft.TextField(
                label="Email",
                bgcolor=secondaryBqColor,  # Background color for the text field
                border=ft.InputBorder.NONE,
                filled=True,  # Filled style for the text field
                color=secondaryFontColor,  # Font color for input text
            ),
        )

        # Password input field with hidden text for security
        self.password_input = ft.Container(
            content=ft.TextField(
                label="Enter Password",
                password=True,  # Enable password masking
                can_reveal_password=True,  # Option to reveal password
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,  # Rounded corners for the container
        )

        # Snackbar component to show error messages
        self.message_error = ft.SnackBar(
            content=ft.Text("Error", color=inputBqErrorColor),
        )

    # Function to define and display the page layout
    def view(self, page: ft.Page):
        # Basic page setup
        page.title = "Page Authorization"
        page.window.width = defaultWidthWindows  # Setting window dimensions
        page.window.height = defaultHeightWindows
        page.window.min_width = 800
        page.window.min_height = 400

        # Loading custom fonts for the page
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

        # Link to navigate to the dashboard page
        dashboard_link = ft.Container(
            content=ft.Text("dashboard", color=defaultFontColor),
            on_click=lambda e: page.go('/dashboard'),  # Redirect to dashboard on click
        )

        # Link to navigate to the signup page
        signup_link = ft.Container(
            content=ft.Text("Create Account", color=defaultFontColor),
            on_click=lambda e: page.go('/signup'),  # Redirect to signup page on click
        )

        # Authorization function to handle login
        def authorization(e):
            db = Database()  # Creating a database instance
            email = self.email_input.content.value  # Retrieving entered email
            password = hesh_password(self.password_input.content.value)  # Hashing entered password

            # Check login credentials with the database
            if db.login_user(email, password):
                page.session.set("auth_user", True)  # Setting session on successful login
                page.go('/dashboard')  # Redirecting to the dashboard
            else:
                self.message_error.open = True  # Show error message if login fails
                page.snack_bar = self.message_error  # Attach the snackbar to the page
                page.update()  # Update the page to reflect changes

        # Return layout for the page view
        return ft.View(
            '/',  # Base path for this view
            controls=[
                # Main row container with left and right panels
                ft.Row(
                    expand=True,
                    controls=[
                        # Left Panel: contains login form and links
                        ft.Container(
                            expand=2,  # Takes up 2/5 of the width
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Welcome text
                                    ft.Text(
                                        "Welcome",
                                        color=defaultFontColor,
                                        size=25,
                                        font_family="prisma-pro-shadow",
                                    ),

                                    # Error message snackbar
                                    self.message_error,

                                    # Email input field
                                    self.email_input,

                                    # Password input field
                                    self.password_input,

                                    # Authorization button
                                    ft.Container(
                                        content=ft.Text("Authorization", color=defaultFontColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBqColor,  # Background color for the button
                                        on_click=lambda e: authorization(e),  # Call authorization function on click
                                    ),

                                    # Signup and dashboard navigation links
                                    signup_link,
                                    dashboard_link,
                                ],
                            ),
                        ),
                        # Right Panel: background image and icon
                        ft.Container(
                            expand=3,  # Takes up 3/5 of the width
                            image_src="images/bg_login.jpg",  # Background image
                            image_fit=ft.ImageFit.COVER,  # Fit image to cover container
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Lock icon for visual effect
                                    ft.Icon(
                                        name=ft.icons.SCREEN_LOCK_PORTRAIT_ROUNDED,
                                        color=hoverBqColor,
                                        size=140,
                                    ),
                                    # Authorization label below the icon
                                    ft.Text(
                                        "Authorization",
                                        color=hoverBqColor,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="muller-extrabold",
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBqColor,  # Background color for the entire page
            padding=0,  # No padding for the view container
        )
