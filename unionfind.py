# unionfind.py

class UnionFind:
    def __init__(self, nodes):
        # Her düğüm başlangıçta kendi kendisinin patronudur (köküdür)
        self.parent = {node: node for node in nodes}
        # Ağaçların derinliğini tutarız ki birleştirirken dengeli olsun
        self.rank = {node: 0 for node in nodes}

    def find(self, item):
        """Bir düğümün 'Büyük Patronunu' (Kökünü) bulur."""
        if self.parent[item] == item:
            return item
        # Path Compression (Yol Sıkıştırma) - Optimizasyon harikası
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        """İki farklı kümeyi birleştirir. Eğer zaten aynı kümedelerse (Döngü varsa) False döner."""
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 != root2:
            # Boyu kısa olan ağacı, uzun olanın altına ekle (Optimizasyon)
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True # Başarıyla birleşti (Döngü yok)
            
        return False # İkisi zaten aynı ağa bağlı! Birleşirse döngü (kısa devre) olur!