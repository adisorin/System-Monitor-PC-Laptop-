# System-Monitor-PC-Laptop
System Monitor – Monitorizare în timp real a resurselor sistemului

<img width="1016" height="740" alt="image" src="https://github.com/user-attachments/assets/c17ac41d-1298-48b1-9225-e5a2b1ee090f" />

Prezentare proiect – System Monitor (PC / Laptop) cu windows 10, 11.

1️⃣ Titlu proiect
System Monitor – Monitorizare în timp real a resurselor sistemului
Aplicație desktop dezvoltată în Python pentru monitorizarea performanței unui PC sau Laptop în timp real.

2️⃣ Tehnologii utilizate
🐍 Python
📊 psutil – colectare date hardware
🎨 CustomTkinter – interfață grafică modernă
📈 Matplotlib – grafic utilizare CPU
🧵 Threading – actualizare în fundal
🕒 datetime & math – calcule și desen analog

3️⃣ Scopul aplicației
Aplicația oferă:
✔ Monitorizare CPU
✔ Monitorizare RAM
✔ Monitorizare SSD
✔ Monitorizare trafic rețea (Download / Upload)
✔ Top 5 aplicații consum CPU
✔ Top 5 aplicații consum RAM
✔ Grafic evoluție CPU în timp real
✔ Indicatori analogici tip „ceas”

Este utilă pentru:
Diagnosticarea performanței
Detectarea aplicațiilor care consumă excesiv resurse
Monitorizare live în timpul jocurilor sau aplicațiilor solicitante

4️⃣ Funcționalități principale

🔹 1. Monitorizare Resurse
Prin psutil se colectează:
cpu_percent() – procent CPU
virtual_memory() – utilizare RAM
disk_usage('/') – utilizare SSD
net_io_counters() – trafic rețea

🔹 2. Ceasuri Analogice
Funcția draw_analog():
Desenează un cerc
Adaugă gradaje 0–100
Plasează numere vizibile
Creează un indicator roșu dinamic
Actualizează la fiecare secundă

Sunt afișate 4 ceasuri:
CPU
RAM
SSD
NET

🔹 3. Grafic CPU în timp real
Folosind Matplotlib:
Se memorează ultimele 30 valori CPU
Se actualizează graficul la fiecare secundă
Limită între 0–100%
Permite observarea fluctuațiilor

🔹 4. Top Procese
Funcția get_top_processes():
Iterează prin procesele active

Sortează după:
CPU
RAM
Afișează top 5 aplicații pentru fiecare categorie

Exemplu afișare:
Top CPU Apps:
chrome.exe        25.4%
python.exe        18.2%

🔹 5. Threading (Actualizare continuă)
Funcția update_stats() rulează într-un thread separat:
Thread(target=update_stats, daemon=True).start()

Avantaj:
Interfața nu se blochează
Datele se actualizează la fiecare 1 secundă
UI rămâne fluid

5️⃣ Structura aplicației
Setări UI
Variabile globale
Funcții utilitare
Funcții desen analog
Funcții update UI
Thread de actualizare
Inițializare interfață
Pornire aplicație

6️⃣ Avantaje ale aplicației
✅ Interfață modernă (Dark Mode)
✅ Actualizare în timp real
✅ Monitorizare completă sistem
✅ Design intuitiv
✅ Ușor de extins (GPU, temperaturi etc.)

7️⃣ Posibile îmbunătățiri
Adăugare monitorizare temperatură CPU
Monitorizare GPU
Salvare log în fișier
Alerte la depășire prag (ex: CPU > 90%)
Export date în CSV
Interfață responsive pentru rezoluții diferite

8️⃣ Concluzie
Aplicația System Monitor este un tool complet pentru monitorizarea performanței unui PC/Laptop, combinând:
programare orientată pe obiect
interfață grafică modernă
vizualizare date în timp real
procesare concurentă (threading)
