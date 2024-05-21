

from PIL import Image


def image_to_bits(image_path):
    image = Image.open(image_path)
    image_data = image.convert('RGB').tobytes()

    bits = [format(byte, '08b') for byte in image_data]

    return bits, image.size

def bits_to_image(bits, image_size):

    image_data = bytes([int(byte, 2) for byte in bits])
    image = Image.frombytes('RGB', image_size, image_data)
    image.show()


image_path = "C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\lesson24\\image.jpg"


bits, image_size = image_to_bits(image_path)
print(len(bits))
print(image_size)

#bits_to_image(bits, image_size)

result = ''.join(bits)

