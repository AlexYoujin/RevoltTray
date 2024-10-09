from PIL import Image, ImageDraw
import pystray
import pyaudio
import numpy as np
import threading
import time


def create_image(level):
    # Создание изображения для значка в зависимости от уровня громкости
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    if level > 70:  # Пример порога громкости
        draw.ellipse((10, 10, 54, 54), fill=(0, 255, 0))  # Зеленый
    elif level > 30:
        draw.ellipse((10, 10, 54, 54), fill=(255, 255, 0))  # Желтый
    else:
        draw.ellipse((10, 10, 54, 54), fill=(255, 0, 0))  # Красный

    return image


def monitor_microphone(icon):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                    frames_per_buffer=1024)  # Уменьшил значение frames_per_buffer

    while True:
        try:
            data = stream.read(1024)  # Используем то же значение, что и frames_per_buffer
            audio_data = np.frombuffer(data, dtype=np.int16)
            level = np.abs(audio_data).mean()  # Вычисление уровня звука
            icon.icon = create_image(level)  # Обновление иконки
            time.sleep(0.1)  # Можно немного увеличить время ожидания
        except OSError as e:
            print(f"Error reading audio data: {e}")


# Создание значка
icon = pystray.Icon("mic_level")
icon.icon = create_image(0)  # Установка начальной иконки

# Запуск потока для мониторинга микрофона
threading.Thread(target=monitor_microphone, args=(icon,), daemon=True).start()
icon.run()
