import json

def main():
    data_path = "math_level3to5_data_processed_with_qwen_prompt.json"
    with open(data_path, "r") as fp:
        data = json.load(fp)
    print(len(data))

    transed_data = []
    for item in data:
        question  = item["input"].split("<|im_start|>user")[-1].split("<|im_end|>")[0].strip()
        item["input"] = """
<|im_start|>system
Please reason step by step, output your process answer in <answer> </answer> tags, and put your final answer within <final_answer> </final_answer> tags. Remember to put your exact answer whthin \\boxed{}.

Here is an output example:
To solve the problem .... <answer>\\boxed{...}</answer> However, ... <answer>\\boxed{...}</answer> Furthermore, ... <answer>\\boxed{...}</answer> ... To sum up, the final answer is <final_answer>\\boxed{...}</final_answer>.
<|im_end|>
<|im_start|>user
""".strip() + "\n" + question + "<|im_end|>\n<|im_start|>assistant"
        transed_data.append(item)
    
    with open(data_path.replace(".json", "_transed2multians.json"), "w") as fp:
        json.dump(transed_data, fp, indent=4)

if __name__ == "__main__":
    main()