import argparse

import json
import jsonlines


PROMPT = """
<|im_start|>system
Please reason step by step, and output the python code enclosed within delimiters in the end.

Output format:
...(your thinking)...
```python
# YOUR CODE HERE
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
        transed_data.append({
            "source": args.input_jsonl,
            "idx": idx,
            "input": PROMPT.format(question=item["description"].strip()),
            "answer": {
                "public_tests": item["public_tests"],
                "private_tests": item["private_tests"],
                "generated_tests": item["generated_tests"]
            }
        })
    
    print(f"Transed {len(transed_data)} data")
    with open(args.input_jsonl.replace(".jsonl", "_4_training.json"), "w") as fp:
        json.dump(transed_data, fp, indent=4)


if __name__ == "__main__":
    main()

    