# 🧬 DATA_MODEL.md – Datamodeller och strukturer

**Syfte:**  
Här dokumenteras alla databastabeller, modeller och scheman i systemet. Claude och utvecklare använder detta för att hålla koll på fält, relationer och datatyper.

> 🧠 **Instruktion till Claude:**  
Varje gång du skapar eller ändrar en datamodell, **uppdatera detta dokument** automatiskt. Lägg till datatyper och validering.

---

## 📌 Exempelmodell

### Modell: `User`

| Fält       | Typ        | Validering / Notering           |
|------------|------------|----------------------------------|
| `id`       | Integer    | Primärnyckel, autoinkrement     |
| `email`    | String     | Unik, krävs, e-postvalidering   |
| `name`     | String     | Obligatorisk                    |
| `created_at` | DateTime | Genereras automatiskt           |

---

## 🧱 Aktuella modeller

*(Lägg till här under projektets gång)*
