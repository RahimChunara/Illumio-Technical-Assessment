import csv
import sys
from collections import defaultdict

PROTOCOL_MAP = {
    '1':  'icmp',
    '6':  'tcp',
    '17': 'udp',
}

def load_lookup_table(lookup_file_path):
    lookup_dict = {}
    with open(lookup_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dstport = row['dstport'].strip().lower()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_dict[(dstport, protocol)] = tag
    return lookup_dict

def parse_flow_log_line(line):
    parts = line.strip().split()
    if len(parts) < 14:
        return None

    try:
        dstport = parts[6]
        protocol_num = parts[7]
        protocol_str = PROTOCOL_MAP.get(protocol_num, protocol_num)
        return (dstport, protocol_str.lower())
    except (IndexError, ValueError):
        return None

def main(flow_log_file_path, lookup_file_path):
    lookup_dict = load_lookup_table(lookup_file_path)
    
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    with open(flow_log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parsed = parse_flow_log_line(line)
            if not parsed:
                continue
            (dstport, protocol) = parsed
            # Count port/protocol
            port_protocol_counts[(dstport, protocol)] += 1
            # Count tag
            if (dstport.lower(), protocol.lower()) in lookup_dict:
                tag_counts[lookup_dict[(dstport.lower(), protocol.lower())]] += 1
            else:
                tag_counts["Untagged"] += 1

    # Write to file
    output_file = "flow_stats_output.csv"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Tag Counts:\n")
        out.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            out.write(f"{tag},{count}\n")

        out.write("\nPort/Protocol Combination Counts:\n")
        out.write("Port,Protocol,Count\n")
        for (port, proto), count in sorted(port_protocol_counts.items()):
            out.write(f"{port},{proto},{count}\n")

    print(f"Done! Results have been written to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <flow_logs_file> <lookup_csv_file>")
        sys.exit(1)

    flow_log_file = sys.argv[1]
    lookup_csv_file = sys.argv[2]
    main(flow_log_file, lookup_csv_file)
