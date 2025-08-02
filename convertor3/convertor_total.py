import convertor_java

def set_types(page, lang):
    if lang == 'Java':
        convertor_java.set_types(page)

def convert(input_elems, lang):
    if lang == 'Java':
        return convertor_java.convert(input_elems)
