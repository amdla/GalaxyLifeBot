import os


def remove_duplicate_labels(label_dir):
    for filename in os.listdir(label_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(label_dir, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Remove duplicate lines while preserving order
            unique_lines = list(dict.fromkeys(lines))

            with open(filepath, 'w') as file:
                file.writelines(unique_lines)
            print(f"{len(lines) - len(unique_lines)} duplicate labels removed from {filename}")


label_directory = "./labels"
remove_duplicate_labels(label_directory)
