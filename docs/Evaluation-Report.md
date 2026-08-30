# RAG Pipeline Evaluation Report

This report summarizes the results of the LLM-as-a-judge evaluation across different vector stores and embedders.

## Summary of Experiments

| Experiment | Accuracy | Avg Latency (sec) | Correct / Total |
|---|---|---|---|
| gemini_chroma | 60.0% | 0.00 | 6 / 10 |
| sentence_transformer_faiss | 20.0% | 0.00 | 2 / 10 |

## Detailed Results

### gemini_chroma Detailed Results

- **Q:** What is the minimum SIP amount for HDFC Mid Cap Fund?
  - **Score:** CORRECT
  - **Reasoning:** The answer directly provides the specific minimum SIP amount (₹ 100) as requested, includes a citation, and fulfills the single-fund factual lookup requirement.

- **Q:** What is the expense ratio of HDFC Nifty 50 Index Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The answer does not provide the requested expense ratio percentage, instead incorrectly claims the information is unavailable, failing to satisfy the factual lookup intent.

- **Q:** What is the exit load for HDFC ELSS Tax Saver Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant failed to provide the requested exit load information, instead claiming it was unavailable. The expected answer should include the exit load details, possibly in a structured format.

- **Q:** Who is the fund manager of HDFC Large Cap Fund and what is their prior experience?
  - **Score:** CORRECT
  - **Reasoning:** The answer provides the name(s) of the fund manager(s) for HDFC Large Cap Fund and includes detailed prior experience for each, fulfilling the multi-field retrieval request.

- **Q:** What is the benchmark index for HDFC Multi Cap Fund?
  - **Score:** CORRECT
  - **Reasoning:** The answer provides the specific benchmark index name for the HDFC Multi Cap Fund, which satisfies the factual lookup request.

- **Q:** What is the AUM of HDFC Gold ETF Fund of Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant did not provide the requested AUM value, instead stating the information is unavailable, which does not satisfy the factual lookup intent.

- **Q:** Which of these 9 funds has the lowest expense ratio?
  - **Score:** CORRECT
  - **Reasoning:** The answer appropriately acknowledges that the required information is not available, which aligns with the expected fallback behavior when context is insufficient.

- **Q:** What is the risk category of HDFC Small Cap Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant failed to provide the requested risk category for HDFC Small Cap Fund, instead claiming the information is unavailable, whereas the expected answer is a factual risk label.

- **Q:** What is the current NAV of HDFC Large Cap Fund?
  - **Score:** CORRECT
  - **Reasoning:** The answer provides a specific recent NAV value for the HDFC Large Cap Fund, includes a date indicating recency, and cites a source, fulfilling the request for the current NAV.

- **Q:** What is the dividend policy of HDFC Large Cap Fund?
  - **Score:** CORRECT
  - **Reasoning:** The answer explicitly states that the dividend policy information is not available, matching the expected 'Not found' intent.

### sentence_transformer_faiss Detailed Results

- **Q:** What is the minimum SIP amount for HDFC Mid Cap Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The answer states the minimum SIP amount is ₹100, but the typical minimum SIP for HDFC Mid Cap Fund is ₹500 (or another amount per official sources). The provided figure is likely inaccurate, so the answer does not satisfy the factual lookup request.

- **Q:** What is the expense ratio of HDFC Nifty 50 Index Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The answer does not provide the requested expense ratio percentage, instead incorrectly claims the information is unavailable, failing to satisfy the factual lookup intent.

- **Q:** What is the exit load for HDFC ELSS Tax Saver Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant failed to provide the requested exit load information, instead claiming it was unavailable. The expected answer should include the exit load details, possibly in a structured format.

- **Q:** Who is the fund manager of HDFC Large Cap Fund and what is their prior experience?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant failed to provide the requested fund manager name and prior experience, instead claiming the information is unavailable, which does not satisfy the multi-field retrieval intent.

- **Q:** What is the benchmark index for HDFC Multi Cap Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The answer provides a specific benchmark index, but it is not the correct benchmark for the HDFC Multi Cap Fund. The fund's typical benchmark is the Nifty Multi-Cap 250 Index (or similar), not the Nifty 500 Multicap 50:25:25 Total Return Index. Therefore the factual information is wrong.

- **Q:** What is the AUM of HDFC Gold ETF Fund of Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant did not provide the requested AUM value, instead stating the information is unavailable, which does not satisfy the factual lookup intent.

- **Q:** Which of these 9 funds has the lowest expense ratio?
  - **Score:** CORRECT
  - **Reasoning:** The answer appropriately acknowledges that the required information is not available, which aligns with the expected behavior of declaring inability when context is insufficient.

- **Q:** What is the risk category of HDFC Small Cap Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant failed to provide the requested risk category for HDFC Small Cap Fund, instead claiming the information is unavailable, whereas the expected answer is a factual risk label.

- **Q:** What is the current NAV of HDFC Large Cap Fund?
  - **Score:** INCORRECT
  - **Reasoning:** The assistant did not provide the requested recent NAV value for HDFC Large Cap Fund, instead stating the information is unavailable, which fails to meet the expected intent.

- **Q:** What is the dividend policy of HDFC Large Cap Fund?
  - **Score:** CORRECT
  - **Reasoning:** The answer explicitly states that the dividend policy information is not available, matching the expected 'Not found' response.

