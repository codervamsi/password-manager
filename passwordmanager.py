from cryptography.fernet import Fernet
import json
import os

# Generate and save a key for encryption/decryption
def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        if os.path.exists('secret.key'):
            with open('secret.key', 'rb') as key_file:
                return key_file.read()
        else:
            key = generate_key()
            with open('secret.key', 'wb') as key_file:
                key_file.write(key)
            return key
    except Exception as e:
        print(f"Error loading or generating key: {e}")
        exit(1)

def encrypt_message(message, key):
    try:
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(message.encode())
        return encrypted_message
    except Exception as e:
        print(f"Error encrypting message: {e}")
        exit(1)

def decrypt_message(encrypted_message, key):
    try:
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception as e:
        print(f"Error decrypting message: {e}")
        exit(1)

def load_passwords(key):
    try:
        if os.path.exists('passwords.json'):
            with open('passwords.json', 'r') as file:
                encrypted_data = file.read()
            decrypted_data = decrypt_message(encrypted_data.encode(), key)
            return json.loads(decrypted_data)
        else:
            return {}
    except Exception as e:
        print(f"Error loading passwords: {e}")
        return {}

def save_passwords(passwords, key):
    try:
        encrypted_data = encrypt_message(json.dumps(passwords), key)
        with open('passwords.json', 'w') as file:
            file.write(encrypted_data.decode())
    except Exception as e:
        print(f"Error saving passwords: {e}")

def add_password(passwords, key):
    site = input("Enter the site name: ").strip()
    password = input("Enter the password: ").strip()
    if site and password:
        passwords[site] = encrypt_message(password, key).decode()
        save_passwords(passwords, key)
        print("Password added successfully.")
    else:
        print("Site name and password cannot be empty.")

def get_password(passwords, key):
    site = input("Enter the site name: ").strip()
    if site in passwords:
        encrypted_password = passwords[site].encode()
        password = decrypt_message(encrypted_password, key)
        print(f"Password for {site}: {password}")
    else:
        print("No password found for this site.")

def delete_password(passwords, key):
    site = input("Enter the site name to delete: ").strip()
    if site in passwords:
        del passwords[site]
        save_passwords(passwords, key)
        print("Password deleted successfully.")
    else:
        print("No password found for this site.")

def main():
    key = load_key()
    passwords = load_passwords(key)

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Delete Password")
        print("4. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_password(passwords, key)
        elif choice == '2':
            get_password(passwords, key)
        elif choice == '3':
            delete_password(passwords, key)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
