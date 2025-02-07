import os
import signal
import tempfile
import argparse
import traceback
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait

from tqdm import tqdm


def test_single_case(
        tags: dict,
        code: str,
        test_in: str,
        test_out: str,
        timeout: int,
):
    test_flag = True
    success_flag = False 
    pass_flag = False
    test_output = ""

    if len(code.strip()) == 0:
        test_output = "Error: Empty code"
        return test_flag, success_flag, pass_flag, test_output, tags

    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        process = subprocess.Popen(
            ['python3', temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
            text=True
        )
        
        stdout, stderr = process.communicate(
            input=str(test_in),
            timeout=timeout
        )
        if stderr:
            test_output = "\nError: " + stderr.strip()
        else:
            success_flag = True
            test_output = stdout.strip()
            pass_flag = (
                test_output.strip() == str(test_out).strip()
            )
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        test_output = f"Timeout after {timeout} seconds"
    except Exception as e:
        test_output = f"Error: {str(e)}"
    finally:
        if temp_file:
            os.unlink(temp_file)

    return test_flag, success_flag, pass_flag, test_output, tags


def test_single_code(
        tags: dict,
        code: str,
        tests: dict,
        testing_workers: int,
        timeout: int,
):
    pass_flag = False
    test_res = {
        key: [
            {
                "input": tests[key]["input"][idx],
                "output": tests[key]["output"][idx],
                "test_flag": False,
                "success_flag": False,
                "pass_flag": False,
                "test_output": "",
            }
            for idx in range(len(tests[key]["input"]))
        ]
        for key in tests.keys()
    }
    with ProcessPoolExecutor(max_workers=testing_workers) as executor:
        futures = [
            executor.submit(
                test_single_case,
                tags={"test_key": test_key, "case_idx": case_idx},
                code=code,
                test_in=test["input"],
                test_out=test["output"],
                timeout=timeout,
            )
            for test_key in test_res.keys()
            for case_idx, test in enumerate(test_res[test_key])
        ]
        for future in as_completed(futures):
            if future.exception() is not None:
                print(f"###\nTERROR:\n{future.exception()}\n{traceback.format_exc()}\n###")
            else:
                test_flag, success_flag, pass_flag, test_output, tags_in = future.result()
                test_key = tags_in["test_key"]
                case_idx = tags_in["case_idx"]
                test_res[test_key][case_idx]["test_flag"] = test_flag
                test_res[test_key][case_idx]["success_flag"] = success_flag
                test_res[test_key][case_idx]["pass_flag"] = pass_flag
                test_res[test_key][case_idx]["test_output"] = test_output
                if not pass_flag:
                    for future in futures:
                        if not future.done():
                            future.cancel()
                    wait(futures)
                    break
        total_pass_flag = all(
            all(test["pass_flag"] for test in test_res[key])
            for key in test_res.keys()
        )
    return total_pass_flag, test_res, tags
