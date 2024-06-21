import requests

#   Funkcja która pobiera numery z pliku txt i w przypadku niepoprawnego formatu informuje w konsoli i pomija linijkę
def getNumber(path):
    file = open(path, 'r')
    numbers = []
    i = 0

    for line in file:
        i += 1
        line = line.strip()

        try:
            number = int(line)
            numbers.append(number)

        except ValueError:
            print(f'Niepoprawny numer w linijce {i}: "{line}"')
            continue

    return numbers

#   Funkcja która na podstawie podanych numerów zwraca url obrazka po sfetchowaniu jsona
def fetchMetadata(numbers):
    metadatas = []

    for number in numbers:
        url = f"https://xkcd.com/{number}/info.0.json"
        response = requests.get(url)

        if response.status_code == 200:
            metadata = response.json()

            if metadata:
                metadatas.append([metadata.get("img"),(metadata.get("alt"))])

        else:
            print(f"Nie udało się uzyskać metadanych komiksu {number}")

    return metadatas


#   Funkcja która tworzy plik html dodając do niego obrazki z wcześniej utworzonej listy url'ów
#   z użyciem klasy img-fluid w celu ustalenia responsywności obrazków
def createHTML(metadatas):
    images = "\n"

    for metadata in metadatas:
        images += f'<div class="col-md-12 d-flex justify-content-center align-items-center"><img src="{metadata[0]}" class="img-fluid mb-3" alt="{metadata[1]}"></div>\n'
    
    content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Komiksy</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    {images}
</body>
</html>"""
    
    file = open("index.html", 'w')
    file.write(content)
    print("Plik HTML poprawnie utworzony")


numbers = getNumber("nr.txt")
images = fetchMetadata(numbers)

createHTML(images)