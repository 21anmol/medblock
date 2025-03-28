document.addEventListener('DOMContentLoaded', function() {
    // Initialize verification status for all blocks
    initBlockVerification();
    
    // Initialize access log searching
    initAccessLogSearch();
    
    // Initialize block visualization interactivity
    initBlockVisualization();
    
    // Initialize encryption key functionality
    initEncryptionKeyFeatures();
    
    // Initialize notification system
    initNotifications();
});

// Initialize block verification functionality
function initBlockVerification() {
    const verifyButtons = document.querySelectorAll('.verify-btn');
    const allBlocksButton = document.querySelector('.security-card button');
    
    // Add verification animation to individual block verify buttons
    verifyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const block = this.closest('.block');
            
            // Add verifying class for animation
            block.classList.add('verifying');
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying';
            
            // Simulate verification process
            setTimeout(() => {
                block.classList.remove('verifying');
                block.classList.add('verified');
                button.innerHTML = '<i class="fas fa-check-circle"></i> Verified';
                
                // Show notification
                showNotification('Block Verified', 'Block integrity has been verified successfully.', 'success');
                
                // Reset after some time
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-check-circle"></i> Verify';
                    block.classList.remove('verified');
                }, 3000);
            }, 1500);
        });
    });
    
    // Add verification for all blocks
    if (allBlocksButton) {
        allBlocksButton.addEventListener('click', function() {
            // Add loading state
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying All Blocks';
            this.disabled = true;
            
            // Get all blocks
            const blocks = document.querySelectorAll('.block');
            
            // Simulate sequential verification
            let index = 0;
            const verifyNextBlock = () => {
                if (index < blocks.length) {
                    const block = blocks[index];
                    block.classList.add('verifying');
                    
                    setTimeout(() => {
                        block.classList.remove('verifying');
                        block.classList.add('verified');
                        index++;
                        verifyNextBlock();
                    }, 800);
                } else {
                    // All blocks verified
                    showNotification('All Blocks Verified', 'All blocks in your health record chain have been verified.', 'success');
                    
                    // Reset button state
                    setTimeout(() => {
                        allBlocksButton.innerHTML = '<i class="fas fa-check-circle"></i> Verify All Blocks';
                        allBlocksButton.disabled = false;
                        
                        // Reset block states
                        blocks.forEach(block => {
                            block.classList.remove('verified');
                        });
                    }, 2000);
                }
            };
            
            verifyNextBlock();
        });
    }
}

// Initialize search functionality for access logs
function initAccessLogSearch() {
    const searchInput = document.querySelector('.search-field input');
    const accessLogRows = document.querySelectorAll('.access-log-row');
    
    if (searchInput && accessLogRows.length > 0) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            
            // Filter rows based on search term
            accessLogRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm) || searchTerm === '') {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
            
            // Show message if no results
            const visibleRows = [...accessLogRows].filter(row => row.style.display !== 'none');
            const noResultsMessage = document.querySelector('.no-results-message');
            
            if (visibleRows.length === 0 && searchTerm !== '') {
                if (!noResultsMessage) {
                    const message = document.createElement('div');
                    message.className = 'no-results-message';
                    message.textContent = 'No matching access logs found.';
                    document.querySelector('.access-log-body').appendChild(message);
                }
            } else if (noResultsMessage) {
                noResultsMessage.remove();
            }
        });
    }
}

// Initialize block chain visualization interactivity
function initBlockVisualization() {
    const blocks = document.querySelectorAll('.block');
    
    // Add click event to blocks to show detailed information
    blocks.forEach(block => {
        block.addEventListener('click', function() {
            // Mark this block as selected
            const selectedBlock = document.querySelector('.block.selected');
            if (selectedBlock) {
                selectedBlock.classList.remove('selected');
            }
            this.classList.add('selected');
            
            // Get block data
            const blockType = this.querySelector('.block-type').textContent;
            const blockDate = this.querySelector('.block-date').textContent;
            const blockHash = this.querySelector('.block-hash .value').textContent;
            const prevHash = this.querySelector('.block-prev .value').textContent;
            const blockData = this.querySelector('.block-data .value').textContent;
            
            // Show block details in a modal or panel (if one exists)
            showBlockDetails({
                type: blockType,
                date: blockDate,
                hash: blockHash,
                prevHash: prevHash,
                data: blockData
            });
        });
    });
    
    // Add hover effect to highlight connections
    blocks.forEach(block => {
        block.addEventListener('mouseenter', function() {
            const blockHash = this.getAttribute('data-hash');
            
            // Find next block that references this hash
            const nextBlock = document.querySelector(`.block .block-prev .value:contains('${blockHash}')`);
            if (nextBlock) {
                const nextBlockElement = nextBlock.closest('.block');
                nextBlockElement.classList.add('connected');
                
                // Highlight connector
                const connector = this.nextElementSibling;
                if (connector && connector.classList.contains('block-connector')) {
                    connector.classList.add('active');
                }
            }
        });
        
        block.addEventListener('mouseleave', function() {
            document.querySelectorAll('.block.connected').forEach(b => {
                b.classList.remove('connected');
            });
            document.querySelectorAll('.block-connector.active').forEach(c => {
                c.classList.remove('active');
            });
        });
    });
    
    // Custom contains method for text content
    jQuery.expr[':'].contains = function(a, i, m) {
        return jQuery(a).text().indexOf(m[3]) >= 0;
    };
}

// Show block details in a modal or side panel
function showBlockDetails(blockData) {
    // Check if details panel already exists
    let detailsPanel = document.querySelector('.block-details-panel');
    
    if (!detailsPanel) {
        // Create details panel
        detailsPanel = document.createElement('div');
        detailsPanel.className = 'block-details-panel';
        document.querySelector('.blockchain-section').appendChild(detailsPanel);
    }
    
    // Update panel content
    detailsPanel.innerHTML = `
        <div class="panel-header">
            <h3>${blockData.type}</h3>
            <button class="close-panel"><i class="fas fa-times"></i></button>
        </div>
        <div class="panel-content">
            <div class="detail-item">
                <span class="label">Date:</span>
                <span class="value">${blockData.date}</span>
            </div>
            <div class="detail-item">
                <span class="label">Hash:</span>
                <span class="value hash">${blockData.hash}</span>
                <button class="copy-btn" data-value="${blockData.hash}"><i class="fas fa-copy"></i></button>
            </div>
            <div class="detail-item">
                <span class="label">Previous Hash:</span>
                <span class="value hash">${blockData.prevHash}</span>
                <button class="copy-btn" data-value="${blockData.prevHash}"><i class="fas fa-copy"></i></button>
            </div>
            <div class="detail-item">
                <span class="label">Data:</span>
                <span class="value">${blockData.data}</span>
            </div>
            <div class="detail-actions">
                <button class="btn-secondary view-record-btn">
                    <i class="fas fa-eye"></i> View Record
                </button>
                <button class="btn-outline share-block-btn">
                    <i class="fas fa-share-alt"></i> Share
                </button>
            </div>
        </div>
    `;
    
    // Show panel
    detailsPanel.classList.add('active');
    
    // Add close functionality
    const closeButton = detailsPanel.querySelector('.close-panel');
    closeButton.addEventListener('click', function() {
        detailsPanel.classList.remove('active');
        document.querySelector('.block.selected').classList.remove('selected');
    });
    
    // Add copy functionality
    const copyButtons = detailsPanel.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-value');
            navigator.clipboard.writeText(textToCopy).then(
                function() {
                    // Show success message
                    const originalHtml = button.innerHTML;
                    button.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        button.innerHTML = originalHtml;
                    }, 1500);
                },
                function() {
                    // Show error message
                    alert('Could not copy text to clipboard.');
                }
            );
        });
    });
    
    // Add record view functionality (simulation)
    const viewRecordBtn = detailsPanel.querySelector('.view-record-btn');
    viewRecordBtn.addEventListener('click', function() {
        showNotification('Fetching Record', 'Retrieving encrypted record from blockchain...', 'info');
        
        // Simulate loading
        setTimeout(() => {
            // Show a more detailed record modal
            showRecordModal(blockData);
        }, 1500);
    });
    
    // Add share functionality (simulation)
    const shareBlockBtn = detailsPanel.querySelector('.share-block-btn');
    shareBlockBtn.addEventListener('click', function() {
        showShareOptions(blockData);
    });
}

// Simulate showing a record modal
function showRecordModal(blockData) {
    // Create modal element
    const modal = document.createElement('div');
    modal.className = 'modal record-modal';
    
    // Create content based on block type
    let contentHtml = '';
    
    if (blockData.data === 'Blood Test Results') {
        contentHtml = `
            <h3>Blood Test Results</h3>
            <div class="record-date">Date: ${blockData.date}</div>
            <div class="record-provider">Provider: General Hospital</div>
            <div class="record-table">
                <table>
                    <thead>
                        <tr>
                            <th>Test</th>
                            <th>Result</th>
                            <th>Normal Range</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Hemoglobin</td>
                            <td>14.2 g/dL</td>
                            <td>12.0-15.5 g/dL</td>
                            <td class="normal">Normal</td>
                        </tr>
                        <tr>
                            <td>WBC Count</td>
                            <td>7.2 K/uL</td>
                            <td>4.5-11.0 K/uL</td>
                            <td class="normal">Normal</td>
                        </tr>
                        <tr>
                            <td>Cholesterol</td>
                            <td>210 mg/dL</td>
                            <td><200 mg/dL</td>
                            <td class="attention">Attention</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    } else if (blockData.data === 'X-Ray Images') {
        contentHtml = `
            <h3>X-Ray Images</h3>
            <div class="record-date">Date: ${blockData.date}</div>
            <div class="record-provider">Provider: City Medical Center</div>
            <div class="x-ray-images">
                <div class="image-container">
                    <img src="https://via.placeholder.com/300x400?text=X-Ray+Image" alt="X-Ray">
                    <div class="image-caption">Chest X-Ray</div>
                </div>
                <div class="x-ray-findings">
                    <h4>Findings:</h4>
                    <p>No acute cardiopulmonary process. Heart size is normal. Lungs are clear. No pneumothorax or pleural effusion.</p>
                    <h4>Impression:</h4>
                    <p>Normal chest X-ray.</p>
                </div>
            </div>
        `;
    } else if (blockData.data === 'Prescription Update') {
        contentHtml = `
            <h3>Prescription Update</h3>
            <div class="record-date">Date: ${blockData.date}</div>
            <div class="record-provider">Provider: Dr. Michael Wilson</div>
            <div class="prescription-details">
                <div class="medication">
                    <h4>Medication:</h4>
                    <div class="med-name">Atorvastatin 10mg</div>
                    <div class="med-instructions">Take 1 tablet daily at bedtime</div>
                    <div class="med-duration">30 day supply, 3 refills</div>
                </div>
                <div class="prescription-notes">
                    <h4>Notes:</h4>
                    <p>Prescribed for management of cholesterol. Follow up in 3 months for blood work.</p>
                </div>
            </div>
        `;
    } else {
        contentHtml = `
            <h3>${blockData.type}</h3>
            <div class="record-date">Date: ${blockData.date}</div>
            <div class="record-details">
                <p>Details for this record are encrypted and secured on the blockchain.</p>
                <p>Hash: ${blockData.hash}</p>
            </div>
        `;
    }
    
    // Add modal structure
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Blockchain Record</h2>
                <button class="close-modal"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                ${contentHtml}
            </div>
            <div class="modal-footer">
                <button class="btn-secondary">Download Record</button>
                <button class="btn-outline close-btn">Close</button>
            </div>
        </div>
    `;
    
    // Add to body
    document.body.appendChild(modal);
    
    // Show modal
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
    
    // Add close functionality
    const closeButtons = modal.querySelectorAll('.close-modal, .close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
            }, 300);
        });
    });
}

// Initialize encryption key features
function initEncryptionKeyFeatures() {
    const copyKeyBtn = document.querySelector('.key-display .copy-btn');
    const rotateKeyBtn = document.querySelector('.rotate-key');
    const backupKeyBtn = document.querySelector('.key-actions .btn-outline');
    
    // Copy key to clipboard
    if (copyKeyBtn) {
        copyKeyBtn.addEventListener('click', function() {
            const keyCode = document.querySelector('.key-display code').textContent;
            navigator.clipboard.writeText(keyCode).then(
                function() {
                    // Show success indicator
                    copyKeyBtn.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        copyKeyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    }, 1500);
                    
                    showNotification('Key Copied', 'Encryption key copied to clipboard', 'success');
                },
                function() {
                    showNotification('Copy Failed', 'Could not copy encryption key', 'error');
                }
            );
        });
    }
    
    // Rotate encryption key
    if (rotateKeyBtn) {
        rotateKeyBtn.addEventListener('click', function() {
            // Show confirmation dialog
            if (confirm('Are you sure you want to rotate your encryption key? This will re-encrypt all your data with a new key.')) {
                // Show loading state
                rotateKeyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Rotating...';
                rotateKeyBtn.disabled = true;
                
                // Simulate key rotation
                setTimeout(() => {
                    // Generate new key
                    const newKey = generateRandomKey();
                    document.querySelector('.key-display code').textContent = newKey;
                    
                    // Reset button state
                    rotateKeyBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Rotate Key';
                    rotateKeyBtn.disabled = false;
                    
                    showNotification('Key Rotated', 'Your encryption key has been updated successfully', 'success');
                }, 2500);
            }
        });
    }
    
    // Backup encryption key
    if (backupKeyBtn) {
        backupKeyBtn.addEventListener('click', function() {
            const keyCode = document.querySelector('.key-display code').textContent;
            
            // Create downloadable file
            const blob = new Blob([
                'MEDBLOCK ENCRYPTION KEY BACKUP\n',
                '================================\n',
                'DO NOT SHARE THIS FILE WITH ANYONE\n',
                '================================\n\n',
                `Encryption Key: ${keyCode}\n`,
                `Backup Date: ${new Date().toLocaleString()}\n`,
                '\nStore this file in a secure location. You will need this key to access your encrypted health records.'
            ], { type: 'text/plain' });
            
            // Create download link
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'medblock_key_backup.txt';
            a.style.display = 'none';
            
            // Add to body, click, and remove
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(a.href);
                showNotification('Backup Created', 'Encryption key backup file has been downloaded', 'success');
            }, 100);
        });
    }
}

// Generate a random encryption key (for simulation)
function generateRandomKey() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 32; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Initialize notifications (if not already done globally)
function initNotifications() {
    // Only define if not already defined
    if (typeof window.showNotification !== 'function') {
        window.showNotification = function(title, message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            
            notification.innerHTML = `
                <div class="notification-icon">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
                </div>
                <div class="notification-content">
                    <h4>${title}</h4>
                    <p>${message}</p>
                </div>
                <button class="close-notification">
                    <i class="fas fa-times"></i>
                </button>
            `;
            
            // Add to body
            document.body.appendChild(notification);
            
            // Add close button functionality
            const closeButton = notification.querySelector('.close-notification');
            closeButton.addEventListener('click', function() {
                notification.classList.add('closing');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            });
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if(document.body.contains(notification)) {
                    notification.classList.add('closing');
                    setTimeout(() => {
                        notification.remove();
                    }, 300);
                }
            }, 5000);
            
            return notification;
        };
    }
}

// Simulate sharing options
function showShareOptions(blockData) {
    // Create modal element
    const modal = document.createElement('div');
    modal.className = 'modal share-modal';
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Share Medical Record</h2>
                <button class="close-modal"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                <div class="share-description">
                    <p>Share access to <strong>${blockData.data}</strong> with healthcare providers or third parties.</p>
                    <p class="security-note"><i class="fas fa-shield-alt"></i> Record will remain encrypted and access will be logged on the blockchain.</p>
                </div>
                
                <div class="share-section">
                    <h3>Healthcare Providers</h3>
                    <div class="provider-list">
                        <div class="provider-item">
                            <div class="provider-info">
                                <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Dr. Michael Wilson">
                                <div class="provider-details">
                                    <h4>Dr. Michael Wilson</h4>
                                    <p>Primary Care Physician</p>
                                </div>
                            </div>
                            <label class="toggle">
                                <input type="checkbox" checked>
                                <span class="toggle-slider"></span>
                            </label>
                        </div>
                        <div class="provider-item">
                            <div class="provider-info">
                                <img src="https://randomuser.me/api/portraits/women/68.jpg" alt="Dr. Sarah Chen">
                                <div class="provider-details">
                                    <h4>Dr. Sarah Chen</h4>
                                    <p>Cardiologist</p>
                                </div>
                            </div>
                            <label class="toggle">
                                <input type="checkbox">
                                <span class="toggle-slider"></span>
                            </label>
                        </div>
                        <div class="provider-item">
                            <div class="provider-info">
                                <img src="https://randomuser.me/api/portraits/men/45.jpg" alt="Dr. James Taylor">
                                <div class="provider-details">
                                    <h4>Dr. James Taylor</h4>
                                    <p>Neurologist</p>
                                </div>
                            </div>
                            <label class="toggle">
                                <input type="checkbox">
                                <span class="toggle-slider"></span>
                            </label>
                        </div>
                    </div>
                </div>
                
                <div class="share-section">
                    <h3>Share via Secure Link</h3>
                    <div class="link-generation">
                        <div class="expiration-select">
                            <label>Link Expiration:</label>
                            <select>
                                <option value="24h">24 hours</option>
                                <option value="48h">48 hours</option>
                                <option value="7d">7 days</option>
                                <option value="30d">30 days</option>
                            </select>
                        </div>
                        <button class="btn-secondary generate-link-btn">
                            <i class="fas fa-link"></i> Generate Secure Link
                        </button>
                    </div>
                    <div class="secure-link-display" style="display: none;">
                        <input type="text" readonly value="https://medblock.io/share/bcdfe123456789">
                        <button class="copy-link-btn"><i class="fas fa-copy"></i></button>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-primary">Update Sharing Settings</button>
                <button class="btn-outline close-btn">Cancel</button>
            </div>
        </div>
    `;
    
    // Add to body
    document.body.appendChild(modal);
    
    // Show modal
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
    
    // Add close functionality
    const closeButtons = modal.querySelectorAll('.close-modal, .close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
            }, 300);
        });
    });
    
    // Add generate link functionality
    const generateLinkBtn = modal.querySelector('.generate-link-btn');
    const secureLinkDisplay = modal.querySelector('.secure-link-display');
    
    generateLinkBtn.addEventListener('click', function() {
        generateLinkBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        
        // Simulate link generation
        setTimeout(() => {
            secureLinkDisplay.style.display = 'flex';
            generateLinkBtn.innerHTML = '<i class="fas fa-link"></i> Generate Secure Link';
            showNotification('Link Generated', 'Secure access link has been generated', 'success');
        }, 1500);
    });
    
    // Add copy link functionality
    const copyLinkBtn = modal.querySelector('.copy-link-btn');
    copyLinkBtn.addEventListener('click', function() {
        const linkInput = modal.querySelector('.secure-link-display input');
        linkInput.select();
        document.execCommand('copy');
        
        this.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
            this.innerHTML = '<i class="fas fa-copy"></i>';
        }, 1500);
        
        showNotification('Link Copied', 'Secure access link copied to clipboard', 'success');
    });
}

// Add a jQuery-like selector utility for finding text content
if (!window.jQuery) {
    Element.prototype.contains = function(text) {
        return this.textContent.indexOf(text) > -1;
    };
} 