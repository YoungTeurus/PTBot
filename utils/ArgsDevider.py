from properties import ArgsDevider


def splitArgs(input: str) -> list[str]:
    quotationMark = ArgsDevider.quotationMark

    output = []

    isInQuotation = False
    start = 0
    inputLen = len(input)
    for i, ch in enumerate(input):
        # Если пробел вне кавычек:
        if ch == ' ' and not isInQuotation:
            # Не добавляем пустые строки
            if i - start > 1:
                output.append(input[start:i])
            start = i + 1
            continue
        if ch == quotationMark:
            if not isInQuotation:
                # Если первая кавычка - заключающая в строке
                if i + 1 == inputLen:
                    raise Exception("Input string '{}' contains not closed quotation mark".format(input))
                # Если первая кавычка в середине строки:
                isInQuotation = True
                start = i + 1
            else:
                # Если вторая кавычка - заключающая в строке
                if i + 1 == inputLen:
                    output.append(input[start:i])
                    break
                # Если вторая кавычка на конце аргумента:
                if input[i+1] == ' ':
                    output.append(input[start:i])
                    isInQuotation = False
                    start = i + 1
                # Если вторая кавычка посреди строки:
                else:
                    raise Exception("Input string '{}' contains wrongly placed quotation mark (index = {})".format(input, i))
        if i + 1 == inputLen:
            if isInQuotation:
                raise Exception("Input string '{}' contains not closed quotation mark".format(input))
            output.append(input[start:i + 1])

    return output

# Тесты
if __name__ == "__main__":
    ArgsDevider.quotationMark = '"'

    print(splitArgs(""))
    print(splitArgs("op"))
    print(splitArgs("op Teurus"))
    print(splitArgs("op Teu rus"))
    print(splitArgs("op \"\""))
    print(splitArgs("op \" \""))
    print(splitArgs("op \"Teurus\""))
    print(splitArgs("op \"Teu rus\""))
    print(splitArgs("op \"Teurus\" 1hr"))
    print(splitArgs("op \" Teurus\" 1hr"))
    print(splitArgs("op \"Teurus \" 1hr"))
    print(splitArgs("op \" Teurus \" 1hr"))
    print(splitArgs("op \"Teu rus\" 1hr"))
    print(splitArgs("op \"Teu rus\" 1hr \"2hr\" 3hr"))
    print(splitArgs("op \"Teu rus\" 1hr 2hr \"3hr\""))
    print(splitArgs("op \"Teu rus\" 1hr 2hr \"3hr\" "))
    try:
        print(splitArgs("op \"Teu rus 1hr 2hr 3hr "))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)
    try:
        print(splitArgs("op \"Teurus 1hr 2hr \"3 hr\""))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)
    try:
        print(splitArgs("op \"Teurus 1hr 2hr \"3 hr\" "))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)
    try:
        print(splitArgs("op \"Teurus 1hr 2hr \"3 hr\" abac"))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)
    try:
        print(splitArgs("op \"Teurus 1hr 2hr \" 3 hr\" abac"))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)

    ArgsDevider.quotationMark = '$'
    print("Замена знака выделения на '$'")

    print(splitArgs(""))
    print(splitArgs("op"))
    print(splitArgs("op Teurus"))
    print(splitArgs("op Teu rus"))
    print(splitArgs("op $$"))
    print(splitArgs("op $ $"))
    print(splitArgs("op $Teurus$"))
    print(splitArgs("op $Teu rus$"))
    print(splitArgs("op $Teurus$ 1hr"))
    print(splitArgs("op $ Teurus$ 1hr"))
    print(splitArgs("op $Teurus $ 1hr"))
    print(splitArgs("op $ Teurus $ 1hr"))
    print(splitArgs("op $Teu rus$ 1hr"))
    print(splitArgs("op $Teu rus$ 1hr $2hr$ 3hr"))
    print(splitArgs("op $Teu rus$ 1hr 2hr $3hr$"))
    print(splitArgs("op $Teu rus$ 1hr 2hr $3hr$ "))
    try:
        print(splitArgs("op $Teu rus 1hr 2hr 3hr "))
        print("ОШИБКА! ПРЕДЫДУЩИЙ ВЫВОД ОШИБОЧНЫЙ")
    except BaseException as ex:
        print(ex)
    print(splitArgs("op $Teurus 1hr 2hr \"3 hr$"))
    print(splitArgs("op $Teurus 1hr 2hr \"3 hr$ "))
    print(splitArgs("op $Teurus 1hr 2hr \"3 hr$ abac"))
    print(splitArgs("op $Teurus 1hr 2hr \" 3 hr$ abac"))
