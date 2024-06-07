import pandas as pd


def take_user_input():
    """As described, needs unpacking/unrolling params when called"""
    while True:
        try:
            p = int(input("Write parameter p: "))
            q = int(input("Write parameter q: "))
            c = int(input("Write ciphered message c: "))
            return p, q, c
        except ValueError:
            print("Bad user input, try again....")


def extended_gcd(phi_n):
    """Function takes in phi_n and returns algorithm values r, x, y needed for
    deciphering message c"""
    e = 67
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    s_values = ['-']
    r_values = ['-']
    x_values = ['-']
    y_values = ['-']
    phi_n_values = [phi_n]
    e_values = [e]
    x2_values = [x2]
    x1_values = [x1]
    y2_values = [y2]
    y1_values = [y1]

    while e > 0:
        s = phi_n // e
        r = phi_n - s * e
        x = x2 - s * x1
        y = y2 - s * y1
        phi_n, e = e, r
        x2, x1 = x1, x
        y2, y1 = y1, y

        s_values.append(s)
        r_values.append(r)
        x_values.append(x)
        y_values.append(y)
        phi_n_values.append(phi_n)
        e_values.append(e)
        x2_values.append(x2)
        x1_values.append(x1)
        y2_values.append(y2)
        y1_values.append(y1)

    df = pd.DataFrame({
        's': s_values,
        'r': r_values,
        'x': x_values,
        'y': y_values,
        'φ(n)': phi_n_values,
        'e': e_values,
        'x2': x2_values,
        'x1': x1_values,
        'y2': y2_values,
        'y1': y1_values
    })

    print(df.to_markdown(index=False))

    print("\nr: ", phi_n)
    print("x: ", x2)
    if y2_values[-1] < 0:
        y2_values[-1] += phi_n_values[0]
        print("y: ", y2_values[-1])
    else:
        print("y: ", y2_values[-1])

    return phi_n_values[-1], x2, y2_values[-1]


def modular_exponentiation(x, d, n):
    """Function returns the result of modular_exponentiation of x^a mod n
    and optionally shows results of each iteration of the loop as a table"""
    d_bin = bin(d)[2:]  # present d as a binary sequence
    w = 1

    # lists for tabular representation
    i_values = list(range(len(d_bin) - 1, -1, -1))  # iter from len(d_bin) - 1 to 0
    ai_values = ['-'] + list(d_bin)  # binary representation bits
    w_values = [1]  # primary w value

    print(f"Decimal representation of d: {d} has binary sequence: {d_bin}\n")

    for i, bit in enumerate(d_bin):
        w = (w * w) % n
        if bit == '1':
            w = (w * x) % n
        w_values.append(w)
        # print(f"Iteration {len(d_bin) - 1 - i} - bit: {bit}, w = {w}")

    # trimming lists
    ai_values = ai_values[:len(d_bin) + 1]
    w_values = w_values[:len(d_bin) + 1]

    # yet another tabular df
    df = pd.DataFrame({
        'i': ['-'] + i_values,
        'a_i': ai_values,
        'w': w_values
    })

    print(df.to_markdown(index=False))
    return w


if __name__ == "__main__":
    # unroll into variables
    p, q, c = take_user_input()

    # calculate n and φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    print(f"n = {n}")
    print(f"φ(n) = {phi_n}")

    # execute algo
    phi_n, x, d = extended_gcd(phi_n)

    # use modular exponentiation to decipher c into m
    m = modular_exponentiation(c, d, n)
    print(f"\nDecipher result: m = {m}")
