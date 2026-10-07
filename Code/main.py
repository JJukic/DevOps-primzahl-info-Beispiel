from fastapi import FastAPI            # Importiert die FastAPI-Klasse, um eine Web-API zu erstellen
from pydantic import BaseModel         # Importiert die BaseModel-Klasse für Daten-Validierung und -Serialisierung
from typing import Optional            # Für optionale Felder im Response-Typ

# Hilfsfunktionen für Primzahl-Logik
def ist_primzahl(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def naechste_primzahl(n: int) -> int:
    k = n + 1
    while not ist_primzahl(k):
        k += 1
    return k

# Definiert das Eingabe-Schema der API: erwartet ein JSON mit dem Feld 'zahl'
class ZahlRequest(BaseModel):
    zahl: int                           # Die zu prüfende ganze Zahl

# Definiert das Ausgabe-Schema der API
class PrimzahlResponse(BaseModel):
    zahl: int                           # Die Eingabezahl
    ist_prim: bool                      # True, wenn Primzahl
    naechste_primz: Optional[int] = None # Nächste Primzahl, falls keine Primzahl eingegeben wurde

# Erstellt eine FastAPI-Applikation mit dem Titel "PrimzahlCheckerAPI"
app = FastAPI(title="PrimzahlCheckerAPI")

# Definiert einen GET-Endpunkt unter "/" für die Root-URL, der eine einfache JSON-Nachricht zurückgibt
@app.get("/")
async def root():
    return {"message": "PrimzahlCheckerAPI läuft"}

# Deklariert einen POST-Endpunkt unter "/primzahl-check"
# response_model sorgt dafür, dass die Antwort dem PrimzahlResponse-Schema entspricht
@app.post("/primzahl-check", response_model=PrimzahlResponse)
async def primzahl_checker(req: ZahlRequest):
    # Prüft, ob die Zahl eine Primzahl ist
    prim = ist_primzahl(req.zahl)

    # Falls nicht, berechnet die Funktion die nächste Primzahl
    next_p = None if prim else naechste_primzahl(req.zahl)

    # Gibt eine Instanz von PrimzahlResponse zurück, die automatisch zu JSON serialisiert wird
    return PrimzahlResponse(
        zahl=req.zahl,
        ist_prim=prim,
        naechste_primz=next_p
    )
