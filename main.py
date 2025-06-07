# main.py
import kivy
import webbrowser
import json
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

# --- CONFIGURACIÓN VISUAL ---
# Window.size = (400, 700) # <--- CORRECCIÓN: Comentamos o borramos esta línea para que la app ocupe toda la pantalla en el móvil.
# Paleta de colores refinada
COLOR_FONDO = get_color_from_hex('#F5F5F5')
COLOR_PRIMARIO = get_color_from_hex('#2196F3')
COLOR_SECUNDARIO = get_color_from_hex('#4CAF50')
COLOR_ALERTA = get_color_from_hex('#F44336')
COLOR_TEXTO_CLARO = get_color_from_hex('#FFFFFF')
COLOR_TEXTO_OSCURO = get_color_from_hex('#212121')
COLOR_HINT_TEXT = get_color_from_hex('#BDBDBD')
COLOR_FONDO_INPUT = get_color_from_hex('#EEEEEE')
COLOR_BOTON_RUTA = get_color_from_hex('#FFFFFF') # Botones de ruta blancos para mejor contraste

class MapLauncherApp(App):
    """
    Aplicación Kivy mejorada para guardar y lanzar rutas de Google Maps
    con una interfaz elegante y la capacidad de añadir rutas dinámicamente.
    """
    def build(self):
        """
        Construye la interfaz principal de la aplicación.
        """
        self.title = "Mis Rutas"
        self.rutas_guardadas = {}
        self.archivo_datos = "rutas_data.json"

        root_layout = FloatLayout()
        Window.clearcolor = COLOR_FONDO

        self.rutas_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=(20, 20, 20, 100))
        self.rutas_layout.bind(minimum_height=self.rutas_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.rutas_layout)
        root_layout.add_widget(scroll_view)

        # --- Botón Flotante de Añadir (+) con MEJOR CONTRASTE ---
        add_button = Button(
            text='+',
            font_size='45sp', # Aumentado para mejor visibilidad
            bold=True,        # Símbolo en negrita
            color=COLOR_TEXTO_CLARO, # Color de texto blanco explícito
            size_hint=(None, None),
            size=(65, 65),
            pos_hint={'right': 0.95, 'bottom': 0.05},
            background_color=(0,0,0,0)
        )
        add_button.bind(on_press=self.mostrar_popup_anadir)
        
        with add_button.canvas.before:
            Color(*COLOR_SECUNDARIO)
            RoundedRectangle(size=add_button.size, pos=add_button.pos, radius=[32.5])
        add_button.bind(pos=self.actualizar_canvas_redondo, size=self.actualizar_canvas_redondo)

        root_layout.add_widget(add_button)
        
        return root_layout
    
    def on_start(self):
        self.cargar_rutas()
        self.actualizar_lista_rutas()

    def actualizar_canvas_redondo(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.color if hasattr(instance, 'color') else COLOR_SECUNDARIO)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[min(instance.size)/2])

    def actualizar_canvas_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.bg_color)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[15])
            # Añade un borde si es un botón de ruta (fondo blanco)
            if instance.bg_color == COLOR_BOTON_RUTA:
                Color(*COLOR_HINT_TEXT)
                Line(rounded_rectangle=(instance.x+1, instance.y+1, instance.width-2, instance.height-2, 15), width=1.2)

    def cargar_rutas(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r') as f:
                    self.rutas_guardadas = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.rutas_guardadas = {}
        else:
            self.rutas_guardadas = {}

    def guardar_rutas(self):
        with open(self.archivo_datos, 'w') as f:
            json.dump(self.rutas_guardadas, f, indent=4)

    def actualizar_lista_rutas(self):
        self.rutas_layout.clear_widgets()
        if not self.rutas_guardadas:
            label_vacio = Label(
                text="Aún no tienes rutas.\n¡Añade una con el botón '+'!",
                font_size='18sp',
                color=COLOR_HINT_TEXT,
                size_hint_y=None,
                height=400,
                halign='center'
            )
            self.rutas_layout.add_widget(label_vacio)
        else:
            # Ordenar las rutas alfabéticamente por nombre
            sorted_rutas = sorted(self.rutas_guardadas.items())
            for nombre, url in sorted_rutas:
                self.anadir_widget_ruta(nombre, url)
            
    def anadir_widget_ruta(self, nombre, url):
        btn = Button(
            text=nombre,
            font_size='20sp',
            bold=True,  # Letra en negrita
            size_hint_y=None,
            height=80,
            background_color=(0,0,0,0),
            color=COLOR_TEXTO_OSCURO, # Letra en color negro
            halign='center',
            valign='middle',
            text_size=(Window.width - 80, None)
        )
        btn.bind(on_press=lambda instance, url=url: self.abrir_link(url))
        
        btn.bg_color = COLOR_BOTON_RUTA # Fondo blanco para el botón
        with btn.canvas.before:
            Color(*btn.bg_color)
            RoundedRectangle(size=btn.size, pos=btn.pos, radius=[15])
        
        btn.bind(pos=self.actualizar_canvas_rect, size=self.actualizar_canvas_rect)
        
        if self.rutas_layout.children and isinstance(self.rutas_layout.children[0], Label):
            self.rutas_layout.clear_widgets()

        self.rutas_layout.add_widget(btn)

    def mostrar_popup_anadir(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        nombre_input = TextInput(hint_text='Nombre de la ruta (ej. Supermercado)', multiline=False, font_size='18sp', background_color=(0,0,0,0), foreground_color=COLOR_TEXTO_OSCURO, cursor_color=COLOR_TEXTO_OSCURO, padding=[15, 15, 15, 15])
        url_input = TextInput(hint_text='Pega aquí el link de Google Maps', multiline=False, font_size='18sp', background_color=(0,0,0,0), foreground_color=COLOR_TEXTO_OSCURO, cursor_color=COLOR_TEXTO_OSCURO, padding=[15, 15, 15, 15])

        for inp in [nombre_input, url_input]:
            with inp.canvas.before:
                Color(*COLOR_FONDO_INPUT)
                RoundedRectangle(pos=inp.pos, size=inp.size, radius=[10])
            inp.bind(pos=self.actualizar_input_canvas, size=self.actualizar_input_canvas)

        botones_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        btn_guardar = self.crear_boton_popup('Guardar', COLOR_SECUNDARIO)
        btn_cancelar = self.crear_boton_popup('Cancelar', COLOR_ALERTA)

        botones_layout.add_widget(btn_guardar)
        botones_layout.add_widget(btn_cancelar)
        
        popup_layout.add_widget(Label(text='Añadir Nueva Ruta', font_size='22sp', color=COLOR_TEXTO_OSCURO, size_hint_y=None, height=40))
        popup_layout.add_widget(nombre_input)
        popup_layout.add_widget(url_input)
        popup_layout.add_widget(botones_layout)
        
        popup = Popup(
            title='',
            separator_height=0,
            content=popup_layout,
            size_hint=(0.9, 0.6),
            auto_dismiss=False,
            background_color=COLOR_FONDO,
            background='atlas://data/images/defaulttheme/bubble'
        )
        
        btn_guardar.bind(on_press=lambda x: self.anadir_nueva_ruta(nombre_input.text, url_input.text, popup))
        btn_cancelar.bind(on_press=popup.dismiss)
        
        popup.open()

    def actualizar_input_canvas(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*COLOR_FONDO_INPUT)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])
            Color(*COLOR_HINT_TEXT)
            Line(rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 10), width=1.2)


    def crear_boton_popup(self, text, color):
        btn = Button(text=text, background_color=(0,0,0,0), font_size='18sp', color=COLOR_TEXTO_CLARO, bold=True)
        btn.bg_color = color
        btn.bind(pos=self.actualizar_canvas_rect, size=self.actualizar_canvas_rect)
        return btn

    def anadir_nueva_ruta(self, nombre, url, popup):
        if not nombre.strip() or not url.strip():
            self.mostrar_popup_mensaje("¡Atención!", "El nombre y la URL no pueden estar vacíos.")
            return

        self.rutas_guardadas[nombre] = url
        self.guardar_rutas()
        self.actualizar_lista_rutas()
        popup.dismiss()

    def mostrar_popup_mensaje(self, title, message):
        # Layout del contenido del popup
        popup_layout = BoxLayout(orientation='vertical', spacing=15, padding=(20, 20, 20, 20))
        
        # Widgets internos
        popup_layout.add_widget(Label(text=title, font_size='22sp', color=COLOR_TEXTO_OSCURO, size_hint_y=None, height=40, bold=True))
        popup_layout.add_widget(Label(text=message, color=COLOR_TEXTO_OSCURO, font_size='16sp', halign='center'))
        
        btn_ok = self.crear_boton_popup('Entendido', COLOR_PRIMARIO)
        btn_ok.size_hint_y = None
        btn_ok.height = 50
        popup_layout.add_widget(btn_ok)

        # Creación del Popup con estilo unificado
        popup = Popup(
            title='',
            separator_height=0,
            content=popup_layout,
            size_hint=(0.85, 0.45),
            auto_dismiss=False,
            background_color=COLOR_FONDO,
            background='atlas://data/images/defaulttheme/bubble'
        )
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()

    def abrir_link(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            self.mostrar_popup_mensaje("Error de Enlace", f"No se pudo abrir la URL.\nError: {e}")

if __name__ == '__main__':
    MapLauncherApp().run()
