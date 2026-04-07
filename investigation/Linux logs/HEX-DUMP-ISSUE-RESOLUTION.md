# Hex Dump Issue Resolution

**Issue**: Hex Dump (GitHub Issue)
**Date**: 2026-03-26
**Status**: ✅ RESOLVED with tooling and documentation

## Problem Summary

The user provided OCR-corrupted certificate data extracted from a terminal screenshot. The certificate (identified as the `CN=grub` MOK certificate) contained extensive OCR errors:

- Cyrillic character substitution (А, В, С, Е, Т, М, etc.)
- Special character insertion (×, Ø, @, •)
- Character confusion (0 vs O, 1 vs I/l)
- Inconsistent line breaks and spacing

Two versions of the same certificate were shown, both with different OCR errors, confirming the corruption was from photographing a terminal screen rather than actual data corruption.

## Root Cause

The certificate data shown was from a `dd` command extracting the MOK certificate:

```bash
dd if=/home/lloyd/MokListRT.raw bs=1 skip=48 2>/dev/null | openssl x509 -inform DER -outform PEM
```

The user photographed the terminal output, and OCR introduced errors. Base64 encoding has no error correction, so even a single character error makes decoding impossible.

## Solution Delivered

### 1. Certificate Extraction Tool

Created `tools/extract_mok_cert.py` - a comprehensive Python tool that can:

- **Extract from raw binary MOK files** with configurable skip offset
- **Process EFI variable dumps** (auto-skips 4-byte attribute header)
- **Clean OCR-corrupted text** (best-effort, maps common OCR errors)
- **Convert DER to PEM format**
- **Verify with OpenSSL** after extraction

**Features**:
- Automatic DER certificate detection (`0x30 0x82` / `0x30 0x83` markers)
- Proper DER length parsing for exact extraction
- Cyrillic-to-Latin character mapping
- Special character cleanup
- Command-line interface with full argument support

### 2. Documentation

Created two comprehensive guides:

**`investigation/Linux logs/MOK-CERT-EXTRACTION-GUIDE.md`**:
- Explains why OCR recovery failed
- Provides 3 extraction methods (EFI variable, raw binary, mokutil)
- Documents the known certificate characteristics
- Includes verification commands
- Next steps for obtaining actual binary data

**`tools/README-extract-mok-cert.md`**:
- Complete tool documentation
- Usage examples for all modes
- Troubleshooting guide
- MOK file structure explanation
- Security notes on MOK certificate capabilities

### 3. Saved Evidence

**`investigation/Linux logs/mok-cert-ocr-corrupted.txt`**:
- Preserved the original OCR-corrupted certificate for reference
- Demonstrates the corruption patterns
- Reference for OCR error analysis

## Key Findings

1. **OCR recovery is not feasible**: Base64 corruption is too extensive for reconstruction

2. **Binary extraction required**: The actual solution requires accessing the system to extract the binary MOK data directly from:
   ```bash
   /sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23
   ```

3. **Tool supports multiple input formats**:
   - Raw MOK binary files
   - EFI variable dumps
   - OCR text (with limitations)

4. **Proper extraction commands**:
   ```bash
   # Direct from EFI variable (recommended):
   sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 \
       bs=1 skip=4 2>/dev/null | \
       openssl x509 -inform DER -outform PEM -out mok-cert.pem

   # Or use the tool:
   python3 tools/extract_mok_cert.py \
       --efi-var \
       --input moklist.bin \
       --output mok-cert.pem \
       --verify
   ```

## Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `tools/extract_mok_cert.py` | MOK certificate extraction tool | 266 |
| `tools/README-extract-mok-cert.md` | Tool documentation | 242 |
| `investigation/Linux logs/MOK-CERT-EXTRACTION-GUIDE.md` | Extraction guide | 147 |
| `investigation/Linux logs/mok-cert-ocr-corrupted.txt` | Original corrupted data | 22 |
| `investigation/Linux logs/mok-cert-cleaned-attempt1.pem` | Cleaning attempt (failed as expected) | 22 |
| `investigation/Linux logs/HEX-DUMP-ISSUE-RESOLUTION.md` | This summary | - |

## Expected Certificate Details

The target certificate (from UEFI-MOK-KERNEL-EVIDENCE):

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

## Next Steps for User

1. **On the Linux system**, run:
   ```bash
   sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 \
       of=~/moklist-raw.bin
   ```

2. **Transfer** `moklist-raw.bin` to a location where you can access it

3. **Extract certificate**:
   ```bash
   python3 tools/extract_mok_cert.py \
       --efi-var \
       --input moklist-raw.bin \
       --output CN-grub-mok.pem \
       --verify
   ```

4. **Verify fingerprint** matches expected:
   ```bash
   openssl x509 -in CN-grub-mok.pem -fingerprint -sha1 -noout
   # Should output: SHA1 Fingerprint=54:F4:18:74:F4:D8:84:28:09:BC:BE:88:10:65:92:0A:17:56:5D:25
   ```

5. **Save to evidence**:
   ```bash
   cp CN-grub-mok.pem investigation/Linux\ logs/
   ```

## Technical Notes

### Why OCR Failed

Base64 encoding maps 6 bits to each character. Changing one character corrupts an entire 3-byte block. With dozens of OCR errors throughout the certificate:

- Early errors shift all subsequent decoding
- Middle errors corrupt ASN.1 DER structure
- End errors invalidate checksums/padding

There is no redundancy or error correction in base64.

### mokutil Blocking

The UEFI evidence report notes that `mokutil --list-enrolled` and `mokutil --export` return help text instead of executing. This selective failure suggests:

- Argument parsing is being intercepted
- Binary has been modified
- Access control is blocking specific operations

Direct EFI variable read bypasses this restriction.

## Connection to Investigation

This MOK certificate is the **firmware-level persistence mechanism** that:

- Survives OS reinstalls (stored in NVRAM, not disk)
- Controls boot chain for both Windows and Linux
- Enables signing of arbitrary kernels, bootloaders, and modules
- Was enrolled during deployment window (evidenced by DISM/Synergy interception)
- Predates the current install by 7 years (created Feb 2019)

Extracting and documenting this certificate is critical evidence for the firmware compromise investigation.

## Status

✅ **Tooling complete** - Full-featured extraction tool created and documented
✅ **Documentation complete** - Two comprehensive guides provided
✅ **OCR analysis complete** - Corruption patterns documented, recovery deemed infeasible
⚠️  **Binary extraction pending** - Requires access to the Linux system's EFI variables
⚠️  **Certificate verification pending** - Cannot verify until binary extraction complete

## Recommendation

This resolves the immediate issue (providing tools and documentation for proper extraction). The next session should focus on obtaining the actual binary MOK data from the system so the certificate can be extracted, verified, and added to the evidence collection.
