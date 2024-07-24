import heapq
import os
import pickle


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):  # for those comparisons :100:
        return self.freq < other.freq


def main():

    print("Choose an option:")
    print("1. Compress a file")
    print("2. Decompress a file")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        file_path = input("Enter the path to the file to compress: ").strip()
        compressed_file_path = input("Enter the path to save the compressed file: ").strip()
        encoding_file_path = input("Enter the path to save the encoding information: ").strip()

        main_compression(file_path, compressed_file_path, encoding_file_path)
        print(f"File compressed and saved to {compressed_file_path}")
        print(f"Encoding information saved to {encoding_file_path}")

    elif choice == '2':
        compressed_file_path = input("Enter the path to the compressed file: ").strip()
        encoding_file_path = input("Enter the path to the encoding information file: ").strip()
        output_file_path = input("Enter the path to save the decompressed file: ").strip()

        main_decompression(compressed_file_path, encoding_file_path, output_file_path)
        print(f"File decompressed and saved to {output_file_path}")

    else:
        print("Invalid choice. Please enter 1 or 2.")
        main() # restart the program


def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies


def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:  # merge nodes
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]


def generate_huffman_codes(node, prefix="", codebook={}):  # generate huffman codes for each character
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook  # return the huffman codes


def compress_text(text, huffman_codes):  # compress the text
    encoded_text = ''.join(huffman_codes[char] for char in text)
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text = f"{encoded_text}{'0' * extra_padding}"
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        byte_array.append(int(byte, 2))

    return byte_array


def save_compressed_file(compressed_data, encoding_info, compressed_file_path, encoding_file_path):
    with open(compressed_file_path, 'wb') as compressed_file:
        compressed_file.write(compressed_data)

    with open(encoding_file_path, 'wb') as encoding_file:
        pickle.dump(encoding_info, encoding_file)


def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    return ''.join([char.lower() for char in text if char.islower() or char.upper()or char in ' .\n123456789'])  # only valid chars


def main_compression(file_path, compressed_file_path, encoding_file_path):
    text = read_file(file_path)
    frequencies = calculate_frequencies(text)
    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)
    compressed_data = compress_text(text, huffman_codes)
    save_compressed_file(compressed_data, huffman_codes, compressed_file_path, encoding_file_path)


def load_encoding_info(encoding_file_path):
    with open(encoding_file_path, 'rb') as encoding_file:
        encoding_info = pickle.load(encoding_file)
    return encoding_info


def decompress_text(compressed_data, huffman_codes):
    encoded_text = ""
    for byte in compressed_data:
        encoded_text += f"{byte:08b}"

    padded_info = encoded_text[:8]
    extra_padding = int(padded_info, 2)
    encoded_text = encoded_text[8:]
    encoded_text = encoded_text[:-extra_padding]

    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}

    current_code = ""
    decoded_text = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_text += reverse_huffman_codes[current_code]
            current_code = ""

    return decoded_text


def load_compressed_file(compressed_file_path):
    with open(compressed_file_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()
    return compressed_data


def main_decompression(compressed_file_path, encoding_file_path, output_file_path):
    huffman_codes = load_encoding_info(encoding_file_path)
    compressed_data = load_compressed_file(compressed_file_path)
    decoded_text = decompress_text(compressed_data, huffman_codes)

    with open(output_file_path, 'w') as output_file:
        output_file.write(decoded_text)


if __name__ == "__main__":
    main()
