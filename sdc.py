def divide_numbers():
    try:
        # Get input from the user
        numerator = input("Enter the numerator: ")
        denominator = input("Enter the denominator: ")

        # Convert inputs to integers
        numerator = int(numerator)
        denominator = int(denominator)

        # Perform division
        result = numerator / denominator
        print(f"The result of {numerator} divided by {denominator} is {result}.")

    except ValueError:
        print("Error: Please enter valid integers for both the numerator and denominator.")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Call the function
divide_numbers()
