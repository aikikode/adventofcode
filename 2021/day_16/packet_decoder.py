import sys
from typing import List, Tuple, Optional


def convert_input(data: str) -> List[str]:
    binary_data = list(bin(int(data, 16))[2:])
    padding = ["0"] * ((4 - len(binary_data) % 4) % 4)
    return padding + binary_data


def to_int(data: List[str]) -> int:
    return int("".join(data), 2)


def read_binary_number(data: List[str], idx: int) -> int:
    while data[idx] == "1":
        idx += 5
    return idx + 5


def decode_packet(data: List[str], start_idx) -> Tuple[int, int]:
    version = to_int(data[start_idx:start_idx + 3])
    packet_type = to_int(data[start_idx + 3:start_idx + 6])
    if packet_type == 4:
        next_idx = read_binary_number(data, start_idx + 6)
    else:
        length_type_id = data[start_idx + 6]
        if length_type_id == "0":
            subpackets_length = to_int(data[start_idx + 7:start_idx + 22])
            next_idx = start_idx + 22 + subpackets_length
            idx = start_idx + 22
            while idx < next_idx:
                v, idx = decode_packet(data, idx)
                version += v
        else:
            subpackets_count = to_int(data[start_idx + 7:start_idx + 18])
            subpackets_processed = 0
            next_idx = start_idx + 18
            while subpackets_processed < subpackets_count:
                v, next_idx = decode_packet(data, next_idx)
                version += v
                subpackets_processed += 1

    return version, next_idx


def get_versions_sum(data: List[str], start_idx: Optional[int] = None) -> int:
    start_idx = start_idx or 0
    return decode_packet(data, start_idx)[0]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin][0]
            print("part 1:", get_versions_sum(convert_input(data)))
            # print("part 2:", get_shortest_extended_path_len(convert_input(data)))

assert get_versions_sum(convert_input("D2FE28")) == 6
assert get_versions_sum(convert_input("38006F45291200")) == 9
assert get_versions_sum(convert_input("EE00D40C823060")) == 14
assert get_versions_sum(convert_input("8A004A801A8002F478")) == 16
assert get_versions_sum(convert_input("620080001611562C8802118E34")) == 12
assert get_versions_sum(convert_input("C0015000016115A2E0802F182340")) == 23
assert get_versions_sum(convert_input("A0016C880162017C3686B18A3D4780")) == 31
#
