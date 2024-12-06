from StackHanoi import Stack

print("\nLet's play the Tower of Hanoi!")

# Initialize an empty list to store the stacks
stacks = []

# Create three instances of the Stack class for the three rods
left_stack = Stack("Left")
middle_stack = Stack("Middle")
right_stack = Stack("Right")

# Add the stacks to the list of stacks
stacks += [left_stack, middle_stack, right_stack]

# Ask the user for the number of disks to play with
num_disks = int(input("\nHow many disks would you like to play with?\n"))

# Validate the number of disks; if less than 3, prompt again
while num_disks < 3:
    num_disks = int(input("Please enter a number greater than or equal to 3\n"))

# Add the disks to the left stack, from largest to smallest
for disk in range(num_disks, 0, -1):
    left_stack.push(disk)

# Calculate the optimal number of moves to solve the game
num_optimal_moves = 2 ** num_disks - 1
print(f"\nThe fastest you can solve this game is in {num_optimal_moves} moves")

# Function to get valid user input for selecting stacks
def get_input():
    # Generate valid choices based on the first letter of each stack's name
    choices = [stack.get_name()[0] for stack in stacks]

    while True:
        print("\nOptions:")
        # Display the stacks with their corresponding first letter choices
        for i in range(len(stacks)):
            name = stacks[i].get_name()
            letter = choices[i]
            print(f"Type {letter} for {name}")
        
        # Get and process the user input
        user_input = input("").strip().upper()
        
        # Check if the input is valid
        if user_input in choices:
            # Return the corresponding stack object
            for i in range(len(stacks)):
                if user_input == choices[i]:
                    return stacks[i]

# Game loop: Continue until all disks are moved to the right stack
num_user_moves = 0  # Initialize a counter for the user's moves

while right_stack.get_size() != num_disks:  # The game ends when the right stack holds all disks
    print("\n\n\n...Current stacks...")
    # Display the current state of all stacks
    for stack in stacks:
        stack.print_items()

    while True:  # Inner loop to handle user input for a valid move
        print("\nWhich stack do you want to move a disk from?\n")
        from_stack = get_input()  # Get the source stack

        print("\nWhich stack do you want to move the disk to?\n")
        to_stack = get_input()  # Get the destination stack

        # Check if the source stack is empty
        if from_stack.get_size() == 0:
            print("\nInvalid move. Try again.")  # Cannot move from an empty stack
        # Check if the move is valid (either to an empty stack or to a stack with a larger disk on top)
        elif to_stack.get_size() == 0 or from_stack.peek() < to_stack.peek():
            disk = from_stack.pop()  # Remove the disk from the source stack
            to_stack.push(disk)  # Place the disk on the destination stack
            num_user_moves += 1  # Increment the user's move count
            break  # Exit the inner loop, move is completed
        else:
            print("\nInvalid move. Try again.")  # Cannot place a larger disk on top of a smaller one

# Final message when the game is completed
print(
    f"\n\nYou completed the game in {num_user_moves} moves! "
    f"\nThe optimal number of moves is {num_optimal_moves}."
)
print("Congratulations! You've finished the game!")
