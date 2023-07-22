import hashlib
import random
import string

NUM_BYTES = 4
TARGET = "00000"
N = 20


def find_nonce(hashed_text, target, byte_length):
    target_len = len(target)
    # loop through hex values
    for h in range(2 ** (8 * byte_length)):
        nonce = str(hex(h))[2:]

        # add to start of hashed text and rehash
        hashed_with_nonce = nonce + hashed_text
        rehashed_text = hashlib.sha256(hashed_with_nonce.encode("utf-8")).hexdigest()

        # compare first chars with target
        if TARGET == rehashed_text[:target_len]:
            return rehashed_text, nonce

    return rehashed_text, None


def main():
    plaintext = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N)
    )
    hashed_text = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
    print(f"{plaintext=}, {hashed_text=}")

    rehashed_text, nonce = find_nonce(hashed_text, TARGET, NUM_BYTES)
    if nonce:
        print(f"Found nonce for target hash {TARGET}. {rehashed_text=}, {nonce=}")
    else:
        print(f"Found no nonce for target hash {TARGET}.")


if __name__ == "__main__":
    main()
