function confirmDelete(url) {
    if (confirm("Вы уверены, что хотите удалить этот файл?")) {
        window.location.href = url;
    }
}

function openModal(url, type, filename) {
    const modal = document.getElementById('mediaModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    
    modalTitle.textContent = filename;
    
    if (type === 'image') {
        modalBody.innerHTML = `<img src="${url}" alt="${filename}">`;
    } else if (type === 'video') {
        modalBody.innerHTML = `
            <video controls autoplay style="max-width: 100%; max-height: 70vh;">
                <source src="${url}">
            </video>
        `;
    }
    
    modal.classList.add('active');
}

function closeModal() {
    const modal = document.getElementById('mediaModal');
    const modalBody = document.getElementById('modalBody');
    
    modal.classList.remove('active');
    modalBody.innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('mediaModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
    
    const fileInput = document.getElementById('fileInput');
    const fileInputLabel = document.querySelector('.file-input-label');
    const fileList = document.getElementById('fileList');
    
    if (fileInput && fileInputLabel) {
        fileInput.addEventListener('change', function(e) {
            const files = e.target.files;
            
            if (files.length > 0) {
                fileInputLabel.innerHTML = `
                    <i class="fas fa-check-circle" style="color: var(--success);"></i>
                    <span>Выбрано файлов: ${files.length}</span>
                    <small>Нажмите "Загрузить" для отправки</small>
                `;
                
                let fileListHTML = '';
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const size = formatFileSize(file.size);
                    const icon = getFileIcon(file.name);
                    
                    fileListHTML += `
                        <div class="file-item">
                            <i class="${icon}"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500;">${file.name}</div>
                                <div style="font-size: 12px; color: var(--text-gray);">${size}</div>
                            </div>
                        </div>
                    `;
                }
                
                fileList.innerHTML = fileListHTML;
                fileList.classList.add('active');
            }
        });
        
        fileInputLabel.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileInputLabel.style.background = '#e8f0fe';
            fileInputLabel.style.borderColor = 'var(--primary)';
        });
        
        fileInputLabel.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileInputLabel.style.background = 'var(--bg-light)';
            fileInputLabel.style.borderColor = 'var(--border)';
        });
        
        fileInputLabel.addEventListener('drop', function(e) {
            e.preventDefault();
            fileInputLabel.style.background = 'var(--bg-light)';
            fileInputLabel.style.borderColor = 'var(--border)';
            
            const files = e.dataTransfer.files;
            fileInput.files = files;
            
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        });
    }
    
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(function(notification) {
        setTimeout(function() {
            notification.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(function() {
                notification.remove();
            }, 300);
        }, 5000);
    });
});

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function getFileIcon(filename) {
    const ext = filename.toLowerCase().split('.').pop();
    const iconMap = {
        'png': 'fas fa-file-image',
        'jpg': 'fas fa-file-image',
        'jpeg': 'fas fa-file-image',
        'gif': 'fas fa-file-image',
        'bmp': 'fas fa-file-image',
        'webp': 'fas fa-file-image',
        'mp4': 'fas fa-file-video',
        'webm': 'fas fa-file-video',
        'mov': 'fas fa-file-video',
        'avi': 'fas fa-file-video',
        'mkv': 'fas fa-file-video',
        'pdf': 'fas fa-file-pdf',
        'doc': 'fas fa-file-word',
        'docx': 'fas fa-file-word',
        'xls': 'fas fa-file-excel',
        'xlsx': 'fas fa-file-excel',
        'zip': 'fas fa-file-archive',
        'rar': 'fas fa-file-archive',
        '7z': 'fas fa-file-archive',
        'mp3': 'fas fa-file-audio',
        'wav': 'fas fa-file-audio',
        'flac': 'fas fa-file-audio',
        'm4a': 'fas fa-file-audio'
    };
    
    return iconMap[ext] || 'fas fa-file';
}