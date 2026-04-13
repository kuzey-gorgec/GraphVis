import itertools
from mydict import MyDict
import sorting

class Graph:
    def __init__(self, is_directed=False):
        self.adj = MyDict(capacity=5)
        self.is_directed = is_directed

    def add_edge(self, u, v, weight=1):
        neighbors_u = self.adj.get(u)
        
        if neighbors_u is None:
            self.adj.add(u, [(v, weight)])
        else:
            exists = False
            for i, (existing_v, w) in enumerate(neighbors_u):
                if existing_v == v:
                    neighbors_u[i] = (v, weight) 
                    exists = True
                    break
            if not exists:
                neighbors_u.append((v, weight))

        if not self.is_directed:
            neighbors_v = self.adj.get(v)
            if neighbors_v is None:
                self.adj.add(v, [(u, weight)])
            else:
                exists = False
                for i, (existing_u, w) in enumerate(neighbors_v):
                    if existing_u == u:
                        neighbors_v[i] = (u, weight)
                        exists = True
                        break
                if not exists:
                    neighbors_v.append((u, weight))

    def remove_edge(self, u, v):

        neighbors_u = self.adj.get(u)
        if neighbors_u is not None:
            # U'nun komşuları içinde V'yi bul ve sil
            for i in range(len(neighbors_u)):
                if neighbors_u[i][0] == v:
                    neighbors_u.pop(i)
                    break

        # Eğer yönsüz graf ise, V'nin komşuları arasından da U'yu sil
        if not self.is_directed:
            neighbors_v = self.adj.get(v)
            if neighbors_v is not None:
                for i in range(len(neighbors_v)):
                    if neighbors_v[i][0] == u:
                        neighbors_v.pop(i)
                        break
    def add_node(self, node):
        if self.adj.get(node) is None:
            self.adj.add(node, [])   
    def add_edges(self, edges):
        for edge in edges:
            if len(edge) == 3: 
                u, v, w = edge
                self.add_edge(u, v, w)
            else: 
                u, v = edge
                self.add_edge(u, v)

    def get_all_nodes(self):
        nodes = set()
        for u, neighbors in self.adj.get_elements():
            nodes.add(u)
            for v, w in neighbors:
                nodes.add(v)
        return list(nodes)

    def _get_sorted_neighbors(self, node):
        """Arayüzden bağımsız, doğrudan kendi yazdığımız Selection Sort'u kullanır."""
        neighbors = self.adj.get(node)
        if not neighbors:
            return []
        # Tuple listesini (Hedef, Ağırlık) alfabetik olarak sıralar
        return sorting.selection_sort(neighbors) 

    def _get_edge_weight(self, u, v):
        """İki düğüm arasındaki ağırlığı döndüren yardımcı fonksiyon."""
        neighbors = self.adj.get(u)
        if neighbors:
            for neighbor, weight in neighbors:
                if neighbor == v:
                    return weight
        return float('inf') # Yol yoksa sonsuz dön

    def dfs(self, start_node):
        visited = set()
        result = []
        self._dfs_rec(visited, start_node, result)
        return result

    def _dfs_rec(self, visited, current_node, result):
        visited.add(current_node)
        result.append(current_node)
        
        for neighbor_data in self._get_sorted_neighbors(current_node):
            node = neighbor_data[0] 
            if node not in visited:
                self._dfs_rec(visited, node, result)

    def bfs(self, start_node):
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        result = []

        while queue:
            current_node = queue.pop(0)
            result.append(current_node)
            
            for neighbor_data in self._get_sorted_neighbors(current_node):
                node = neighbor_data[0] 
                if node not in visited:
                    visited.add(node)
                    queue.append(node)
        return result

    def dijkstra(self, start_node, target_node):
        all_nodes = self.get_all_nodes()
        if start_node not in all_nodes or target_node not in all_nodes:
            return [], float('inf')
            
        distances = {node: float('inf') for node in all_nodes}
        distances[start_node] = 0
        predecessors = {node: None for node in all_nodes}
        unvisited = list(all_nodes)
        
        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current)
            
            if distances[current] == float('inf') or current == target_node:
                break
                
            neighbors = self.adj.get(current)
            if neighbors:
                for neighbor, weight in neighbors:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = current
        
        path = []
        curr = target_node
        if predecessors[curr] is None and curr != start_node:
            return [], float('inf')
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        return path[::-1], distances[target_node]

    def a_star(self, start_node, target_node, heuristics=None):
        if heuristics is None:
            heuristics = {}
            
        all_nodes = self.get_all_nodes()
        if start_node not in all_nodes or target_node not in all_nodes:
            return [], float('inf')

        g_score = {node: float('inf') for node in all_nodes}
        g_score[start_node] = 0

        f_score = {node: float('inf') for node in all_nodes}
        f_score[start_node] = heuristics.get(start_node, 0)

        predecessors = {node: None for node in all_nodes}
        unvisited = list(all_nodes)

        while unvisited:
            current = min(unvisited, key=lambda node: f_score[node])
            unvisited.remove(current)

            if current == target_node:
                break

            neighbors = self.adj.get(current)
            if neighbors:
                for neighbor, weight in neighbors:
                    tentative_g_score = g_score[current] + weight
                    if tentative_g_score < g_score[neighbor]:
                        predecessors[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristics.get(neighbor, 0)

        path = []
        curr = target_node
        if predecessors[curr] is None and curr != start_node:
            return [], float('inf')
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        return path[::-1], g_score[target_node]

    def kruskal(self):
        mst = []
        total_cost = 0
        all_nodes = self.get_all_nodes()
        
        from unionfind import UnionFind
        uf = UnionFind(all_nodes)

        edges = []
        for u, neighbors in self.adj.get_elements():
            for v, weight in neighbors:
                if self.is_directed or str(u) < str(v):
                    edges.append((weight, u, v))

        edges.sort(key=lambda x: x[0])

        for weight, u, v in edges:
            if uf.union(u, v):
                mst.append((u, v, weight))
                total_cost += weight

        return mst, total_cost

    def prim(self, start_node):
        mst = []
        total_cost = 0
        visited = set([start_node])
        all_nodes = self.get_all_nodes()

        while len(visited) < len(all_nodes):
            possible_edges = []
            for u in visited:
                neighbors = self.adj.get(u)
                if neighbors:
                    for v, weight in neighbors:
                        if v not in visited:
                            possible_edges.append((weight, u, v))

            if not possible_edges:
                break

            weight, u, v = min(possible_edges, key=lambda x: x[0])
            visited.add(v)
            mst.append((u, v, weight))
            total_cost += weight

        return mst, total_cost

    def tsp_nearest_neighbor(self, start_node):
        """Açgözlü (Greedy) yaklaşım. Hızlıdır ama en iyi sonucu garanti etmez."""
        all_nodes = self.get_all_nodes()
        if start_node not in all_nodes:
            return [], float('inf')

        unvisited = set(all_nodes)
        unvisited.remove(start_node)
        current_node = start_node
        path = [start_node]
        total_cost = 0

        while unvisited:
            neighbors = self.adj.get(current_node)
            if not neighbors:
                return [], float('inf') # Çıkmaz sokak

            # Sadece gidilmemiş komşuları filtrele
            valid_neighbors = [(v, w) for v, w in neighbors if v in unvisited]

            if not valid_neighbors:
                return [], float('inf') # Gidilecek yer kalmadı ama döngü bitmedi

            # En ucuz komşuyu seç
            next_node, weight = min(valid_neighbors, key=lambda x: x[1])

            path.append(next_node)
            total_cost += weight
            unvisited.remove(next_node)
            current_node = next_node

        # Başlangıç noktasına geri dön (Döngüyü kapat)
        return_weight = self._get_edge_weight(current_node, start_node)
        if return_weight == float('inf'):
            return [], float('inf') # Başlangıca yol yoksa TSP başarısız

        path.append(start_node)
        total_cost += return_weight

        return path, total_cost

    def tsp_brute_force(self, start_node):
        """Kaba kuvvet. TÜM ihtimalleri dener. Kusursuzdur ama işlemciyi ağlatır."""
        all_nodes = self.get_all_nodes()
        if start_node not in all_nodes:
            return [], float('inf')

        # Başlangıç hariç gidilecek diğer şehirler
        nodes_to_visit = [n for n in all_nodes if n != start_node]
        best_path = []
        min_cost = float('inf')

        # Gidilecek şehirlerin tüm olası dizilişlerini (permütasyonlarını) üret
        for perm in itertools.permutations(nodes_to_visit):
            # Rotayı oluştur: Başlangıç -> Permütasyon -> Başlangıç
            current_path = [start_node] + list(perm) + [start_node]
            current_cost = 0
            valid = True

            # Bu rotanın maliyetini hesapla
            for i in range(len(current_path) - 1):
                u = current_path[i]
                v = current_path[i+1]
                weight = self._get_edge_weight(u, v)
                
                if weight == float('inf'): # Böyle bir yol yoksa bu rotayı çöpe at
                    valid = False
                    break
                current_cost += weight

            # Eğer rota geçerliyse ve şu ana kadar bulduğumuz en iyisinden ucuzsa kaydet
            if valid and current_cost < min_cost:
                min_cost = current_cost
                best_path = current_path

        return best_path, min_cost
    def ford_fulkerson(self, source, sink):
        """Edmonds-Karp yaklaşımı ile Maksimum Akış hesaplar."""
        all_nodes = self.get_all_nodes()
        if source not in all_nodes or sink not in all_nodes:
            return 0, {}

        # 1. Kalan Kapasite (Residual Capacity) tablosunu oluştur
        rc = {u: {v: 0 for v in all_nodes} for u in all_nodes}
        
        for u, neighbors in self.adj.get_elements():
            for v, cap in neighbors:
                rc[u][v] = cap
                
        parent = {}

        # BFS ile kapasitesi dolmamış bir yol (Augmenting Path) bul
        def bfs():
            visited = set([source])
            queue = [source]
            while queue:
                u = queue.pop(0)
                for v in rc[u]:
                    if v not in visited and rc[u][v] > 0: # Eğer boruda hala yer varsa
                        queue.append(v)
                        visited.add(v)
                        parent[v] = u
                        if v == sink:
                            return True
            return False

        max_flow = 0

        # Barajdan eve gidecek yol bulabildiğin sürece suyu pompala!
        while bfs():
            # Bulunan yoldaki EN DAR boruyu (darboğazı) bul
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, rc[parent[s]][s])
                s = parent[s]

            # Akışı ekle
            max_flow += path_flow
            
            # Borulardaki kalan kapasiteleri güncelle (Ters akış sihri burada dönüyor)
            v = sink
            while v != source:
                u = parent[v]
                rc[u][v] -= path_flow # Düz yönde yer azaldı
                rc[v][u] += path_flow # Ters yönde (iptal hakkı) arttı
                v = parent[v]

        # Görselleştirici için her borudan ne kadar su geçtiğini hesapla
        flows = {}
        for u, neighbors in self.adj.get_elements():
            for v, cap in neighbors:
                flows[(u, v)] = cap - rc[u][v]

        return max_flow, flows
    def remove_node(self, node_to_remove):
        """Bir düğümü ve ona bağlı tüm kenarları grafikten tamamen siler."""
        all_elements = self.adj.get_elements()
        # MyDict yapısını bozmamak için sözlüğü sıfırdan güvenlice oluşturuyoruz
        from mydict import MyDict
        self.adj = MyDict(capacity=5)
        
        for u, neighbors in all_elements:
            if u != node_to_remove:
                # Silinen düğüme giden yolları da filtrele
                new_neighbors = [(v, w) for v, w in neighbors if v != node_to_remove]
                self.adj.add(u, new_neighbors)

    def rename_node(self, old_name, new_name):
        """Bir düğümün ismini günceller ve tüm bağlantılarını yeni isme göre ayarlar."""
        all_elements = self.adj.get_elements()
        from mydict import MyDict
        self.adj = MyDict(capacity=5)
        
        for u, neighbors in all_elements:
            # Düğümün kendi ismi değiştiyse güncelle
            current_u = new_name if u == old_name else u
            new_neighbors = []
            for v, w in neighbors:
                # Komşuların içindeki eski ismi de güncelle
                current_v = new_name if v == old_name else v
                new_neighbors.append((current_v, w))
            self.adj.add(current_u, new_neighbors)