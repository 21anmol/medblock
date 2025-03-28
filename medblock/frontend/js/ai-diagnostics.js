document.addEventListener('DOMContentLoaded', function() {
    // Initialize health risk chart
    initHealthRiskChart();
    
    // Add event listeners for AI models
    initModelButtons();
    
    // Handle time period filters
    initTimePeriodFilters();
});

// Initialize health risk chart
function initHealthRiskChart() {
    const ctx = document.getElementById('healthRiskChart').getContext('2d');
    
    // Get theme colors
    const textColor = getComputedStyle(document.body).getPropertyValue('--text').trim();
    const textSecondaryColor = getComputedStyle(document.body).getPropertyValue('--text-secondary').trim();
    const accentBlue = getComputedStyle(document.body).getPropertyValue('--accent-blue').trim();
    const accentGreen = getComputedStyle(document.body).getPropertyValue('--accent-green').trim();
    
    // Create gradient for areas
    const gradientCardio = ctx.createLinearGradient(0, 0, 0, 300);
    gradientCardio.addColorStop(0, 'rgba(52, 152, 219, 0.4)');
    gradientCardio.addColorStop(1, 'rgba(52, 152, 219, 0.05)');
    
    const gradientMetabolic = ctx.createLinearGradient(0, 0, 0, 300);
    gradientMetabolic.addColorStop(0, 'rgba(46, 204, 113, 0.4)');
    gradientMetabolic.addColorStop(1, 'rgba(46, 204, 113, 0.05)');
    
    const gradientCognitive = ctx.createLinearGradient(0, 0, 0, 300);
    gradientCognitive.addColorStop(0, 'rgba(155, 89, 182, 0.4)');
    gradientCognitive.addColorStop(1, 'rgba(155, 89, 182, 0.05)');
    
    // Chart configuration
    window.healthRiskChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Cardiovascular', 'Respiratory', 'Metabolic', 'Immune', 'Cognitive', 'Mental'],
            datasets: [{
                label: 'Current Risk',
                data: [15, 20, 25, 30, 18, 22],
                backgroundColor: 'rgba(231, 76, 60, 0.2)',
                borderColor: '#e74c3c',
                borderWidth: 2,
                pointBackgroundColor: '#e74c3c',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#e74c3c',
                pointRadius: 4,
                pointHoverRadius: 6
            }, {
                label: 'Average Risk',
                data: [25, 25, 25, 25, 25, 25],
                backgroundColor: 'rgba(52, 152, 219, 0.2)',
                borderColor: '#3498db',
                borderWidth: 2,
                pointBackgroundColor: '#3498db',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#3498db',
                pointRadius: 4,
                pointHoverRadius: 6
            }, {
                label: 'Optimal Health',
                data: [10, 10, 10, 10, 10, 10],
                backgroundColor: 'rgba(46, 204, 113, 0.2)',
                borderColor: '#2ecc71',
                borderWidth: 2,
                pointBackgroundColor: '#2ecc71',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#2ecc71',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    align: 'start',
                    labels: {
                        boxWidth: 15,
                        padding: 15,
                        color: textColor,
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: 'rgba(255, 255, 255, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: 'bold',
                        family: 'Inter, sans-serif'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter, sans-serif'
                    },
                    padding: 12,
                    boxPadding: 6,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.r !== null) {
                                const value = context.parsed.r;
                                const risk = getRiskLevel(value);
                                label += value + ' - ' + risk;
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    pointLabels: {
                        color: textColor,
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        }
                    },
                    ticks: {
                        color: textSecondaryColor,
                        backdropColor: 'transparent',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 10
                        },
                        stepSize: 10
                    },
                    suggestedMin: 0,
                    suggestedMax: 50
                }
            },
            elements: {
                line: {
                    tension: 0.1
                }
            }
        }
    });
}

// Helper function to get risk level text
function getRiskLevel(value) {
    if (value <= 15) {
        return 'Low Risk';
    } else if (value <= 30) {
        return 'Moderate Risk';
    } else {
        return 'High Risk';
    }
}

// Initialize AI model buttons
function initModelButtons() {
    const modelButtons = document.querySelectorAll('.ai-model-card .btn-primary');
    
    modelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.ai-model-card');
            const modelName = card.querySelector('h2').textContent;
            
            // Show loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';
            this.disabled = true;
            
            // Simulate AI model processing
            setTimeout(() => {
                // Reset button state
                this.innerHTML = originalText;
                this.disabled = false;
                
                // Show success message
                showNotification(`${modelName} Analysis Complete`, 'Your health data has been analyzed successfully. View the results below.', 'success');
                
                // Update chart with new data if it's a Health Predictor
                if (modelName === 'Health Predictor') {
                    updateHealthChart();
                } else if (modelName === 'Fraud Detection') {
                    showFraudDetectionResults();
                } else if (modelName === 'Anomaly Detection') {
                    showAnomalyDetectionResults();
                }
                
                // Scroll to results section
                document.querySelector('.analysis-section').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 3000);
        });
    });
}

// Update health chart with new data
function updateHealthChart() {
    // Simulate new data after analysis
    const newData = [12, 18, 22, 25, 15, 20];
    
    // Animate transition to new data
    animateChartUpdate(window.healthRiskChart, 0, newData);
}

// Animate chart data update
function animateChartUpdate(chart, datasetIndex, newData) {
    const currentData = [...chart.data.datasets[datasetIndex].data];
    const steps = 20;
    let currentStep = 0;
    
    const differences = newData.map((value, index) => {
        return (value - currentData[index]) / steps;
    });
    
    const animation = setInterval(() => {
        currentStep++;
        
        const updatedData = currentData.map((value, index) => {
            return value + (differences[index] * currentStep);
        });
        
        chart.data.datasets[datasetIndex].data = updatedData;
        chart.update('none');
        
        if (currentStep >= steps) {
            clearInterval(animation);
            chart.data.datasets[datasetIndex].data = newData;
            chart.update();
            
            // Update insights with new information
            updateInsightsAfterAnalysis();
        }
    }, 30);
}

// Update insights after analysis
function updateInsightsAfterAnalysis() {
    const insightsList = document.querySelector('.insights-list');
    
    // Add a new insight with animation
    const newInsight = document.createElement('div');
    newInsight.className = 'insight-item';
    newInsight.style.opacity = '0';
    newInsight.style.transform = 'translateY(20px)';
    newInsight.style.transition = 'all 0.5s ease';
    
    newInsight.innerHTML = `
        <div class="insight-icon success">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="insight-content">
            <h4>Cardiovascular Improvement</h4>
            <p>Your cardiovascular risk has decreased by 3 points since your last analysis. Keep up the good work!</p>
        </div>
    `;
    
    // Replace the last insight with the new one
    const lastInsight = insightsList.lastElementChild;
    insightsList.replaceChild(newInsight, lastInsight);
    
    // Trigger animation
    setTimeout(() => {
        newInsight.style.opacity = '1';
        newInsight.style.transform = 'translateY(0)';
    }, 100);
}

// Show fraud detection results
function showFraudDetectionResults() {
    showNotification('Fraud Detection Results', 'No fraudulent activities detected in your recent medical records.', 'info');
}

// Show anomaly detection results
function showAnomalyDetectionResults() {
    showNotification('Anomaly Detection Results', 'Minor sleep pattern anomalies detected. See insights for details.', 'warning');
    
    // Update insights for anomaly detection
    const insightsList = document.querySelector('.insights-list');
    const firstInsight = insightsList.firstElementChild;
    
    const newInsight = document.createElement('div');
    newInsight.className = 'insight-item';
    newInsight.style.opacity = '0';
    newInsight.style.transform = 'translateY(20px)';
    newInsight.style.transition = 'all 0.5s ease';
    
    newInsight.innerHTML = `
        <div class="insight-icon warning">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <div class="insight-content">
            <h4>Sleep Pattern Anomaly</h4>
            <p>Irregular sleep patterns detected in the last week. Consider maintaining a more consistent sleep schedule.</p>
        </div>
    `;
    
    // Replace the first insight with the new one
    insightsList.replaceChild(newInsight, firstInsight);
    
    // Trigger animation
    setTimeout(() => {
        newInsight.style.opacity = '1';
        newInsight.style.transform = 'translateY(0)';
    }, 100);
}

// Initialize time period filters
function initTimePeriodFilters() {
    const timePeriods = document.querySelectorAll('.time-period');
    
    timePeriods.forEach(period => {
        period.addEventListener('click', function() {
            // Update active state
            timePeriods.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            
            // Update chart based on selected period
            updateChartForTimePeriod(this.dataset.period);
        });
    });
}

// Update chart based on selected time period
function updateChartForTimePeriod(period) {
    let data;
    
    switch(period) {
        case 'week':
            data = [18, 22, 27, 32, 20, 25];
            break;
        case 'month':
            data = [15, 20, 25, 30, 18, 22];
            break;
        case 'year':
            data = [12, 17, 22, 28, 15, 20];
            break;
        default:
            return;
    }
    
    // Update chart with animation
    animateChartUpdate(window.healthRiskChart, 0, data);
}

// Show notification
function showNotification(title, message, type = 'info') {
    // Check if notifications container exists
    let notificationsContainer = document.querySelector('.notifications-container');
    
    if (!notificationsContainer) {
        notificationsContainer = document.createElement('div');
        notificationsContainer.className = 'notifications-container';
        document.body.appendChild(notificationsContainer);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Set icon based on type
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
    notificationsContainer.appendChild(notification);
    
    // Add styles if they don't exist
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notifications-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 350px;
            }
            
            .notification {
                background-color: var(--surface);
                border-radius: var(--border-radius-md);
                padding: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                animation: slideIn 0.3s ease forwards;
                overflow: hidden;
            }
            
            .notification.success {
                border-left: 4px solid #2ecc71;
            }
            
            .notification.error {
                border-left: 4px solid #e74c3c;
            }
            
            .notification.warning {
                border-left: 4px solid #f1c40f;
            }
            
            .notification.info {
                border-left: 4px solid #3498db;
            }
            
            .notification-content {
                display: flex;
                gap: 15px;
            }
            
            .notification-content i {
                font-size: 20px;
                margin-top: 3px;
            }
            
            .notification-content h4 {
                margin: 0 0 5px 0;
                font-size: 16px;
            }
            
            .notification-content p {
                margin: 0;
                font-size: 14px;
                color: var(--text-secondary);
            }
            
            .notification.success i {
                color: #2ecc71;
            }
            
            .notification.error i {
                color: #e74c3c;
            }
            
            .notification.warning i {
                color: #f1c40f;
            }
            
            .notification.info i {
                color: #3498db;
            }
            
            .close-notification {
                background: none;
                border: none;
                color: var(--text-secondary);
                cursor: pointer;
                font-size: 16px;
                padding: 0;
                margin-left: 10px;
            }
            
            .notification.fadeOut {
                animation: fadeOut 0.3s ease forwards;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes fadeOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Close button functionality
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