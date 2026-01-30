def calculate_mean(numbers):
    """
    Calculate the mean (average) of a list of numbers.
    
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numbers.")
    
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median of a list of numbers.
    
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numbers.")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 0:
     
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
       
        return sorted_numbers[n//2]


def calculate_mode(numbers):
    """
    Calculate the mode (most frequent value) of a list of numbers.

    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numbers.")
    
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_frequency = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_frequency]
    
   
    if max_frequency == 1:
        return []
    
    return sorted(modes)


def calculate_variance(numbers):
    """
    Calculate the variance of a list of numbers.
    
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numbers.")
    
    mean = calculate_mean(numbers)
    squared_differences = [(x - mean) ** 2 for x in numbers]
    variance = sum(squared_differences) / len(numbers)
    
    return variance


def calculate_std_deviation(numbers):
    """
    Calculate the standard deviation of a list of numbers.
    
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numbers.")
    
    variance = calculate_variance(numbers)
    return variance ** 0.5