# Flow Log Tagging and Analysis

Solution to Illumio Technical Assessment

## Features
- Supports **AWS VPC Flow Logs (version 2)** in default format.
- Provides a count of:
  - Matches for each tag.
  - Occurrences of `(destination port, protocol)` pairs.
- Generates a plain text output file (`flow_stats_output.txt`).

---

## Assumptions
1. **Flow Log Format**: The program supports only AWS VPC Flow Log **version 2** and assumes the default format.
2. **Case Insensitivity**: Matches `(destination port, protocol)` values in a case-insensitive manner.
3. **Protocol Mapping**: Recognizes protocols `icmp`, `tcp`, and `udp` based on numeric protocol values (`1`, `6`, `17`). Unrecognized protocols are processed as-is.
4. **Dependencies**: Uses only built-in Python libraries (`csv`, `sys`, `defaultdict`).
5. **Custom Formats**: Custom flow log formats are not supported.
6. **Tagged and Untagged**: Any log entry without a matching tag is categorized as "Untagged."

---

## Usage

### Prerequisites
- Python 3.6 or later installed on your machine.

### Running the Script
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

### Running the Script
To run the script, use the following command:
```bash
python3 script.py flow_logs.txt lookup_table.csv

