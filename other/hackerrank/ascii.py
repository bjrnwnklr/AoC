def decode(encoded):
    rev = list(encoded[::-1])

    buffer = ""
    result = ""
    while rev:
        c = rev.pop(0)
        buffer += c

        i = int(buffer)
        if (65 <= i <= 90) or (97 <= i <= 122) or (i == 32):
            result += chr(i)
            buffer = ""

    return result


if __name__ == "__main__":
    encoded = "23511011501782351112179911801562340161171141148"
    assert decode(encoded) == "Truth Always Wins "

    encoded = "2312179862310199501872379231018117927"
    assert decode(encoded) == "Have a Nice Day "

    encoded = "1219950180111108236115111016623101401611235115012312161151110101111127"
    assert decode(encoded) == "Honesty is the Best Policy"
