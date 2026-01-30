import pytest
from src import stats

def test_calculate_mean():
    """Test mean calculation"""
    assert stats.calculate_mean([1, 2, 3, 4, 5]) == 3.0
    assert stats.calculate_mean([10, 20, 30]) == 20.0
    assert stats.calculate_mean([5]) == 5.0
    assert stats.calculate_mean([-1, 0, 1]) == 0.0
    assert stats.calculate_mean([2.5, 3.5, 4.5]) == 3.5


def test_calculate_median():
    """Test median calculation"""
    assert stats.calculate_median([1, 2, 3, 4, 5]) == 3
    assert stats.calculate_median([1, 2, 3, 4]) == 2.5
    assert stats.calculate_median([5]) == 5
    assert stats.calculate_median([3, 1, 2]) == 2
    assert stats.calculate_median([10, 20, 30, 40, 50]) == 30


def test_calculate_mode():
    """Test mode calculation"""
    assert stats.calculate_mode([1, 2, 2, 3, 4]) == [2]
    assert stats.calculate_mode([1, 1, 2, 2, 3]) == [1, 2]
    assert stats.calculate_mode([5, 5, 5, 1, 2]) == [5]
    assert stats.calculate_mode([1, 2, 3, 4, 5]) == []  # No mode
    assert stats.calculate_mode([7, 7, 7]) == [7]


def test_calculate_variance():
    """Test variance calculation"""
    assert stats.calculate_variance([1, 2, 3, 4, 5]) == 2.0
    assert stats.calculate_variance([10, 10, 10]) == 0.0
    assert round(stats.calculate_variance([2, 4, 6, 8]), 2) == 5.0
    assert stats.calculate_variance([5]) == 0.0


def test_calculate_std_deviation():
    """Test standard deviation calculation"""
    assert round(stats.calculate_std_deviation([1, 2, 3, 4, 5]), 4) == 1.4142
    assert stats.calculate_std_deviation([10, 10, 10]) == 0.0
    assert round(stats.calculate_std_deviation([2, 4, 6, 8]), 4) == 2.2361
    assert stats.calculate_std_deviation([5]) == 0.0


def test_empty_list_errors():
    """Test that empty lists raise ValueError"""
    with pytest.raises(ValueError, match="List cannot be empty"):
        stats.calculate_mean([])
    
    with pytest.raises(ValueError, match="List cannot be empty"):
        stats.calculate_median([])
    
    with pytest.raises(ValueError, match="List cannot be empty"):
        stats.calculate_mode([])


def test_invalid_input_errors():
    """Test that non-numeric values raise ValueError"""
    with pytest.raises(ValueError, match="All elements must be numbers"):
        stats.calculate_mean([1, 2, "three"])
    
    with pytest.raises(ValueError, match="All elements must be numbers"):
        stats.calculate_median([1, None, 3])