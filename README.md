# How to Run:

Du kommer måsta ha python installerat (duh), för att köra skriptet sen ska du först installera alla dependencies med hjälp av `pip install playwright beautifulsoup4 requests pillow`, och sedan kör du `python -m playwright install
` en gång. Sedan efter är det bara att köra `python scraper.py`

Är du på Linux måste du göra en virtual environment, det gör du via `python -M venv DORK`, sedan går du in i den med `source DORK/bin/activate`.

För att få alla data från alla spel så är det literally så enkelt som att klistra in alla BGG länkar i `input.txt`, köra `python scraper.py`, och sedan har du all data formatterad i `output.txt` med bilder av spelen i `images/` döpta i nummerordningen du angav spelen i. Så om din ordning var t.ex. Brass, Shobu, Root, så kommer de få bilderna 000.png, 001.png, 002.png, osv.

Sedan är det bara att copy-pastea in i google forms, och det här lär spara typ 4 arbetsdagar i att göra allt manuellt. (Future improvement kanske är att sitta i google api och ha sig ;)))

Tagga DORK! :D
