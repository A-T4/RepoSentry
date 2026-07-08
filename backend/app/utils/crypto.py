import math

def calculate_shannon_entropy(data: str) -> float:
    """
    Calculates the Shannon entropy of a string.
    High entropy (> 4.5) indicates highly randomized data, often indicative of cryptographic secrets, 
    PEM certificates, or hardcoded passwords.
    """
    if not data:
        return 0.0

    entropy = 0.0
    length = len(data)
    
    # Calculate frequency of each character
    frequencies = {}
    for char in data:
        frequencies[char] = frequencies.get(char, 0) + 1
        
    # Apply Shannon entropy formula
    for count in frequencies.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
        
    return entropy