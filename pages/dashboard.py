import os
import flet as ft  # Importing Flet for UI components
from dotenv import set_key, load_dotenv  # For managing environment variables

from utils.style import *  # Importing style variables
from pathlib import Path  # For creating paths for environment files


class DashboardPage:
    # Define the path to the .env file
    env_file_path = Path('.') / 'env.'
    load_dotenv(dotenv_path=env_file_path)  # Load environment variables

    # Initial states
    AUTH_USER = False
    token_bot = os.getenv('TOKEN_BOT')  # Load token bot if available
    channel_link = os.getenv('CHANNEL_LINK')  # Load channel link if available

    # Define the main view of the Dashboard page
    def view(self, page: ft.Page):
        # Check if the user is authenticated
        self.AUTH_USER = page.session.get('auth_user')

        # Set up basic page properties
        page.title = "Dashboard"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 900
        page.window.min_height = 400

        # Print token_bot to verify loading (for debugging)
        print(self.token_bot)

        # Define fonts to be used across the page
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

        # Function to save token and channel link settings
        def save_settings(e):
            token_bot = token_input.content.value
            channel_link = channel_input.content.value
            # Save to .env file
            set_key(dotenv_path=self.env_file_path, key_to_set='TOKEN_BOT', value_to_set=token_bot)
            set_key(dotenv_path=self.env_file_path, key_to_set='CHANNEL_LINK', value_to_set=channel_link)
            # Disable input fields after saving
            token_input.disabled = True
            channel_input.disabled = True
            # Save to session and update session variables
            page.session.set('TOKEN_BOT', token_bot)
            page.session.set('CHANNEL_LINK', channel_link)
            save_btn.text = "Saving"
            save_btn.disabled = True
            save_btn.update()
            token_input.update()
            channel_input.update()
            page.update()

        # Function to create an input field
        def input_form(label, value):
            return ft.TextField(label=label, value=value,
                                bgcolor=secondaryBqColor,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                color=secondaryFontColor)

        # Function to create a disabled input field
        def input_disable(value):
            return ft.TextField(value=value,
                                bgcolor=secondaryBqColor,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                disabled=True,
                                color=secondaryFontColor)

        # Define style for the menu items
        style_menu = ft.ButtonStyle(
            color={ft.ControlState.HOVERED: ft.colors.WHITE, ft.ControlState.DEFAULT: menuColorFont},
            icon_size=14,
            overlay_color=hoverBqColor,
            shadow_color=hoverBqColor
        )

        # Sidebar components
        logotype = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(src='images/logo.png', width=45, height=32, fit=ft.ImageFit.FILL),
                    ft.Text('Tlogo', expand=True, color=defaultFontColor, font_family='muller-extrabold', size=16)
                ], alignment=ft.MainAxisAlignment.START,
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text('Menu', color=menuColorFont, size=12, font_family='muller-extrabold'),
                    ft.TextButton('Header', icon='space_dashboard_rounded', style=style_menu,
                                  on_click=lambda e: page.go('/dashboard')),
                    ft.TextButton('Send', icon='post_add', style=style_menu,
                                  on_click=lambda e: page.go('/posting')),
                    ft.TextButton('Test Button', icon='verified_user', style=style_menu),
                ],
            )
        )

        # Input forms for token and channel link based on availability in session or environment
        if not self.token_bot and not page.session.get('TOKEN_BOT'):
            token_input = ft.Container(
                content=input_form('Enter Token', page.session.get('TOKEN_BOT')),
                border_radius=15)
        elif page.session.get('TOKEN_BOT'):
            token_input = ft.Container(
                content=input_disable(page.session.get('TOKEN_BOT')),
                border_radius=15)
        else:
            token_input = ft.Container(
                content=input_disable(self.token_bot),
                border_radius=15)

        if not self.channel_link and not page.session.get('CHANNEL_LINK'):
            channel_input = ft.Container(
                content=input_form('Enter link to channel', page.session.get('CHANNEL_LINK')),
                border_radius=15)
        elif page.session.get('CHANNEL_LINK'):
            channel_input = ft.Container(
                content=input_disable(page.session.get('CHANNEL_LINK')),
                border_radius=15)
        else:
            channel_input = ft.Container(
                content=input_disable(self.channel_link),
                border_radius=15)

        # Save button configuration
        if not self.token_bot and not self.channel_link:
            save_btn = ft.ElevatedButton('Save Data', bgcolor=hoverBqColor, color=defaultFontColor, icon='settings',
                                         on_click=lambda e: save_settings(e))
        else:
            save_btn = ft.ElevatedButton('Saving', bgcolor=hoverBqColor, color=defaultFontColor, icon='save',
                                         disabled=True)

        # Header section with control panel title and icons
        header = ft.Container(content=ft.Row(controls=[
            ft.Text('Control Panel', color=defaultFontColor, size=20, font_family='muller-extrabold'),
            ft.Row(controls=[
                ft.CircleAvatar(foreground_image_src='images/avatar.png',
                                content=ft.Text('Avatar')),
                ft.IconButton(
                    icon=ft.icons.NOTIFICATIONS_ROUNDED,
                    icon_size=20,
                    hover_color=hoverBqColor,
                    icon_color=defaultFontColor,
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))

        # Returning the main view layout of the page
        return ft.View(
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Sidebar container
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                controls=[logotype, sidebar_menu]
                            ),
                            bgcolor=secondaryBqColor,
                        ),
                        # Main content area with header and input forms
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column([header, token_input, channel_input, save_btn])
                        )
                    ]
                )
            ], bgcolor=defaultBqColor,
            padding=0
        )
