# AutoCrackerV2

## Overview

AutoCrackerV2 is a tool designed to automate the process of cracking Wi-Fi handshakes. It takes raw `.pcap` files, converts them into `.2200` files, and uses Hashcat to attempt to crack the passwords.

## Usage

1. Place your raw `.pcap` files into the `~/rawCAP/` directory.
2. Use the converter script to convert the `.pcap` files into `.2200` files for cracking.
3. Ensure that Hashcat (version 6.2.6) is included in the folder.
4. Run the `autocracker.py` script to start the cracking process.

## Legal Disclaimer

This tool is intended for educational purposes only. Unauthorized use of this tool to crack Wi-Fi passwords without permission is illegal and unethical. The authors of this tool are not responsible for any misuse or damage caused by this tool. Use it responsibly and only on networks you own or have explicit permission to test.
