from dataclasses import dataclass
from typing import List

@dataclass
class TestQuestion:
    id: int
    question: str
    expected_intent: str

TEST_QUESTIONS: List[TestQuestion] = [
    TestQuestion(1, "What is the minimum SIP amount for HDFC Mid Cap Fund?", "Single-fund factual lookup. Expect a specific currency amount."),
    TestQuestion(2, "What is the expense ratio of HDFC Nifty 50 Index Fund?", "Single-fund factual lookup. Expect a percentage."),
    TestQuestion(3, "What is the exit load for HDFC ELSS Tax Saver Fund?", "Table/structured data retrieval. Expect an explanation of exit loads."),
    TestQuestion(4, "Who is the fund manager of HDFC Large Cap Fund and what is their prior experience?", "Multi-field retrieval. Expect name and experience details."),
    TestQuestion(5, "What is the benchmark index for HDFC Multi Cap Fund?", "Single-fund factual lookup. Expect an index name."),
    TestQuestion(6, "What is the AUM of HDFC Gold ETF Fund of Fund?", "Single-fund factual lookup. Expect a large currency value (crores)."),
    TestQuestion(7, "Which of these 9 funds has the lowest expense ratio?", "Cross-document comparison. Expect the pipeline to evaluate multiple funds and return the one with the lowest expense ratio, or declare inability to do so if context is limited."),
    TestQuestion(8, "What is the risk category of HDFC Small Cap Fund?", "Single-fund factual lookup. Expect a risk label (e.g. Very High)."),
    TestQuestion(9, "What is the current NAV of HDFC Large Cap Fund?", "Scheduler test. Expect a recent NAV value."),
    TestQuestion(10, "What is the dividend policy of HDFC Large Cap Fund?", "'Not found' test. Expect the system to explicitly declare it cannot find this information in the context.")
]
