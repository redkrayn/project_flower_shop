flower_bouquets = {
    1: {
        "id": 1,
        "price": 350,
        "price_range": "до 500",
        "description": "Нежный букет из ромашек и гипсофилы",
        "image": "https://example.com/images/bouquet1.jpg",
        "occasion": "день рождения"
    },
    2: {
        "id": 2,
        "price": 450,
        "price_range": "до 500",
        "description": "Миниатюрный букет тюльпанов в упаковке",
        "image": "https://example.com/images/bouquet2.jpg",
        "occasion": "в школу"
    },
    3: {
        "id": 3,
        "price": 750,
        "price_range": "до 1000",
        "description": "Элегантный букет из 5 роз с зеленью",
        "image": "https://example.com/images/bouquet3.jpg",
        "occasion": "день рождения"
    },
    4: {
        "id": 4,
        "price": 950,
        "price_range": "до 1000",
        "description": "Яркий букет из гербер и хризантем",
        "image": "https://example.com/images/bouquet4.jpg",
        "occasion": "в школу"
    },
    5: {
        "id": 5,
        "price": 1500,
        "price_range": "до 2000",
        "description": "Роскошный букет из 11 роз в коробке",
        "image": "https://example.com/images/bouquet5.jpg",
        "occasion": "без повода"
    },
    6: {
        "id": 6,
        "price": 1800,
        "price_range": "до 2000",
        "description": "Экзотический букет из орхидей и калл",
        "image": "https://example.com/images/bouquet6.jpg",
        "occasion": "день рождения"
    },
    7: {
        "id": 7,
        "price": 2500,
        "price_range": "свыше 2000",
        "description": "Премиальный букет из 101 розы с доставкой",
        "image": "https://example.com/images/bouquet7.jpg",
        "occasion": "свадьба"
    },
    8: {
        "id": 8,
        "price": 3500,
        "price_range": "свыше 2000",
        "description": "Эксклюзивный букет из редких сортов пионов",
        "image": "https://example.com/images/bouquet8.jpg",
        "occasion": "без повода"
    }
}


def get_occasion(flower_bouquets: dict) -> list:
    return list(set(bouquet['occasion'] for bouquet in flower_bouquets.values()))


def get_price_range(flower_bouquets: dict) -> list:
    return list(set(bouquet['price_range'] for bouquet in flower_bouquets.values()))
