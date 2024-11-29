def parse_pla(file_path):
    """
    Parse a PLA file to extract the minterms.
    Returns the list of minterms as binary strings.
    """
    minterms = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() and not line.startswith("."):  # Ignore comments or directives
                parts = line.strip().split()
                if len(parts) > 1 and parts[1] == '1':  # Look for output = 1
                    minterms.append(parts[0])  # Add input binary
    return minterms

def group_minterms(minterms):
    """
    Groups minterms based on the number of 1's in the binary representation.
    Returns a dictionary of grouped minterms.
    """
    groups = {}
    for minterm in minterms:
        count = minterm.count('1')
        groups.setdefault(count, []).append(minterm)
    return groups

def combine_minterms(groups):
    """
    Combines minterms that differ by one bit.
    Returns new groups and the list of prime implicants.
    """
    new_groups = {}
    prime_implicants = set()
    checked = set()

    keys = sorted(groups.keys())
    for i in range(len(keys) - 1):
        for term1 in groups[keys[i]]:
            for term2 in groups[keys[i + 1]]:
                # Check if they differ by one bit
                diff = [j for j in range(len(term1)) if term1[j] != term2[j]]
                if len(diff) == 1:
                    new_term = term1[:diff[0]] + '-' + term1[diff[0] + 1:]
                    new_groups.setdefault(keys[i], []).append(new_term)
                    checked.add(term1)
                    checked.add(term2)
    
    # Add uncombined terms as prime implicants
    for group in groups.values():
        for term in group:
            if term not in checked:
                prime_implicants.add(term)

    return new_groups, prime_implicants

def find_prime_implicants(minterms):
    """
    Iteratively combine minterms and extract prime implicants.
    """
    groups = group_minterms(minterms)
    all_prime_implicants = set()

    while groups:
        groups, prime_implicants = combine_minterms(groups)
        all_prime_implicants.update(prime_implicants)

    return all_prime_implicants

def minimize_implicants(prime_implicants, minterms):
    """
    Build a prime implicant chart and use it to minimize the solution.
    """
    chart = {minterm: [] for minterm in minterms}
    for implicant in prime_implicants:
        for minterm in minterms:
            if is_covered(implicant, minterm):
                chart[minterm].append(implicant)

    # Extract essential prime implicants
    essential_implicants = set()
    for minterm, implicants in chart.items():
        if len(implicants) == 1:
            essential_implicants.add(implicants[0])

    return essential_implicants

def is_covered(implicant, minterm):
    """
    Check if a prime implicant covers a given minterm.
    """
    for i in range(len(implicant)):
        if implicant[i] != '-' and implicant[i] != minterm[i]:
            return False
    return True

def write_pla(output_path, reduced_logic):
    """
    Write the minimized logic to a PLA file.
    """
    with open(output_path, 'w') as file:
        file.write(".i <number of inputs>\n")
        file.write(".o <number of outputs>\n")
        for implicant in reduced_logic:
            file.write(f"{implicant} 1\n")
        file.write(".e\n")

# Example usage
input_path = 'input.pla'
output_path = 'output.pla'

minterms = parse_pla(input_path)
prime_implicants = find_prime_implicants(minterms)
reduced_logic = minimize_implicants(prime_implicants, minterms)
write_pla(output_path, reduced_logic)
print("PLA reduction complete. Output written to", output_path)
