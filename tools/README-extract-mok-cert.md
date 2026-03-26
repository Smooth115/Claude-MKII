# MOK Certificate Extraction Tool

Command-line tool for extracting X.509 certificates from Machine Owner Key (MOK) binary data and cleaning OCR-corrupted certificate text.

## Features

- Extract certificates from raw MOK binary files
- Process EFI variable dumps
- Clean OCR-corrupted certificate text (best-effort)
- Convert DER to PEM format
- Verify certificates with OpenSSL

## Installation

Requires Python 3.6+ and OpenSSL.

```bash
# No installation needed - standalone script
chmod +x tools/extract_mok_cert.py
```

## Usage

### Extract from Raw Binary MOK File

```bash
python3 tools/extract_mok_cert.py \
    --input MokListRT.raw \
    --output mok-cert.pem \
    --skip 48 \
    --verify
```

Parameters:
- `--input`: Path to raw MOK binary file
- `--output`: Output PEM certificate file
- `--skip`: Bytes to skip (MOK header, default: 48)
- `--verify`: Verify with OpenSSL after extraction

### Extract from EFI Variable Dump

```bash
# First, dump the EFI variable
sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 \
    of=moklist.bin

# Then extract certificate
python3 tools/extract_mok_cert.py \
    --efi-var \
    --input moklist.bin \
    --output mok-cert.pem \
    --verify
```

Parameters:
- `--efi-var`: Input is an EFI variable dump (skips 4-byte attribute header)

### Clean OCR-Corrupted Certificate Text

```bash
python3 tools/extract_mok_cert.py \
    --clean-ocr \
    --input corrupted-cert.txt \
    --output cleaned-cert.pem
```

**Note**: OCR cleaning is best-effort only. Severely corrupted base64 cannot be recovered because base64 has no error correction. You will need the original binary data for reliable extraction.

## Command Reference

### Direct EFI Variable Extraction (One-liner)

```bash
# Extract and convert to PEM in one command
sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 \
    bs=1 skip=4 2>/dev/null | \
    openssl x509 -inform DER -outform PEM -out mok-cert.pem
```

### Verify Extracted Certificate

```bash
# View full certificate details
openssl x509 -in mok-cert.pem -text -noout

# Check subject and issuer
openssl x509 -in mok-cert.pem -subject -issuer -noout

# Get fingerprints
openssl x509 -in mok-cert.pem -fingerprint -sha1 -noout
openssl x509 -in mok-cert.pem -fingerprint -sha256 -noout

# Check dates and serial
openssl x509 -in mok-cert.pem -serial -dates -noout
```

## How It Works

### MOK File Structure

MOK (Machine Owner Key) files contain X.509 certificates in DER format, typically with a header.

```
[Header (variable)] [DER Certificate] [Optional additional data]
```

### DER Format

X.509 certificates in DER format start with:
- `0x30 0x82` - SEQUENCE tag with 2-byte length
- `0x30 0x83` - SEQUENCE tag with 3-byte length

The tool searches for these markers and extracts the complete certificate structure.

### EFI Variable Format

EFI variables have a 4-byte attribute header:
```
[Attributes (4 bytes)] [Data]
```

Use `--efi-var` to automatically skip this header.

## OCR Cleaning Details

Common OCR errors the tool attempts to correct:

| OCR Error | Correct | Type |
|-----------|---------|------|
| А, В, С, Е, Т, М | A, B, C, E, T, M | Cyrillic → Latin |
| О, Р, Х, К, Н | O, P, X, K, H | Cyrillic → Latin |
| × | x | Special char |
| Ø | 0 | Special char |
| • | (removed) | Bullet point |

**Limitation**: Even with cleaning, extensively corrupted base64 cannot be decoded. The certificate must be extracted from binary source.

## Examples

### Example 1: Extract CN=grub MOK Certificate

```bash
# Dump from EFI variable
sudo dd if=/sys/firmware/efi/efivars/MokListRT-605dab50-e046-4300-abb6-3dd810dd8b23 \
    of=moklist-raw.bin

# Extract certificate
python3 tools/extract_mok_cert.py \
    --efi-var \
    --input moklist-raw.bin \
    --output CN-grub.pem \
    --verify

# Expected verification output:
# Subject: CN=grub
# Issuer: CN=grub
# Serial: B2:94:8E:B3:CA:BC:48:27:A0:A5:67:A2:B9:59:D4:63
# SHA1 Fingerprint: 54:F4:18:74:F4:D8:84:28:09:BC:BE:88:10:65:92:0A:17:56:5D:25
```

### Example 2: Process Raw dd Output

```bash
# Create raw dump (skip MOK header)
dd if=/dev/disk/by-path/... bs=1 skip=48 count=2048 of=mok.raw

# Extract
python3 tools/extract_mok_cert.py \
    --input mok.raw \
    --skip 0 \
    --output cert.pem
```

## Troubleshooting

### "No certificate data found"

- Verify input file contains DER certificate data
- Try adjusting `--skip` value
- Check if file is actually an EFI variable dump (use `--efi-var`)
- Use `hexdump -C file.bin | head -50` to inspect file structure

### "Unable to load certificate" from OpenSSL

- Certificate data is corrupted
- Base64 encoding has errors (if from OCR)
- DER structure is incomplete
- You need the original binary source

### mokutil Commands Failing

If `mokutil --list-enrolled` returns help text instead of executing:

1. Try direct EFI variable read (bypasses mokutil)
2. Check `mokutil --version` for unusual output
3. Use `strace mokutil --list-enrolled` to see what's failing
4. Consider mokutil binary integrity issue

## Related Documentation

- [MOK Certificate Extraction Guide](investigation/Linux%20logs/MOK-CERT-EXTRACTION-GUIDE.md)
- [UEFI MOK Evidence Report](investigation/Linux%20logs/UEFI-MOK-KERNEL-EVIDENCE-2026-03-26.md)

## Security Notes

MOK certificates with `CA:TRUE` + Code Signing capabilities can:
- Sign arbitrary UEFI binaries
- Sign kernel modules
- Sign subordinate certificates
- Bypass Secure Boot validation (if enrolled in shim)

Always verify certificate fingerprints against known-good values.

## License

Part of ClaudeMKII investigation framework.
