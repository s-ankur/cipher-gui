from Crypto.Cipher import DES
from Crypto import Random
from PIL import Image


def get_iv():
    return Random.new().read(DES.block_size)


def encrypt_image(path, path_out, cipher):
    with open(path, "rb") as f:
        image = f.read()
    header, image = image[:64], image[64:]
    image, ign = image[:(len(image) // 8) * 8], image[(len(image) // 8) * 8:]
    encrypted_image = cipher.encrypt(image)
    encrypted_image = encrypted_image + ign
    encrypted_image = header + encrypted_image
    with open(path_out, "wb") as f:
        f.write(encrypted_image)


if __name__ == '__main__':
    path = input()
    if path.endswith('.png') or path.endswith('.jpg'):
        image = Image.open(path)
        imag = image.convert('L').point(lambda x: 255 if x > 128 else 0, mode='1')
        imag.save(path[:-4] + '.bmp')
    key = bytes(input()[:8], 'ascii')
    cipher_ecb = DES.new(key, mode=DES.MODE_ECB)
    cipher_cbc = DES.new(key, DES.MODE_CBC, get_iv())
    encrypt_image(path[:-4] + '.bmp', path[:-4] + '_ecb' + '.bmp', cipher_ecb)
    encrypt_image(path[:-4] + '.bmp', path[:-4] + '_cbc' + '.bmp', cipher_cbc)
