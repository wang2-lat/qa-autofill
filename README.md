# qa-autofill

Automate security questionnaire filling for SaaS sales teams.

## Problem

SaaS companies spend 4-5 hours filling 200-question security questionnaires for every enterprise deal. Sales and customer success teams waste time on repetitive copy-paste work instead of talking to customers.

## Solution

This CLI tool maintains a standard answer database and automatically fills questionnaires by matching questions with stored answers.

## Installation


## Usage

### Add Q&A pairs to database


### List all Q&A pairs


### Update a Q&A pair


### Delete a Q&A pair


### Fill a questionnaire

Input file must be Excel (.xlsx) or CSV with a "Question" column.


The threshold (0-1) controls matching sensitivity. Higher = stricter matching.

## File Format

Input questionnaire should have at least a "Question" column:

| Question | Answer |
|----------|--------|
| What is your data retention policy? | |
| Do you perform penetration testing? | |

The tool will fill the "Answer" column based on your database.

## Tips

- Start with common security questions your team answers repeatedly
- Use threshold 0.6-0.8 for good balance between accuracy and coverage
- Review auto-filled answers before sending to customers
- Keep your answer database updated as policies change
# 添加答案
python main.py add "Do you encrypt data?" "Yes, AES-256 for rest, TLS 1.3 for transit"

# 查看所有答案
python main.py list

# 自动填充问卷
python main.py fill questionnaire.xlsx filled.xlsx --threshold 0.7