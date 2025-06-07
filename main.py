import os
import json
import webbrowser
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar


Window.size = (400, 700)

KV_STRING = """
<RouteListItem>:
    style: "elevated"
    radius: 16
    padding: "8dp"
    on_release: app.launch_route(root.route_url)
    
    TwoLineAvatarIconListItem:
        text: root.route_name
        secondary_text: root.route_url_short
        _no_ripple_effect: True

        IconLeftWidget:
            icon: "map-marker-distance"

        IconRightWidget:
            icon: "pencil-outline"
            on_release: app.go_to_edit_screen(root.route_id)

<MDTextFieldWithButton>:
    orientation: 'horizontal'
    adaptive_height: True
    spacing: "10dp"
    
    MDTextField:
        id: text_field
        hint_text: root.hint_text
        helper_text: root.helper_text
        helper_text_mode: "on_focus"
        mode: "round"
        size_hint_x: 0.85

    MDIconButton:
        icon: 'clipboard-paste-outline'
        pos_hint: {'center_y': 0.5}
        on_release: app.paste_from_clipboard()
        
ScreenManager:
    id: screen_manager
    MainScreen:
        name: "main_screen"
    EditScreen:
        name: "edit_screen"
    SettingsScreen:
        name: "settings_screen"

<MainScreen@MDScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Trayectos"
            elevation: 4
            left_action_items: [["cog-outline", lambda x: app.go_to_settings_screen()]]
            right_action_items: [["sort-alphabetical-ascending", lambda x: app.sort_routes()]]
            
        MDFloatLayout:
            MDLabel:
                id: empty_label
                text: "No tienes trayectos guardados.\\n¡Añade uno con el botón +!"
                halign: "center"
                theme_text_color: "Secondary"
                font_style: "H6"
                opacity: 0
                pos_hint: {'center_y': .5}
                
            RecycleView:
                id: recycle_view
                key_viewclass: 'viewclass'
                key_size: 'height'
                bar_width: "10dp"
                
                RecycleBoxLayout:
                    padding: "12dp"
                    default_size: None, dp(90)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: "12dp"

            MDFloatingActionButton:
                icon: "plus"
                pos_hint: {"center_x": .9, "center_y": .1}
                md_bg_color: app.theme_cls.primary_color
                on_release: app.go_to_add_screen()

<EditScreen@MDScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Añadir / Editar Trayecto"
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_to_main_screen()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: "24dp"
            spacing: "24dp"
            adaptive_height: True
            pos_hint: {"top": 1}
            MDTextField:
                id: route_name
                hint_text: "Nombre del Trayecto"
                helper_text: "Ej: Camino a casa"
                helper_text_mode: "on_focus"
                icon_right: "text-box-outline"
                mode: "round"
                max_text_length: 50
            MDTextFieldWithButton:
                id: url_field_custom
                hint_text: "URL de Google Maps"
                helper_text: "Pega aquí el enlace de la ruta"
        MDFloatLayout:
            MDFillRoundFlatButton:
                text: "GUARDAR TRAYECTO"
                pos_hint: {'center_x': .5, 'center_y': .6}
                padding: "32dp", "12dp"
                on_release: app.save_route()
            MDTextButton:
                id: delete_button
                text: "Eliminar"
                theme_text_color: "Error"
                pos_hint: {'center_x': .5, 'center_y': .4}
                on_release: app.show_delete_dialog()

# NUEVO: Pantalla de Ajustes
<SettingsScreen@MDScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Ajustes"
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_to_main_screen()]]
    
        MDBoxLayout:
            padding: "24dp"
            
            OneLineAvatarIconListItem:
                text: "Modo Oscuro"
                
                IconLeftWidget:
                    icon: "theme-light-dark"
                
                MDListItemTrailingIcon:
                    MDSwitch:
                        id: theme_switch
                        active: app.is_dark_mode
                        on_active: app.set_theme(self.active)

"""

class RouteListItem(MDCard):
    route_id = NumericProperty()
    route_name = StringProperty()
    route_url_short = StringProperty()
    route_url = StringProperty()

class MDTextFieldWithButton(MDBoxLayout):
    hint_text = StringProperty()
    helper_text = StringProperty()

class TrayectosApp(MDApp):
    current_route_id = -1
    dialog = None
    sort_ascending = True
    is_dark_mode = BooleanProperty(False)

    def build(self):
        # El tema se carga desde el archivo de ajustes
        self.title = "Trayectos"
        return Builder.load_string(KV_STRING)

    def on_start(self):
        self.routes_data_file = os.path.join(self.user_data_dir, "routes_data.json")
        self.settings_file = os.path.join(self.user_data_dir, "settings.json")
        self.load_settings()
        self.load_routes()
        Clock.schedule_once(lambda dt: self.refresh_routes_list())
        Window.bind(on_keyboard=self.handle_back_button)

    # NUEVO: Carga, guardado y aplicación de ajustes
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.is_dark_mode = settings.get("is_dark_mode", False)
        except (FileNotFoundError, json.JSONDecodeError):
            self.is_dark_mode = False
        self.theme_cls.theme_style = "Dark" if self.is_dark_mode else "Light"
        self.theme_cls.primary_palette = "Teal"

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump({'is_dark_mode': self.is_dark_mode}, f)

    def set_theme(self, active):
        self.is_dark_mode = active
        self.theme_cls.theme_style = "Dark" if self.is_dark_mode else "Light"
        self.save_settings()

    # NUEVO: Gestión del botón "Atrás" de Android
    def handle_back_button(self, window, key, *args):
        if key == 27:
            current_screen = self.root.current
            if current_screen in ["edit_screen", "settings_screen"]:
                self.go_to_main_screen()
                return True
        return False

    # NUEVO: Snackbar para feedback
    def show_snackbar(self, text):
        MDSnackbar(text=text, snackbar_x="10dp", snackbar_y="10dp", size_hint_x=0.9, pos_hint={'center_x': 0.5}).open()

    # NUEVO: Ordenar rutas
    def sort_routes(self):
        self.sort_ascending = not self.sort_ascending
        self.routes_data.sort(key=lambda item: item['name'].lower(), reverse=not self.sort_ascending)
        self.refresh_routes_list()
        order = "ascendente" if self.sort_ascending else "descendente"
        self.show_snackbar(f"Rutas ordenadas de forma {order}")

    def load_routes(self):
        try:
            with open(self.routes_data_file, 'r') as f:
                self.routes_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.routes_data = []

    def save_routes(self):
        with open(self.routes_data_file, 'w') as f:
            json.dump(self.routes_data, f, indent=4)

    def refresh_routes_list(self):
        recycle_view = self.root.get_screen('main_screen').ids.recycle_view
        empty_label = self.root.get_screen('main_screen').ids.empty_label
        if not self.routes_data:
            empty_label.opacity = 1
            recycle_view.data = []
        else:
            empty_label.opacity = 0
            recycle_view.data = [{'viewclass': 'RouteListItem', 'route_name': route['name'], 'route_url_short': route['url'][:50] + '...', 'route_id': index, 'route_url': route['url']} for index, route in enumerate(self.routes_data)]
        recycle_view.refresh_from_data()

    def go_to_main_screen(self):
        self.root.current = 'main_screen'

    def go_to_add_screen(self):
        self.current_route_id = -1
        edit_screen = self.root.get_screen('edit_screen')
        edit_screen.ids.route_name.text = ""
        edit_screen.ids.url_field_custom.ids.text_field.text = ""
        edit_screen.ids.delete_button.opacity = 0
        edit_screen.ids.delete_button.disabled = True
        self.root.current = 'edit_screen'

    def go_to_settings_screen(self):
        self.root.current = 'settings_screen'

    def go_to_edit_screen(self, route_id):
        self.current_route_id = route_id
        route = self.routes_data[route_id]
        edit_screen = self.root.get_screen('edit_screen')
        edit_screen.ids.route_name.text = route['name']
        edit_screen.ids.url_field_custom.ids.text_field.text = route['url']
        edit_screen.ids.delete_button.opacity = 1
        edit_screen.ids.delete_button.disabled = False
        self.root.current = 'edit_screen'
    
    def paste_from_clipboard(self):
        clipboard_content = Clipboard.paste()
        if clipboard_content:
            self.root.get_screen('edit_screen').ids.url_field_custom.ids.text_field.text = clipboard_content
            
    def launch_route(self, url):
        if url:
            webbrowser.open(url)

    def save_route(self):
        edit_screen = self.root.get_screen('edit_screen')
        name = edit_screen.ids.route_name.text.strip()
        url = edit_screen.ids.url_field_custom.ids.text_field.text.strip()
        if not name or not url:
            self.show_snackbar("El nombre y la URL no pueden estar vacíos")
            return
        new_route = {'name': name, 'url': url}
        if self.current_route_id == -1:
            self.routes_data.append(new_route)
        else:
            self.routes_data[self.current_route_id] = new_route
        self.save_routes()
        self.refresh_routes_list()
        self.show_snackbar(f"Trayecto '{name}' guardado")
        self.go_to_main_screen()

    def show_delete_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(title="¿Eliminar Trayecto?", text="Esta acción no se puede deshacer.", buttons=[MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog.dismiss()), MDRaisedButton(text="ELIMINAR", md_bg_color=self.theme_cls.error_color, on_release=lambda x: self.delete_route()),],)
        self.dialog.open()

    def delete_route(self):
        if self.dialog:
            self.dialog.dismiss()
        if self.current_route_id != -1:
            route_name = self.routes_data.pop(self.current_route_id)['name']
            self.save_routes()
            self.refresh_routes_list()
            self.show_snackbar(f"Trayecto '{route_name}' eliminado")
            self.go_to_main_screen()

if __name__ == '__main__':
    TrayectosApp().run()
