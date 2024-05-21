import subprocess
import time


bit = []

start = time.time()

# Компилируем программу на языке C
compile_process = subprocess.Popen(["g++", "C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\file_to_byte.cpp", "-o", "my_program"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
compile_output, compile_error = compile_process.communicate()

if compile_process.returncode != 0:
    print("Ошибка компиляции:\n", compile_error.decode())
else:
    # Запускаем программу на языке C
    run_process = subprocess.Popen(["./my_program"], stdout=subprocess.PIPE)
    program_output, _ = run_process.communicate()
    bit = program_output.decode()
end = time.time() - start


print(end)
print(bit[:31])