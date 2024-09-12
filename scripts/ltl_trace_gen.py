import random
import json

def generate_ltl_trace(symbols, length):
    trace = []

    for _ in range(length):
        instant_size=random.randint(0, len(symbols))
        instant = random.sample(symbols, instant_size)
        trace.append(instant)

    return trace

def generate_json(pos_traces_count, neg_traces_count, symbols, length, signature=[]):
    
    if signature:
        json_output = {"P": [], "N": [], "S": signature}
    
    else:
        json_output = {"P": [], "N": []}

    for _ in range(pos_traces_count):
        trace = generate_ltl_trace(symbols, length)
        json_output["P"].append(trace)

    for _ in range(neg_traces_count):
        trace = generate_ltl_trace(symbols, length)
        json_output["N"].append(trace)

    return json_output

def main():
    all_symbols = ["p", "q", "r", "s", "t"]
    max_count = 5

    for pos_count in range(1, max_count+1):
        for neg_count in range(1, max_count+1):
            for symbol_count in range(1, len(all_symbols)+1):
                symbols = random.sample(all_symbols, symbol_count)
                for length in [5, 10, 15, 20, 25, 30]:
                    for sig_size in range(1, symbol_count+1):
                        signature = random.sample(symbols, sig_size)
                        json_output = generate_json(pos_count, neg_count, symbols, length, signature)

                        filename = f'output_pos{pos_count}_neg{neg_count}_symbols{"_".join(symbols)}_length{length}_sig{"_".join(signature)}.json'

                        with open(filename, 'w') as f:
                            json.dump(json_output, f, indent=2)
                        
                        print(f"Generated {filename}")

if __name__ == "__main__":
    main()