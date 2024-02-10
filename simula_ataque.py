import hashlib
import json
from time import time

# Lista de nós
nodes = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9']

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.node_data = {node: {'player_H_energy': 100} for node in nodes}
        self.new_block(previous_hash="1")

    def new_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
        }

        # Resetar a lista de transações atuais
        self.current_transactions = []
        self.chain.append(block)
        return block

    def attack_node(self, attacked_node):
        # Simula o ataque a um nó específico e mostra seu conteúdo
        print(f"Simulando ataque ao nó {attacked_node}.")
        print(f"Conteúdo do nó antes do ataque: {json.dumps(self.node_data[attacked_node], indent=2)}")
        # Modifica os dados do nó atacado
        self.node_data[attacked_node] = {'player_H_energy': 10000}
        print(f"Conteúdo do nó após o ataque: {json.dumps(self.node_data[attacked_node], indent=2)}")

    def verify_and_remove_attacked_node(self, attacked_node):
        # Verifica e remove o nó atacado se inconsistências são detectadas
        if self.node_data[attacked_node]['player_H_energy'] != 100:
            print(f"Inconsistência detectada no nó {attacked_node}. Removendo da blockchain.")
            self.chain = [block for block in self.chain if attacked_node not in [tx.get('receiver') for tx in block['transactions']]]
            del self.node_data[attacked_node]
            print(f"Nó {attacked_node} removido da blockchain.")
        else:
            print(f"Nó {attacked_node} não removido da blockchain, pois o ataque foi simulado.")

    def get_user_input(self):
        return input("Escolha o nó alvo (n1-n9): ").lower()

    @property
    def last_block(self):
        return self.chain[-1]

# Inicialização da Blockchain
blockchain = Blockchain()

# Interação com o usuário
while True:
    attacked_node = blockchain.get_user_input()

    # Simulação de ataque ao nó
    blockchain.attack_node(attacked_node)

    # Verificar e remover o nó atacado, se necessário
    blockchain.verify_and_remove_attacked_node(attacked_node)

    # Exibir a cadeia de blocos
    print("\nCadeia de Blocos:")
    print(json.dumps(blockchain.chain, indent=2))

    # Perguntar se o usuário deseja realizar outro ataque
    another_attack = input("\nDeseja fazer outro ataque? (Sim/Não): ").lower()
    if another_attack != 'sim':
        break
