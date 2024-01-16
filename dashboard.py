from admin_interface.models import Theme
from admin_interface.dashboard import modules, Dashboard, AppListDashboardModule
from .models import ProductDB, ProductDetails, ProductColorVariations

class MyDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # Add an "App List" panel to the dashboard
        self.children.append(modules.AppListDashboardModule(
            column=1,
            order=1,
            title='My App',
            exclude=('django.contrib.*',),
        ))

        # Add a custom panel for ProductDB
        self.children.append(modules.ModelListDashboardModule(
            column=2,
            order=1,
            title='Model Group 1',
            models=[ProductDB],
        ))

        # Add a custom panel for ProductDetails
        self.children.append(modules.ModelListDashboardModule(
            column=2,
            order=2,
            title='Model Group 2',
            models=[ProductDetails],
        ))

        # Add a custom panel for ProductColorVariations
        self.children.append(modules.ModelListDashboardModule(
            column=3,
            order=1,
            title='Model Group 3',
            models=[ProductColorVariations],
        ))

        # Set the admin interface theme
        theme = Theme.objects.get(pk=1)
        context['admin_interface_theme'] = theme
