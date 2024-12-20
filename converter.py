import os
import subprocess
import pyshark
import asyncio
import time

def check_complete_handshake(pcap_file):
    try:
        cap = pyshark.FileCapture(pcap_file, display_filter="eapol.keydes.type == 2")
        messages = {1: False, 2: False, 3: False, 4: False}

        for packet in cap:
            try:
                msg_number = int(packet.layers[4].wlan_rsna_keydes_msgnr)
                if msg_number in messages:
                    messages[msg_number] = True
            except AttributeError:
                continue
        
        # Properly closing the capture
        cap.close()
        
        return all(messages.values())
    except pyshark.capture.capture.TSharkCrashException as e:
        print(f"Error processing {pcap_file}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error processing {pcap_file}: {e}")
        return False

def convert_to_22000(pcap_file, output_file):
    try:
        pcap_file_wsl = subprocess.run(['wsl', 'wslpath', '-a', pcap_file.replace('\\', '\\\\')], capture_output=True, text=True, check=True).stdout.strip()
        output_file_wsl = subprocess.run(['wsl', 'wslpath', '-a', output_file.replace('\\', '\\\\')], capture_output=True, text=True, check=True).stdout.strip()

        print(f"pcap_file_wsl: {pcap_file_wsl}")
        print(f"output_file_wsl: {output_file_wsl}")

        command = f"wsl hcxpcapngtool -o {output_file_wsl} {pcap_file_wsl}"
        print(f"command: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pcap_file} to {output_file}: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error during conversion: {e}")

def main(pcap_dir):
    output_dir = r"D:\\fun\\AutoCrackerV2\\handshakes"
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(pcap_dir):
        if filename.endswith('.pcap'):
            pcap_file = os.path.join(pcap_dir, filename)
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.22000")

            if check_complete_handshake(pcap_file):
                print(f"Complete handshake found in {filename}")
                convert_to_22000(pcap_file, output_file)
            else:
                print(f"Incomplete handshake in {filename}")

if __name__ == "__main__":
    pcap_dir = r"D:\\fun\\AutoCrackerV2\\rawCAP"  # Replace with your actual directory path
    main(pcap_dir)
