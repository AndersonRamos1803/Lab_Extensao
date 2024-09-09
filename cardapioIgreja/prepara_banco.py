import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `cardapio`;")

cursor.execute("CREATE DATABASE `cardapio`;")

cursor.execute("USE `cardapio`;")

# criando tabelas
TABLES = {}
TABLES['Itens'] = ('''
      CREATE TABLE `itens` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `descricao` varchar(100) NOT NULL,
      `preco` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Guerreiros", "admin", generate_password_hash("guerreiros").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from cardapio.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo itens
itens_sql = 'INSERT INTO itens (nome, descricao, preco) VALUES (%s, %s, %s)'
itens = [
      ('Espetinho de Carne', 'Espetinho de acém assado, acompanhado de farofa e vinagrete', 'R$ 12,00'),
      ('Espetinho de Frango', 'Espetinho de peito de frango assado, acompanhado de farofa e vinagrete', 'R$ 12,00'),
      ('Espetinho de Linguiça', 'Espetinho de linguiça bovina assada, acompanhada de farofa e vinagrete', 'R$ 12,00'),
      ('Torta de Frango', 'Fatia de torta de frango com catupiry, fofinha e saborosa', 'R$ 10,00'),
      ('Bolo Confeitado', 'Fatia de bolo confeitado, sabor a ser confirmado diariamente', 'R$ 10,00'),
      ('Cachorro Quente', 'Pão de hotdog com duas salsichas, molho de tomate temperado, milho, purê de batata e batata palha', 'R$ 10,00'),
]
cursor.executemany(itens_sql, itens)

cursor.execute('select * from cardapio.itens')
print(' -------------  Itens:  -------------')
for item in cursor.fetchall():
    print(item[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()