from scipy.stats import binomtest
for zeros in [482, 516, 530, 560]:
    p = binomtest(zeros, n=1000, p=0.5).pvalue
    verdict = 'no evidence' if p >= 0.05 else 'looks biased'
    print(f'{zeros} zeros: p-value = {p:.4f} -> {verdict}')
