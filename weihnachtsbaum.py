import random

def draw_christmas_tree(height):
    trunk_height = height // 4
    for i in range(1, height + 1):
        print(' ' * (height - i) + '*' * (2 * i - 1))
    
    for _ in range(trunk_height):
        print(' ' * (height - trunk_height) + '|' * (trunk_height * 2 - 1))

def draw_decorated_tree(height):
    trunk_height = height // 4
    max_width = 2 * height - 1  # Maximale Breite des Baumes
    for i in range(1, height + 1):
        spaces = ' ' * (height - i)
        stars = '*' * (2 * i - 1)
        decorations = ''
        for _ in range(max_width - len(stars)):
            if random.random() < 0.3:  # Wahrscheinlichkeit für Dekorationen
                decoration = random.choice(['o', 'I', 'x'])  # Zufällige Auswahl der Dekoration
                decorations += decoration
            else:
                decorations += ' '
        print(spaces + stars + decorations)
    
    for _ in range(trunk_height):
        print(' ' * (height - 1) + '|')
    
    print(' ' * (height - 1) + 'H')
    print(' ' * (height - 1) + 'H')
    print(' ' * (height - 1) + 'H')

def main():
    print("Bitte wählen Sie eine Variante des Weihnachtsbaums aus:")
    print("1. Variante 1")
    print("2. Variante 2")
    print("3. Variante 3")
    print("4. Variante 4")
    print("5. Grüner und bunt geschmückter Weihnachtsbaum")
    
    choice = int(input("Geben Sie die Nummer der Variante ein: "))
    
    if choice == 1:
        height = int(input("Geben Sie die Höhe des Baums (zwischen 5 und 40) ein: "))
        draw_christmas_tree(height)
    elif choice == 2:
        height = int(input("Geben Sie die Höhe des Baums (zwischen 5 und 40) ein: "))
        for i in range(1, height + 1):
            print(' ' * (height - i) + '*' * (2 * i - 1) + ' ' * (height - i))
    elif choice == 3:
        height = int(input("Geben Sie die Höhe des Baums (zwischen 5 und 40) ein: "))
        for i in range(1, height + 1):
            print(' ' * (height - i) + '*' * (i) + ' ' * (height - i))
    elif choice == 4:
        height = int(input("Geben Sie die Höhe des Baums (zwischen 5 und 40) ein: "))
        for i in range(1, height + 1):
            print(' ' * (height - i) + '*' * (i * 2 - 1) + ' ' * (height - i))
    elif choice == 5:
        height = int(input("Geben Sie die Höhe des Baums (zwischen 5 und 40) ein: "))
        draw_decorated_tree(height)
    else:
        print("Ungültige Auswahl")

if __name__ == "__main__":
    main()