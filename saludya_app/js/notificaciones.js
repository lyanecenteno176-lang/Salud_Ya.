// 1. Pedir permiso al usuario al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    if ("Notification" in window && Notification.permission !== "granted") {
        Notification.requestPermission();
    }
});

// 2. Función para lanzar notificaciones
function enviarNotificacion(titulo, mensaje, icono) {
    // Si el usuario dio permiso a las notificaciones del navegador
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification(titulo, {
            body: mensaje,
            icon: icono || 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png' // Ícono por defecto
        });
    } else {
        // Alternativa visual en la página si no hay permisos de sistema
        mostrarNotificacionToast(titulo, mensaje);
    }
}

// 3. Banner/Toast dinámico dentro de la misma web
function mostrarNotificacionToast(titulo, mensaje) {
    const container = document.createElement('div');
    container.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #2e7d32;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        font-family: sans-serif;
        animation: slideIn 0.5s ease-out;
    `;
    container.innerHTML = `<strong>${titulo}</strong><br><small>${mensaje}</small>`;
    document.body.appendChild(container);

    setTimeout(() => {
        container.remove();
    }, 5000); // Se elimina a los 5 segundos
}

// 4. Bucle en tiempo real (Simulador de Recordatorios)
// Revisa cada cierto tiempo si toca lanzar una alerta
function iniciarRecordatoriosEnTiempoReal() {
    
    // Recordatorio de Agua cada ciertos minutos (Simulado a 45 segundos para pruebas)
    setInterval(() => {
        enviarNotificacion(
            "💧 ¡Hora de Hidratarte!", 
            "Recuerda beber un vaso de agua para mantener tu cuerpo al 100%."
        );
    }, 45000); // 45,000 ms = 45 segundos (ajustar a 3600000 para 1 hora real)

    // Recordatorio de Pausa Activa / Ejercicios
    setInterval(() => {
        enviarNotificacion(
            "🧘 Pausa Activa", 
            "Llevas un buen rato sentado. ¡Ponte de pie y realiza unos estiramientos breves!"
        );
    }, 90000); // Cada 90 segundos para pruebas

    // Recordatorio de Medicamentos
    setInterval(() => {
        enviarNotificacion(
            "💊 Recordatorio de Medicación", 
            "Es hora de tomar tu dosis programada (Paracetamol 500mg)."
        );
    }, 120000); // Cada 2 minutos para pruebas
}

// Iniciar el temporizador
iniciarRecordatoriosEnTiempoReal();
