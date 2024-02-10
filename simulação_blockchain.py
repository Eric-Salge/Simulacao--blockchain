import hashlib
import json
from time import time

# Lista de players
players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.player_energy = {player: 100 for player in players}
        self.player_h2 = {player: 0 for player in players}
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

    def new_transaction(self, player, contract_type, amount, password):
        if contract_type == 'sell':
            # Se for uma transação de venda, a quantidade de H2 é extraída da quantidade total
            h2_amount = amount
            energy_amount = None  # Não é uma transação de compra de energia
        else:
            # Se for uma transação de compra, a quantidade de energia é somada à quantidade total
            energy_amount = amount
            h2_amount = None  # Não é uma transação de venda de H2 verde

        transaction = {
            'player': player,
            'contract_type': contract_type,
            'amount_h2': h2_amount,
            'amount_energy': energy_amount,
            'password': password,
        }
        self.current_transactions.append(transaction)
        return transaction

    def calculate_h2_from_energy(self, energy_amount):
        # Assumindo que 50 MWh de energia geram 1 tonelada de H2 verde
        h2_amount = energy_amount / 50
        return h2_amount

    def calculate_energy_from_h2(self, h2_amount):
        # Assumindo que 1 tonelada de H2 verde gera 50 MWh de energia
        energy_amount = h2_amount * 50
        return energy_amount

    def validate_contract(self, transaction):
        if transaction['contract_type'] == 'sell':
            player = transaction['player']
            amount_h2 = transaction['amount_h2']
            
            # Calcula a energia disponível considerando as compras anteriores e subtraindo a produção de H2
            available_energy = self.player_energy[player] - self.calculate_energy_from_h2(self.player_h2[player])
            
            # Verifica se a quantidade de energia é suficiente
            if available_energy < 50 * amount_h2:
                print(f"Transação não autorizada! Quantidade de H2 verde insuficiente para venda por {player}."
                      f"\nQuantidade disponível de energia: {available_energy} MWh. Quantidade solicitada de H2: {amount_h2} toneladas.")
                return False
        elif transaction['contract_type'] == 'buy':
            # Somar a quantidade comprada à energia existente
            player = transaction['player']
            energy_amount = transaction['amount_energy']
            self.player_energy[player] += energy_amount

        return True

    def get_user_input(self):
        player = input("Escolha o jogador (A-T): ").upper()
        contract_type = input("Escolha o tipo de contrato (buy/sell): ").lower()
        amount = float(input("Digite a quantidade (em toneladas ou MWh): "))
        password = input("Digite a senha: ")
        return player, contract_type, amount, password

    def sign_transaction(self, transaction):
        expected_password = transaction['player'] + '1234'
        if transaction['password'] == expected_password:
            print(f"Transação assinada por {transaction['player']}.")
            return True
        else:
            print(f"Senha incorreta para {transaction['player']}. Transação recusada.")
            return False

    @property
    def last_block(self):
        return self.chain[-1]

# Inicialização da Blockchain
blockchain = Blockchain()

# Interação com o usuário
while True:
    player, contract_type, amount, password = blockchain.get_user_input()

    # Simulação de contratos
    transaction = blockchain.new_transaction(player, contract_type, amount, password)

    # Validar e adicionar blocos à blockchain
    if blockchain.validate_contract(transaction) and blockchain.sign_transaction(transaction):
        if transaction['contract_type'] == 'sell':
            blockchain.player_h2[transaction['player']] += transaction['amount_h2']
            # Ajustar a quantidade disponível de energia após a transação de venda
            blockchain.player_energy[transaction['player']] -= 50 * transaction['amount_h2']
        # Se desejar deduzir a quantidade comprada de energia, adicione a lógica correspondente aqui

        blockchain.new_block(previous_hash=hashlib.sha256(json.dumps(blockchain.last_block, sort_keys=True).encode()).hexdigest())
        print("Contrato adicionado à blockchain.")
    else:
        print("Contrato inválido. Não adicionado à blockchain.")

    # Exibir a cadeia de blocos
    print("\nCadeia de Blocos:")
    print(json.dumps(blockchain.chain, indent=2))

    # Perguntar se o usuário deseja realizar outra transação
    another_transaction = input("\nDeseja fazer outra transação? (Sim/Não): ").lower()
    if another_transaction != 'sim':
        break
