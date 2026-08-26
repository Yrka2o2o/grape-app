from datetime import datetime
from pathlib import Path
import json

from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# =========================================================
# НАЧАЛЬНАЯ БАЗА ПРЕПАРАТОВ
# =========================================================

DEFAULT_PREPARATIONS = [
    {
        "name": "Свитч",
        "amount": 10,
        "unit": "г",
        "water": 10
    },
    {
        "name": "Скор",
        "amount": 2,
        "unit": "мл",
        "water": 10
    },
    {
        "name": "Хорус",
        "amount": 3,
        "unit": "г",
        "water": 10
    },
    {
        "name": "Топаз",
        "amount": 3,
        "unit": "мл",
        "water": 10
    },
    {
        "name": "Тиовит Джет",
        "amount": 30,
        "unit": "г",
        "water": 10
    }
]


# =========================================================
# КАРТОЧКА ОБРАБОТКИ
# =========================================================

class TreatmentCard(BoxLayout):

    def __init__(self, treatment, callback, **kwargs):

        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(65),
            padding=(dp(15), 0),
            spacing=dp(5),
            **kwargs
        )

        self.treatment = treatment
        self.callback = callback

        with self.canvas.before:

            Color(
                0.93,
                0.93,
                0.93,
                1
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        date_label = Label(
            text=treatment.get(
                "date",
                ""
            ),
            font_size="18sp",
            bold=True,
            color=(
                0.1,
                0.1,
                0.1,
                1
            ),
            halign="left",
            valign="middle",
            size_hint_x=0.6
        )

        date_label.bind(
            size=date_label.setter(
                "text_size"
            )
        )

        time_label = Label(
            text=treatment.get(
                "time",
                ""
            ),
            font_size="18sp",
            color=(
                0.3,
                0.3,
                0.3,
                1
            ),
            halign="right",
            valign="middle",
            size_hint_x=0.4
        )

        time_label.bind(
            size=time_label.setter(
                "text_size"
            )
        )

        self.add_widget(
            date_label
        )

        self.add_widget(
            time_label
        )

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

    def on_touch_down(self, touch):

        if self.collide_point(
            *touch.pos
        ):

            self.callback(
                self.treatment
            )

            return True

        return super().on_touch_down(
            touch
        )


# =========================================================
# КАРТОЧКА ПРЕПАРАТА
# =========================================================

class PreparationCard(BoxLayout):

    def __init__(
        self,
        preparation,
        edit_callback,
        delete_callback,
        **kwargs
    ):

        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(65),
            padding=(dp(10), 0),
            spacing=dp(5),
            **kwargs
        )

        with self.canvas.before:

            Color(
                0.93,
                0.93,
                0.93,
                1
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        info = Label(
            text=(
                f"{preparation['name']}\n"
                f"{preparation['amount']} "
                f"{preparation['unit']} / "
                f"{preparation['water']} л"
            ),
            font_size="16sp",
            halign="left",
            valign="middle",
            size_hint_x=0.65
        )

        info.bind(
            size=info.setter(
                "text_size"
            )
        )

        self.add_widget(
            info
        )

        edit_button = Button(
            text="✏",
            size_hint_x=None,
            width=dp(50)
        )

        edit_button.bind(
            on_release=lambda x:
            edit_callback(
                preparation
            )
        )

        self.add_widget(
            edit_button
        )

        delete_button = Button(
            text="✕",
            size_hint_x=None,
            width=dp(50)
        )

        delete_button.bind(
            on_release=lambda x:
            delete_callback(
                preparation
            )
        )

        self.add_widget(
            delete_button
        )

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size


# =========================================================
# ПРИЛОЖЕНИЕ
# =========================================================

class GrapeNotesApp(App):

    # =====================================================
    # ПАПКА ДАННЫХ
    # =====================================================

    def get_data_folder(self):

        folder = Path(
            self.user_data_dir
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder

    # =====================================================
    # BUILD
    # =====================================================

    def build(self):

        self.data_folder = (
            self.get_data_folder()
        )

        self.treatments_file = (
            self.data_folder /
            "treatments.json"
        )

        self.preparations_file = (
            self.data_folder /
            "preparations.json"
        )

        self.treatments = self.load_json(
            self.treatments_file,
            []
        )

        self.preparations = self.load_json(
            self.preparations_file,
            DEFAULT_PREPARATIONS
        )

        if not self.preparations_file.exists():

            self.save_preparations()

        main = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        title = Label(
            text="🍇 Обработки винограда",
            font_size="24sp",
            size_hint_y=None,
            height=dp(55),
            color=(
                0.1,
                0.1,
                0.1,
                1
            )
        )

        main.add_widget(
            title
        )

        scroll = ScrollView()

        self.treatments_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )

        self.treatments_layout.bind(
            minimum_height=
            self.treatments_layout.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.treatments_layout
        )

        main.add_widget(
            scroll
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        preparation_button = Button(
            text="💊 Препараты",
            font_size="16sp"
        )

        preparation_button.bind(
            on_release=
            self.open_preparations
        )

        new_button = Button(
            text="+ Новая обработка",
            font_size="16sp"
        )

        new_button.bind(
            on_release=
            self.new_treatment
        )

        buttons.add_widget(
            preparation_button
        )

        buttons.add_widget(
            new_button
        )

        main.add_widget(
            buttons
        )

        self.refresh_treatments()

        return main

    # =====================================================
    # ЗАГРУЗКА JSON
    # =====================================================

    def load_json(
        self,
        filename,
        default
    ):

        if not filename.exists():

            return list(default)

        try:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as error:

            print(
                "Ошибка загрузки:",
                filename,
                error
            )

            return list(default)

    # =====================================================
    # СОХРАНЕНИЕ ОБРАБОТОК
    # =====================================================

    def save_treatments(self):

        try:

            with open(
                self.treatments_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.treatments,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as error:

            print(
                "Ошибка сохранения обработок:",
                error
            )

    # =====================================================
    # СОХРАНЕНИЕ ПРЕПАРАТОВ
    # =====================================================

    def save_preparations(self):

        try:

            with open(
                self.preparations_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.preparations,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as error:

            print(
                "Ошибка сохранения препаратов:",
                error
            )

    # =====================================================
    # НОВАЯ ОБРАБОТКА
    # =====================================================

    def new_treatment(
        self,
        instance
    ):

        now = datetime.now()

        treatment = {
            "date": now.strftime(
                "%d.%m.%Y"
            ),
            "time": now.strftime(
                "%H:%M"
            ),
            "water": "",
            "preparations": [],
            "note": ""
        }

        self.open_editor(
            treatment,
            True
        )

    # =====================================================
    # ПРОСМОТР ОБРАБОТКИ
    # =====================================================

    def open_treatment(
        self,
        treatment
    ):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        date_time = Label(
            text=(
                f"{treatment.get('date', '')}    "
                f"{treatment.get('time', '')}"
            ),
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        layout.add_widget(
            date_time
        )

        scroll = ScrollView()

        info = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
            padding=(0, dp(5))
        )

        info.bind(
            minimum_height=
            info.setter("height")
        )

        water = Label(
            text=(
                f"💧 Вода: "
                f"{treatment.get('water', '')} л"
            ),
            font_size="17sp",
            size_hint_y=None,
            height=dp(35),
            halign="left"
        )

        water.bind(
            size=water.setter(
                "text_size"
            )
        )

        info.add_widget(
            water
        )

        title = Label(
            text="💊 Препараты:",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(35),
            halign="left"
        )

        title.bind(
            size=title.setter(
                "text_size"
            )
        )

        info.add_widget(
            title
        )

        for item in treatment.get(
            "preparations",
            []
        ):

            amount = item.get(
                "amount",
                item.get(
                    "grams",
                    ""
                )
            )

            unit = item.get(
                "unit",
                "г"
            )

            label = Label(
                text=(
                    f"• {item.get('name', '')} — "
                    f"{amount} {unit}"
                ),
                font_size="17sp",
                size_hint_y=None,
                height=dp(32),
                halign="left"
            )

            label.bind(
                size=label.setter(
                    "text_size"
                )
            )

            info.add_widget(
                label
            )

        note_value = treatment.get(
            "note",
            ""
        )

        if note_value:

            note_title = Label(
                text="📝 Заметка:",
                font_size="18sp",
                bold=True,
                size_hint_y=None,
                height=dp(35),
                halign="left"
            )

            note_title.bind(
                size=note_title.setter(
                    "text_size"
                )
            )

            info.add_widget(
                note_title
            )

            note = Label(
                text=note_value,
                font_size="17sp",
                size_hint_y=None,
                halign="left",
                valign="top"
            )

            note.bind(
                texture_size=
                lambda instance, value:
                setattr(
                    instance,
                    "height",
                    value[1] + dp(10)
                )
            )

            note.bind(
                width=
                lambda instance, value:
                setattr(
                    instance,
                    "text_size",
                    (value, None)
                )
            )

            info.add_widget(
                note
            )

        scroll.add_widget(
            info
        )

        layout.add_widget(
            scroll
        )

        # =================================================
        # КНОПКИ
        # =================================================

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        edit_button = Button(
            text="✏ Редактировать"
        )

        delete_button = Button(
            text="🗑 Удалить"
        )

        close_button = Button(
            text="Закрыть"
        )

        buttons.add_widget(
            edit_button
        )

        buttons.add_widget(
            delete_button
        )

        buttons.add_widget(
            close_button
        )

        layout.add_widget(
            buttons
        )

        popup = Popup(
            title="Обработка",
            content=layout,
            size_hint=(0.95, 0.85)
        )

        # =================================================
        # ЗАКРЫТЬ
        # =================================================

        close_button.bind(
            on_release=
            popup.dismiss
        )

        # =================================================
        # РЕДАКТИРОВАТЬ
        # =================================================

        def edit(instance):

            popup.dismiss()

            self.open_editor(
                treatment,
                False
            )

        edit_button.bind(
            on_release=edit
        )

        # =================================================
        # УДАЛИТЬ
        # =================================================

        def delete(instance):

            self.confirm_delete_treatment(
                treatment,
                popup
            )

        delete_button.bind(
            on_release=delete
        )

        popup.open()

    # =====================================================
    # ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ ОБРАБОТКИ
    # =====================================================

    def confirm_delete_treatment(
        self,
        treatment,
        treatment_popup
    ):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        label = Label(
            text=(
                "Удалить эту обработку?\n\n"
                f"{treatment.get('date', '')} "
                f"{treatment.get('time', '')}"
            ),
            font_size="17sp"
        )

        layout.add_widget(
            label
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(10)
        )

        cancel = Button(
            text="Отмена"
        )

        delete = Button(
            text="Удалить"
        )

        buttons.add_widget(
            cancel
        )

        buttons.add_widget(
            delete
        )

        layout.add_widget(
            buttons
        )

        popup = Popup(
            title="Подтверждение",
            content=layout,
            size_hint=(0.85, 0.35)
        )

        cancel.bind(
            on_release=
            popup.dismiss
        )

        def confirm(instance):

            if treatment in self.treatments:

                self.treatments.remove(
                    treatment
                )

                self.save_treatments()

                self.refresh_treatments()

            popup.dismiss()

            treatment_popup.dismiss()

        delete.bind(
            on_release=confirm
        )

        popup.open()

    # =====================================================
    # РЕДАКТОР ОБРАБОТКИ
    # =====================================================

    def open_editor(
        self,
        treatment,
        is_new=False
    ):

        edit_date = [
            treatment.get(
                "date",
                datetime.now().strftime(
                    "%d.%m.%Y"
                )
            )
        ]

        edit_time = [
            treatment.get(
                "time",
                datetime.now().strftime(
                    "%H:%M"
                )
            )
        ]

        edit_preparations = [
            item.copy()
            for item in treatment.get(
                "preparations",
                []
            )
        ]

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        date_button = Button(
            text=f"📅 Дата: {edit_date[0]}",
            size_hint_y=None,
            height=dp(50)
        )

        date_button.bind(
            on_release=lambda x:
            self.choose_date(
                date_button,
                edit_date
            )
        )

        layout.add_widget(
            date_button
        )

        time_button = Button(
            text=f"🕐 Время: {edit_time[0]}",
            size_hint_y=None,
            height=dp(50)
        )

        time_button.bind(
            on_release=lambda x:
            self.choose_time(
                time_button,
                edit_time
            )
        )

        layout.add_widget(
            time_button
        )

        water = TextInput(
            text=treatment.get(
                "water",
                ""
            ),
            hint_text="Количество воды, литров",
            multiline=False,
            input_filter="float",
            font_size="17sp",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            water
        )

        add_preparation = Button(
            text="+ Добавить препарат",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            add_preparation
        )

        preparations_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None
        )

        preparations_layout.bind(
            minimum_height=
            preparations_layout.setter(
                "height"
            )
        )

        preparations_scroll = ScrollView(
            size_hint_y=None,
            height=dp(200)
        )

        preparations_scroll.add_widget(
            preparations_layout
        )

        layout.add_widget(
            preparations_scroll
        )

        self.refresh_editor_preparations(
            edit_preparations,
            preparations_layout,
            water
        )

        add_preparation.bind(
            on_release=lambda x:
            self.choose_treatment_preparation(
                edit_preparations,
                preparations_layout,
                water
            )
        )

        note = TextInput(
            text=treatment.get(
                "note",
                ""
            ),
            hint_text="Дополнительная заметка...",
            multiline=True,
            font_size="17sp"
        )

        layout.add_widget(
            note
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(10)
        )

        cancel = Button(
            text="Отмена"
        )

        save = Button(
            text="Сохранить"
        )

        buttons.add_widget(
            cancel
        )

        buttons.add_widget(
            save
        )

        layout.add_widget(
            buttons
        )

        popup = Popup(
            title=(
                "Новая обработка"
                if is_new
                else "Редактирование"
            ),
            content=layout,
            size_hint=(0.95, 0.95)
        )

        cancel.bind(
            on_release=
            popup.dismiss
        )

        def save_data(instance):

            if not water.text.strip():
                return

            if not edit_preparations:
                return

            treatment["date"] = (
                edit_date[0]
            )

            treatment["time"] = (
                edit_time[0]
            )

            treatment["water"] = (
                water.text.strip()
            )

            treatment["preparations"] = [
                item.copy()
                for item in edit_preparations
            ]

            treatment["note"] = (
                note.text.strip()
            )

            if is_new:

                self.treatments.insert(
                    0,
                    treatment
                )

            self.save_treatments()

            self.refresh_treatments()

            popup.dismiss()

        save.bind(
            on_release=save_data
        )

        popup.open()

    # =====================================================
    # ВЫБОР ПРЕПАРАТА
    # =====================================================

    def choose_treatment_preparation(
        self,
        selected,
        layout,
        water_input
    ):

        popup_layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        names = [
            item["name"]
            for item in self.preparations
        ]

        spinner = Spinner(
            text="Выберите препарат",
            values=names,
            size_hint_y=None,
            height=dp(50)
        )

        popup_layout.add_widget(
            spinner
        )

        calculation = Label(
            text="",
            font_size="16sp",
            size_hint_y=None,
            height=dp(55)
        )

        popup_layout.add_widget(
            calculation
        )

        add = Button(
            text="Добавить",
            size_hint_y=None,
            height=dp(50)
        )

        popup_layout.add_widget(
            add
        )

        popup = Popup(
            title="Выбор препарата",
            content=popup_layout,
            size_hint=(0.9, 0.45)
        )

        def update_calculation(*args):

            if (
                spinner.text ==
                "Выберите препарат"
            ):

                calculation.text = ""

                return

            preparation = (
                self.find_preparation(
                    spinner.text
                )
            )

            if preparation is None:
                return

            try:

                water = float(
                    water_input.text
                )

                result = (
                    self.calculate_amount(
                        preparation,
                        water
                    )
                )

                calculation.text = (
                    f"Расход: "
                    f"{preparation['amount']} "
                    f"{preparation['unit']} / "
                    f"{preparation['water']} л\n"
                    f"Нужно: {result:g} "
                    f"{preparation['unit']}"
                )

            except ValueError:

                calculation.text = (
                    "Введите количество воды"
                )

        spinner.bind(
            text=update_calculation
        )

        water_input.bind(
            text=update_calculation
        )

        def add_preparation(instance):

            if (
                spinner.text ==
                "Выберите препарат"
            ):
                return

            preparation = (
                self.find_preparation(
                    spinner.text
                )
            )

            if preparation is None:
                return

            try:

                water = float(
                    water_input.text
                )

            except ValueError:

                return

            amount = (
                self.calculate_amount(
                    preparation,
                    water
                )
            )

            selected.append(
                {
                    "name":
                    preparation["name"],

                    "amount":
                    amount,

                    "unit":
                    preparation["unit"],

                    "rate":
                    preparation["amount"],

                    "rate_water":
                    preparation["water"]
                }
            )

            self.refresh_editor_preparations(
                selected,
                layout,
                water_input
            )

            popup.dismiss()

        add.bind(
            on_release=add_preparation
        )

        popup.open()

    #
    
    #=====================================================
    # РАСЧЁТ КОЛИЧЕСТВА
    # =====================================================

    def calculate_amount(
        self,
        preparation,
        water
    ):

        result = (
            float(
                preparation["amount"]
            )
            * water
            / float(
                preparation["water"]
            )
        )

        return round(
            result,
            2
        )

    # =====================================================
    # ПОИСК ПРЕПАРАТА
    # =====================================================

    def find_preparation(
        self,
        name
    ):

        for preparation in self.preparations:

            if (
                preparation["name"]
                == name
            ):

                return preparation

        return None

    # =====================================================
    # СПИСОК ПРЕПАРАТОВ В РЕДАКТОРЕ
    # =====================================================

    def refresh_editor_preparations(
        self,
        selected,
        layout,
        water_input
    ):

        layout.clear_widgets()

        for index, item in enumerate(
            selected
        ):

            row = BoxLayout(
                size_hint_y=None,
                height=dp(50),
                spacing=dp(5)
            )

            label = Label(
                text=(
                    f"{item['name']} — "
                    f"{item['amount']:g} "
                    f"{item['unit']}"
                ),
                font_size="16sp",
                halign="left",
                valign="middle"
            )

            label.bind(
                size=label.setter(
                    "text_size"
                )
            )

            delete = Button(
                text="✕",
                size_hint_x=None,
                width=dp(45)
            )

            def remove(
                instance,
                index=index
            ):

                del selected[index]

                self.refresh_editor_preparations(
                    selected,
                    layout,
                    water_input
                )

            delete.bind(
                on_release=remove
            )

            row.add_widget(
                label
            )

            row.add_widget(
                delete
            )

            layout.add_widget(
                row
            )

    # =====================================================
    # БАЗА ПРЕПАРАТОВ
    # =====================================================

    def open_preparations(
        self,
        instance
    ):

        main = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        scroll = ScrollView()

        self.preparations_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        self.preparations_layout.bind(
            minimum_height=
            self.preparations_layout.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.preparations_layout
        )

        main.add_widget(
            scroll
        )

        add = Button(
            text="+ Добавить препарат",
            size_hint_y=None,
            height=dp(55)
        )

        main.add_widget(
            add
        )

        popup = Popup(
            title="База препаратов",
            content=main,
            size_hint=(0.95, 0.9)
        )

        self.preparations_popup = popup

        add.bind(
            on_release=lambda x:
            self.edit_preparation(
                None
            )
        )

        self.refresh_preparations()

        popup.open()

    # =====================================================
    # ОБНОВЛЕНИЕ БАЗЫ ПРЕПАРАТОВ
    # =====================================================

    def refresh_preparations(self):

        if not hasattr(
            self,
            "preparations_layout"
        ):

            return

        self.preparations_layout.clear_widgets()

        for preparation in self.preparations:

            card = PreparationCard(
                preparation,
                self.edit_preparation,
                self.delete_preparation
            )

            self.preparations_layout.add_widget(
                card
            )

    # =====================================================
    # ДОБАВЛЕНИЕ / РЕДАКТИРОВАНИЕ ПРЕПАРАТА
    # =====================================================

    def edit_preparation(
        self,
        preparation
    ):

        is_new = (
            preparation is None
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        name = TextInput(
            text=(
                ""
                if is_new
                else preparation["name"]
            ),
            hint_text="Название препарата",
            multiline=False,
            font_size="17sp",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            name
        )

        amount = TextInput(
            text=(
                ""
                if is_new
                else str(
                    preparation["amount"]
                )
            ),
            hint_text="Количество препарата",
            multiline=False,
            input_filter="float",
            font_size="17sp",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            amount
        )

        unit = Spinner(
            text=(
                "г"
                if is_new
                else preparation["unit"]
            ),
            values=[
                "г",
                "мл"
            ],
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            unit
        )

        water = TextInput(
            text=(
                "10"
                if is_new
                else str(
                    preparation["water"]
                )
            ),
            hint_text="На сколько литров воды",
            multiline=False,
            input_filter="float",
            font_size="17sp",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            water
        )

        info = Label(
            text=(
                "Например: "
                "10 г на 10 л воды"
            ),
            font_size="15sp",
            size_hint_y=None,
            height=dp(35)
        )

        layout.add_widget(
            info
        )

        save = Button(
            text="Сохранить",
            size_hint_y=None,
            height=dp(55)
        )

        layout.add_widget(
            save
        )

        popup = Popup(
            title=(
                "Добавить препарат"
                if is_new
                else "Редактировать препарат"
            ),
            content=layout,
            size_hint=(0.9, 0.65)
        )

        def save_data(instance):

            if not name.text.strip():
                return

            try:

                amount_value = float(
                    amount.text
                )

                water_value = float(
                    water.text
                )

                if amount_value <= 0:
                    return

                if water_value <= 0:
                    return

            except ValueError:

                return

            if is_new:

                self.preparations.append(
                    {
                        "name":
                        name.text.strip(),

                        "amount":
                        amount_value,

                        "unit":
                        unit.text,

                        "water":
                        water_value
                    }
                )

            else:

                preparation["name"] = (
                    name.text.strip()
                )

                preparation["amount"] = (
                    amount_value
                )

                preparation["unit"] = (
                    unit.text
                )

                preparation["water"] = (
                    water_value
                )

            self.save_preparations()

            self.refresh_preparations()

            popup.dismiss()

        save.bind(
            on_release=save_data
        )

        popup.open()

    # =====================================================
    # УДАЛЕНИЕ ПРЕПАРАТА
    # =====================================================

    def delete_preparation(
        self,
        preparation
    ):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        label = Label(
            text=(
                "Удалить препарат?\n\n"
                f"{preparation['name']}"
            ),
            font_size="17sp"
        )

        layout.add_widget(
            label
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        cancel = Button(
            text="Отмена"
        )

        delete = Button(
            text="Удалить"
        )

        buttons.add_widget(
            cancel
        )

        buttons.add_widget(
            delete
        )

        layout.add_widget(
            buttons
        )

        popup = Popup(
            title="Удаление",
            content=layout,
            size_hint=(0.8, 0.35)
        )

        cancel.bind(
            on_release=
            popup.dismiss
        )

        def confirm(instance):

            if (
                preparation
                in self.preparations
            ):

                self.preparations.remove(
                    preparation
                )

                self.save_preparations()

                self.refresh_preparations()

            popup.dismiss()

        delete.bind(
            on_release=confirm
        )

        popup.open()

    # =====================================================
    # ОБНОВЛЕНИЕ СПИСКА ОБРАБОТОК
    # =====================================================

    def refresh_treatments(self):

        self.treatments_layout.clear_widgets()

        for treatment in self.treatments:

            card = TreatmentCard(
                treatment,
                self.open_treatment
            )

            self.treatments_layout.add_widget(
                card
            )

    # =====================================================
    # ВЫБОР ДАТЫ
    # =====================================================

    def choose_date(
        self,
        button,
        selected_date
    ):

        try:

            current = datetime.strptime(
                selected_date[0],
                "%d.%m.%Y"
            )

        except ValueError:

            current = datetime.now()

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        day = TextInput(
            text=current.strftime("%d"),
            hint_text="День",
            multiline=False,
            input_filter="int"
        )

        month = TextInput(
            text=current.strftime("%m"),
            hint_text="Месяц",
            multiline=False,
            input_filter="int"
        )

        year = TextInput(
            text=current.strftime("%Y"),
            hint_text="Год",
            multiline=False,
            input_filter="int"
        )

        layout.add_widget(
            day
        )

        layout.add_widget(
            month
        )

        layout.add_widget(
            year
        )

        ok = Button(
            text="Выбрать",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            ok
        )

        popup = Popup(
            title="Выберите дату",
            content=layout,
            size_hint=(0.8, 0.5)
        )

        def set_date(instance):

            try:

                date = datetime(
                    int(year.text),
                    int(month.text),
                    int(day.text)
                )

                value = date.strftime(
                    "%d.%m.%Y"
                )

                selected_date[0] = value

                button.text = (
                    f"📅 Дата: {value}"
                )

                popup.dismiss()

            except ValueError:

                pass

        ok.bind(
            on_release=set_date
        )

        popup.open()

    # =====================================================
    # ВЫБОР ВРЕМЕНИ
    # =====================================================

    def choose_time(
        self,
        button,
        selected_time
    ):

        try:

            current = datetime.strptime(
                selected_time[0],
                "%H:%M"
            )

        except ValueError:

            current = datetime.now()

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        hour = TextInput(
            text=current.strftime("%H"),
            hint_text="Часы",
            multiline=False,
            input_filter="int"
        )

        minute = TextInput(
            text=current.strftime("%M"),
            hint_text="Минуты",
            multiline=False,
            input_filter="int"
        )

        layout.add_widget(
            hour
        )

        layout.add_widget(
            minute
        )

        ok = Button(
            text="Выбрать",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(
            ok
        )

        popup = Popup(
            title="Выберите время",
            content=layout,
            size_hint=(0.8, 0.4)
        )

        def set_time(instance):

            try:

                h = int(hour.text)
                m = int(minute.text)

                if not 0 <= h <= 23:
                    return

                if not 0 <= m <= 59:
                    return

                value = (
                    f"{h:02d}:{m:02d}"
                )

                selected_time[0] = value

                button.text = (
                    f"🕐 Время: {value}"
                )

                popup.dismiss()

            except ValueError:

                pass

        ok.bind(
            on_release=set_time
        )

        popup.open()


# =========================================================
# ЗАПУСК
# =========================================================

if __name__ == "__main__":
    GrapeNotesApp().run()