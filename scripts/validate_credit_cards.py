import os
import sys
import logging
import argparse

# Configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "credit_card_validation.log")

def setup_logging():
    """Sets up logging for the script, ensuring the log directory exists."""
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
        except OSError as e:
            print(f"Error creating log directory '{LOG_DIR}': {e}")
            sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def is_valid_luhn(card_number: str) -> bool:
    """
    Validates a credit card number using the Luhn algorithm.
    """
    # Remove any spaces or hyphens from the card number
    card_number = card_number.replace(' ', '').replace('-', '')

    if not card_number.isdigit():
        return False

    digits = [int(d) for d in str(card_number)]
    checksum = 0
    reverse_digits = digits[::-1]

    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = digit * 2
            checksum += doubled if doubled < 10 else doubled - 9
        else:
            checksum += digit

    return checksum % 10 == 0

def mask_card_number(card_number: str) -> str:
    """
    Masks a credit card number, leaving only the last 4 digits visible.
    """
    clean_number = card_number.replace(' ', '').replace('-', '')
    if len(clean_number) > 4:
        return "*" * (len(clean_number) - 4) + clean_number[-4:]
    return clean_number

def validate_card(card_number: str):
    """
    Validates a single card and logs the result, masking the card number.
    """
    try:
        clean_number = card_number.strip()
        if not clean_number:
            return

        masked_number = mask_card_number(clean_number)

        if is_valid_luhn(clean_number):
            logging.info(f"VALID: Credit card '{masked_number}' is valid.")
        else:
            logging.warning(f"INVALID: Credit card '{masked_number}' is invalid.")
    except Exception as e:
        logging.error(f"ERROR: Failed to validate '{mask_card_number(card_number)}'. Exception: {e}")

def main():
    parser = argparse.ArgumentParser(description="Validate credit card numbers using the Luhn algorithm.")
    parser.add_argument('numbers', nargs='*', help="Credit card numbers to validate")
    parser.add_argument('-f', '--file', type=str, help="File containing credit card numbers (one per line)")

    args = parser.parse_args()

    if not args.numbers and not args.file:
        parser.print_help()
        sys.exit(1)

    setup_logging()
    logging.info("Starting credit card validation...")

    if args.numbers:
        for number in args.numbers:
            validate_card(number)

    if args.file:
        if not os.path.isfile(args.file):
            logging.error(f"ERROR: File '{args.file}' not found.")
            sys.exit(1)

        try:
            with open(args.file, 'r') as file:
                for line in file:
                    validate_card(line)
        except Exception as e:
            logging.error(f"ERROR: Failed to read file '{args.file}'. Exception: {e}")
            sys.exit(1)

    logging.info("Credit card validation finished.")

if __name__ == "__main__":
    main()
