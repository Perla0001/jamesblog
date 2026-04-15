// Temporizador Pomodoro
function iniciarPomodoro() {
    const display = document.getElementById('timer-display');
    if (!display) return;

    let minutos = 25, segundos = 0;
    let corriendo = false;
    let intervalo = null;

    document.getElementById('btn-iniciar').addEventListener('click', () => {
        if (corriendo) {
            clearInterval(intervalo);
            corriendo = false;
            document.getElementById('btn-iniciar').textContent = 'Continuar';
        } else {
            corriendo = true;
            document.getElementById('btn-iniciar').textContent = 'Pausar';
            intervalo = setInterval(() => {
                if (segundos === 0) {
                    if (minutos === 0) {
                        clearInterval(intervalo);
                        corriendo = false;
                        display.textContent = '¡Tiempo!';
                        new Audio('/static/audio/ding.mp3').play().catch(() => {});
                        return;
                    }
                    minutos--;
                    segundos = 59;
                } else {
                    segundos--;
                }
                display.textContent =
                    String(minutos).padStart(2,'0') + ':' + String(segundos).padStart(2,'0');
            }, 1000);
        }
    });

    document.getElementById('btn-reiniciar').addEventListener('click', () => {
        clearInterval(intervalo);
        corriendo = false;
        minutos = 25; segundos = 0;
        display.textContent = '25:00';
        document.getElementById('btn-iniciar').textContent = 'Iniciar';
    });
}

document.addEventListener('DOMContentLoaded', iniciarPomodoro);