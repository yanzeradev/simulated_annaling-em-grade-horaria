import random
import pandas as pd

# Parâmetros
DIAS_DA_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
HORARIOS = ["08:00-10:00", "10:00-12:00", "13:00-15:00", "15:00-17:00"]
SALAS = ["Sala 1", "Sala 2"]
PROFESSORES = ["Prof. Sergio", "Prof. Ricardo", "Prof. Dayse", "Prof. Nubia", "Prof. Tercio"]
MATERIAS = ["Inteligência Artificial", "Redes I", "Analise de Algoritmo", "Teoria da computação", 
            "Processamento de Imagens", "Compiladores", "Banco de dados", "Organizacao de Computadores"]

GRADE_TURMA = {
    "Inteligência Artificial": 6,
    "Redes I": 6,
    "Analise de Algoritmo": 5,
    "Teoria da computação": 3,
    "Banco de dados I": 6,
    "Processamento de Imagens": 3,
    "Organizacao de Computadores": 5,
    "Compiladores": 6
}

PROFESSORES_MATERIAS = {
    "Prof. Sergio": ["Inteligência Artificial", "Processamento de Imagens", "Compiladores"],
    "Prof. Ricardo": ["Redes I"],
    "Prof. Dayse": ["Analise de Algoritmo", "Banco de dados I"],
    "Prof. Nubia": ["Teoria da computação"],
    "Prof. Tercio": ["Organizacao de Computadores"]
}

# Função de Custo: Penaliza alocações de horários conflitantes (mesmo professor/sala em dois lugares ao mesmo tempo)
def calcular_custo(horarios):
    custo = 0
    for dia in horarios:
        slots_ocupados = {}
        for slot in horarios[dia]:
            sala, horario, professor = horarios[dia][slot]
            if (horario, sala) in slots_ocupados:
                custo += 1
            slots_ocupados[(horario, sala)] = professor
    return custo

# Função para gerar um horário inicial aleatório
def gerar_horario_inicial():
    horario = {}
    for dia in DIAS_DA_SEMANA:
        horario[dia] = {}
        for materia in GRADE_TURMA:
            aulas_necessarias = GRADE_TURMA[materia]
            for _ in range(aulas_necessarias):
                sala = random.choice(SALAS)
                horario_do_dia = random.choice(HORARIOS)
                professor = next(p for p, materias in PROFESSORES_MATERIAS.items() if materia in materias)
                slot = f"{materia} ({professor})"
                horario[dia][slot] = (sala, horario_do_dia, professor)
    return horario

# Simulated Annealing
def simulated_annealing():
    temperatura = 100
    resfriamento = 0.95
    horario_atual = gerar_horario_inicial()
    custo_atual = calcular_custo(horario_atual)
    
    while temperatura > 1:
        novo_horario = gerar_horario_inicial()
        novo_custo = calcular_custo(novo_horario)
        
        if novo_custo < custo_atual or random.uniform(0, 1) < pow(2.71828, -(novo_custo - custo_atual) / temperatura):
            horario_atual = novo_horario
            custo_atual = novo_custo
        
        temperatura *= resfriamento

    return horario_atual

# Função para formatar e exibir a tabela final em formato tabular
def exibir_horario(horario):
    tabela = []
    for dia in DIAS_DA_SEMANA:
        for slot, info in horario[dia].items():
            materia_prof = slot.split(" (")[0]
            sala, hora, professor = info
            tabela.append([dia, materia_prof, professor, sala, hora])
    
    df = pd.DataFrame(tabela, columns=["Dia", "Matéria", "Professor", "Sala", "Horário"])
    print(df)
    return df

# Função para salvar em arquivo Excel
def salvar_horario(horario, nome_arquivo='horario_automatico.xlsx'):
    df = exibir_horario(horario)
    df.to_excel(nome_arquivo, index=False)
    print(f"Horário salvo em {nome_arquivo}")

# Execução do Simulated Annealing e exibição do resultado
horario_final = simulated_annealing()
salvar_horario(horario_final)