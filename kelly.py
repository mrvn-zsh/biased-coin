# The math part: growth rate, Kelly fraction, and the point where you start losing.
#
# Setup: a coin lands on heads with probability p (here 0.6).
# Each flip you bet a fraction f of your money on heads:
#   - heads: your money is multiplied by (1 + f)
#   - tails: your money is multiplied by (1 - f)

from math import log

P_HEADS = 0.6


def exp_wealth(w0, f, n, p=P_HEADS):
    return w0 * (1 + (2 * p - 1) * f) ** n


def growth(f, p=P_HEADS):
    if f >= 1:
        # ln(0) is -infinity: if you bet everything you lose everything at the first tails
        return float("-inf")
    return p * log(1 + f) + (1 - p) * log(1 - f)


def kelly_f(p=P_HEADS):
    return 2 * p - 1


def ruin_thresh(p=P_HEADS):
    low = kelly_f(p)   # here g > 0
    high = 0.999999           # here g < 0
    for i in range(60):
        mid = (low + high) / 2
        if growth(mid, p) > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


if __name__ == "__main__":
    f_star = kelly_f()
    print("Probability of heads:", P_HEADS)
    print(f"Kelly fraction f* = {f_star:.2f}")
    print(f"Growth rate at f*: g(f*) = {growth(f_star):.4f} per flip")
    print(f"g(f) < 0 when f > {ruin_thresh():.3f}")
    print()
    print("  f     g(f)      E[W_100] (start 25)")
    for f in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8]:
        print(f"  {f:.2f}  {growth(f):+.4f}   {exp_wealth(25, f, 100):,.0f}")
