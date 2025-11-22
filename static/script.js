function showMessage() {
    const messages = [
        "Harika! Flask ile web geliştirmeye başladınız! 🎉",
        "Mükemmel! Yeni bir yolculuk başlıyor! 🚀",
        "Tebrikler! Web uygulamanız çalışıyor! 💫",
        "Süper! Devam edin! ⭐"
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    
    // Create notification
    const notification = document.createElement('div');
    notification.textContent = randomMessage;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        font-size: 1.1rem;
        z-index: 1000;
        animation: slideIn 0.5s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
