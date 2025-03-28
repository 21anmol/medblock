document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();
    
    // Initialize charts
    initHealthChart();
    
    // Initialize modals and dropdowns
    initModals();
    
    // Initialize notifications
    initNotifications();
    
    // Add interactions for other dashboard elements
    initInteractions();
});

// Theme management
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference or use default
    const savedTheme = localStorage.getItem('medblock-theme');
    if (savedTheme === 'light') {
        body.classList.add('light-mode');
        document.querySelector('.toggle-switch').checked = true;
    }
    
    // Handle theme toggle
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('light-mode');
            localStorage.setItem('medblock-theme', 'light');
        } else {
            body.classList.remove('light-mode');
            localStorage.setItem('medblock-theme', 'dark');
        }
        
        // Redraw charts for theme change
        updateChartsForTheme();
    });
}

// Initialize health analytics chart
function initHealthChart() {
    const ctx = document.getElementById('healthChart').getContext('2d');
    
    // Get theme colors
    const textColor = getComputedStyle(document.body).getPropertyValue('--text').trim();
    const textSecondaryColor = getComputedStyle(document.body).getPropertyValue('--text-secondary').trim();
    const accentBlue = getComputedStyle(document.body).getPropertyValue('--accent-blue').trim();
    const accentGreen = getComputedStyle(document.body).getPropertyValue('--accent-green').trim();
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, `${accentBlue}80`); // Semi-transparent blue
    gradient.addColorStop(1, `${accentBlue}00`); // Transparent
    
    // Chart configuration
    window.healthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [
                {
                    label: 'Health Score',
                    data: [75, 78, 76, 79, 85, 87, 84, 88, 90, 89, 91, 94],
                    fill: {
                        target: 'origin',
                        above: gradient
                    },
                    borderColor: accentBlue,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: accentBlue,
                    pointBorderColor: 'rgba(255, 255, 255, 0.8)',
                    pointBorderWidth: 2,
                    tension: 0.3
                },
                {
                    label: 'Activity Level',
                    data: [65, 59, 70, 72, 66, 75, 80, 79, 84, 82, 88, 86],
                    borderColor: accentGreen,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: accentGreen,
                    pointBorderColor: 'rgba(255, 255, 255, 0.8)',
                    pointBorderWidth: 2,
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: textColor,
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        },
                        boxWidth: 12,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: 'rgba(255, 255, 255, 0.8)',
                    borderColor: accentBlue,
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    boxPadding: 6,
                    usePointStyle: true,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: textSecondaryColor,
                        font: {
                            family: 'Inter, sans-serif',
                            size: 11
                        }
                    }
                },
                y: {
                    min: 50,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: textSecondaryColor,
                        font: {
                            family: 'Inter, sans-serif',
                            size: 11
                        },
                        stepSize: 10
                    }
                }
            }
        }
    });
    
    // Time period selector functionality
    const timePeriods = document.querySelectorAll('.time-period');
    timePeriods.forEach(period => {
        period.addEventListener('click', function() {
            timePeriods.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            
            // Update chart data based on selected period
            updateChartData(this.dataset.period);
        });
    });
}

// Update chart data based on selected time period
function updateChartData(period) {
    let labels, healthData, activityData;
    
    switch(period) {
        case 'week':
            labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            healthData = [82, 87, 84, 89, 92, 94, 90];
            activityData = [70, 75, 72, 80, 85, 86, 78];
            break;
        case 'month':
            labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            healthData = [85, 88, 91, 94];
            activityData = [76, 80, 85, 88];
            break;
        case 'year':
            // Already set in initial chart
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            healthData = [75, 78, 76, 79, 85, 87, 84, 88, 90, 89, 91, 94];
            activityData = [65, 59, 70, 72, 66, 75, 80, 79, 84, 82, 88, 86];
            break;
        default:
            return;
    }
    
    // Update chart data
    window.healthChart.data.labels = labels;
    window.healthChart.data.datasets[0].data = healthData;
    window.healthChart.data.datasets[1].data = activityData;
    window.healthChart.update();
}

// Update charts when theme changes
function updateChartsForTheme() {
    const textColor = getComputedStyle(document.body).getPropertyValue('--text').trim();
    const textSecondaryColor = getComputedStyle(document.body).getPropertyValue('--text-secondary').trim();
    
    // Update health chart
    if (window.healthChart) {
        window.healthChart.options.plugins.legend.labels.color = textColor;
        window.healthChart.options.scales.x.ticks.color = textSecondaryColor;
        window.healthChart.options.scales.y.ticks.color = textSecondaryColor;
        window.healthChart.update();
    }
}

// Initialize modals
function initModals() {
    // Upload Record Modal
    const uploadBtn = document.getElementById('upload-btn');
    const uploadModal = document.getElementById('upload-modal');
    const closeModal = document.querySelector('.close-modal');
    const modalCancel = document.getElementById('modal-cancel');
    
    if (uploadBtn && uploadModal) {
        uploadBtn.addEventListener('click', function() {
            uploadModal.classList.add('active');
        });
    }
    
    if (closeModal && uploadModal) {
        closeModal.addEventListener('click', function() {
            uploadModal.classList.remove('active');
        });
    }
    
    if (modalCancel && uploadModal) {
        modalCancel.addEventListener('click', function() {
            uploadModal.classList.remove('active');
        });
    }
    
    // Close modal on outside click
    window.addEventListener('click', function(e) {
        if (e.target === uploadModal) {
            uploadModal.classList.remove('active');
        }
    });
    
    // Upload area functionality
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('fileInput');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                document.querySelector('.upload-info').textContent = `Selected file: ${fileName}`;
                uploadArea.style.borderColor = getComputedStyle(document.body).getPropertyValue('--accent-green').trim();
            }
        });
    }
}

// Initialize notifications
function initNotifications() {
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationDropdown.classList.toggle('active');
        });
        
        // Close dropdown on outside click
        document.addEventListener('click', function(e) {
            if (!notificationDropdown.contains(e.target) && e.target !== notificationBtn) {
                notificationDropdown.classList.remove('active');
            }
        });
        
        // Mark all as read
        const markAllRead = document.querySelector('.mark-all-read');
        if (markAllRead) {
            markAllRead.addEventListener('click', function() {
                const unreadItems = document.querySelectorAll('.notification-item.unread');
                unreadItems.forEach(item => {
                    item.classList.remove('unread');
                });
                
                // Update notification badge count
                const badge = document.querySelector('.notification-badge');
                if (badge) {
                    badge.textContent = '0';
                }
            });
        }
        
        // Handle notification actions
        const actionButtons = document.querySelectorAll('.notification-actions button');
        actionButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const notificationItem = this.closest('.notification-item');
                
                if (this.classList.contains('approve')) {
                    // Handle approve action
                    notificationItem.style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
                    setTimeout(() => {
                        notificationItem.remove();
                        updateNotificationCount();
                    }, 500);
                } else if (this.classList.contains('deny')) {
                    // Handle deny action
                    notificationItem.style.backgroundColor = 'rgba(255, 71, 87, 0.1)';
                    setTimeout(() => {
                        notificationItem.remove();
                        updateNotificationCount();
                    }, 500);
                } else if (this.classList.contains('view')) {
                    // Handle view action
                    notificationItem.classList.remove('unread');
                    updateNotificationCount();
                }
            });
        });
    }
}

// Update notification count
function updateNotificationCount() {
    const unreadItems = document.querySelectorAll('.notification-item.unread');
    const badge = document.querySelector('.notification-badge');
    
    if (badge) {
        badge.textContent = unreadItems.length;
        
        if (unreadItems.length === 0) {
            badge.style.display = 'none';
        } else {
            badge.style.display = 'flex';
        }
    }
}

// General dashboard interactions
function initInteractions() {
    // Ripple effect for buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add micro-interactions and animations
    addMicroInteractions();
    
    // Add loading state to primary buttons in forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('.btn-primary[type="submit"]');
            
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';
                
                // Simulate form submission
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit';
                    
                    // Close modal if form is in modal
                    const modal = this.closest('.modal');
                    if (modal) {
                        modal.classList.remove('active');
                    }
                    
                    // Show success notification
                    showNotification('Success', 'Record has been uploaded successfully!', 'success');
                }, 1500);
            }
        });
    });
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileMenuToggle && sidebar) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Initialize chatbot
    initChatbot();
}

// Add micro-interactions for better UX
function addMicroInteractions() {
    // Card hover effect
    const cards = document.querySelectorAll('.dashboard-card, .stat-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--card-shadow)';
        });
    });
    
    // Navigation hover effect
    const navItems = document.querySelectorAll('.nav-item a');
    
    navItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            if (!this.parentElement.classList.contains('active')) {
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                this.style.color = 'var(--text)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            if (!this.parentElement.classList.contains('active')) {
                this.style.backgroundColor = '';
                this.style.color = '';
            }
        });
    });
}

// Initialize chatbot widget
function initChatbot() {
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbot = document.querySelector('.chatbot-widget');
    const closeChat = document.querySelector('.close-chat');
    const chatForm = document.querySelector('.chat-form');
    const chatMessages = document.querySelector('.chat-messages');
    
    if (chatbotToggle && chatbot) {
        chatbotToggle.addEventListener('click', function() {
            chatbot.classList.toggle('active');
        });
    }
    
    if (closeChat && chatbot) {
        closeChat.addEventListener('click', function() {
            chatbot.classList.remove('active');
        });
    }
    
    if (chatForm && chatMessages) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const input = this.querySelector('input');
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                addChatMessage(message, 'user');
                input.value = '';
                
                // Simulate AI response after a short delay
                setTimeout(() => {
                    // Show typing indicator
                    const typingIndicator = document.createElement('div');
                    typingIndicator.className = 'message ai typing';
                    typingIndicator.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
                    chatMessages.appendChild(typingIndicator);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    // After a delay, replace with actual response
                    setTimeout(() => {
                        typingIndicator.remove();
                        getAIResponse(message);
                    }, 1500);
                }, 500);
            }
        });
    }
}

// Add message to chat
function addChatMessage(message, sender) {
    const chatMessages = document.querySelector('.chat-messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}`;
    messageEl.innerHTML = `<p>${message}</p>`;
    
    chatMessages.appendChild(messageEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Get AI response based on user message
function getAIResponse(userMessage) {
    // Simple responses for demo purposes
    const responses = {
        'hi': 'Hello! How can I assist you with MedBlock today?',
        'hello': 'Hi there! What can I help you with regarding your health records?',
        'how are you': 'I\'m functioning optimally! How can I help you?',
        'what is medblock': 'MedBlock is a decentralized healthcare records system that uses blockchain technology to securely store and manage your medical data while leveraging AI for health insights.',
        'how does it work': 'MedBlock stores your medical records on a secure blockchain and uses machine learning to provide health insights. Your data remains private and you control who accesses it.',
        'who can see my data': 'Only you and the healthcare providers you explicitly grant permission to can access your medical records. All access is tracked on the blockchain for transparency.',
        'is it secure': 'Yes, MedBlock uses advanced encryption and blockchain technology to ensure your medical data remains secure and tamper-proof.',
        'help': 'I can help with managing your health records, understanding your health analytics, or navigating the MedBlock platform. What do you need assistance with?'
    };
    
    let response = '';
    const lowerMessage = userMessage.toLowerCase();
    
    // Check for known phrases
    for (const key in responses) {
        if (lowerMessage.includes(key)) {
            response = responses[key];
            break;
        }
    }
    
    // Default response if no matches
    if (!response) {
        if (lowerMessage.includes('appointment') || lowerMessage.includes('schedule')) {
            response = 'To schedule an appointment, you can use the "Upcoming Appointments" section on your dashboard or contact your healthcare provider directly through the platform.';
        } else if (lowerMessage.includes('upload') || lowerMessage.includes('record') || lowerMessage.includes('file')) {
            response = 'You can upload medical records by clicking the "Upload Record" button on your dashboard. We support various file formats including PDF, JPEG, and DICOM.';
        } else if (lowerMessage.includes('analytics') || lowerMessage.includes('health') || lowerMessage.includes('prediction')) {
            response = 'Your health analytics are calculated based on the medical records you\'ve uploaded and any connected health devices. The AI analyzes this data to provide insights and recommendations.';
        } else {
            response = 'I\'m still learning about that. For specific assistance, you might want to check our Help Center or contact support through your dashboard.';
        }
    }
    
    addChatMessage(response, 'ai');
}

// Show notification
function showNotification(title, message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'exclamation-circle';
    if (type === 'warning') icon = 'exclamation-triangle';
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${icon}"></i>
            <div>
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
        </div>
        <button class="close-notification"><i class="fas fa-times"></i></button>
    `;
    
    // Add to DOM
    const notificationsContainer = document.querySelector('.notifications-container');
    if (!notificationsContainer) {
        const container = document.createElement('div');
        container.className = 'notifications-container';
        document.body.appendChild(container);
        container.appendChild(notification);
    } else {
        notificationsContainer.appendChild(notification);
    }
    
    // Close button
    const closeBtn = notification.querySelector('.close-notification');
    closeBtn.addEventListener('click', function() {
        notification.classList.add('fadeOut');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto close after 5 seconds
    setTimeout(() => {
        notification.classList.add('fadeOut');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
} 