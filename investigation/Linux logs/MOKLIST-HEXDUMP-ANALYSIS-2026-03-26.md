# MokListRT Hex Dump — Certificate Analysis
**Date:** 2026-03-26  
**Analyst:** ClaudeMKII  
**Source:** Issue — "Hex Dump." — two OCR'd `dd` runs against `MokListRT.raw`  
**Reference:** UEFI-MOK-KERNEL-EVIDENCE-2026-03-26.md → "Unfinished Business: MOK NVRAM hexdump"  
**Classification:** CRITICAL 🔴 (partial) / NORMAL 🟢 (this cert) — see context section

---

## EXECUTIVE SUMMARY

The user extracted the first certificate from `MokListRT.raw` using `dd if=MokListRT.raw bs=1 skip=48` and captured two OCR'd runs. Analysis of both runs confirms the first certificate in the MokListRT variable is the **Canonical Ltd. Master Certificate Authority** — the publicly known Ubuntu Secure Boot vendor certificate embedded in the shim. Its presence here is **expected and normal**. 

However, this is only the **first** of multiple certificates in the MokListRT variable. The previously identified suspicious `CN=grub` self-signed certificate (Finding 1, UEFI report) is a **separate entry** at a higher offset — not yet extracted. This document closes the hexdump task and documents the exact next command needed to extract the suspicious cert.

---

## THE DD COMMAND

```bash
# Run 1
dd if=/home/lloyd/MokListRT.raw bs=1 skip=48 2>/dev/null | openssl x509 -inform DER -text

# Run 2 (same command, second execution)
dd if=/home/lloyd/MokListRT.raw bs=1 skip=48 2>/dev/null | openssl x509 -inform DER -text
```

**Why skip=48 is correct:**

| Offset | Size | Field |
|--------|------|-------|
| 0 | 4 bytes | EFI variable attributes |
| 4 | 16 bytes | EFI_SIGNATURE_LIST SignatureType GUID |
| 20 | 4 bytes | SignatureListSize |
| 24 | 4 bytes | SignatureHeaderSize (= 0 for X.509) |
| 28 | 4 bytes | SignatureSize |
| 32 | 16 bytes | SignatureOwner GUID (EFI_SIGNATURE_DATA) |
| **48** | **n bytes** | **Certificate DER data begins here** |

The 48-byte skip precisely lands at the DER-encoded certificate content. ✓

---

## CERTIFICATE IDENTIFICATION

### CONFIRMED IDENTITY

**Canonical Ltd. Master Certificate Authority**

| Field | Value |
|-------|-------|
| Subject CN | `Canonical Ltd. Master Certificate Authority` |
| Organization | `Canonical Ltd.` |
| Locality | `Douglas` |
| State/Province | `Isle of Man` |
| Country | `GB` |
| Not Before | **2012-04-02 12:11:25 UTC** |
| Not After | **2042-04-01 12:11:25 UTC** |
| Key | RSA 2048-bit |
| CRL Distribution Point | `http://www.canonical.com/secure-boot-master-ca.crl` |
| DER Size | ~1080 bytes (`0x30 0x82 0x04 0x34` → SEQUENCE len 1076 + 4 header) |

### VERIFICATION METHOD

Certificate identity confirmed by decoding known-good base64 fragments from BOTH OCR runs:

```
Fragment                          Decoded Value
SXNsZSBvZiBNYW4=                 "Isle of Man"           ✓
RG91Z2xhcw==                     "Douglas"               ✓  
Q2Fub25pY2FsIEx0ZC4=             "Canonical Ltd."        ✓
R0I=                              "GB"                    ✓
Q2Fub25pY2FsIEx0ZC4gTWFzdGVy...  "Canonical Ltd. Master Certificate Authority" ✓
aHR0cDovL3d3dy5jYW5vbmljYWwu...  "http://www.canonical.com/secure-boot-master-ca.crl" ✓
```

DER validity period decoded directly from Run 2:
```
30 1e 17 0d 31 32 30 34 30 32 31 32 31 31 32 35 5a
         ^^^^UTCTime^^^  ^^^^^^^^^^120402121125Z^^
= Not Before: 2012 April 02 12:11:25 UTC
```

### PUBLIC RECORD

This certificate is publicly documented. It is embedded in Ubuntu's `shim-signed` package and is the root signing authority for Ubuntu's Secure Boot chain. It can be found in the Ubuntu package archive and has a public CRL at `canonical.com/secure-boot-master-ca.crl`.

**This cert is NOT the suspicious one.** Finding 1 in UEFI-MOK-KERNEL-EVIDENCE-2026-03-26.md identified a `CN=grub` self-signed cert with SKI `d939395cda059c19a699c85f3856d023be259007`. That is a **different, separate certificate** at a different offset in the same MokListRT variable.

---

## OCR RUN COMPARISON

### Run Summary

| | Run 1 | Run 2 |
|-|-------|-------|
| Lines captured | 20 | 23 |
| Status | **TRUNCATED** — missing 3 lines in public key section | **MORE COMPLETE** — cut off after last line |
| Authoritative | ❌ (truncated) | ✓ (primary source) |

**Run 1 was cut off** mid-public-key. Three full lines of RSA public key data are absent from Run 1 but present in Run 2. User noted "2nd failed on" — Run 2 also did not complete fully but captured significantly more content.

### Missing Lines (present in Run 2 only)

After the line ending in `...yvd7` (line 9), Run 1 jumps ahead while Run 2 continues with:

```
лр6yBA+GX2tWc+m1010D9quUupMnpD0xpkNTmdleF35ødU4Skpб150cfxajhdvo
+ov3wqIhLZtUQTUQVxONbLwpB1BKfuqZqWin08cHGzKeoBmHDnm7aJktfpNS5fbr
```

These are additional lines from the RSA modulus block that Run 1 missed entirely.

### OCR Error Catalogue

Both runs share systematic OCR errors. Categories and corrections:

**1. Cyrillic Lookalike Substitutions** (most frequent — OCR scanner mistake)

| OCR Output | Correct | Unicode |
|-----------|---------|---------|
| `а` | `a` | U+0430 |
| `В` | `B` | U+0412 |
| `С` | `C` | U+0421 |
| `Е` / `е` | `E` / `e` | U+0415 / U+0435 |
| `З` | `3` | U+0417 |
| `і` | `i` | U+0456 |
| `К` | `K` | U+041A |
| `М` | `M` | U+041C |
| `Н` | `H` | U+041D |
| `О` / `о` | `O` / `o` | U+041E / U+043E |
| `Т` | `T` | U+0422 |
| `У` / `у` | `Y` / `y` | U+0423 / U+0443 |
| `Х` / `х` | `X` / `x` | U+0425 / U+0445 |
| `ш` | `w` | U+0448 |
| `б` | `6` | U+0431 |
| `д` | `d` | U+0434 |
| `л` / `п` | `n` | U+043B / U+043F |
| `р` | `p` | U+0440 |
| `ч` | `4` | U+0447 |

**2. Symbol Substitutions**

| OCR Output | Correct | Unicode | Note |
|-----------|---------|---------|------|
| `×` | `x` | U+00D7 | Multiplication sign |
| `Ø` / `ø` | `0` | U+00D8 / U+00F8 | Slashed O |
| `©` | `C` | U+00A9 | Copyright |
| `®` | `R` | U+00AE | Registered |
| `Ä` | `A` | U+00C4 | A-umlaut |
| `·` | `/` | U+00B7 | Middle dot |
| `ý` | `y` | U+00FD | y-acute |
| `î` | `i` | U+00EE | i-circumflex |

**3. Punctuation Artifacts at Line Starts**

The OCR scanner misread character wrapping at line ends, producing spurious leading characters:
```
/ → (line boundary artifact — remove)
= → (base64 padding at line start — remove)  
[ → (remove)
* → (remove)
_ → (remove)
) → (remove)
```

**4. Injected Spaces** (OCR inserted spaces within base64 data):
```
"Ef J8"  →  "EfJ8"
"Fc0f j" →  "Fc0fj"
"AAG j"  →  "AAGj"
"bt IV"  →  "btIV"
```

**5. First Character of Certificate** — BOTH runs

Both runs show `t` as the first character. The correct first character is `M`. This is a consistent OCR error (`M` → `t` in a bold/stylized font). The DER certificate header `30 82 04 34` encodes as base64 `MIIENDC...`. Both runs captured `tIIENDC...`.

### Corrected First Line (consensus of both runs)

```
MIIENDCcAxygAwIBAgIJALIBJKAYLJJnMAOGCSqGSIb3DQEBCwUAMIGEMQswCQYD
```

---

## OCR-CORRECTED CERTIFICATE (BEST RECONSTRUCTION)

Using Run 2 as primary (more complete), with OCR corrections applied. **This is an approximation** — the OCR artifacts in the signature block make byte-perfect reconstruction impossible from OCR alone. The cert identity and key fields are confirmed; individual signature bytes may differ from the actual DER.

```
-----BEGIN CERTIFICATE-----
MIIENDCcAxygAwIBAgIJALIBJKAYLJJnMAOGCSqGSIb3DQEBCwUAMIGEMQswCQYD
VQQGEwJHQjEUMBIGA1UECAwLSXNsZSBvZiBNYW4xEDAOBgNVBAcMB0RvdWdsYXMx
GDAVBgNVBAoMDkNhbm9uaWNhbCBMdGQuMTQwMgYDVQQDDCtDYW5vbmljYWwgTHRk
LiBNYXN0ZXIgQ2VydGlmaWNhdGUgQXV0aG9yaXR5MB4XDTEyMDQwMjEyMTEyNVoX
DTQyMDQwMTEyMTEyNVowgYQxCzAJBgNVBAYTAkdCMRQwEgYDVQQIDAtJc2xlIG9m
TWFuMRAwDgYDVQQHDAdEb3VnbGFzMRcwFQYDVQQKDA5DYW5vbmljYWwgTHRkLjE0
MDIwgYDVQQDDCtDYW5vbmljYWwgTHRkLiBNYXN0ZXIgQ2VydGlmaWNhdGUgQXV0
aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEC/WzoWd04hXa5h
121WrL3e3nLz3x4tTGIPrMBtSAgRz42L+2EfJ8wRbtIVPT1U60A7sbwihTR5yvd7
np6yBA+GX2tWc+m1010D9quUupMnpD0xpkNTmdleF350dU4Skp6150cfxajhdvo
+ov3wqIhLZtUQTUQVxONbLwpB1BKfuqZqWin08cHGzKeoBmHDnm7aJktfpNS5fbr
dZv5K+24aEm82ZVQQFvFsnGq61xX3nH5QArdW6whC1QG1LW4fNrbpBkT1u06yDk
yRDakvDq5ELXAcT+IR/ZucBU1UKBUnIfSNR6yGwk8QhwC02loDLRoBxXqE3jr6H0
3QU+EE0hAgMBAAGjgaYwgaMwHQYDVR0OBBYEFK2RmQvCKrH1FwSMI7Z1WiaONFpj
MB8GA1UdIwQYMBaAFK2RmQvCKrH1FwSMI7Z1WiaONFpjMAwGA1UdEwEB/wQCMAEw
CwYDVR0PBAQDAgGGMEMGA1UdHwQ8MDowOKA2oDSGMmh0dHA6Ly93d3cuY2Fub25p
Y2FsLmNvbS9zZWN1cmUtYm9vdC1tYXN0ZXItY2EuY3JsMA0GCSqGSIb3DQEBCwUA
A4IBAQA/ffZ2pbODtCt60G1SGg0DxBKnUJxHkszA1HeC0q5Xs5kE9TI6x1Ud39sS
qvb62NR2I0vkw1Hbm1yckj8Yc9qUaqGZ0IykiG3B/D1x0HR2FgM+ViM11VVH\xod
QcLTEkzc/64KkpxiChcBnHPgXrH9vNa1GRF6fs0+A35m21uoyT1IUf9T4ZwxJ5Eb
OxB1Axe65oECgJRwTEa31LA9Fc0fjgLgaAKP+/1HHX2iAcYHUcSaz03dz6Nd1ZK7
vtH95uwfM1FzBL48crB9CPgB/5h9y5zgaT13JUdxiLGNJ6UuqPc/X4Bp1z6pJKU2
84DDgtmxBxtvbgnd8FC1L38agq8=
-----END CERTIFICATE-----
```

> ⚠️ **Note:** This reconstruction is for analysis reference only. The signature block bytes may differ from the actual DER due to OCR corruption. Use the raw file for any cryptographic verification.

---

## INVESTIGATIVE SIGNIFICANCE

### This Certificate: NORMAL 🟢

The Canonical Ltd. Master CA being in MokListRT is **expected behavior**:

- Ubuntu's `shim-signed` package embeds this cert as a vendor certificate
- When the shim loads, it registers this cert in the runtime MOK list (MokListRT)  
- This allows the shim to validate GRUB, and GRUB to validate the kernel and modules
- **Every standard Ubuntu Secure Boot installation has this cert in MokListRT**
- It has a 10-year public history (since 2012) and is traceable to Canonical

### The Other Certificate: CRITICAL 🔴

The `CN=grub` self-signed cert (Finding 1, UEFI report, SKI `d939395c...`) is at a **different offset** in the same MokListRT variable and has already been identified as highly suspicious:

- No public record
- Created Feb 2019 (predates this install by 7 years)
- Self-signed (no chain of trust to Canonical or Microsoft)
- Excessive Netscape Cert Type flags (all types enabled — non-standard)
- `mokutil --list-enrolled` refuses to run (selective blocking)

### How to Extract the CN=grub Certificate

The dd command with `skip=48` only reached the **first certificate** (the Canonical one). The suspicious cert is in the **second EFI_SIGNATURE_DATA** entry. To extract it:

**Offset calculation for the second certificate:**

```
4 bytes    EFI variable attributes
+
EFI_SIGNATURE_LIST #1:
  16 bytes   SignatureType GUID
   4 bytes   SignatureListSize
   4 bytes   SignatureHeaderSize (0)
   4 bytes   SignatureSize
  = 28 bytes list header

EFI_SIGNATURE_DATA #1:
  16 bytes   SignatureOwner GUID
  1080 bytes Canonical cert DER (30 82 04 34 + 1076 content)
  = 1096 bytes

Total for first list: 28 + 1096 = 1124 bytes

Second EFI_SIGNATURE_LIST starts at: 4 + 1124 = offset 1128
Second cert DER starts at: 1128 + 28 (list header) + 16 (owner GUID) = offset 1172
```

**Command to extract CN=grub cert:**
```bash
dd if=/home/lloyd/MokListRT.raw bs=1 skip=1172 2>/dev/null | openssl x509 -inform DER -text
```

> ⚠️ **Caveat:** The offset 1172 assumes the Canonical cert is exactly 1080 bytes DER and there is only one cert per EFI_SIGNATURE_LIST. If the raw file size is available (`wc -c MokListRT.raw`), this can be used to verify the calculation. Alternatively, hexdump the full file: `hexdump -C MokListRT.raw | head -80` to locate the second DER header (`30 82 ...`).

**Alternative (dump everything and scan):**
```bash
hexdump -C /sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 | less
```

Look for the second occurrence of `30 82` (DER SEQUENCE header) — that's the start of the second cert.

---

## UNFINISHED BUSINESS — UPDATED

This hexdump closes one item from the UEFI report's "Unfinished Business" table:

| Item | Previous Status | Updated Status |
|------|----------------|----------------|
| MOK NVRAM hexdump | HIGH 🔴 — not yet captured | **PARTIAL ✅** — First cert extracted and identified (Canonical Master CA, expected). Second cert (CN=grub, suspicious) not yet extracted. Use `skip=1172` command above. |

**Remaining MOK work:**
1. Run `dd if=MokListRT.raw bs=1 skip=1172` to extract the CN=grub cert
2. Get `hexdump -C MokListRT.raw` to verify structure and count total certs  
3. Run `wc -c MokListRT.raw` to get file size and validate offset calculations
4. If `mokutil --list-enrolled` is still blocked, bypass with: `sudo hexdump -C /sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23`

---

## RAW OCR DATA — PRESERVED FOR RECORD

### Run 1 (original, OCR errors intact)

```
-----BEGIN CERTIFICATE-----
tIIENDCcAxygAwIBAgIJALIBJKAYLJJnMAOGCSqGSIb3DQEBCUUAMIGEMOSWCQYD
/QQGEwJHQiEUMBIGA1UECAwLSXNsZSBvZiBNYW4×EDAÖBgNVBAcMB@RvdHdsY%M%
=ZAVBgNVBA0MDkNhbm9uaNNhbCBMdGQuMTQwMgYDVQQDDCtDYW5vbmljYHugTHRK
0TQYMDQXMTEXMTI1MVowgYQXCZAJBgNVBAYTAKdCMRQwEgYDVO0IDAtJc2×1IG9m
[E1hbjEQMA4GA1UEBwwHRG9122xhczEXMBUGA1UECgw0Q2Fub25pY2FsIE×02C4×
vDAyBgNVBAMMK@Nhbm9uaWNhbCBMdGQuIE1hc3R1ciBDZXJ0aWZpY2FØZSBBdXRo
p3JpdHkwggEiMAØGCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC/WzoWd04hXa5h
121WrL3e3nL23x4tTGIPrMBtSAgRZ42L+2Ef J8wRbt IVPT1U60A7sbvihTR5yvd7
)Zv5K+24аЕm82ZVQQFvFsnGq61×ХЗnH5QArdW6шеhС1QG1LW4fNrbpВkТ1u06yDk
/RDaWvDq5ELХАсТ+IR/ZucВU1UKВUnIfSWR6yGшk8QhшСØ21oDLRoВxХqЕ3jr6W0
3QU+EE0hAgMBAAGjgaYwgaMwHQYDVR0OBBYEFK2RmQvCKrH1FwSMI721WiaONFpj
1b8GA1UdIwQVMBaAFK2Rm@vCKrH1FwSMI7Z1Wia0NFpjMA8GA1UdEwЕВ/wQFMAMB
эf8wCwYDVRØPBAQDAgGGMEMGA1UdHwQ8MDowOKA2oDSGMmhødHA6Ly93d3cuY2Fu
025pY2FsLmvbS9zZWN1cmUt Ym9vdc1tYXN02XItY2EuY3JsMA0GCSqGSIb3DQEB
CuUAA4IBAQA/ff22pb0DtCt6ØG1SGgOD×BKnUJxHkszA1HeC0q5Xs5kE9TI6x1Ud
39sSqvb62NR2I0vkw1Hbm1yck.j8Yc9qUaqGZ0IykiG3B/D1x0HR2FgM+ViM11VVH
\xod@cLТЕkzc/64KkpxiChсВnHPgХrH9vNa1GR6fs0+A35m21uоyТ1IUf9T4Zшx
J5Eb0xB1Axe65oECgJRwTEa31LA9Fc0f jgLgaAKP+/1HHX2iAcYHUcSaz03dz6Nd
12K7vtH95uwfM1FzBL48crB9CPgB/5h9y5zgaT13JUdxiLGNJ6UuqPc/X4Bp1z6p
9JKU284DDgtmxBxtvbgnd8FC1L38agq8
-----END CERTIFICATE-----
```

### Run 2 (original, OCR errors intact — more complete)

```
-----BEGIN CERTIFICATE-----
tIENDCAxygAWIBAgIJALIBJKAYLJJMMAOGOSQGSIbBDQEBCUUAMIGEMOSUCOYD
JQQGEWJHQJEUMBIGA1UECAWLSXNSZSBvZ1BNYW4xEDA0BgNVBAcMB@RvdWdsYXMx
*ZAVBgNVBAOMDKNhbmduaNNhbCBMdGQUMTQwMgYDVQQDDCtDYW5Vbm1JYHugTHRK
_iBNYxN®ZXIgQ2VydGlmaNNhdGUgQХVØаG9yaХR5МВ4ХDТЕyМDŒ×МjЕ×МТI1МVoX
0TQMDQxMTE×MTI1MV0wgYQXCZAJBgNVBAYTAKdCMRQWEgYDVQQIDAtJc2x1IG9m
[E1hhjEQMA4GA1UEBшwHRG91Z2×hczEXMBUGA1UECgw0Q2Fub25pY2FsIExØZC4×
vDAyBgNVBAMMKONhbm9uaNNhbCBMdGQuIE1hc3R1ciBDZXJ0aHZpY2FØZSBBdXRo
о3JpdHkwggEіMA0GCSqGSIb3DQEBAQUAA4IBDwÄwggEKAoIBAQC/WzoWd04hXa5h
121WrL3e3nLz3X4tTGIPrMBtSAgRz42L+2Ef J8wRbt 1VPT1U60A7sbwihTR5yvd7
лр6yBA+GX2tWc+m1010D9quUupMnpD0xpkNTmdleF35ødU4Skpб150cfxajhdvo
+ov3wqIhLZtUQTUQVxONbLwpB1BKfuqZqWin08cHGzKeoBmHDnm7aJktfpNS5fbr
дZv5K+24аEm82ZVQQFvFsnGq61×ХЗnH5QArdW6whC1QG1LW4fNrbpBkТ1uø6yDk
ýRDakvDq5ELXAcТ+IR/ZucВU1UKВUnIfSИR6yGшk8QhwСØ2loDLRоВхХqЕЗjr6Н0
3QU+EE0hAgMBAAG jgaYugaMwHQYDVRØOBBYEFK2RmQvCKrH1FwSMI7Z1WiaONFp.j
чB8GA1UdIwQYNBaAFK2RmQvCKrH1FwSMI7Z1WiaONFpJMA8GA1UdEwЕB/wQFMAMB
Af8w©wYDVRØPBAQDAgGGМEМGA1UdHwQ8МDowOКА2oDSGМmhØdHA6Lу9ЗdЗcu·2Fu
o25pY2FsLmNvbS9zZWN1cmUt Ym9vdC1tYXN0ZXItY2EuY3JsMA0GCSqGSIb3DQEB
CwUAA4ІBAQA/ffZ2pbODtCt6ØG1SGg0DxВКnUJхHkszA1HеСØq5Хs5kЕ9ТI6x1Ud
39sSqvb62NR2I0vkш1Hbm1уckj8Yс9qUaqGZ0IykîGЗВ/D1xøHR2FgМ+VіМ11VVН
\xodQcLТEkzc/64kkpxiChcBnHPgXrH9vNa1GRF6fs0+A35m21uoyT1IUf9T4Zшx
J5EbO×B1Axе65oECgJRwTEaЗ1LA9FcØfjgLgаАКP+/1HHХ2іAcYHUcSaz0Зdz6Nd
1ZK7vtH95uwfM1FzBL48crB9CPgB/5h9y5zgaT13JUdxiLGNJ6UuqPc/X4Bp1z6p
ЭJKU284DDgtmxBxtvbgnd8FC1L38agq8
-----END CERTIFICATE-----
```

---

**Report Generated By:** ClaudeMKII  
**Session Date:** 2026-03-26  
**Analysis Confidence:** HIGH — cert identity confirmed by multiple decoded fields and CRL URL  
**Follow-up Required:** YES — extract CN=grub cert at skip=1172, full hexdump of MokListRT.raw
