# 📘 API_SPEC.md – API-specifikation

**Syfte:**  
Detta dokument innehåller en översikt över samtliga API-endpoints i projektet. Det hjälper både utvecklare och Claude att förstå strukturen, vad som krävs för varje endpoint, och vad som returneras.

> 🧠 **Instruktion till Claude:**  
Varje gång du skapar, ändrar eller raderar en endpoint, **uppdatera detta dokument** automatiskt. Beskriv även headers, URL, metoder och payload.

---

## 📌 Exempelstruktur

### [GET] `/api/users/{id}`

- **Beskrivning:** Hämtar användarinformation baserat på ID.
- **Request:**
    - URL-parametrar: `id` (int)
    - Headers: `Authorization: Bearer <token>`
- **Response:**  
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Ada Lovelace"
}

Statuskoder: 200 OK, 404 Not Found, 401 Unauthorized