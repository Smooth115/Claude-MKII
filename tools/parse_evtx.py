#!/usr/bin/env python3
"""
EVTX Parser for Claude-MKII
Converts Windows Event Log files to JSON for analysis

Usage:
    python parse_evtx.py <evtx_file> [output.json] [--pids PID1,PID2] [--all]

Security Event IDs tracked:
    4688 - Process Created
    4689 - Process Terminated
    7045 - Service Installed
    7040 - Service Start Type Changed
    1102 - Audit Log Cleared
    4697 - Service Installed (Security)
    4698 - Scheduled Task Created
    5379 - Credential Manager Read
    1100 - Event Logging Shutdown
    1101 - Audit Events Dropped
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    from evtx import PyEvtxParser
except ImportError:
    print("ERROR: python-evtx not installed")
    print("Install with: pip install evtx")
    sys.exit(1)

# Security-relevant event IDs
SECURITY_EVENTS = {
    4688: "Process Created",
    4689: "Process Terminated",
    7045: "Service Installed",
    7040: "Service Start Type Changed",
    1102: "Audit Log Cleared",
    4697: "Service Installed (Security)",
    4698: "Scheduled Task Created",
    5379: "Credential Manager Read",
    1100: "Event Logging Shutdown",
    1101: "Audit Events Dropped",
    # Network events
    5156: "Windows Filtering Platform Connection",
    5158: "Windows Filtering Platform Bind",
    # Logon events
    4624: "Successful Logon",
    4625: "Failed Logon",
    4648: "Explicit Credentials Logon",
}


def extract_event_id(data):
    """Extract event ID from parsed event data."""
    try:
        event_id = data.get('Event', {}).get('System', {}).get('EventID')
        if isinstance(event_id, dict):
            event_id = event_id.get('#text')
        return int(event_id) if event_id else None
    except (ValueError, TypeError):
        return None


def extract_process_info(data):
    """Extract process creation info from 4688 events."""
    try:
        event_data = data.get('Event', {}).get('EventData', {})
        if not event_data:
            return {}
        
        # Direct dict format (most common in modern EVTX)
        if isinstance(event_data, dict):
            # Check if it's already a flat dict with process info
            if 'NewProcessId' in event_data or 'NewProcessName' in event_data:
                return {
                    'NewProcessId': event_data.get('NewProcessId', ''),
                    'NewProcessName': event_data.get('NewProcessName', ''),
                    'ProcessId': event_data.get('ProcessId', ''),
                    'ParentProcessName': event_data.get('ParentProcessName', ''),
                    'CommandLine': event_data.get('CommandLine', ''),
                    'SubjectUserName': event_data.get('SubjectUserName', ''),
                    'SubjectDomainName': event_data.get('SubjectDomainName', ''),
                    'TargetUserName': event_data.get('TargetUserName', ''),
                }
            
            # Legacy format with Data array
            items = event_data.get('Data', [])
            if isinstance(items, list):
                info = {}
                for item in items:
                    if isinstance(item, dict) and '@Name' in item:
                        info[item['@Name']] = item.get('#text', '')
                return info
        return {}
    except Exception:
        return {}


def parse_evtx(filepath, filter_ids=None, target_pids=None, include_all=False):
    """
    Parse EVTX file and extract events.
    
    Args:
        filepath: Path to EVTX file
        filter_ids: Set of event IDs to include (None = security events only)
        target_pids: List of PIDs to search for in process events
        include_all: If True, include all events regardless of ID
    
    Returns:
        List of parsed events
    """
    parser = PyEvtxParser(filepath)
    events = []
    
    for record in parser.records_json():
        try:
            data = json.loads(record['data'])
            event_id = extract_event_id(data)
            
            # Filter by event ID unless include_all
            if not include_all:
                if filter_ids and event_id not in filter_ids:
                    continue
            
            event = {
                'timestamp': record['timestamp'],
                'event_id': event_id,
                'event_name': SECURITY_EVENTS.get(event_id, 'Unknown'),
                'record_id': record.get('record_id'),
            }
            
            # For process events, extract detailed info
            if event_id == 4688:
                proc_info = extract_process_info(data)
                event['process_info'] = proc_info
                
                # If searching for specific PIDs
                if target_pids:
                    new_pid = proc_info.get('NewProcessId', '')
                    parent_pid = proc_info.get('ProcessId', '')
                    
                    pid_matches = False
                    for pid in target_pids:
                        pid_str = str(pid).strip()
                        
                        # Convert decimal to hex for comparison
                        try:
                            if pid_str.isdigit():
                                pid_hex = hex(int(pid_str))
                            elif pid_str.lower().startswith('0x'):
                                pid_hex = pid_str.lower()
                            else:
                                # Skip invalid PID format
                                continue
                        except ValueError:
                            continue
                        
                        # Check both decimal and hex representations
                        if (pid_str in new_pid or pid_str in parent_pid or
                            pid_hex in new_pid.lower() or pid_hex in parent_pid.lower()):
                            pid_matches = True
                            break
                    
                    if not pid_matches:
                        continue
            
            # Include raw data for debugging
            event['raw'] = data
            events.append(event)
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            # Log parsing errors but continue
            events.append({
                'timestamp': record.get('timestamp', 'unknown'),
                'error': str(e),
                'record_id': record.get('record_id'),
            })
    
    return events


def main():
    parser = argparse.ArgumentParser(
        description='Parse Windows EVTX files to JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('evtx_file', help='Path to EVTX file')
    parser.add_argument('output', nargs='?', help='Output JSON file (default: stdout)')
    parser.add_argument('--pids', help='Comma-separated PIDs to search for')
    parser.add_argument('--all', action='store_true', help='Include all events, not just security')
    parser.add_argument('--ids', help='Comma-separated event IDs to filter')
    parser.add_argument('--summary', action='store_true', help='Print summary only')
    
    args = parser.parse_args()
    
    # Check file exists
    if not Path(args.evtx_file).exists():
        print(f"ERROR: File not found: {args.evtx_file}", file=sys.stderr)
        sys.exit(1)
    
    # Parse filter options
    filter_ids = set(SECURITY_EVENTS.keys())
    if args.ids:
        filter_ids = set(int(x.strip()) for x in args.ids.split(','))
    
    target_pids = None
    if args.pids:
        target_pids = [x.strip() for x in args.pids.split(',')]
    
    # Parse the file
    print(f"Parsing: {args.evtx_file}", file=sys.stderr)
    events = parse_evtx(
        args.evtx_file,
        filter_ids=filter_ids if not args.all else None,
        target_pids=target_pids,
        include_all=args.all
    )
    
    print(f"Found {len(events)} events", file=sys.stderr)
    
    if args.summary:
        # Print summary by event type
        from collections import Counter
        counts = Counter(e.get('event_id') for e in events)
        print("\nEvent Summary:")
        for event_id, count in sorted(counts.items()):
            name = SECURITY_EVENTS.get(event_id, 'Unknown')
            print(f"  {event_id}: {name} - {count} events")
        return
    
    # Output
    output_data = {
        'source_file': str(args.evtx_file),
        'parsed_at': datetime.now(timezone.utc).isoformat(),
        'total_events': len(events),
        'events': events
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"Wrote {len(events)} events to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output_data, indent=2, default=str))


if __name__ == "__main__":
    main()
