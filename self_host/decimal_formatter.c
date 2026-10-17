/*
 * Freestanding binary64 -> shortest-roundtrip decimal formatter.
 * Dragon4-style interval generation with fixed-size base-2^32 integers.
 * The 40-limb capacity covers the full binary64 exponent range; small
 * decimal quotient digits are found by subtraction, not big-integer division.
 */
typedef struct {
    unsigned int limb[40];
} KuroBig;

static void big_zero(KuroBig *a)
{
    unsigned int i;
    for (i = 0; i < 40; ++i) a->limb[i] = 0;
}

static void big_set(KuroBig *a, unsigned int value)
{
    big_zero(a);
    a->limb[0] = value;
}

static void big_copy(KuroBig *dst, const KuroBig *src)
{
    unsigned int i;
    for (i = 0; i < 40; ++i) dst->limb[i] = src->limb[i];
}

static void big_from_u64(KuroBig *a, unsigned long long value)
{
    big_zero(a);
    a->limb[0] = (unsigned int)value;
    a->limb[1] = (unsigned int)(value >> 32);
}

static void big_shift_left(KuroBig *a, unsigned int bits)
{
    unsigned int words = bits >> 5;
    unsigned int rem = bits & 31U;
    unsigned int i;
    if (words != 0) {
        for (i = 40; i > 0; --i) {
            unsigned int at = i - 1;
            a->limb[at] = at >= words ? a->limb[at - words] : 0;
        }
    }
    if (rem != 0) {
        unsigned int carry = 0;
        for (i = 0; i < 40; ++i) {
            unsigned long long v = ((unsigned long long)a->limb[i] << rem) | carry;
            a->limb[i] = (unsigned int)v;
            carry = (unsigned int)(v >> 32);
        }
    }
}

static void big_mul_small(KuroBig *a, unsigned int factor)
{
    unsigned int i;
    unsigned long long carry = 0;
    for (i = 0; i < 40; ++i) {
        unsigned long long v = (unsigned long long)a->limb[i] * factor + carry;
        a->limb[i] = (unsigned int)v;
        carry = v >> 32;
    }
}

static int big_compare(const KuroBig *a, const KuroBig *b)
{
    unsigned int i = 40;
    while (i != 0) {
        --i;
        if (a->limb[i] < b->limb[i]) return -1;
        if (a->limb[i] > b->limb[i]) return 1;
    }
    return 0;
}

static void big_subtract(KuroBig *a, const KuroBig *b)
{
    unsigned int i;
    unsigned long long borrow = 0;
    for (i = 0; i < 40; ++i) {
        unsigned long long av = a->limb[i];
        unsigned long long bv = (unsigned long long)b->limb[i] + borrow;
        a->limb[i] = (unsigned int)(av - bv);
        borrow = av < bv;
    }
}

/* Small nonnegative integer conversion, using place subtraction only. */
static unsigned int put_small_decimal(unsigned int value, char *out)
{
    static const unsigned int places[4] = { 1000U, 100U, 10U, 1U };
    unsigned int i, started = 0, n = 0;
    for (i = 0; i < 4; ++i) {
        unsigned int digit = 0;
        while (value >= places[i]) {
            value -= places[i];
            ++digit;
        }
        if (digit != 0 || started || places[i] <= 10U) {
            out[n++] = (char)('0' + digit);
            started = 1;
        }
    }
    return n;
}

unsigned int kuro_decimal_format(unsigned long long bits, char *out)
{
    unsigned long long fraction = bits & 0x000fffffffffffffULL;
    unsigned int expbits = (unsigned int)((bits >> 52) & 0x7ffULL);
    unsigned int negative = (unsigned int)(bits >> 63);
    unsigned int pos = 0;
    unsigned int digits_count = 0;
    char digits[24];
    int binary_exp;
    int decimal_exp = 0;
    unsigned long long significand;
    KuroBig n, d, low, high, temp;
    unsigned int inclusive;

    if (expbits == 0x7ffU) {
        if (fraction != 0) {
            out[0] = 'n'; out[1] = 'a'; out[2] = 'n'; out[3] = '\n';
            return 4;
        }
        if (negative) {
            out[0] = '-'; out[1] = 'i'; out[2] = 'n'; out[3] = 'f'; out[4] = '\n';
            return 5;
        }
        out[0] = 'i'; out[1] = 'n'; out[2] = 'f'; out[3] = '\n';
        return 4;
    }

    if (expbits == 0 && fraction == 0) {
        if (negative) out[pos++] = '-';
        out[pos++] = '0'; out[pos++] = '.'; out[pos++] = '0'; out[pos++] = '\n';
        return pos;
    }

    if (negative) out[pos++] = '-';
    if (expbits == 0) {
        significand = fraction;
        binary_exp = -1074;
    } else {
        significand = (1ULL << 52) | fraction;
        binary_exp = (int)expbits - 1023 - 52;
    }

    /* Scale the value and its rounding interval by four. */
    big_from_u64(&n, significand);
    big_shift_left(&n, 2);
    big_set(&low, 2U);
    big_set(&high, 2U);
    if (expbits > 1U && fraction == 0) big_set(&low, 1U);
    big_set(&d, 1U);
    if (binary_exp - 2 >= 0) {
        unsigned int shift = (unsigned int)(binary_exp - 2);
        big_shift_left(&n, shift);
        big_shift_left(&low, shift);
        big_shift_left(&high, shift);
    } else {
        big_shift_left(&d, (unsigned int)(2 - binary_exp));
    }
    inclusive = (unsigned int)(significand & 1ULL) == 0U;

    /* Normalize N/D to [1,10), tracking its base-ten exponent. */
    for (;;) {
        big_copy(&temp, &d);
        big_mul_small(&temp, 10U);
        if (big_compare(&n, &temp) < 0) break;
        big_copy(&d, &temp);
        ++decimal_exp;
    }
    while (big_compare(&n, &d) < 0) {
        big_mul_small(&n, 10U);
        big_mul_small(&low, 10U);
        big_mul_small(&high, 10U);
        --decimal_exp;
    }

    /* Generate decimal digits until the residual lies in the rounding interval. */
    for (;;) {
        unsigned int digit = 0;
        while (big_compare(&n, &d) >= 0) {
            big_subtract(&n, &d);
            ++digit;
        }
        digits[digits_count++] = (char)('0' + digit);

        {
            int low_ok, high_ok, round_up = 0;
            low_ok = big_compare(&n, &low) <= 0;
            big_copy(&temp, &d);
            big_subtract(&temp, &n);
            high_ok = big_compare(&temp, &high) <= 0;
            if (!inclusive) {
                if (big_compare(&n, &low) == 0) low_ok = 0;
                if (big_compare(&temp, &high) == 0) high_ok = 0;
            }
            if (low_ok || high_ok) {
                if (low_ok && high_ok) {
                    big_copy(&temp, &n);
                    big_mul_small(&temp, 2U);
                    {
                        int midpoint = big_compare(&temp, &d);
                        round_up = midpoint > 0 || (midpoint == 0 && ((digits[digits_count - 1] - '0') & 1));
                    }
                } else {
                    round_up = high_ok;
                }
                if (round_up) {
                    unsigned int j = digits_count;
                    while (j != 0 && digits[j - 1] == '9') {
                        digits[j - 1] = '0';
                        --j;
                    }
                    if (j == 0) {
                        digits[0] = '1';
                        digits_count = 1;
                        ++decimal_exp;
                    } else {
                        ++digits[j - 1];
                    }
                }
                break;
            }
        }
        big_mul_small(&n, 10U);
        big_mul_small(&low, 10U);
        big_mul_small(&high, 10U);
    }

    /* Python-compatible presentation threshold: scientific below 1e-4 or >=1e16. */
    if (decimal_exp < -4 || decimal_exp >= 16) {
        unsigned int evalue;
        unsigned int en;
        unsigned int i;
        out[pos++] = digits[0];
        if (digits_count > 1U) {
            out[pos++] = '.';
            for (i = 1; i < digits_count; ++i) out[pos++] = digits[i];
        }
        out[pos++] = 'e';
        if (decimal_exp < 0) {
            out[pos++] = '-';
            evalue = (unsigned int)(-decimal_exp);
        } else {
            out[pos++] = '+';
            evalue = (unsigned int)decimal_exp;
        }
        en = put_small_decimal(evalue, out + pos);
        pos += en;
    } else if (decimal_exp < 0) {
        int zeros = -decimal_exp - 1;
        int i;
        out[pos++] = '0';
        out[pos++] = '.';
        for (i = 0; i < zeros; ++i) out[pos++] = '0';
        for (i = 0; i < (int)digits_count; ++i) out[pos++] = digits[i];
    } else if ((unsigned int)decimal_exp >= digits_count - 1U) {
        unsigned int i;
        for (i = 0; i < digits_count; ++i) out[pos++] = digits[i];
        for (i = digits_count; i <= (unsigned int)decimal_exp; ++i) out[pos++] = '0';
        out[pos++] = '.';
        out[pos++] = '0';
    } else {
        unsigned int i;
        unsigned int split = (unsigned int)decimal_exp + 1U;
        for (i = 0; i < split; ++i) out[pos++] = digits[i];
        out[pos++] = '.';
        for (i = split; i < digits_count; ++i) out[pos++] = digits[i];
    }
    out[pos++] = '\n';
    return pos;
}
