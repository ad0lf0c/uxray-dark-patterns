# Data Dictionary

This file documents the main fields used in `dark_patterns.csv`.

| Field               | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| site                | Website domain or URL analysed                             |
| sector              | Website sector or category                                 |
| scan_date           | Date/time of the capture                                   |
| status              | analysed, inconclusive, blocked, or failed                 |
| rule_score          | Rule-based dark-pattern risk score                         |
| risk_level          | None, Low, Medium, or High                                 |
| banner_detected     | Whether consent/banner evidence was captured               |
| accept_detected     | Whether an accept action was detected                      |
| reject_detected     | Whether a reject action was detected                       |
| accept_reject_ratio | Area ratio between accept and reject buttons, if available |
| preselected_options | Whether pre-selected consent options were detected         |
| detected_patterns   | Dark-pattern categories detected by the pipeline           |
| reference_label     | Researcher-assigned reference label                        |
| notes               | Short explanation of the classification                    |

## Reference labels

| Label        | Meaning                                                                   |
| ------------ | ------------------------------------------------------------------------- |
| confirmed    | Visible evidence strongly supports a dark-pattern concern                 |
| suspected    | Partial or borderline evidence suggests risk                              |
| none         | Captured evidence appears balanced                                        |
| inconclusive | Site reached but evidence was insufficient                                |
| blocked      | Bot wall, CAPTCHA, timeout, or access barrier prevented normal assessment |
