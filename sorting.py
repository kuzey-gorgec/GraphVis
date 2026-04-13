# sorting.py

def bubble_sort(arr):
    """Yan yana olanları karşılaştırıp büyük olanı sağa atar."""
    data = list(arr)
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return data

def selection_sort(arr):
    """Her turda tüm diziyi tarayıp en küçüğü bulur ve başa çeker."""
    data = list(arr)
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data

def insertion_sort(arr):
    """Kart oynarken elimizdeki kağıtları dizdiğimiz gibi çalışır.
    Her elemanı alır, solundaki sıralı kısımda doğru yere sokuşturur."""
    data = list(arr)
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        # Key'den büyük olanları bir sağa kaydır
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        # Boşalan yere key'i yerleştir
        data[j + 1] = key
    return data

def merge_sort(arr):
    """Böl ve Yönet (Divide & Conquer): Diziyi sürekli ortadan ikiye böler,
    tek eleman kalana kadar parçalar, sonra sıralayarak geri birleştirir."""
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # İki sıralı yarıyı birleştirme işlemi
    result = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            result.append(left_half[i])
            i += 1
        else:
            result.append(right_half[j])
            j += 1
            
    # Arta kalanları ekle
    result.extend(left_half[i:])
    result.extend(right_half[j:])
    return result

def quick_sort(arr):
    """Bir Pivot (merkez) seçer, küçükleri sola, büyükleri sağa atar. (Recursive)"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)