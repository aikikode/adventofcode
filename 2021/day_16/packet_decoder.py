import operator
import re
import sys
from functools import reduce
from typing import List, Tuple

DEBUG = False


def debug(string: str):
    if DEBUG:
        print(string)


def convert_input(data: str) -> List[str]:
    m = re.search("^0+", data)
    prefix = ["0"] * 4 * len(m.group()) if m else []
    binary_data = prefix + list(bin(int(data, 16))[2:])
    padding = ["0"] * ((4 - len(binary_data) % 4) % 4)
    return padding + binary_data


def to_int(data: List[str]) -> int:
    return int("".join(data), 2)


def read_binary_number(data: List[str], idx: int) -> Tuple[int, int]:
    binary_number = []
    while data[idx] == "1":
        binary_number.extend(data[idx + 1:idx + 5])
        idx += 5
    binary_number.extend(data[idx + 1:idx + 5])
    return to_int(binary_number), idx + 5


def decode_packet(data: List[str], start_idx, tab="") -> Tuple[int, int, int]:
    version = to_int(data[start_idx:start_idx + 3])
    packet_type = to_int(data[start_idx + 3:start_idx + 6])
    debug_str = (
        f"{tab}"
        f"{''.join(data[start_idx:start_idx + 3])}({version}) "
        f"{''.join(data[start_idx + 3:start_idx + 6])}({packet_type})"
    )
    if packet_type == 4:
        result, next_idx = read_binary_number(data, start_idx + 6)
        debug_str = f"{debug_str}: {''.join(data[start_idx + 6:next_idx])}({result})"
        debug(debug_str)
        debug(f"{tab}<-{result}")
    else:
        subpacket_results = []
        length_type_id = data[start_idx + 6]
        debug_str = f"{debug_str} {data[start_idx + 6]}"
        debug(debug_str)
        if length_type_id == "0":
            subpackets_length = to_int(data[start_idx + 7:start_idx + 22])
            next_idx = start_idx + 22 + subpackets_length
            idx = start_idx + 22
            while idx < next_idx:
                v, _result, idx = decode_packet(data, idx, tab=f"  {tab}")
                version += v
                subpacket_results.append(_result)
        else:
            subpackets_count = to_int(data[start_idx + 7:start_idx + 18])
            subpackets_processed = 0
            next_idx = start_idx + 18
            while subpackets_processed < subpackets_count:
                v, _result, next_idx = decode_packet(data, next_idx, tab=f"  {tab}")
                version += v
                subpackets_processed += 1
                subpacket_results.append(_result)

        if packet_type == 0:
            result = sum(subpacket_results)
        elif packet_type == 1:
            result = reduce(operator.mul, subpacket_results)
        elif packet_type == 2:
            result = min(subpacket_results)
        elif packet_type == 3:
            result = max(subpacket_results)
        elif packet_type in [5, 6, 7]:
            assert len(subpacket_results) == 2
            if packet_type == 5:
                result = int(subpacket_results[0] > subpacket_results[1])
            elif packet_type == 6:
                result = int(subpacket_results[0] < subpacket_results[1])
            elif packet_type == 7:
                result = int(subpacket_results[0] == subpacket_results[1])
            else:
                raise Exception(f"Unsupported packet_type: {packet_type}")
        else:
            raise Exception(f"Unsupported packet_type: {packet_type}")
        debug(f"{tab}<-{result}")

    return version, result, next_idx


def get_versions_sum(data: List[str]) -> int:
    debug("".join(data))
    return decode_packet(data, 0)[0]


def get_result(data: List[str]) -> int:
    debug("".join(data))
    return decode_packet(data, 0)[1]


def run_tests():
    print("Running tests...")
    assert convert_input("4") == ["0", "1", "0", "0"]
    assert convert_input("04") == ["0", "0", "0", "0", "0", "1", "0", "0"]

    assert get_versions_sum(convert_input("D2FE28")) == 6
    assert get_versions_sum(convert_input("38006F45291200")) == 9
    assert get_versions_sum(convert_input("EE00D40C823060")) == 14
    assert get_versions_sum(convert_input("8A004A801A8002F478")) == 16
    assert get_versions_sum(convert_input("620080001611562C8802118E34")) == 12
    assert get_versions_sum(convert_input("C0015000016115A2E0802F182340")) == 23
    assert get_versions_sum(convert_input("A0016C880162017C3686B18A3D4780")) == 31

    # Type 0 (sum - OK)
    assert get_result(convert_input("C200B40A82")) == 3
    # Type 1 (product - OK)
    assert get_result(convert_input("04005AC33890")) == 54
    # Type 2 (min - OK)
    assert get_result(convert_input("880086C3E88112")) == 7
    # Type 3 (max - OK)
    assert get_result(convert_input("CE00C43D881120")) == 9
    assert get_result(convert_input("8C0086C3E88112")) == 9
    # Type 6
    assert get_result(convert_input("D8005AC2A8F0")) == 1
    # Type 5
    assert get_result(convert_input("F600BC2D8F")) == 0
    # Type 7 (equal - OK):
    assert get_result(convert_input("9C005AC2F8F0")) == 0
    assert get_result(convert_input("9C0141080250320F1802104A08")) == 1

    print("All done")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = convert_input([line.strip() for line in fin][0])
            print("part 1:", get_versions_sum(data))
            print("part 2:", get_result(data))
    else:
        run_tests()
