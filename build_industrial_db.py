import sqlite3
import csv
import os
import random
from datetime import datetime, timedelta

# Configurações de diretórios e caminhos do projeto
DB_PATH = "industrial_plant.db"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Conexão com o banco de dados SQLite
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# 1. Tabela Dimensão: Equipamentos
cursor.execute("""
CREATE TABLE equipment (
    equipment_id TEXT PRIMARY KEY,
    equipment_name TEXT,
    sector TEXT,
    installation_date TEXT,
    criticality TEXT
)
""")

# 2. Tabela Fato: Logs de Produção
cursor.execute("""
CREATE TABLE production_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT,
    date TEXT,
    actual_operating_time_min INTEGER,
    planned_operating_time_min INTEGER,
    downtime_failure_min INTEGER,
    downtime_maintenance_min INTEGER,
    units_produced INTEGER,
    defective_units INTEGER,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
)
""")

# 3. Tabela Fato: Ordens de Manutenção
cursor.execute("""
CREATE TABLE maintenance_orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT,
    maintenance_date TEXT,
    maintenance_type TEXT,
    labor_cost REAL,
    parts_cost REAL,
    downtime_caused_min INTEGER,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
)
""")

# Inserção de Equipamentos com diferentes setores e criticidades
equipments = [
    ('EQ-01', 'Prensa Hidráulica A1', 'Estampagem', '2018-01-15', 'Alta'),
    ('EQ-02', 'Robô de Solda B2', 'Montagem', '2018-06-20', 'Crítica'),
    ('EQ-03', 'Centro de Usinagem C3', 'Usinagem', '2019-01-10', 'Alta'),
    ('EQ-04', 'Linha de Pintura D4', 'Acabamento', '2018-11-05', 'Média')
]
cursor.executemany("INSERT INTO equipment VALUES (?, ?, ?, ?, ?)", equipments)

# Semente aleatória para reprodutibilidad consistente
random.seed(42)

start_date = datetime(2019, 1, 1)
end_date = datetime(2021, 12, 31)
current_date = start_date

print("[ETL] Gerando histórico industrial com variação estocástica (2019-2021)...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    is_weekend = current_date.weekday() >= 5
    
    for eq_id, _, sector, _, criticality in equipments:
        # Variação de acordo com o fim de semana e o tipo de máquina
        if is_weekend:
            planned = 240
            actual = random.randint(180, 230)
            failure = random.randint(5, 25)
            maint = 15
            units = random.randint(350, 600)
            defects = random.randint(2, 8)
        else:
            planned = 480
            actual = random.randint(380, 475)
            failure = random.randint(10, 45)
            maint = random.randint(15, 30)
            units = random.randint(1000, 1700)
            defects = random.randint(5, 25)
            
        # Inserção do log diário
        cursor.execute("""
            INSERT INTO production_logs (equipment_id, date, actual_operating_time_min, planned_operating_time_min, downtime_failure_min, downtime_maintenance_min, units_produced, defective_units)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (eq_id, date_str, actual, planned, failure, maint, units, defects))
        
        # Geração dinâmica de ordens de manutenção com custos variados por setor/criticidade
        if current_date.day in [3, 12, 22]:
            m_type = 'Preventiva' if current_date.day != 22 else 'Corretiva'
            
            # Multiplicador de custo baseado na criticidade
            crit_multiplier = 1.5 if criticality == 'Crítica' else (1.2 if criticality == 'Alta' else 1.0)
            
            if m_type == 'Preventiva':
                l_cost = round(random.uniform(120.0, 250.0) * crit_multiplier, 2)
                p_cost = round(random.uniform(200.0, 500.0) * crit_multiplier, 2)
                d_cause = random.randint(30, 60)
            else:
                l_cost = round(random.uniform(400.0, 900.0) * crit_multiplier, 2)
                p_cost = round(random.uniform(900.0, 2500.0) * crit_multiplier, 2)
                d_cause = random.randint(90, 240)
            
            cursor.execute("""
                INSERT INTO maintenance_orders (equipment_id, maintenance_date, maintenance_type, labor_cost, parts_cost, downtime_caused_min)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (eq_id, date_str, m_type, l_cost, p_cost, d_cause))

    current_date += timedelta(days=1)

connection.commit()

def export_table_to_csv(table_name, filename):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column_names)
        for row in rows:
            formatted_row = [
                str(val).replace(',', '.') if isinstance(val, float) else val 
                for val in row
            ]
            writer.writerow(formatted_row)

export_table_to_csv("equipment", "equipment.csv")
export_table_to_csv("production_logs", "production_logs.csv")
export_table_to_csv("maintenance_orders", "maintenance_orders.csv")

connection.close()
print("[ETL] Concluído! Custos e dados operacionais agora possuem variabilidade real por setor.")