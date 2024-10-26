import json

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

# Função para salvar usuários de volta no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Função para criar um novo usuário
def create_user(users, new_username, new_email, new_password, new_idade, new_role):
    if new_username not in users:
        new_id = max([details['id'] for details in users.values()]) + 1 if users else 1
        users[new_username] = {
            "id": new_id,
            "nome": new_username,
            "email": new_email,
            "senha": new_password,
            "idade": new_idade,
            "role": new_role
        }
        return True
    return False

# Função para deletar um usuário
def delete_user(users, username):
    if username in users:
        del users[username]
        return True
    return False

# Função para editar um usuário
def edit_user(users, username, new_name, new_email, new_password, new_age, new_role):
    if username in users:
        users[username]["nome"] = new_name
        users[username]["email"] = new_email
        users[username]["senha"] = new_password
        users[username]["idade"] = new_age
        users[username]["role"] = new_role
        return True
    return False
