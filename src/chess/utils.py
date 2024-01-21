"""
Holds misc. functions
"""

def valid_move_input(prompt):
    while True:
        response = input(prompt)
        
        if len(response) == 5:
            if response[0] in "abcdefgh" and response[3] in "abcdefgh":
                if response[1] in "12345678" and response[4] in "12345678":
                    if response[2] == " ":
                        return response

        print(f"Invalid input ('{response}')", end="\n\n")