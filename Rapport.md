# Rapport — ScanTrack AB: Containerisera och deploya din nod

**Grupp:** Consuela
**Deltagare:** Sebastian G / M
**Datum:**  2026/09/06
**Namn:** Sebastian Moscoso
---

## 1. Arkitektur

Byggde om allt från scratch från C# till Python (reverse engineered) -> bröt ned koden för att sedan kunna bygga upp det igen i python -> docker build -> gjorde test runs lokalt för att se att våran image
fungerade korrekt -> deployade våran image till azure via CLI -> testkörde image för att se att vi fick positiv respons av andra städer -> happy days.

```
Exempel:
Dockerfile (multi-stage) → docker build → ACR push → ACI deploy → publik IP
```

---

## 2. NODE_URL-problemet

Problemet löste sig att istället för att låta CLI:T ändra våran ip-address så gav vi den ett dns namn när vi skapade containergruppen. fördel med detta är att adressen blir mer lättläst samt
att man inte blir beroende av den tilldelade azure ipaddressen. 

---

## 3. Bevis
![Node ipadress](/image.png)

![Paket som skickas](/image_paket.png)

![Status](/image_status.png)




---

## 4. Ansvarsområden

Vi satt och arbetade ihop då vi bor tillsammans, Gonzales drog större last eftersom han är den som är den kunniga inom python av oss två och jag såg 
en möjlighet att få lära mig att koda lite med Python och få lära mig utav honom. men timmarna gjordes tillsammans och vi arbetade inte enskilt.


## Individuell reflektion

_Varje gruppmedlem lämnar in sin egen reflektion. Ska vara personlig — inte kopierad från gruppen._

- **Vad var svårast?**  Python/ CLI delen för docker.
- **Vad förstår du nu som du inte förstod innan?**  Python, och lite mer förståelse för Docker och hur man sätter upp resursen via CLI
- **Vad skulle du ha gjort annorlunda?**  Python tog många timmar ifrån oss där vi kunde ha fokuserat på själva Docker delen. Annars var det en bra erfarenhet och jag hade gjort likadant
  om vi hade haft lite mera tid på oss för att kunna verkligen sätta sig ner och försöka förstå mera utav Python.
- **Hur planerades projektet?**  Vi planerade ihop och kom överens om vad vi skulle göra när vi satt ihop. alla beslut har tagits tillsammans och i gruppmentalitet.
- **Hur fungerade sambarbetet?**  Jag och Gonza kommer bra överens och samarbetar bra.