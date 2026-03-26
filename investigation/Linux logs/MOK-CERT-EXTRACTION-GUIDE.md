# MOK Certificate Extraction Guide

## Issue: OCR-Corrupted Certificate Data

The certificate data shown in Issue #[number] contains OCR errors from photographing a terminal screen. The certificate cannot be recovered from the corrupted base64 text alone because too many characters have been misrecognized.

## Known Certificate Details (from UEFI-MOK-KERNEL-EVIDENCE-2026-03-26.md)

The certificate we're looking for has these characteristics:

```
Subject: CN=grub
Issuer: CN=grub (self-signed)
Serial: b2:94:8e:b3:ca:bc:48:27:a0:a5:67:a2:b9:59:d4:63
Not Before: Feb 24 22:38:00 2019 GMT
Not After: Feb 21 22:38:00 2029 GMT
Key: 2048-bit RSA, Exponent 65537
SHA1 Fingerprint: 54:F4:18:74:F4:D8:84:28:09:BC:BE:88:10:65:92:0A:17:56:5D:25
Subject Key Identifier: D9:39:39:5C:DA:05:9C:19:A6:99:C8:5F:38:56:D0:23:BE:25:90:07
```

## Proper Extraction Methods

### Method 1: Extract from EFI Variable (Recommended)

This bypasses `mokutil` restrictions and reads directly from NVRAM:

```bash
# Read MokListRT directly from EFI variables
sudo hexdump -C /sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 > moklist-hexdump.txt

# Or extract as binary
sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 of=moklist.bin

# Skip first 4 bytes (EFI variable attributes), then extract certificate
sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 bs=1 skip=4 2>/dev/null | openssl x509 -inform DER -outform PEM -out mok-cert.pem

# Or use the extraction tool
python3 tools/extract_mok_cert.py --efi-var --input moklist.bin --output mok-cert.pem --verify
```

### Method 2: Extract from MokListRT.raw (if available)

If you have a `MokListRT.raw` file created from a dump:

```bash
# Original command shown in issue (with typo corrections):
# Note: skip=48 assumes a specific MOK list structure
dd if=/home/lloyd/MokListRT.raw bs=1 skip=48 2>/dev/null | openssl x509 -inform DER -outform PEM

# Or use the extraction tool
python3 tools/extract_mok_cert.py --input MokListRT.raw --skip 48 --output mok-cert.pem --verify
```

### Method 3: mokutil export (if working)

```bash
# List enrolled MOK keys
mokutil --list-enrolled

# Export specific key
mokutil --export

# Note: In the user's case, these commands were returning help text instead of executing.
# This suggests selective blocking or an unusual mokutil version.
```

## OCR Corruption Analysis

The certificate data in the issue has these OCR errors:

1. **Cyrillic substitution**: Latin characters replaced with Cyrillic (А→A, В→B, С→C, Е→E, Т→T, М→M, Н→H, К→K, О→O, Р→P, Х→X, У→Y)

2. **Special character insertion**: `×`, `Ø`, `@`, `•`, etc. inserted into base64 stream

3. **Character confusion**:
   - Zero (0) vs letter O
   - One (1) vs letter I/l
   - Number 8 vs letter B

4. **Line breaks and spacing**: Inconsistent line wrapping and extra spaces

5. **Two versions shown**: Both have different errors, confirming OCR instability

## Why Recovery from OCR Text Failed

Base64 encoding has no error correction. Even a single wrong character makes the entire block undecodable. With dozens of errors distributed throughout the certificate, reconstruction is not feasible without the original binary data.

## Extraction Tool

The `tools/extract_mok_cert.py` script provides:

- Binary DER extraction from raw MOK dumps
- EFI variable processing (skips 4-byte header)
- OCR cleaning (best-effort, but cannot recover severely corrupted data)
- PEM output format
- OpenSSL verification

## Verification After Extraction

```bash
# View certificate details
openssl x509 -in mok-cert.pem -text -noout

# Check fingerprints
openssl x509 -in mok-cert.pem -fingerprint -sha1 -noout
openssl x509 -in mok-cert.pem -fingerprint -sha256 -noout

# Verify it's the expected CN=grub certificate
openssl x509 -in mok-cert.pem -subject -issuer -serial -dates -noout

# Expected output:
# subject=CN=grub
# issuer=CN=grub
# serial=B2:94:8E:B3:CA:BC:48:27:A0:A5:67:A2:B9:59:D4:63
# notBefore=Feb 24 22:38:00 2019 GMT
# notAfter=Feb 21 22:38:00 2029 GMT
```

## Next Steps

1. **Obtain binary MOK data**: Use Method 1 (direct EFI variable read) to extract the actual certificate binary

2. **Extract to PEM**: Use `extract_mok_cert.py` or `openssl` to convert DER to PEM

3. **Verify fingerprints**: Compare SHA1 fingerprint against known value (`54:F4:18:74...`)

4. **Document in evidence**: Save extracted certificate to `investigation/Linux logs/CN-grub-mok-certificate.pem`

5. **Submit to Certificate Transparency**: Upload to crt.sh and other CT logs to create public record

## Status

- ✅ Extraction tool created: `tools/extract_mok_cert.py`
- ✅ OCR corruption documented
- ⚠️  Binary MOK data needed: EFI variable must be dumped from the actual system
- ❌ Certificate recovery from OCR text: Not feasible due to extensive corruption

## Related Files

- Evidence report: `investigation/Linux logs/UEFI-MOK-KERNEL-EVIDENCE-2026-03-26.md`
- Extraction tool: `tools/extract_mok_cert.py`
- OCR corrupted sample: `investigation/Linux logs/mok-cert-ocr-corrupted.txt`
- This guide: `investigation/Linux logs/MOK-CERT-EXTRACTION-GUIDE.md`
