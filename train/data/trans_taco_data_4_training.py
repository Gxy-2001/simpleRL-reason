import argparse

import json
import jsonlines


PROMPT = """
<|im_start|>system
Please reason step by step, and output the python code enclosed within delimiters in the end.

Output format:
...(your thinking)...
```python
{starter_code}
```<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
""".strip()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_jsonl', type=str, required=True)
    return parser.parse_args()


def main():
    args = get_args()
    with jsonlines.open(args.input_jsonl) as reader:
        data = list(reader)
    
    transed_data = []
    for idx, item in enumerate(data):
        starter_code = item["starter_code"].strip()
        if len(starter_code.strip()) == 0:
            prompt = PROMPT.replace("{starter_code}", "# YOUR CODE HERE")
        else:
            prompt = PROMPT.replace("{starter_code}", starter_code)
        transed_data.append({
            "source": args.input_jsonl,
            "idx": idx,
            "input": prompt.format(question=item["question"].strip()),
            "answer": {
                "input_output": item["input_output"],
            }
        })
    
    print(f"Transed {len(transed_data)} data")
    with open(args.input_jsonl.replace(".jsonl", "_4_training.json"), "w") as fp:
        json.dump(transed_data, fp, indent=4)


if __name__ == "__main__":
    main()

    