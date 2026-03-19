# Evidence Index

Master index of all documented evidence.

---

## CRITICAL FINDINGS

| ID | Date | Description | File |
|----|------|-------------|------|
| IMG_0277 | 2026-03-19 | **CRITICAL:** Synergy/DISM active interception during Windows install | [dism-synergy-interception-2026-03-19.md](dism-synergy-interception-2026-03-19.md) |

---

## Evidence Images (Session 2026-03-19)

| Image | Description | Status |
|-------|-------------|--------|
| IMG_0270 | Registry file - 54 second scroll (mass UID injection) | Documented in DISM finding |
| IMG_0271 | Measwell evidence batch | Logged |
| IMG_0272 | Measwell evidence batch | Logged |
| IMG_0273 | Timing context evidence | Logged |
| IMG_0274 | Timing context evidence | Logged |
| IMG_0275 | Evidence batch | Logged |
| IMG_0276 | Evidence batch | Logged |
| **IMG_0277** | **Synergy/DISM critical** | **FULLY DOCUMENTED** |

Total: 21 images logged in session

---

## Attack Pattern Summary

### Registry UID Attack
- **Method:** Mass injection of 100s of entries around known UIDs
- **Tracer UIDs:** 33554432 (0x02000000), 50331648 (0x03000000), 51150848 (0x030D0000)
- **Evidence:** 54-second scroll time in registry export

### Active Interception During Install
- **Method:** Synergy + multiple binaries during DISM phase
- **Evidence:** IMG_0277
- **Impact:** Real-time control during Windows deployment

### Network Persistence
- **Suspicious IPs:** 109.61.19.21:80 (G-Core Labs London), 85.234.74.60:80
- **Evidence:** Mini-Tank-MKII first boot connections

---

## Image URLs

For reference, the GitHub-hosted evidence images:

```
IMG_0270: https://github.com/user-attachments/assets/f6af2b04-403a-49f7-ab5f-15c338e07905
IMG_0271: https://github.com/user-attachments/assets/364dec41-5c8c-4af8-a472-5b020a75662e
IMG_0272: https://github.com/user-attachments/assets/5210dbb7-b05d-468c-927c-6c527ed2df29
IMG_0273: https://github.com/user-attachments/assets/9e977fb3-e06e-437a-9feb-3a6f87a9aba8
IMG_0274: https://github.com/user-attachments/assets/92d36d05-6dbc-4ebc-b428-07e670934902
IMG_0275: https://github.com/user-attachments/assets/dfe8392a-8e60-45ab-b835-505f89c99908
IMG_0276: https://github.com/user-attachments/assets/278e8845-0358-4136-8f9d-9b84f2fb92f9
IMG_0277: https://github.com/user-attachments/assets/fd757bc4-9b87-4b35-b0e2-42003586e80f
```

---

*Last updated: 2026-03-19*
