import pyperclip

isCharArray = False

text = pyperclip.paste().replace('[', '{').replace(']', '}').replace(',', ', ')
if isCharArray:
    text = text.replace('"', '\'')

print(text)
pyperclip.copy(text)
