def text_validator(text: str):
    if len(text.split()) < 2:
        raise ValueError('Текст должен содержать минимум два слова')

    if "превосходно" not in text and "роскошно" not in text:
        raise ValueError("Текст должен содержать слова превосходно или роскошно")