# Overview
Detta dokument beskriver **Fas 0: Kodgranskning, Verifiering & Baslinje-Dokumentation** för projektet Tradera Budassistent. Fasen fokuserar uteslutande på att analysera, verifiera och dokumentera den *befintliga* AI-genererade kodbasen.

**Syfte:** Att skapa en pålitlig, korrekt och väldokumenterad baslinje som utgångspunkt för efterföljande utvecklingsfaser (Fas 1-6). Ingen ny funktionalitet kommer att utvecklas under denna fas.

**Problem som löses i denna fas:** Osäkerhet kring den befintliga kodens status, korrekthet, fullständighet och dokumentation. Risk för att bygga vidare på en instabil eller felaktig grund.

**Värde:** Ökad förståelse, minskad risk för framtida omarbete, tydligt definierat utgångsläge för vidareutveckling, säkerställande att återanvändbar kod identifieras och verifieras.

# Core Features (of Phase 0)
"Funktionerna" i denna fas är de aktiviteter som krävs för att uppnå målet:

-   **Kodbasinventering & Rensning:**
    -   *Vad:* Systematisk genomgång av all kod i `frontend/` och `backend/`.
    -   *Varför:* Förstå befintlig struktur, identifiera potentiella problem och upptäcka oanvänd/irrelevant kod.
    -   *Hur:* Manuell kodgranskning, analys av filstruktur och modulinteraktioner.

-   **Beroende- & Importverifiering:**
    -   *Vad:* Kontrollera att alla externa paket (`package.json`, `requirements.txt`) och interna importer fungerar korrekt.
    -   *Varför:* Säkerställa att projektet kan byggas och köras i sitt nuvarande skick och att kopplingarna mellan moduler är korrekta.
    -   *Hur:* Köra installationskommandon (`pnpm install`, `uv pip install`), statisk analys (via linters om möjligt), manuell granskning av import-satser.

-   **Baslinje-Dokumentationsuppdatering:**
    -   *Vad:* Uppdatera befintliga dokument (`API_SPEC.md`, `DATA_MODEL.md`, `README.md`) så att de korrekt reflekterar den *faktiska* implementationen efter granskning.
    -   *Varför:* Skapa en sann och pålitlig bild av systemets nuvarande tillstånd som kan användas i kommande faser.
    -   *Hur:* Modifiera markdown-filerna baserat på resultaten från kodinventeringen och verifieringen.

-   **Funktionell Grundtestning (Smoke Testing):**
    -   *Vad:* Verifiera att de mest grundläggande funktionerna i den befintliga koden fungerar som förväntat (inom ramen för vad som är implementerat).
    -   *Varför:* Få en grundläggande uppfattning om systemets stabilitet och identifiera uppenbara kritiska fel.
    -   *Hur:* Starta backend- och frontend-servrarna, anropa grundläggande API-endpoints (t.ex. `/health`), ladda grundläggande frontend-vyer.

# User Experience (for Phase 0)
-   **Primär "Användare":** Utvecklaren/teamet som ska genomföra Fas 1-6.
-   **Användarresa/Upplevelse:**
    1.  Börjar med en oklar bild av kodbasens kvalitet och status.
    2.  Genomför systematiskt gransknings- och verifieringsaktiviteterna.
    3.  Dokumenterar löpande fynd och korrigerar befintlig dokumentation.
    4.  Avslutar fasen med en klar, faktabaserad förståelse av kodbasen och ökad tilltro till det som ska återanvändas.
-   **UI/UX:** Inte tillämpbart i traditionell mening. Fokus ligger på tydlighet i dokumentationen och en strukturerad arbetsprocess.

# Technical Architecture (as relevant to Phase 0)
-   **Fokus:** Att *verifiera* och *dokumentera* den faktiska tekniska implementationen.
-   **Förväntad Arkitektur (att verifiera):**
    -   Frontend: React, Vite, pnpm, Clerk, Supabase client.
    -   Backend: FastAPI, Uvicorn, Pydantic, Supabase client (Python), Clerk JWT.
    -   Databas: Supabase (PostgreSQL).
-   **Verktyg för Fas 0:** Manuell kodgranskning, terminalkommandon (installation, serverstart), befintliga linters (ESLint, Ruff om konfigurerade), textredigerare för dokumentation.

# Development Roadmap (within Phase 0)
Fasen genomförs iterativt tills alla punkter är uppfyllda:
1.  **Initial Översikt:** Grov genomläsning av huvudfiler (`main.py`, `App.jsx`, router-filer, databas-filer) för att få en känsla för strukturen.
2.  **Beroendekontroll:** Kör `pnpm install` i `frontend/` och `uv pip install -r requirements.txt` i `backend/`. Åtgärda eventuella installationsfel.
3.  **Serverstart-verifiering:** Försök starta backend (`uvicorn main:app`) och frontend (`pnpm dev`). Åtgärda uppenbara startproblem.
4.  **Backend Granskning & Dokumentation:**
    -   Detaljerad granskning av `main.py`, `db.py`, `models.py`, `tradera_api.py`, `routes/*.py`.
    -   Verifiera interna importer.
    -   Uppdatera `docs/API_SPEC.md` med *faktiskt* implementerade endpoints och deras struktur.
    -   Uppdatera `docs/DATA_MODEL.md` baserat på `models.py` och (om möjligt) verifiering mot `schema.sql`.
5.  **Frontend Granskning & Dokumentation:**
    -   Detaljerad granskning av `main.jsx`, `App.jsx`, `components/`, `pages/`, `api/` (om den finns), `contexts/`.
    -   Verifiera interna importer och beroenden (t.ex. Clerk, React Router).
    -   Notera eventuella avvikelser (t.ex. `.jsx` vs `.tsx`).
6.  **README Uppdatering:** Säkerställ att instruktionerna i `README.md` för installation och start är korrekta och fungerar efter verifieringarna ovan.
7.  **Kodrensning:** Identifiera och diskutera/ta bort uppenbart död, duplicerad eller irrelevant kod.
8.  **Slutlig Check:** Säkerställ att all dokumentation som uppdaterats är konsekvent och korrekt återspeglar kodbasens verifierade tillstånd.

# Logical Dependency Chain (within Phase 0)
1.  Beroendekontroll är grundläggande för att kunna köra/analysera koden.
2.  Serverstart-verifiering ger en första indikation på grundläggande funktion.
3.  Detaljerad kodgranskning (backend/frontend) är nödvändig för att förstå implementationen.
4.  Dokumentationsuppdatering måste ske *efter* granskning av respektive del för att vara korrekt.
5.  Kodrensning bör ske efter fullständig granskning för att undvika att ta bort något nödvändigt.

# Risks and Mitigations (for Phase 0)
-   **Risk:** Kodens kvalitet är mycket låg, vilket gör granskningen tidskrävande och svår.
    -   **Mitigation:** Budgetera tillräckligt med tid. Fokusera på att förstå *vad* koden försöker göra, även om *hur* är dåligt. Var beredd på att mycket kan behöva skrivas om i senare faser.
-   **Risk:** Dokumentationen blir snabbt inaktuell igen om inte uppdateringar sker disciplinerat.
    -   **Mitigation:** Uppdatera relevant dokumentationsavsnitt direkt efter att en kodmodul/fil har granskats och verifierats.
-   **Risk:** Dolda fel eller beroenden som inte upptäcks under denna fas.
    -   **Mitigation:** Denna fas syftar till en *baslinje*, inte en fullständig buggfri garanti. Fokusera på struktur, beroenden och dokumentation. Djupare funktionella tester kommer i senare faser.
-   **Risk:** Otydlig logik i AI-genererad kod.
    -   **Mitigation:** Lägg tid på att förstå. Om nödvändigt, lägg till tillfälliga kommentarer eller utför minimal refaktorering *enbart för läsbarhet* (utan att ändra funktionalitet).

# Appendix
-   Referens till övergripande projektplan finns i tidigare konversation/diskussion (se `prd.txt` som skapades tidigare, även om den raderades).
-   Ursprungliga kravdokument: `.setup/internal_docs/tradera_assistant_prd.md`, `.setup/internal_docs/manus_instructions.md`
-   Teknisk stack-definition: `.setup/internal_docs/tech_stack.md` 