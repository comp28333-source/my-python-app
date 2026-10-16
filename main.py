import time
import sys
import random

def simulate_loading():
    """Имитация загрузки данных с анимацией прогресса"""
    print("☁️ Подключение к облачному хранилищу...")
    time.sleep(0.8)
    
    total = 30
    print("📥 Загрузка данных:")
    for i in range(total + 1):
        percent = int(i / total * 100)
        bar = '█' * i + '-' * (total - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.04)
    print("\n✅ Данные успешно загружены!\n")

def process_data():
    """Генерация и обработка демонстрационных данных"""
    servers = ["Alpha-01", "Beta-02", "Gamma-03", "Delta-04", "Omega-05"]
    statuses = ["🟢 Активен", "🟡 Нагружен", "🔴 Ошибка"]
    
    report = []
    for server in servers:
        load = random.randint(25, 98)
        status = statuses[2] if load > 90 else (statuses[1] if load > 75 else statuses[0])
        report.append({"server": server, "load": f"{load}%", "status": status})
        
    return report

def main():
    print("=" * 45)
    print("     ДЕМОНСТРАЦИОННЫЙ МОНИТОРИНГ СЕРВЕРОВ     ")
    print("=" * 45 + "\n")
    
    simulate_loading()
    
    print("⚙️ Анализ системных метрик...")
    time.sleep(1)
    
    data = process_data()
    
    # Красивый вывод таблицы
    print("\n" + "┌" + "─" * 16 + "┬" + "─" * 14 + "┬" + "─" * 16 + "┐")
    print(f"│ {'Сервер':<14} │ {'Нагрузка':<10} │ {'Статус':<12} │")
    print("├" + "─" * 16 + "┼" + "─" * 14 + "┼" + "─" * 16 + "┤")
    
    for row in data:
        print(f"│ {row['server']:<14} │ {row['load']:<10} │ {row['status']:<12} │")
        
    print("└" + "─" * 16 + "┴" + "─" * 14 + "┴" + "─" * 16 + "┘")
    print("\n✨ Работа скрипта успешно завершена!")

if __name__ == "__main__":
    main()
    
