import numpy as np
import matplotlib.pyplot as plt

# Thiết lập random seed để tái hiện kết quả
np.random.seed(42)

# Giả lập internal và external scores (theo phân phối chuẩn)
n_samples = 1000
internal_scores = np.random.normal(loc=0.6, scale=0.1, size=n_samples)
external_scores = np.random.normal(loc=0.8, scale=0.1, size=n_samples)

# Giới hạn điểm về khoảng [0, 1]
internal_scores = np.clip(internal_scores, 0, 1)
external_scores = np.clip(external_scores, 0, 1)

# Các giá trị lambda từ 0 → 1
lambdas = np.linspace(0, 1, 11)  # λ = 0.0, 0.1, ..., 1.0

# Tính toán final_score cho từng lambda
final_scores_by_lambda = []
for lam in lambdas:
    noise = np.random.uniform(-0.01, 0.01, size=n_samples)
    final_scores = (1 - lam) * internal_scores + lam * external_scores + noise
    final_scores_by_lambda.append(final_scores)

# Vẽ biểu đồ histogram (xấp xỉ phân bố)
plt.figure(figsize=(12, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(lambdas)))

for i, lam in enumerate(lambdas):
    plt.hist(final_scores_by_lambda[i], bins=50, alpha=0.4, density=True,
             label=f"λ = {lam:.1f}", color=colors[i])

plt.title("Phân bố điểm final_score theo từng lambda (λ)")
plt.xlabel("Final Score")
plt.ylabel("Mật độ xác suất (xấp xỉ)")
plt.legend(title="lambda")
plt.xlim(0, 1.05)
plt.tight_layout()
plt.show()
