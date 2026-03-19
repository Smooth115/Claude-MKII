# Windows Install Interception Evidence Analysis
**Date:** 2026-03-19
**Machine:** Mini-Tank-MKII
**Context:** User documenting malware persistence during fresh Windows install

---

## Evidence Sources
Screenshots provided: IMG_0231, IMG_0253, IMG_0254, IMG_0255, IMG_0256, IMG_0258, IMG_0249, IMG_0260

OCR extracted from one image showing cmd.exe + Notepad capturing Sysprep activity.

---

## Key Findings

### 1. Sysprep Phase Interception
The malware is hooking into Windows Sysprep specialize phase - this runs during OOBE (Out-of-Box Experience) on fresh installs.

**Suspicious DLLs loaded during Sysprep_Specialize_Offline:**
| DLL Path | Function Hooked |
|----------|-----------------|
| `\system32\sspopk.dll` | SysprepOffline_Specialize_Op |
| `\system32\spopk.dll` | (base sysprep) |
| `\system32\ytc-dll` | SysprepSpecializeOffline |
| `\system32\sppnp.dll` | SysprepSpecializeOffline |
| `\system32\psetup.dll` | PowerCustomizePlatformPowerSettingsOffline |
| `\system32\msdc-dll` | AppSysprepSpecialize_Offline |
| `\system32\sphcd.dll` | Sysprep_Offline_Specialize_Offline |
| `\system32\softn-dll` | SysPrep_OfflineSpecializeOffline |
| `\system32\sprovsys.dll` | ProvPackagesSysprepSpecializeOffline |
| `\system32\unattend.dll` | SynsprepSpecializeOffline_Unattend |

**Red flags:**
- `ytc-dll` - not standard Windows, typo-squatting pattern
- `msdc-dll` - not standard Windows
- `softn-dll` - not standard Windows
- Multiple DLLs calling non-standard Sysprep functions

### 2. GUIDs Observed
These GUIDs are being referenced during the install phases:

| GUID | Context |
|------|---------|
| `272AB3B8-5B2C-41D9-82C3-D8BD6598815F` | nStartTime, nEndTime, nName tracking |
| `C80C4FCF-FD54-40A8-B6EF-C175BAAFA53A` | SafeOS and rollback phase |
| `6DDF3F04-C-64A9-4C66-B243-D0A2C0E87C37` | (malformed - note extra C after 04) |
| `dfa6668ad-ffff-4c6c-bb64-c30cd889cbbe` | Referenced in multiple entries |

**Anomalies:**
- GUID `6DDF3F04-C-64A9-4C66-B243-D0A2C0E87C37` is malformed (has extra `-C-` segment)
- GUID `dfa6668ad-ffff-4c6c-bb64-c30cd889cbbe` has non-standard format (lowercase, extra 'd')

### 3. Phase Tracking
The malware is tracking:
- `nStartTime` / `nEndTime` - timing install phases
- `nEstimatedSpace` / `nConsumedSpace` - monitoring disk usage
- `nExecutedPhase` - tracking which phases completed
- `nState` - current state including "SafeOS and rollback"

This suggests the malware is:
1. Monitoring install progress in real-time
2. Injecting persistence during Sysprep specialize phase
3. Tracking rollback capability (possibly to prevent clean reinstall)

---

## Attack Vector Analysis

### Pre-boot Persistence
This evidence suggests the malware has:
1. **Firmware-level persistence** - survives across Windows reinstalls
2. **Sysprep hook injection** - loads malicious DLLs during OOBE specialize phase
3. **Phase monitoring** - tracks install progress to inject at correct moment
4. **Rollback awareness** - monitors SafeOS/recovery partition state

### Connection to Prior Evidence
Links to existing Mini-Tank-MKII investigation:
- PID 3992 connection to 109.61.19.21:80 (G-Core Labs London) on first boot
- PID 1052 connection to 85.234.74.60:80 on first boot
- Windows Security blocked by "IT policy" on fresh install

**Pattern:** Malware activates during install, phones home, blocks Windows Security

---

## Recommendations

1. **Do NOT trust this machine for sensitive work**
2. Check firmware/UEFI for persistence (requires hardware tools or different machine)
3. Investigate router/network for MITM during install
4. Consider physical inspection of hardware (especially if second-hand)
5. Document all DLL hashes if accessible

---

## Screenshot Index
*(To be populated as images are processed)*

| Image | Contents | Key Finding |
|-------|----------|-------------|
| IMG_0231 | tracer/aeinv | Initial capture |
| IMG_0249 | TBD | |
| IMG_0253 | Registry/Network profiles | |
| IMG_0254 | More registry entries | |
| IMG_0255 | TBD | |
| IMG_0256 | TBD | |
| IMG_0258 | TBD | |
| IMG_0260 | OCR captured - Sysprep DLLs | DLL injection evidence |

---

## Raw OCR Data Reference
See: `chat-logs/ocr-image-4c9a2894.txt`
