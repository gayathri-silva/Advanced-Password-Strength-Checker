import re
import math

# List of common weak passwords (blacklist)
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "password123",
    "admin", "letmein", "welcome", "monkey", "123456789", "iloveyou",
    "1234567", "sunshine", "princess", "admin123", "password1", "123123",
    "football", "baseball", "superman", "trustno1"
}

def calculate_entropy(password):
    """Calculate password entropy in bits (higher = stronger)"""
    if not password:
        return 0.0
    
    pool_size = 0
    if re.search(r'[a-z]', password):
        pool_size += 26
    if re.search(r'[A-Z]', password):
        pool_size += 26
    if re.search(r'[0-9]', password):
        pool_size += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>/?~`]', password):
        pool_size += 32
    
    if pool_size == 0:
        pool_size = 95  # Default printable ASCII
    
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


def password_strength_checker(password):
    """Analyze password and return strength result"""
    if not password:
        return "Invalid", [" Password cannot be empty."], 0.0

    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>/?~`]', password))

    score = 0
    feedback = []
    entropy = calculate_entropy(password)

    # Check common weak passwords
    if password.lower() in COMMON_PASSWORDS:
        feedback.append(" This password is very common and easily guessable!")
        return "Weak", feedback, entropy

    # Length Check
    if length >= 14:
        score += 3
    elif length >= 10:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append(" Password is too short. Use at least 12 characters.")

    # Character variety checks
    if has_upper:
        score += 1
    else:
        feedback.append(" Add at least one uppercase letter (A-Z)")

    if has_lower:
        score += 1
    else:
        feedback.append(" Add at least one lowercase letter (a-z)")

    if has_digit:
        score += 1
    else:
        feedback.append(" Add at least one number (0-9)")

    if has_special:
        score += 2
    else:
        feedback.append(" Add at least one special character (!@#$%^&*)")

    # Determine strength level
    if score <= 4 or entropy < 40:
        strength = "Weak"
        color = "\033[91m"      # Red
    elif score <= 7 or entropy < 60:
        strength = "Medium"
        color = "\033[93m"      # Yellow
    else:
        strength = "Strong"
        color = "\033[92m"      # Green

    if not feedback:
        feedback.append(" Great! This is a strong and secure password.")

    feedback.append(f" Entropy: {entropy} bits")

    return strength, feedback, entropy, color


def main():
    print("=" * 70)
    print(" ADVANCED PASSWORD STRENGTH CHECKER  ")
    print("=" * 70)
    print("Enter your password below (it will be visible while typing)\n")

    while True:
        password = input("Enter password: ").strip()
        
        if password.lower() in ['exit', 'quit', 'q']:
            print(" Thank you for using Password Checker!")
            break

        strength, feedback_list, entropy, color = password_strength_checker(password)

        print(f"\n Password Strength: {color}{strength}\033[0m")
        print(f" Entropy: {entropy} bits")
        print("-" * 55)
        
        for msg in feedback_list:
            print(msg)
        
        print("=" * 70)

        again = input("\nWould you like to check another password? (y/n): ").strip().lower()
        if again != 'y':
            print("\nProject Completed Successfully! Great Job!")
            break


if __name__ == "__main__":
    main()