import hashlib

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    try:
        hash_func = hashlib.new(hash_algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except ValueError:
        return f"Invalid hash algorithm: {hash_algorithm}"

if __name__ == '__main__':
    while True:
        choice = input("Choose option:\n1. Calculate file hash\n2. Compare files\n3. Exit\nEnter option: ")
        
        if choice == '1':
            file_path = input("Enter file path: ")
            algorithm = input("Enter hash algorithm (sha256, sha1, md5): ")
                
            hash_algorithm = algorithm.lower()         
            hash_value = calculate_file_hash(file_path, hash_algorithm)
            print(f"({hash_algorithm}) HASH FILE: {hash_value}")

        elif choice == '2':
            file_path1 = input("Enter first file path: ")
            file_path2 = input("Enter second file path: ")
            algorithm = input("Enter hash algorithm (sha256, sha1, md5): ")
                
            hash_algorithm = algorithm.lower()
            first_file_hash_value = calculate_file_hash(file_path1, hash_algorithm)
            secon_file_hash_value = calculate_file_hash(file_path2, hash_algorithm)
            
            if first_file_hash_value == secon_file_hash_value:
                print(f"({hash_algorithm}) HASH MATCHED")
                print(f"{first_file_hash_value}\n")
            else:
                print(f"({hash_algorithm}) HASH NOT MATCHED")
                print(f"First file hash: {first_file_hash_value}")
                print(f"Second file hash: {secon_file_hash_value}\n")

        elif choice == '3':
            break

        else:
            print("Invalid option. Please try again.\n")
