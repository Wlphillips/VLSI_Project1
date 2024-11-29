import sys
from itertools import combinations


def read_pla_file(filename):
    """Reads a PLA file and extracts the raw data."""
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)


def parse_pla_data(pla_data):
    """Parse the PLA data from a string into minterms, number of inputs, and outputs."""
    lines = pla_data.splitlines()
    num_inputs = 0
    num_outputs = 0
    minterms = []
    
    for line in lines:
        # Ignore comments and blank lines
        if line.startswith("."):
            if line.startswith(".i"):
                num_inputs = int(line.split()[1])
            elif line.startswith(".o"):
                num_outputs = int(line.split()[1])
            continue
        
        # Process the minterms
        parts = line.split()
        if len(parts) == 2:  # Only consider lines with exactly 2 elements (minterm and output)
            term, output = parts
            print(f"Debug: Parsing line: {line}, parts: {parts}")
            if output == '1':  # Only consider minterms where the output is 1
                minterms.append(term)
            else:
                print(f"Debug: Skipped term: {term} because output is {output}")
    
    print(f"Debug: Final minterms: {minterms}")
    return minterms, num_inputs, num_outputs


def quine_mccluskey(num_inputs, minterms):
    """Implements the Quine-McCluskey algorithm for logic minimization."""
    def count_ones(binary_string):
        return binary_string.count('1')

    def combine_terms(term1, term2):
        """Combine two terms if they differ by exactly one bit."""
        diff_count = 0
        combined = []
        for b1, b2 in zip(term1, term2):
            if b1 != b2:
                diff_count += 1
                combined.append('-')
            else:
                combined.append(b1)
        if diff_count == 1:
            return ''.join(combined)
        return None

    # Step 1: Group minterms by the number of 1s in their binary representation
    groups = {i: [] for i in range(num_inputs + 1)}
    print(f"Debug: Initial minterms: {minterms}")  # Debugging line
    for term in minterms:
        if len(term) != num_inputs or not all(c in '01-' for c in term):
            print(f"Warning: Invalid term skipped: {term}")
            continue
        groups[count_ones(term)].append(term)

    print(f"Debug: Grouped terms: {groups}")  # Debugging line

    # Step 2: Iteratively combine terms
    prime_implicants = set()
    while True:
        next_groups = {i: [] for i in range(num_inputs + 1)}
        used = set()
        for i in range(num_inputs):
            for term1 in groups[i]:
                for term2 in groups[i + 1]:
                    combined = combine_terms(term1, term2)
                    if combined:
                        next_groups[count_ones(combined)].append(combined)
                        used.add(term1)
                        used.add(term2)
        for group in groups.values():
            for term in group:
                if term not in used:
                    prime_implicants.add(term)

        print(f"Debug: Prime implicants: {prime_implicants}")  # Debugging line

        if not any(next_groups.values()):  # Stop if no more combinations are possible
            break
        groups = next_groups

    return sorted(prime_implicants)



def write_pla_output(filename, minimized_terms, num_inputs, num_outputs):
    """Writes the minimized output to a PLA file."""
    with open(filename, 'w') as file:
        file.write(f".i {num_inputs}\n")
        file.write(f".o {num_outputs}\n")
        for term in minimized_terms:
            file.write(f"{term} 1\n")
        file.write(".e\n")


def main():
    """Main function to read PLA file and run Quine-McCluskey."""
    # Check if a file argument was provided
    if len(sys.argv) < 2:
        print("Usage: python quine_mccluskey.py <input_file>")
        sys.exit(1)
    
    # Use the input file provided via the command line
    input_file = sys.argv[1]
    print(f"Reading input file: {input_file}")
    
    # Read the content of the PLA file
    with open(input_file, 'r') as file:
        pla_data = file.read()

    # Parse the PLA data
    minterms, num_inputs, num_outputs = parse_pla_data(pla_data)

    # Run the Quine-McCluskey algorithm
    minimized_terms = quine_mccluskey(num_inputs, minterms)

    print(f"Minimized terms: {minimized_terms}")

    # Write the minimized logic to a new PLA file
    output_file = input_file.replace('.pla', '_minimized.pla')
    with open(output_file, 'w') as file:
        file.write(f'.i {num_inputs}\n.o {num_outputs}\n')
        for term in minimized_terms:
            file.write(f'{term} 1\n')
        file.write('.e\n')

    print(f"Minimized logic written to {output_file}")

if __name__ == "__main__":
    main()