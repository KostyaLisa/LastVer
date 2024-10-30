import flet as ft  # Importing Flet for building the UI
import time  # Importing time for delay in redirection
from pages.login import LoginPage  # Importing login page for navigation
from utils.Database import Database  # Importing database operations
from utils.style import *  # Importing style variables for consistency
from utils.Validation import Validation  # Importing validation utilities
from utils.function import hesh_password  # Importing password hashing function


class SignupPage:
    # Initialize the validator for input validation checks
    validators = Validation()

    def __init__(self):
        # Define the email input field with error-clearing on change
        self.email_input = ft.Container(
            content=ft.TextField(
                label="Email",
                bgcolor=secondaryBqColor,  # Set background color
                border=ft.InputBorder.NONE,  # No border style
                filled=True,
                color=secondaryFontColor,  # Font color for input text
                on_change=self.clear_error  # Clear error when field changes
            ),
            border_radius=15,  # Rounded corners for container
        )

        # Define the login input field with error-clearing on change
        self.login_input = ft.Container(
            content=ft.TextField(
                label="Login",
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error
            ),
            border_radius=15,
        )

        # Define the password input field with hidden text for security
        self.password_input = ft.Container(
            content=ft.TextField(
                label="Password",
                password=True,  # Enable password masking
                can_reveal_password=True,  # Allow user to reveal password
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error
            ),
            border_radius=15,
        )

        # Define the confirm password field to check matching passwords
        self.confirm_password_input = ft.Container(
            content=ft.TextField(
                label="Confirm Password",
                password=True,
                can_reveal_password=True,
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error
            ),
            border_radius=15,
        )

        # Text element for displaying error messages to the user
        self.error_field = ft.Text('', color='red')

    # Clear error message when input changes
    def clear_error(self, e):
        self.error_field.value = ""
        self.error_field.update()

    # Define the layout of the signup page
    def view(self, page: ft.Page):
        # Setup basic page properties
        page.title = "Page Registration"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 800
        page.window.min_height = 400

        # Link to redirect to the login page
        login_link = ft.Container(
            content=ft.Text("Login", color=defaultFontColor),
            on_click=lambda e: page.go('/'),  # Redirect to login page
        )

        # Load custom fonts for the page
        page.fonts = {"muller-extrabold": "fonts/muller-extrabold.ttf"}

        # Function to handle user signup
        def signup(e):
            # Retrieve values from input fields
            email_value = self.email_input.content.value
            login_value = self.login_input.content.value
            password_value = self.password_input.content.value
            confirm_password_value = self.confirm_password_input.content.value

            # Validate fields
            if email_value and login_value and password_value and confirm_password_value:
                db = Database()  # Initialize database connection

                # Check email format
                if not self.validators.is_valid_email(email_value):
                    self.email_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = 'Invalid email format'
                    self.error_field.size = 12
                    self.email_input.update()
                    self.error_field.update()

                # Check if email is already in use
                elif db.check_email(email_value):
                    self.email_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "This email is already taken"
                    self.error_field.size = 12
                    self.email_input.update()
                    self.error_field.update()

                # Check if login is already taken
                elif db.check_login(login_value):
                    self.login_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "This login is already taken"
                    self.error_field.size = 12
                    self.login_input.update()
                    self.error_field.update()

                # Validate password strength
                elif not self.validators.is_valid_password(password_value):
                    self.password_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "Invalid password"
                    self.error_field.size = 12
                    self.password_input.update()
                    self.error_field.update()

                # Check if passwords match
                elif password_value != confirm_password_value:
                    self.error_field.value = "Passwords do not match"
                    self.error_field.size = 12
                    self.error_field.update()

                # If all validations pass, register the user
                else:
                    db.register_user(email_value, login_value, hesh_password(password_value))
                    self.error_field.value = "Registration successful!"
                    self.error_field.size = 12
                    self.error_field.color = ft.colors.GREEN
                    self.error_field.update()
                    time.sleep(2)  # Delay before redirecting
                    page.go("/")  # Redirect to login page

            else:
                # If any field is empty, show error
                self.error_field.value = "All fields are required!"
                self.error_field.size = 12
                self.error_field.update()

        # Define the page layout structure and controls
        return ft.View(
            "/",
            controls=[
                # Main row containing left and right panels
                ft.Row(
                    expand=True,
                    controls=[
                        # Left panel with input fields and register button
                        ft.Container(
                            expand=2,
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Title for registration
                                    ft.Text(
                                        "Welcome to Registration",
                                        color=defaultFontColor,
                                        size=25,
                                        font_family="prisma-pro-shadow",
                                    ),
                                    # Error message display
                                    self.error_field,
                                    # Input fields
                                    self.email_input,
                                    self.login_input,
                                    self.password_input,
                                    self.confirm_password_input,
                                    # Register button
                                    ft.Container(
                                        content=ft.Text("Register", color=defaultFontColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBqColor,  # Button background color
                                        on_click=lambda e: signup(e),  # Trigger signup on click
                                    ),
                                    login_link  # Link to login page
                                ]
                            )
                        ),
                        # Right panel with background image and icon
                        ft.Container(
                            expand=3,
                            image_src="images/bg_login.jpg",  # Background image source
                            image_fit=ft.ImageFit.COVER,  # Cover fit for background
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Icon for visual effect
                                    ft.Icon(
                                        name=ft.icons.VERIFIED_USER_ROUNDED,
                                        color=hoverBqColor,
                                        size=140,
                                    ),
                                    # Registration form title
                                    ft.Text(
                                        "Form Registration",
                                        color=hoverBqColor,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="muller-extrabold",
                                    ),
                                ]
                            ),
                        ),
                    ]
                )
            ],
            bgcolor=defaultBqColor,  # Background color for entire page
            padding=0  # No padding around page content
        )
