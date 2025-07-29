mode = 'otherArray'

def convert(text):
    if mode == 'otherArray':
        text = text.replace('[', '{').replace(']', '}').replace(',', ', ')
    elif mode == 'charArray':
        text = text.replace('[', '{').replace(']', '}').replace(',', ', ').replace('"', '\'')
    return text


input_file = open('input.txt', encoding='UTF-8')
output_file = open('output.txt', 'w', encoding='UTF-8')

for text in input_file.readlines():
    if text[0] != '[':
        mode = text[:-1]
    else:
        output_file.write(convert(text))

input_file.close()
output_file.close()
