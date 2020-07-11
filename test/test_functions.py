def max_for_dicts(elements, key):
    if not elements:
        return
    max_key = elements[0][key]
    max_element = elements[0]

    for element in elements:
        if element['time'] > max_key:
            max_key = element[key]
            max_element = element

    return max_element
