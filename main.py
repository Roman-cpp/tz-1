import time
import sys

import requests

def fetch(url: str) -> tuple[int, float]:
    CHUNK_SIZE = 64 * 1024

    start = time.perf_counter()
    total = 0
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            total += len(chunk)
    elapsed = time.perf_counter() - start
    return total, elapsed


def main() -> int:
    MB = 1024 * 1024 

    url = input("Enter URL: ")
    print(f"URL entered: {url}")

    total_bytes = 0
    total_time = 0.0
    done = 0

    for i in range(10):
        try:
            size, elapsed = fetch(url)
        except requests.RequestException as e:
            print(f"#{i:>2}  ошибка: {e}", file=sys.stderr)
            continue

        speed = size / elapsed / MB if elapsed > 0 else 0.0
        total_bytes += size
        total_time += elapsed
        done += 1
        print(f"#{i + 1:>3}  {size / MB:8.3f} МБ  {elapsed * 1000:9.2f} мс  {speed:8.2f} МБ/с")

    if done == 0:
        print("\nНи один запрос не завершился успешно.", file=sys.stderr)
        return 1
    
    avg_time = total_time / done
    avg_speed = total_bytes / total_time / MB if total_time > 0 else 0.0


    print("\n--- Итого ---")
    print(f"Успешных запросов:     {done} из 10")
    print(f"Среднее время запроса: {avg_time * 1000:.2f} мс")
    print(f"Общий объём:           {total_bytes / MB:.3f} МБ ({total_bytes} байт)")
    print(f"Скорость скачивания:   {avg_speed:.2f} МБ/с")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(130)