import pandas as pd

# Расширяем вывод таблицы
pd.set_option('display.width', 0)


def caesar_shift_rus(text, shift):
    result = []
    for ch in text:
        lower = ch.lower()
        if lower in rus_alphabet:
            old_index = rus_alphabet.index(lower)
            new_index = (old_index - shift) % len(rus_alphabet)
            new_ch = rus_alphabet[new_index]
            if ch.isupper():
                new_ch = new_ch.upper()
            result.append(new_ch)
        else:
            result.append(ch)
    return "".join(result)


def caesar_shift_eng(text, shift):
    result = []
    for ch in text:
        lower = ch.lower()
        if lower in eng_alphabet:
            old_index = eng_alphabet.index(lower)
            new_index = (old_index - shift) % len(eng_alphabet)
            new_ch = eng_alphabet[new_index]
            if ch.isupper():
                new_ch = new_ch.upper()
            result.append(new_ch)
        else:
            result.append(ch)
    return "".join(result)


def score_decoding(text):
    """
    Считаем, сколько раз встречаются слова из address_dictionary.
    """
    count = 0
    for word in address_dictionary:
        if word in text:
            count += 1
    return count


def decode_line_address(line):
    """
    Перебираем ВСЕ сдвиги для рус алф и выбираем тот, который даёт максимальный «score_decoding».
    Результат
      - best_text: лучшая расшифровка
      - best_code: тот сдвиг, при котором score_decoding максимален
    """
    best_text = line
    best_code = 0
    best_score = -1

    # Перебираем все сдвиги от 1 до длины русского алфавита
    for shift in range(1, len(rus_alphabet)):
        shifted = caesar_shift_rus(line, shift)
        s = score_decoding(shifted)
        if s > best_score:
            best_score = s
            best_text = shifted
            best_code = shift

    return best_text, best_code


def main(filename):
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        exit(1)

    address_list = df["Адрес"].tolist()
    email_list = df["email"].tolist()
    all_results = []

    for addr_original, email_original in zip(address_list, email_list):

        # Ищем лучший сдвиг для адреса
        addr_decoded, addr_code = decode_line_address(addr_original)

        # Используем тот же сдвиг, но для почты
        email_decoded = caesar_shift_eng(email_original, addr_code)

        all_results.append({
            "Адрес": addr_decoded,
            "Email": email_decoded,
            "Код": addr_code
        })

    # Формируем DataFrame и выводим
    df_results = pd.DataFrame(all_results)
    df_results.to_csv("decrypted.csv", index=False)
    print(df_results)


if __name__ == "__main__":

    rus_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    eng_alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Добавляем известные слова для столбца «Адрес»
    address_dictionary = {
        "ул.", "улица",
        "кв.", "квартира",
        "дом", "д.",
        "пр.", "проспект",
        "шоссе", "ш.",
        "пер.", "переулок",
        "к.", "корп.", "корпус",
        "область", "обл.",
        "город", "г.", "гор."
    }
    main("encrypted.csv")
