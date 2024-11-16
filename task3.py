import timeit


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0  # Starting index in the main text
    iterations = 0  # Track the number of iterations

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Start from the end of the pattern

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
            iterations += 1  # Increment for each character comparison

        if j < 0:
            return (iterations, i)  # Pattern found

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
        iterations += 1

    return (iterations, -1)  # Pattern not found


def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    lps = [0] * m
    compute_lps_array(pattern, m, lps)
    i = j = 0
    iterations = 0  # Track iterations

    while i < n:
        iterations += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return (iterations, i - j)
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return (iterations, -1)


def compute_lps_array(pattern, m, lps):
    length = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1


def polynomial_hash(s, base=256, modulus=101):
    h = 0
    for char in s:
        h = (base * h + ord(char)) % modulus
    return h


def rabin_karp_search(text, pattern, base=256, modulus=101):
    m, n = len(pattern), len(text)
    if m > n:
        return (-1, -1)

    pattern_hash = polynomial_hash(pattern, base, modulus)
    text_hash = polynomial_hash(text[:m], base, modulus)
    h = pow(base, m - 1, modulus)
    iterations = 0  # Track iterations

    for i in range(n - m + 1):
        iterations += 1
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return (iterations, i)
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % modulus
            if text_hash < 0:
                text_hash += modulus

    return (iterations, -1)


def measure_performance(text, pattern):
    results = {}
    results['Boyer-Moore'] = timeit.timeit(lambda: boyer_moore_search(text, pattern), number=1)
    results['Knuth-Morris-Pratt'] = timeit.timeit(lambda: kmp_search(text, pattern), number=1)
    results['Rabin-Karp'] = timeit.timeit(lambda: rabin_karp_search(text, pattern), number=1)
    return results


def main():
    with open("article1.txt", "r", encoding="utf8") as file:
        text1 = file.read()
    with open("article2.txt", "r", encoding="utf8") as file:
        text2 = file.read()

    existing_substring = "таблиці"  # Replace with a substring present in the articles
    fictional_substring = "qwe123wetxcb2q34"

    print("Performance for article1.txt:")
    results1_existing = measure_performance(text1, existing_substring)
    results1_fictional = measure_performance(text1, fictional_substring)

    print("Existing substring:")
    print(results1_existing)
    print("Fictional substring:")
    print(results1_fictional)
    fastest1 = min(results1_existing, key=results1_existing.get)
    print(f"Fastest algorithm for article1.txt: {fastest1}")

    print("\nPerformance for article2.txt:")
    results2_existing = measure_performance(text2, existing_substring)
    results2_fictional = measure_performance(text2, fictional_substring)

    print("Existing substring:")
    print(results2_existing)
    print("Fictional substring:")
    print(results2_fictional)
    fastest2 = min(results2_existing, key=results2_existing.get)
    print(f"Fastest algorithm for article2.txt: {fastest2}")

    overall_fastest_existing = min(results1_existing.keys(), key=lambda k: results1_existing[k] + results2_existing[k])
    overall_fastest_fictional = min(results1_fictional.keys(),
                                    key=lambda k: results1_fictional[k] + results2_fictional[k])

    print("\nOverall fastest algorithm for existing substring search:", overall_fastest_existing)
    print("Overall fastest algorithm for fictional substring search:", overall_fastest_fictional)


if __name__ == "__main__":
    main()
