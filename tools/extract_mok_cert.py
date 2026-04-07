#!/usr/bin/env python3
"""
MOK Certificate Extraction Tool

Extracts X.509 certificates from raw MOK (Machine Owner Key) binary data
and cleans OCR-corrupted certificate text.

Usage:
    # Extract from raw binary file:
    python3 extract_mok_cert.py --input MokListRT.raw --output cert.pem

    # Clean OCR-corrupted certificate text:
    python3 extract_mok_cert.py --clean-ocr --input corrupted.txt --output cleaned.pem

    # Extract from EFI variable dump:
    python3 extract_mok_cert.py --efi-var --input moklist.bin --output cert.pem
"""

import sys
import argparse
from pathlib import Path


def clean_ocr_base64(text):
    """
    Clean OCR-corrupted base64 certificate text.

    Common OCR errors:
    - Cyrillic characters (А, В, С, Е, Т, М, etc.) instead of Latin
    - Special characters (×, Ø, ×, •, etc.) instead of standard chars
    - Zero (0) vs letter O confusion
    - One (1) vs letter I/l confusion
    """

    # Mapping of common OCR errors to correct base64 characters
    ocr_map = {
        # Cyrillic to Latin
        'А': 'A', 'В': 'B', 'С': 'C', 'Е': 'E', 'Т': 'T', 'М': 'M',
        'Н': 'H', 'К': 'K', 'О': 'O', 'Р': 'P', 'Х': 'X', 'У': 'Y',
        'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',

        # Special characters
        '×': 'x',
        'Ø': '0',
        '•': '',
        '–': '-',
        '—': '-',
        '\xa0': '',  # non-breaking space

    }

    cleaned = text

    # Apply character mappings
    for bad, good in ocr_map.items():
        cleaned = cleaned.replace(bad, good)

    # Remove any non-base64 characters except newlines and dashes
    # Valid base64: A-Z, a-z, 0-9, +, /, =
    lines = cleaned.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Keep BEGIN/END markers
        if 'BEGIN CERTIFICATE' in line or 'END CERTIFICATE' in line:
            cleaned_lines.append('-----' + line.split('-----')[1] + '-----' if '-----' in line else line)
        # Clean base64 content lines
        elif line and not line.startswith('-'):
            # Keep only valid base64 characters
            clean_line = ''.join(c for c in line if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
            if clean_line:
                cleaned_lines.append(clean_line)
        elif line:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def parse_der_length(data):
    """
    Parse DER-encoded length and return (content_length, header_length).

    DER length encoding:
    - Short form (< 0x80): length is in this byte, header is tag + 1 byte
    - Long form (>= 0x80): lower 7 bits encode number of following length bytes

    Raises ValueError if data is too short or declared length exceeds buffer.
    """
    if len(data) < 2:
        raise ValueError("Invalid DER: insufficient data")

    len_byte = data[1]

    if len_byte & 0x80 == 0:
        # Short form
        content_len = len_byte
        header_len = 2
    else:
        num_len_bytes = len_byte & 0x7F
        if len(data) < 2 + num_len_bytes:
            raise ValueError("Invalid DER length: insufficient data for long-form length")
        length_bytes = data[2:2 + num_len_bytes]
        content_len = int.from_bytes(length_bytes, byteorder="big")
        header_len = 2 + num_len_bytes

    total_len = header_len + content_len
    if total_len > len(data):
        raise ValueError("Invalid DER length: declared length exceeds available data")

    return content_len, header_len


def extract_from_raw_binary(input_file, skip_bytes=48):
    """
    Extract certificate from raw MOK binary file.

    Args:
        input_file: Path to raw binary file
        skip_bytes: Number of bytes to skip (MOK header, default 48)

    Returns:
        bytes: Raw certificate data
    """
    with open(input_file, 'rb') as f:
        # Skip MOK header
        f.seek(skip_bytes)

        # Read remaining data
        cert_data = f.read()

        # Look for DER certificate header (0x30 0x82 for SEQUENCE)
        # X.509 certificates start with a SEQUENCE tag
        der_start = cert_data.find(b'\x30\x82')

        if der_start == -1:
            # Try alternative DER markers
            der_start = cert_data.find(b'\x30\x83')

        if der_start >= 0:
            # Extract from DER start
            cert_data = cert_data[der_start:]

            # Parse DER length to extract exactly one certificate
            if len(cert_data) > 2:
                content_len, header_len = parse_der_length(cert_data)
                cert_len = header_len + content_len
                cert_data = cert_data[:cert_len]

        return cert_data


def extract_from_efi_var(input_file):
    """
    Extract certificate from EFI variable dump.

    EFI variables have a header before the actual data.
    MokListRT format: attributes (4 bytes) + data
    """
    with open(input_file, 'rb') as f:
        data = f.read()

        # Skip EFI variable attributes (first 4 bytes)
        if len(data) > 4:
            data = data[4:]

        # Look for DER certificate
        der_start = data.find(b'\x30\x82')
        if der_start == -1:
            der_start = data.find(b'\x30\x83')

        if der_start >= 0:
            cert_data = data[der_start:]
            # Parse DER length to return exactly one certificate
            if len(cert_data) > 2:
                content_len, header_len = parse_der_length(cert_data)
                cert_data = cert_data[:header_len + content_len]
            return cert_data

        return data


def der_to_pem(der_data):
    """
    Convert DER format certificate to PEM format.
    """
    import base64

    # Encode to base64
    b64_data = base64.b64encode(der_data).decode('ascii')

    # Split into 64-character lines
    lines = [b64_data[i:i+64] for i in range(0, len(b64_data), 64)]

    # Build PEM format
    pem = '-----BEGIN CERTIFICATE-----\n'
    pem += '\n'.join(lines)
    pem += '\n-----END CERTIFICATE-----\n'

    return pem


def main():
    parser = argparse.ArgumentParser(
        description='Extract and clean MOK certificates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('-i', '--input', required=True,
                        help='Input file (raw binary, EFI var dump, or OCR text)')
    parser.add_argument('-o', '--output', required=True,
                        help='Output PEM file')
    parser.add_argument('--clean-ocr', action='store_true',
                        help='Clean OCR-corrupted certificate text')
    parser.add_argument('--efi-var', action='store_true',
                        help='Input is an EFI variable dump')
    parser.add_argument('--skip', type=int, default=48,
                        help='Bytes to skip in raw binary (default: 48)')
    parser.add_argument('--verify', action='store_true',
                        help='Verify certificate with openssl after extraction')

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        if args.clean_ocr:
            # Read and clean OCR text
            print(f"Cleaning OCR-corrupted certificate from {input_path}...")
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                corrupted = f.read()

            cleaned = clean_ocr_base64(corrupted)

            # Write cleaned certificate
            with open(output_path, 'w') as f:
                f.write(cleaned)

            print(f"Cleaned certificate written to {output_path}")

        else:
            # Extract from binary
            if args.efi_var:
                print(f"Extracting certificate from EFI variable dump: {input_path}...")
                der_data = extract_from_efi_var(input_path)
            else:
                print(f"Extracting certificate from raw binary: {input_path} (skip={args.skip})...")
                der_data = extract_from_raw_binary(input_path, args.skip)

            if not der_data:
                print("Error: No certificate data found", file=sys.stderr)
                return 1

            # Convert to PEM
            pem_data = der_to_pem(der_data)

            # Write PEM certificate
            with open(output_path, 'w') as f:
                f.write(pem_data)

            print(f"Certificate extracted to {output_path} ({len(der_data)} bytes DER)")

        # Verify with openssl if requested
        if args.verify:
            import subprocess
            print("\nVerifying certificate with openssl...")
            result = subprocess.run(
                ['openssl', 'x509', '-in', str(output_path), '-text', '-noout'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✓ Certificate is valid")
                print("\nCertificate details:")
                print(result.stdout)
            else:
                print("✗ Certificate verification failed:", file=sys.stderr)
                print(result.stderr, file=sys.stderr)
                return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
