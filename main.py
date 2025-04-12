import json
import datetime
import uuid
import os  # Para variáveis de ambiente (credenciais Azure)

# *** Integração Conceitual com Serviços Azure ***
# Em um ambiente real, você usaria os SDKs do Azure para interagir com esses serviços.

# Exemplo conceitual de como buscar uma variável de ambiente para uma chave de acesso
# chave_acesso_cosmos = os.environ.get("AZURE_COSMOS_DB_KEY")
# if not chave_acesso_cosmos:
#     print("Aviso: Chave de acesso do Azure Cosmos DB não configurada!")

def enviar_mensagem_service_bus(queue_name, message):
    """
    Função conceitual para enviar uma mensagem para o Azure Service Bus.
    Em um cenário real, usaria o SDK `azure-servicebus`.
    """
    print(f"Enviando mensagem para a fila '{queue_name}' no Azure Service Bus: {message}")
    # Aqui você implementaria a lógica real usando o SDK do Azure

def salvar_no_cosmos_db(container_name, data):
    """
    Função conceitual para salvar dados no Azure Cosmos DB.
    Em um cenário real, usaria o SDK `azure-cosmos`.
    """
    print(f"Salvando dados no container '{container_name}' do Azure Cosmos DB: {data}")
    # Aqui você implementaria a lógica real usando o SDK do Azure

def obter_do_cosmos_db(container_name, item_id):
    """
    Função conceitual para obter dados do Azure Cosmos DB.
    Em um cenário real, usaria o SDK `azure-cosmos`.
    """
    print(f"Obtendo item com ID '{item_id}' do container '{container_name}' do Azure Cosmos DB.")
    return None # Retornaria os dados reais do Cosmos DB

# *** Classes de Domínio ***

class Carro:
    """Representa um carro disponível para aluguel."""
    def __init__(self, carro_id, marca, modelo, ano, placa, disponivel=True):
        self.carro_id = carro_id
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.placa = placa
        self.disponivel = disponivel

    def __repr__(self):
        return f"<Carro(id={self.carro_id}, marca='{self.marca}', modelo='{self.modelo}', placa='{self.placa}', disponivel={self.disponivel})>"

    def to_dict(self):
        return {
            "carro_id": self.carro_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "placa": self.placa,
            "disponivel": self.disponivel
        }

class Cliente:
    """Representa um cliente da locadora."""
    def __init__(self, cliente_id, nome, email, telefone):
        self.cliente_id = cliente_id
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def __repr__(self):
        return f"<Cliente(id={self.cliente_id}, nome='{self.nome}', email='{self.email}')>"

    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone
        }

class Reserva:
    """Representa uma reserva de carro."""
    def __init__(self, reserva_id, cliente_id, carro_id, data_inicio, data_fim):
        self.reserva_id = reserva_id
        self.cliente_id = cliente_id
        self.carro_id = carro_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.ativa = True

    def __repr__(self):
        return f"<Reserva(id={self.reserva_id}, cliente_id={self.cliente_id}, carro_id={self.carro_id}, inicio={self.data_inicio}, fim={self.data_fim}, ativa={self.ativa})>"

    def to_dict(self):
        return {
            "reserva_id": self.reserva_id,
            "cliente_id": self.cliente_id,
            "carro_id": self.carro_id,
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat(),
            "ativa": self.ativa
        }

# *** Simulação de Microsserviços com Integração Azure (Conceitual) ***

class ServicoCarros:
    def __init__(self):
        # Em um ambiente real, buscaria dados do Azure Cosmos DB ou Azure SQL
        self.carros = {}
        # self.carros = self._carregar_carros_do_banco()

    def _carregar_carros_do_banco(self):
        # Lógica conceitual para carregar carros do Azure Cosmos DB
        carros_data = obter_do_cosmos_db("carros", "all") # Exemplo de ID
        if carros_data:
            return {carro['carro_id']: Carro(**carro) for carro in carros_data}
        return {}

    def adicionar_carro(self, marca, modelo, ano, placa):
        carro_id = str(uuid.uuid4())
        carro = Carro(carro_id, marca, modelo, ano, placa)
        self.carros[carro_id] = carro
        # Em um ambiente real, salvaria no Azure Cosmos DB
        salvar_no_cosmos_db("carros", carro.to_dict())
        return carro

    def listar_carros_disponiveis(self):
        return [carro for carro in self.carros.values() if carro.disponivel]

    def obter_carro(self, carro_id):
        # Em um ambiente real, buscaria do Azure Cosmos DB pelo ID
        return self.carros.get(carro_id)

    def marcar_carro_como_indisponivel(self, carro_id):
        carro = self.obter_carro(carro_id)
        if carro:
            carro.disponivel = False
            # Em um ambiente real, atualizaria no Azure Cosmos DB
            salvar_no_cosmos_db("carros", carro.to_dict())
            return True
        return False

    def marcar_carro_como_disponivel(self, carro_id):
        carro = self.obter_carro(carro_id)
        if carro:
            carro.disponivel = True
            # Em um ambiente real, atualizaria no Azure Cosmos DB
            salvar_no_cosmos_db("carros", carro.to_dict())
            return True
        return False

class ServicoClientes:
    def __init__(self):
        # Em um ambiente real, buscaria dados do Azure Cosmos DB ou Azure SQL
        self.clientes = {}

    def adicionar_cliente(self, nome, email, telefone):
        cliente_id = str(uuid.uuid4())
        cliente = Cliente(cliente_id, nome, email, telefone)
        self.clientes[cliente_id] = cliente
        # Em um ambiente real, salvaria no Azure Cosmos DB
        salvar_no_cosmos_db("clientes", cliente.to_dict())
        return cliente

    def obter_cliente(self, cliente_id):
        # Em um ambiente real, buscaria do Azure Cosmos DB pelo ID
        return self.clientes.get(cliente_id)

class ServicoReservas:
    def __init__(self, servico_carros):
        # Em um ambiente real, buscaria dados do Azure Cosmos DB
        self.reservas = {}
        self.servico_carros = servico_carros

    def criar_reserva(self, cliente_id, carro_id, data_inicio_str, data_fim_str):
        carro = self.servico_carros.obter_carro(carro_id)
        if not carro or not carro.disponivel:
            return None, "Carro não disponível para reserva."

        try:
            data_inicio = datetime.datetime.fromisoformat(data_inicio_str).date()
            data_fim = datetime.datetime.fromisoformat(data_fim_str).date()
            if data_inicio >= data_fim:
                return None, "Data de início deve ser anterior à data de fim."
        except ValueError:
            return None, "Formato de data inválido (ISO 8601: YYYY-MM-DD)."

        reserva_id = str(uuid.uuid4())
        reserva = Reserva(reserva_id, cliente_id, carro_id, data_inicio, data_fim)
        self.reservas[reserva_id] = reserva
        self.servico_carros.marcar_carro_como_indisponivel(carro_id)
        # Em um ambiente real, salvaria no Azure Cosmos DB
        salvar_no_cosmos_db("reservas", reserva.to_dict())
        # Enviar mensagem para o Azure Service Bus (ex: para processamento de pagamentos)
        enviar_mensagem_service_bus("reservas-criadas", reserva.to_dict())
        return reserva, None

    def cancelar_reserva(self, reserva_id):
        reserva = self.reservas.get(reserva_id)
        if reserva and reserva.ativa:
            reserva.ativa = False
            self.servico_carros.marcar_carro_como_disponivel(reserva.carro_id)
            # Em um ambiente real, atualizaria no Azure Cosmos DB
            salvar_no_cosmos_db("reservas", reserva.to_dict())
            # Enviar mensagem para o Azure Service Bus (ex: para reembolso)
            enviar_mensagem_service_bus("reservas-canceladas", {"reserva_id": reserva_id, "cliente_id": reserva.cliente_id})
            return True, None
        elif not reserva:
            return False, "Reserva não encontrada."
        else:
            return False, "Reserva já está cancelada."

    def listar_reservas_ativas_por_cliente(self, cliente_id):
        # Em um ambiente real, consultaria o Azure Cosmos DB filtrando por cliente_id e status
        return [reserva for reserva in self.reservas.values() if reserva.cliente_id == cliente_id and reserva.ativa]

# *** Simulação de API (Executaria em Azure Functions ou Azure Container Apps) ***

def api_adicionar_carro(servico_carros, data):
    try:
        carro = servico_carros.adicionar_carro(data['marca'], data['modelo'], data['ano'], data['placa'])
        return {"status": "success", "carro": carro.to_dict()}, 201
    except KeyError:
        return {"status": "error", "message": "Dados incompletos para adicionar o carro."}, 400

def api_listar_carros_disponiveis(servico_carros):
    carros_disponiveis = [carro.to_dict() for carro in servico_carros.listar_carros_disponiveis()]
    return {"status": "success", "carros": carros_disponiveis}, 200

def api_adicionar_cliente(servico_clientes, data):
    try:
        cliente = servico_clientes.adicionar_cliente(data['nome'], data['email'], data['telefone'])
        return {"status": "success", "cliente": cliente.to_dict()}, 201
    except KeyError:
        return {"status": "error", "message": "Dados incompletos para adicionar o cliente."}, 400

def api_criar_reserva(servico_reservas, data):
    try:
        reserva, erro = servico_reservas.criar_reserva(
            data['cliente_id'],
            data['carro_id'],
            data['data_inicio'],
            data['data_fim']
        )
        if reserva:
            return {"status": "success", "reserva": reserva.to_dict()}, 201
        else:
            return {"status": "error", "message": erro}, 400
    except KeyError:
        return {"status": "error", "message": "Dados incompletos para criar a reserva."}, 400

def api_cancelar_reserva(servico_reservas, reserva_id):
    sucesso, erro = servico_reservas.cancelar_reserva(reserva_id)
    if sucesso:
        return {"status": "success", "message": f"Reserva {reserva_id} cancelada."}, 200
    else:
        return {"status": "error", "message": erro}, 404

def api_listar_reservas_cliente(servico_reservas, cliente_id):
    reservas = [reserva.to_dict() for reserva in servico_reservas.listar_reservas_ativas_por_cliente(cliente_id)]
    return {"status": "success", "reservas": reservas}, 200

if __name__ == "__main__":
    # Inicialização dos serviços (em um ambiente real, seriam instâncias separadas rodando em contêineres no AKS)
    servico_carros = ServicoCarros()
    servico_clientes = ServicoClientes()
    servico_reservas = ServicoReservas(servico_carros)

    # Simulação de chamadas de API (estas chamadas viriam de clientes web/mobile para a API exposta no Azure)
    print("\n--- Adicionando Carros ---")
    api_adicionar_carro(servico_carros, {"marca": "Volkswagen", "modelo": "Gol", "ano": 2022, "placa": "ABC-1234"})
    api_adicionar_carro(servico_carros, {"marca": "Fiat", "modelo": "Uno", "ano": 2020, "placa": "DEF-5678"})

    print("\n--- Adicionando Cliente ---")
    cliente_response, _ = api_adicionar_cliente(servico_clientes, {"nome": "João Silva", "email": "joao.silva@email.com", "telefone": "11999999999"})
    cliente_joao_id = cliente_response[0]['cliente_id'] if cliente_response else None

    if cliente_joao_id:
        print("\n--- Listando Carros Disponíveis ---")
        print(api_listar_carros_disponiveis(servico_carros)[0]['carros'])

        print("\n--- Criando Reserva ---")
        carro_id_para_reservar = list(servico_carros.carros.keys())[0]
        reserva_data = {
            "cliente_id": cliente_joao_id,
            "carro_id": carro_id_para_reservar,
            "data_inicio": "2025-04-15",
            "data_fim": "2025-04-2