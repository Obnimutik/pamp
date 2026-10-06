import tkinter as tk # Для создания графического интерфейса
from PIL import ImageTk, Image, ImageDraw # Для рисования кнопки-цветка
from PIL.ImageFont import ImageFont # Для текста внутри цветка
import random # Для имитации случайных ошибок насосов
import math # Для расчёта координат лепестков
from PIL import ImageShow # Для показа картинки

# Класс логики насоса
class PumpSystem:
    def __init__(self):
        # Уровень воды в баке от 0 до 4 (100%, 75%, 50%, 25%, 0%)
        self.level = 4
        # Счётчик циклов откачки
        self.cycles = 0

    def start(self):
        """Запускает цикл откачивания."""
        if self.level == 0:
            return "Ошибка: бак пуст."

        # Выбираем случайный резервуар для откачки (от 1 до 3).
        reserve = random.randint(1, 3)  # int(random.random() * 3) + 1 тоже подойдёт

        # Имитируем ошибку при откачке с вероятностью ~5%.
        # Это значит, что примерно раз на 20 попытка будет неудачной.
        error_chance = random.random()
        if error_chance < 0.05:
            return f"ОШИБКА! Резервуар {reserve} не сработал."

        # Успешная откачка
        self.level -= 1
        self.cycles += 1
        water_percent = self.level / 4 * 100
        return f"Уровень воды снизился. Осталось заполнить {int(water_percent)}%"

    # Класс главного окна программы
    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Насос с тремя резервами")
            # Запускаем систему из предыдущего блока
            self.pump = PumpSystem()

            # Создаём элементы управления
            tk.Label(self, text="Кол-во циклов:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
            self.lbl_cycles = tk.Label(self, font=("Arial", 16))  # Сюда будем выводить число циклов
            self.lbl_cycles.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

            tk.Label(self, text="Воды в баке:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
            self.lbl_water = tk.Label(self, fg="red", font=("Arial", 18))  # Счётчик воды
            self.lbl_water.grid(row=1, column=1, sticky="e", padx=10, pady=5)

            # Поле для вывода статуса операции
            self.lbl_status = tk.Label(self, fg="blue", wraplength=250)
            self.lbl_status.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

            # Наша красивая кнопка-цветок!
            btn_start = FlowerButton(self, text="ПУСК", command=self.on_click)
            btn_start.grid(row=3, column=0, columnspan=2, pady=10)

            # Рисуем сам бак
            self.canvas = tk.Canvas(width=170, height=250, bg="#e0e0e0")
            self.draw_tank(4)  # Изначально бак полон
            self.canvas.grid(row=4, column=0, columnspan=2, pady=10)

        # Обработчик нажатия кнопки ПУСК
        def on_click(self):
            result = self.pump.start()  # Вызываем метод из класса PumpSystem
            self.update_ui(result)

        # Метод перерисовки интерфейса после каждого действия
        def update_ui(self, status_text):
            water_percent = self.pump.level / 4 * 100

            # Меняем цвет текста "Воды в баке" в зависимости от уровня
            color = "#00cc00" if water_percent > 25 else "red"

            # Перерисовываем уровень воды в баке
            self.canvas.delete("water")
            tank_height = 200
            fill_height = tank_height * (water_percent / 100)
            y_bottom = 210 - int(fill_height)
            self.canvas.create_rectangle(
                10, y_bottom, 160, 210,
                fill="blue",
                width=0,
                tags="water"
            )
            self.lbl_cycles.config(text=f"Кол-во циклов: {self.pump.cycles}")
            water_percent = self.pump.level / 4 * 100
            color = "#00cc00" if water_percent > 25 else "red"
            self.lbl_water.config(
                text=f"Воды в баке: {int(water_percent)}%", fg=color)
            self.lbl_status.config(text=status_text)

            # Обновление светофора
            if self.pump.level == 4:
                self.green_light.itemconfig(1, fill="#4CAF50")
                self.yellow_light.itemconfig(1, fill="#fffbea")
                self.red_light.itemconfig(1, fill="#ffebee")
            elif self.pump.level in [3, 2]:
                self.green_light.itemconfig(1, fill="#d9ffc8")
                self.yellow_light.itemconfig(1, fill="#FFC107")
                self.red_light.itemconfig(1, fill="#ffebee")
            else:
                self.green_light.itemconfig(1, fill="#d9ffc8")
                self.yellow_light.itemconfig(1, fill="#fffbea")
                self.red_light.itemconfig(1, fill="#f44336")
            self.lbl_cycles.config(text=f"Кол-во циклов: {self.pump.cycles}")
            self.lbl_water.config(text=f"Воды в баке: {int(water_percent)}%", fg=color)
            self.lbl_status.config(text=status_text)

            # Класс для кнопки с изображением цветка
            class FlowerButton(tk.Button):
                def __init__(self, master=None, **kwargs):
                    class App(tk.Tk):
                        def __init__(self):
                            def _on_hover(self, is_entering: bool):
                                """Меняет цвет рамки при наведении."""
                                if is_entering:
                                    self.config(bg="#ffebee")  # Светло-розовый фон при наведении
                                else:
                                    self.config(bg="SystemButtonFace")  # Возвращает стандартный системный цвет

                            def _on_click_animate(self, event=None):
                                """Анимация нажатия: уменьшение -> пауза -> возврат."""
                                current_size = 150  # Исходный размер
                                pressed_size = 130  # Размер во время "нажатия"

                                # Уменьшаем кнопку
                                self["image"] = self._create_flower_image(self["text"], size=pressed_size)
                                self.after(100, lambda: self._return_to_normal(current_size))

                            def _return_to_normal(self, normal_size=150):
                                """Возвращает кнопку к исходному размеру через паузу."""
                                self["image"] = self._create_flower_image(self["text"], size=normal_size)
                            super().__init__()
                            self.bind("<Enter>", lambda e: self._on_hover(True))  # При наведении курсора
                            self.bind("<Leave>", lambda e: self._on_hover(False))  # При уходе курсора
                            self.bind("<Button-1>", self._on_click_animate)  # При нажатии кнопки мыши
                            self.title("Насос с тремя резервами")
                            self.pump = PumpSystem()
                            self.update_ui("Программа запущена.")
                    text = kwargs.pop("text")

                    image = self._create_flower_image(text)  # Рисуем цветок

                    super().__init__(
                        master=master,
                        image=image,
                        compound=tk.CENTER,
                        relief=tk.FLAT,
                        borderwidth=0,
                        highlightthickness=0,
                        activebackground="#ffd9f2",
                        **kwargs
                    )
                    self.image = image

                import tkinter as tk  # Для создания графического интерфейса
                from PIL import ImageTk, Image, ImageDraw  # Для рисования кнопки-цветка
                from PIL.ImageFont import ImageFont  # Для текста внутри цветка
                from PIL import ImageShow  # Для показа картинки
                import math  # Для расчёта координат лепестков

                # ⚘️ Функция для рисования цветка
                def draw_flower(text="ПУСК", *, size=150):
                    img = Image.new("RGBA", (size, size), "#ffffff00")
                    draw = ImageDraw.Draw(img)

                    # Лепестки
                    for angle in range(0, 360, 60):
                        r_inner = int(size * 0.3)
                        r_outer = int(size * 0.6)

                        cx1 = size // 2 + int(r_inner * math.cos(math.radians(angle)))
                        cy1 = size // 2 + int(r_inner * math.sin(math.radians(angle)))
                        cx2 = size // 2 + int(r_outer * math.cos(math.radians(angle)))
                        cy2 = size // 2 + int(r_outer * math.sin(math.radians(angle)))

                        x1 = min(cx1, cx2)
                        y1 = min(cy1, cy2)
                        x2 = max(cx1, cx2)
                        y2 = max(cy1, cy2)

                        # ГРАДИЕНТ лепестков
                        gradient = Image.new("RGBA", (x2 - x1, y2 - y1))
                        for y in range(y2 - y1):
                            color = int(255 * ((y / (y2 - y1)) ** 2))
                        gradient.putpixel((0, y), (color, color + 70, color + 80, 255))
                        draw.bitmap((x1, y1), gradient)

                        # Серединка
                        draw.ellipse(
                            [size * 0.3, size * 0.3, size * 0.7, size * 0.7],
                            fill="#ffe680"
                        )

                        # Текст
                        font_size = int(size * 0.2)
                        font = ImageFont.load_default()
                        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
                        draw.text(
                            ((size - text_width) / 2, (size - text_height) / 2),
                            text,
                            font=font,
                            fill="white"
                        )

                    return img

                if __name__ == "__main__":
                    # Запускаем нашу функцию
                    flower_img = draw_flower(text="СТАРТ!", size=250)
                    ImageShow.show(flower_img)