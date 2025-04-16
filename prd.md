# Overview
Tradera Budassistent är en fullstack-webbapplikation designad för att automatisera processen för att övervaka, välja ut och (i framtiden) lägga bud på Tradera-auktioner. Applikationen syftar till att hjälpa användare att identifiera potentiellt undervärderade objekt och underlätta förvärv till fördelaktiga priser, särskilt för auktioner som avslutas vid obekväma tider.

Projektet är för närvarande i ett tidigt skede och har genererats av en AI. En initial granskning har visat att grundstrukturen finns men att implementationen är ofullständig och kräver en noggrann genomgång och baslinje-dokumentation (Steg 0) innan vidareutveckling kan ske på ett stabilt sätt.

# Core Features
De planerade huvudfunktionerna för den färdiga produkten inkluderar:

-   **Automatiserad Auktionssökning & Övervakning:** Konfigurera detaljerade sökkriterier (nyckelord, kategorier, prisintervall, etc.) och schemalägg automatiska sökningar på Tradera.
-   **Dashboard Gränssnitt:** Ett webbaserat gränssnitt för att hantera sökskript, granska funna auktioner, se statistik och (i framtiden) konfigurera budgivning.
-   **Centraliserad Auktionsdata:** Samla in och lagra relevant information om bevakade auktioner i en databas (Supabase).
-   **Statistik & Rapportering:** Visa översikter och statistik över bevakade auktioner, sökresultat och (i framtiden) budhistorik och framgångsgrad.
-   **Automatiserad Budgivning (Uppskjuten till Steg 6):** Möjlighet att konfigurera automatiska bud (maxpris) på utvalda auktioner, vilka sedan placeras via webbläsarautomatisering (Playwright) kort före auktionens slut.

# User Experience
-   **Målanvändare:** Skaparen av koden, enskild, användare i nuläget som vill automatisera och effektivisera sin auktionsbevakning och budgivning.
-   **Nyckelflöden:**
    1.  Användaren loggar in (via Clerk).
    2.  Användaren skapar/hanterar `SearchScript` i dashboarden.
    3.  Systemet kör skripten i bakgrunden och samlar `Auction`-data.
    4.  Användaren granskar funna auktioner i dashboarden.
    5.  Användaren ser statistik över sökningar och auktioner.
    6.  *(Framtida Steg 6)* Användaren väljer auktioner och konfigurerar `BidConfig` (maxbud).
    7.  *(Framtida Steg 6)* Systemet försöker placera bud automatiskt via Playwright.
-   **UI/UX Överväganden:** Tydligt, informativt och lättanvänt gränssnitt för att hantera komplexa sökningar och (senare) budinställningar. Visuell feedback på status för sökningar och bud.

# Technical Architecture
-   **Frontend:** React med TypeScript (mål), Vite, pnpm, Axios/fetch, Zod, Clerk (auth), Supabase client. Hosting: Vercel.
-   **Backend:** FastAPI (Python 3.13), Uvicorn, Pydantic, Supabase client (Python), python-dotenv, Clerk (JWT-verifiering). Hosting: Koyeb.
-   **Databas:** Supabase (PostgreSQL) med Row Level Security (RLS).
-   **Bakgrundsjobb:** Schemaläggning via Koyeb cron-jobb eller inbyggd lösning (t.ex. APScheduler).
-   **Budgivning (Steg 6):** Playwright (Python) för webbläsarautomatisering.
-   **Struktur:** Monorepo med separata `frontend/` och `backend/` kataloger.

# Development Roadmap
Utvecklingen sker i faser enligt den reviderade planen:

-   **Fas 0: Kodgranskning, Verifiering & Baslinje-Dokumentation (NUVARANDE FOKUS)**
    -   Mål: Skapa en verifierad, rensad och korrekt dokumenterad baslinje av den *befintliga* koden. Ingen ny funktionalitet.
    -   Aktiviteter: Iterativ kodgranskning, verifiering av beroenden/importer, uppdatering av befintlig dokumentation (`API_SPEC`, `DATA_MODEL`, `README`) till faktiskt nuläge, identifiering/borttagning av irrelevant kod.

-   **Fas 1: Verifiera & Implementera Databas**
    -   Mål: En korrekt uppsatt och fungerande databasstruktur i Supabase.
    -   Aktiviteter: Slutföra `schema.sql`, sätta upp tabeller, implementera grundläggande DB-interaktion i `db.py`, implementera RLS.

-   **Fas 2: Implementera Kärnlogik (Backend - Exkl. Playwright)**
    -   Mål: Fungerande API-endpoints för att hantera sökningar och grundläggande auktionsdata.
    -   Aktiviteter: Implementera Tradera API-anrop för sök/info, CRUD för `SearchScript` och `BidConfig`, integrera Clerk JWT-auth.

-   **Fas 3: Implementera Bakgrundstjänster (Exkl. Playwright)**
    -   Mål: Automatisk körning av sökningar och schemaläggning av (placeholder) bud.
    *   Aktiviteter: Sätta upp schemaläggning, implementera `Script Runner`, `BidScheduler`, initial `BidExecutor` (loggning/markering).

-   **Fas 4: Utveckla Frontend UI & Logik**
    -   Mål: Ett fungerande användargränssnitt för att hantera sökningar och se auktionsdata.
    *   Aktiviteter: Bygga UI-komponenter, implementera API-anrop, state management, UI för `SearchScript`/`BidConfig`.

-   **Fas 5: Dokumentation & Testning (Löpande under Fas 1-4 & 6)**
    -   Mål: Kontinuerligt uppdaterad dokumentation och testtäckning.
    *   Aktiviteter: Uppdatera `API_SPEC`/`DATA_MODEL`, skriva enhets-/integrationstester, underhålla `CHANGELOG`/`ERROR_GUIDE`.

-   **Fas 6: Implementera Budgivning via Playwright (Senare Fas)**
    -   Mål: Fungerande automatiserad budgivning.
    *   Aktiviteter: Utveckla Playwright-skript, integrera med `BidExecutor`, hantera resultat/fel.

# Logical Dependency Chain
Utvecklingsordningen är baserad på följande logiska beroenden:

1.  **Fas 0 (Baslinje)** är nödvändig för att säkerställa en stabil grund.
2.  **Fas 1 (Databas)** är fundamental för all datalagring.
3.  **Fas 2 (Backend Kärnlogik)** bygger på databasen och krävs för att hantera sökningar. Tradera API för sökning behövs här.
4.  **Fas 3 (Bakgrundstjänster)** automatiserar logiken från Fas 2 och kräver en fungerande databas och backend-logik.
5.  **Fas 4 (Frontend)** visualiserar och interagerar med data/logik från Fas 1, 2 och 3. Kräver fungerande API:er.
6.  **Fas 6 (Playwright Budgivning)** är den mest komplexa och fristående delen. Den bygger på att all annan infrastruktur (databas, backend-logik för `BidConfig`, frontend-UI) är på plats. Att skjuta upp detta minskar risk och initial komplexitet.
7.  **Fas 5 (Dokumentation/Testning)** är en kontinuerlig process som stödjer alla andra faser.

# Risks and Mitigations
-   **Risk:** Befintlig kodbas är mer ofullständig/felaktig än väntat.
    -   **Mitigation:** Grundlig genomgång och dokumentation i Fas 0. Var beredd på att skriva om/kasta delar av befintlig kod om den inte håller måttet.
-   **Risk:** Tradera ändrar sin webbplats/interna API:er, vilket bryter sökning eller (framtida) Playwright-budgivning.
    -   **Mitigation:** Bygg robust felhantering i API-interaktioner. Isolera Playwright-logiken (Fas 6). Ha beredskap för att behöva uppdatera skripten vid ändringar. Övervaka Traderas webbplats.
-   **Risk:** Komplexitet och bräcklighet i Playwright-automatisering (Fas 6).
    -   **Mitigation:** Skjut upp implementationen till sist. Noggrann testning. Logga utförligt. Informera användaren om potentiell instabilitet.
-   **Risk:** Säkerhet vid hantering av Tradera-inloggningsuppgifter för Playwright.
    -   **Mitigation:** Undersök säkra sätt att lagra och hantera känsliga uppgifter (t.ex. via secret management-tjänster). Implementeras först i Fas 6.
-   **Risk:** Scope creep – nya funktioner läggs till under utvecklingen.
    -   **Mitigation:** Håll fast vid den fasade planen. Nya krav hanteras genom en separat prioriteringsprocess och läggs eventuellt till *efter* den initiala planen är genomförd.

# Appendix
-   Ursprunglig PRD från AI: `.setup/internal_docs/tradera_assistant_prd.md`
-   Ursprungliga instruktioner: `.setup/internal_docs/manus_instructions.md`
-   Teknisk stack-definition: `.setup/internal_docs/tech_stack.md` 