import sys
from wakeonlan import send_magic_packet
import socket
import struct

def get_broadcast_address(ip, subnet_mask):
    ip_parts = list(map(int, ip.split('.')))
    mask_parts = list(map(int, subnet_mask.split('.')))
    broadcast_parts = [(ip_parts[i] | (255 - mask_parts[i])) for i in range(4)]
    return '.'.join(map(str, broadcast_parts))

def send_wol_broadcast(ip_range, mac_address):
    # 计算广播地址
    broadcast_ip = get_broadcast_address(ip_range, '255.255.0.0')  # 假设是 /16 网络
    print(f"Sending WOL magic packet to broadcast address: {broadcast_ip}")

    # 发送魔法包
    send_magic_packet(mac_address, ip_address=broadcast_ip)

if __name__ == "__main__":
    # 网段范围和目标 MAC 地址
    ip_range = '59.79.0.0'  # 替换为您的网段
    mac_address = 'XX:XX:XX:XX:XX:XX'  # 替换为目标设备的 MAC 地址

    send_wol_broadcast(ip_range, mac_address)
