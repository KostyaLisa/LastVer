import flet as ft

from pages.login import LoginPage
from pages.signup import SignupPage
from pages.dashboard import DashboardPage
from pages.posting import PostPage






class Router:
    def __init__(self, page: ft.Page):
        self.page = page

        # Define routing table
        self.app_router = {
            "/": LoginPage().view,
            "/signup": SignupPage().view,
            "/dashboard": DashboardPage().view,
            "/posting": PostPage().view

        }

        # Attach route change handler
        page.on_route_change = self.route_change

        # Go to the current route
        page.go(page.route)

    def route_change(self, route, ft=None):
        view_fn = self.app_router.get(self.page.route, None)
        if view_fn:
            self.page.views.clear()  # Clear the previous view if needed
            self.page.views.append(view_fn(self.page))  # Load the new view
        else:
            self.page.views.append(ft.Text("404 Page not found"))
        self.page.update()  # Refresh the page