# 🐞 ERROR_GUIDE.md – Vanliga fel & lösningar

**Syfte:**  
Här samlar vi återkommande fel, buggar och misstag – både för att underlätta felsökning och för att Claude ska kunna undvika dem i framtida kod.

> 🧠 **Instruktion till Claude:**  
Om du genererar kod som leder till fel (eller om du skriver kod för att hantera fel), **lägg till problemet och lösningen här**.

---

## 📌 Exempelfel

### ❌ Fel: `CORS policy: No ‘Access-Control-Allow-Origin’`

- **Orsak:** Frontend försöker anropa backend på en annan domän utan CORS-stöd.
- **Lösning:**  
Lägg till CORS-middleware i FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # eller specificera Vercel-URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
