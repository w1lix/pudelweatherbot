def degrees_to_direction(degrees):
    # Определяем список направлений ветра
    directions = ['северный', 'северно-восточный', 'восточный', 'юго-восточный',
                  'южный', 'юго-западный', 'западный', 'северо-западный']

    # Определяем количество направлений
    num_directions = len(directions)

    # Определяем размер сектора
    sector_size = 360 / num_directions

    # Определяем индекс направления
    direction_index = int((degrees + sector_size / 2) /
                          sector_size) % num_directions

    # Возвращаем текстовое описание направления
    return directions[direction_index]
