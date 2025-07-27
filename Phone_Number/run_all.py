import subprocess
import time

def run_with_output(command, name):
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )


bot = run_with_output(["python", "safe_bot.py"], "BOT")
time.sleep(5)


worker = run_with_output(["python", "safe_worker.py"], "WORKER")

print("✅ Đã khởi động bot và worker.\n--- Log đang chạy bên dưới ---\n")

try:
    while True:
        bot_output = bot.stdout.readline()
        if bot_output:
            print(f"[BOT] {bot_output.strip()}")
        worker_output = worker.stdout.readline()
        if worker_output:
            print(f"[WORKER] {worker_output.strip()}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Đang dừng...")
    bot.terminate()
    worker.terminate()
