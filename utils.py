def print_file(file_path):
    with open(file_path, "r") as file:
        # Iterate over each line in the file
        for line in file:
            # Print the line
            print(line, end="")