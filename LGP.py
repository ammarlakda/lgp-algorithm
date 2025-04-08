"""
This program implements parts of a Linear Genetic Programming algorithm
CISC455/851 Winter'25
"""

import random

# Set random seed for reproducibility
random.seed(0)

# Define global parameters
operations = ['+', '-', '*', '/']
num_constants = 10
num_input_registers = 2
num_calc_registers = 2
total_registers = num_constants + num_input_registers + num_calc_registers

# Initialize registers: First `num_constants` registers are constants, others are initialized to 1
registers = [i if i < num_constants else 1 for i in range(total_registers)]

# Training Data (Inputs and Expected Outputs)
input_data = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
output_data = [3, 7, 11, 15, 19]

# Print register assignments
print(f"Output register: R{total_registers - 1}")
print(f"Input registers: {[f'R{i}' for i in range(num_constants, num_constants + num_input_registers)]}")

# For pretty-printing instructions
def pretty_print_instructions(instructions):
    for instruction in instructions:
        op = operations[instruction[0]]
        dest = f'R{instruction[1]}'
        src1 = f'R{instruction[2]}' if instruction[2] >= num_constants else f'{instruction[2]}  '
        src2 = f'R{instruction[3]}' if instruction[3] >= num_constants else f'{instruction[3]}'
        print(f'{dest} = {src1} {op} {src2}')


# Function to evaluate a program while removing introns only during execution
def evaluate(instructions, num_input_registers, num_calc_registers, input_data, output_data):
    original_instructions = instructions[:]  # Keep original program unchanged
    reduced_instructions = []
    total_error = 0

    # Step 1: **Identify Effective Instructions (Structural Intron Removal)**
    effective_registers = set([total_registers - 1])  # Start with only the output register (the last register)
    for instruction in instructions[::-1]:  # Process in reverse order
        if instruction[1] in effective_registers:  # If dest register is in the effective set
            reduced_instructions.append(instruction)
            effective_registers.remove(instruction[1])
            effective_registers.add(instruction[2])  # Mark source registers as effective
            effective_registers.add(instruction[3])

    reduced_instructions = reduced_instructions[::-1]  # Restore correct order

    # Step 2: **Evaluate Only Effective Instructions**
    for sample_index, sample in enumerate(input_data):
        # Create a fresh copy of registers for each sample
        local_registers = registers[:]

        # Initialize input registers
        for i, j in enumerate(range(num_constants, num_constants + num_input_registers)):
            local_registers[j] = sample[i]

        # Execute only effective instructions
        for instruction in reduced_instructions:
            op, dest, src1, src2 = instruction
            if op == 0:  # Addition
                local_registers[dest] = local_registers[src1] + local_registers[src2]
            elif op == 1:  # Subtraction
                local_registers[dest] = local_registers[src1] - local_registers[src2]
            elif op == 2:  # Multiplication
                local_registers[dest] = local_registers[src1] * local_registers[src2]
            elif op == 3:  # Protected Division
                local_registers[dest] = local_registers[src1] / local_registers[src2] if local_registers[src2] != 0 else 1
            else:
                raise ValueError('Invalid operation')

        # Step 3: **Compute Fitness (Sum of Squared Errors)**
        total_error += (local_registers[-1] - output_data[sample_index]) ** 2

    print(f'\nTotal Error: {total_error}\n')

    # Step 4: **Print Both Full and Reduced Programs**
    print("**Full Program (With Introns):**")
    pretty_print_instructions(original_instructions)

    print("\n**Effective Instructions (Introns Removed During Execution):**")
    pretty_print_instructions(reduced_instructions)

    return total_error


# Generate a random linear genetic program
def initialize(min_instructions, max_instructions, num_input_registers, num_calc_registers, const_prob=0.2):
    instructions = []
    num_instructions = random.randint(min_instructions, max_instructions)

    for _ in range(num_instructions):
        op = random.randint(0, len(operations) - 1)  # Choose an operation
        dest = random.randint(num_constants + num_input_registers, total_registers - 1)  # Destination register
        src1 = random.randint(0, num_constants - 1) if random.random() < const_prob else random.randint(num_constants, total_registers - 1)
        src2 = random.randint(0, num_constants - 1) if random.random() < const_prob else random.randint(num_constants, total_registers - 1)

        instructions.append([op, dest, src1, src2])

    # Return both the program and its fitness
    return instructions, evaluate(instructions, num_input_registers, num_calc_registers, input_data, output_data)


# Main function to generate a population of programs
def main():
    max_instructions = 10
    min_instructions = 5
    population_size = 2

    population = [initialize(min_instructions, max_instructions, num_input_registers, num_calc_registers) for _ in range(population_size)]



if __name__ == '__main__':
    main()
