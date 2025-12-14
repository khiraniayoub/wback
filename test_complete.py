import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/users"

# Usar timestamp para emails únicos
timestamp = int(time.time())
test_email = f"test{timestamp}@example.com"

def print_test(num, title, status, response_json):
    status_icon = "✅" if status < 400 else "❌"
    print(f"\n{status_icon} TEST {num}: {title}")
    print(f"   Status: {status}")
    print(f"   Response: {json.dumps(response_json, indent=4, ensure_ascii=False)}")

print("\n" + "="*70)
print("🚀 PRUEBAS COMPLETAS DE LA API - USERS APP")
print("="*70)

# TEST 1: Registro de usuario
print("\n📝 FASE 1: AUTENTICACIÓN")
register_data = {
    "email": test_email,
    "password": "TestPassword123!"
}
response = requests.post(f"{BASE_URL}/register/", json=register_data)
print_test(1, "Registro de nuevo usuario", response.status_code, response.json())

# TEST 2: Login
login_data = {
    "email": test_email,
    "password": "TestPassword123!"
}
response = requests.post(f"{BASE_URL}/login/", json=login_data)
print_test(2, "Login de usuario", response.status_code, response.json())

if response.status_code == 200:
    token = response.json().get("token")
    headers = {"Authorization": f"Token {token}"}
    
    print("\n👤 FASE 2: GESTIÓN DE PERFIL")
    
    # TEST 3: Ver perfil
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print_test(3, "Ver perfil del usuario", response.status_code, response.json())
    
    # TEST 4: Actualizar perfil
    update_data = {
        "first_name": "Juan",
        "last_name": "Pérez",
        "phone": "+34123456789"
    }
    response = requests.patch(f"{BASE_URL}/profile/", json=update_data, headers=headers)
    print_test(4, "Actualizar perfil", response.status_code, response.json())
    
    # TEST 5: Ver perfil actualizado
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print_test(5, "Ver perfil actualizado", response.status_code, response.json())
    
    print("\n📋 FASE 3: GESTIÓN DE USUARIOS")
    
    # TEST 6: Listar todos los usuarios
    response = requests.get(f"{BASE_URL}/", headers=headers)
    print_test(6, "Listar todos los usuarios", response.status_code, response.json())
    
    # TEST 7: Ver detalle de un usuario específico
    if response.status_code == 200 and len(response.json()) > 0:
        user_id = response.json()[0]['id']
        response = requests.get(f"{BASE_URL}/{user_id}/", headers=headers)
        print_test(7, f"Ver detalle del usuario ID {user_id}", response.status_code, response.json())
    
    print("\n🔑 FASE 4: CAMBIO DE CONTRASEÑA")
    
    # TEST 8: Cambiar contraseña
    change_password_data = {
        "old_password": "TestPassword123!",
        "new_password": "NewPassword123!",
        "new_password_confirm": "NewPassword123!"
    }
    response = requests.post(f"{BASE_URL}/change-password/", json=change_password_data, headers=headers)
    print_test(8, "Cambiar contraseña", response.status_code, response.json())
    
    if response.status_code == 200:
        new_token = response.json().get("token")
        headers = {"Authorization": f"Token {new_token}"}
        
        # TEST 9: Login con nueva contraseña
        login_data["password"] = "NewPassword123!"
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        print_test(9, "Login con nueva contraseña", response.status_code, response.json())

print("\n❌ FASE 5: PRUEBAS DE VALIDACIÓN Y ERRORES")

# TEST 10: Acceso sin autenticación
response = requests.get(f"{BASE_URL}/profile/")
print_test(10, "Acceso a perfil sin autenticación", response.status_code, response.json())

# TEST 11: Registro con email duplicado
duplicate_data = {
    "email": test_email,
    "password": "AnotherPassword123!"
}
response = requests.post(f"{BASE_URL}/register/", json=duplicate_data)
print_test(11, "Registro con email duplicado", response.status_code, response.json())

# TEST 12: Login con credenciales incorrectas
bad_login = {
    "email": test_email,
    "password": "WrongPassword!"
}
response = requests.post(f"{BASE_URL}/login/", json=bad_login)
print_test(12, "Login con contraseña incorrecta", response.status_code, response.json())

# TEST 13: Login con email inexistente
bad_login = {
    "email": "noexiste@example.com",
    "password": "Password123!"
}
response = requests.post(f"{BASE_URL}/login/", json=bad_login)
print_test(13, "Login con email inexistente", response.status_code, response.json())

print("\n" + "="*70)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print("="*70 + "\n")
