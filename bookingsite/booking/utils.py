
app_name = 'booking'
unauth_menu = [
    {'title':'Sign up', 'url_name': (app_name + ':sign_up')},
    {'title':'Sign in', 'url_name': (app_name + ':sign_in')},
]


auth_menu = [
    {'title':'Profile', 'url_name': (app_name + ':profile')},
    {'title':'Log out', 'url_name': (app_name + ':logout')},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['auth_menu'] = auth_menu
        context['unauth_menu'] = unauth_menu
        if 'menu_item_selected' not in context:
            context['menu_item_selected'] = '------'
        return context
