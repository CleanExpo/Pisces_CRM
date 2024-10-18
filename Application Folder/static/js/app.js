// Initialize Socket.IO
const socket = io();

let technicianName = 'Technician ' + Math.floor(Math.random() * 1000);
let inspectionId = document.getElementById('inspectionId').value;

// Join the inspection room
socket.emit('join', { inspection_id: inspectionId, technician_name: technicianName });

// Handle user joined event
socket.on('user_joined', (data) => {
    addChatMessage('System', data.message);
    updateUserList(data.technician_name, 'online');
});

// Handle user left event
socket.on('user_left', (data) => {
    addChatMessage('System', data.message);
    updateUserList(data.technician_name, 'offline');
});

// Handle new chat messages
socket.on('new_chat_message', (data) => {
    addChatMessage(data.sender, data.message);
});

// Handle technician typing event
socket.on('technician_typing', (data) => {
    updateTypingIndicator(data.technician_name, data.is_typing);
});

// Handle technician working on step event
socket.on('technician_working', (data) => {
    updateTechnicianWorking(data.technician_name, data.step_id);
});

// Handle step completed event
socket.on('step_completed', (data) => {
    notifyStepCompleted(data.technician_name, data.step_id);
});

// Handle inspection data update event
socket.on('inspection_data_update', (data) => {
    updateInspectionData(data);
});

// Handle SSRA update event
socket.on('ssra_update', (data) => {
    updateSSRA(data);
});

// Handle grid map update event
socket.on('grid_map_update', (data) => {
    updateGridMap(data);
});

// Function to add a chat message to the chat window
function addChatMessage(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to update the user list
function updateUserList(technicianName, status) {
    const userList = document.getElementById('userList');
    let userElement = document.getElementById(`user-${technicianName}`);
    
    if (!userElement) {
        userElement = document.createElement('li');
        userElement.id = `user-${technicianName}`;
        userList.appendChild(userElement);
    }
    
    userElement.innerHTML = `${technicianName}: ${status}`;
    userElement.className = `list-group-item ${status === 'online' ? 'text-success' : 'text-secondary'}`;
}

// Function to update the typing indicator
function updateTypingIndicator(technicianName, isTyping) {
    const typingIndicator = document.getElementById('typingIndicator');
    if (isTyping) {
        typingIndicator.textContent = `${technicianName} is typing...`;
    } else {
        typingIndicator.textContent = '';
    }
}

// Function to update which technician is working on which step
function updateTechnicianWorking(technicianName, stepId) {
    const workingIndicator = document.getElementById(`technicianWorking${stepId}`);
    workingIndicator.textContent = `${technicianName} is working on this step`;
    workingIndicator.classList.remove('d-none');
}

// Function to notify when a step is completed
function notifyStepCompleted(technicianName, stepId) {
    const stepElement = document.getElementById(`step${stepId}`);
    const notificationElement = document.createElement('div');
    notificationElement.className = 'alert alert-success mt-2';
    notificationElement.textContent = `${technicianName} has completed this step`;
    stepElement.appendChild(notificationElement);
    setTimeout(() => notificationElement.remove(), 5000);
}

// Function to update inspection data in real-time
function updateInspectionData(data) {
    const resultElement = document.getElementById(`result${data.step_id}`);
    if (resultElement) {
        resultElement.innerHTML = `<strong>Data Type:</strong> ${data.data_type}<br>
                                   <strong>Content:</strong> ${data.data_content}<br>
                                   <strong>AI Interpretation:</strong> ${data.ai_interpretation}<br>
                                   <strong>Submitted by:</strong> ${data.technician_name}`;
    }
}

// Function to update SSRA in real-time
function updateSSRA(data) {
    const ssraList = document.getElementById('ssraList');
    const ssraEntry = document.createElement('li');
    ssraEntry.className = 'list-group-item';
    ssraEntry.innerHTML = `<strong>Hazard:</strong> ${data.hazard}<br>
                           <strong>Risk Level:</strong> ${data.risk_level}<br>
                           <strong>Control Measure:</strong> ${data.control_measure}<br>
                           <strong>Added by:</strong> ${data.technician_name}`;
    ssraList.appendChild(ssraEntry);
}

// Function to update grid map in real-time
function updateGridMap(data) {
    if (window.canvas) {
        const gridData = JSON.parse(data.grid_data);
        window.canvas.clear();
        gridData.forEach(cell => {
            const rect = new fabric.Rect({
                left: cell.x * 20,
                top: cell.y * 20,
                width: 20,
                height: 20,
                fill: 'rgba(255, 0, 0, 0.5)',
                selectable: false
            });
            window.canvas.add(rect);
        });
        window.canvas.renderAll();
        addChatMessage('System', `${data.technician_name} updated the grid map`);
    }
}

// Event listeners for user interactions
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (message) {
            socket.emit('chat_message', { inspection_id: inspectionId, technician_name: technicianName, message: message });
            chatInput.value = '';
        }
    });

    chatInput.addEventListener('input', function() {
        socket.emit('typing', { inspection_id: inspectionId, technician_name: technicianName, is_typing: true });
    });

    chatInput.addEventListener('blur', function() {
        socket.emit('typing', { inspection_id: inspectionId, technician_name: technicianName, is_typing: false });
    });

    // Add event listeners for submitting inspection data
    const steps = document.querySelectorAll('.inspection-step');
    steps.forEach(step => {
        const stepId = step.id.replace('step', '');
        const submitButton = document.getElementById(`submitButton${stepId}`);
        const textInput = document.getElementById(`textInput${stepId}`);
        const imageInput = document.getElementById(`imageInput${stepId}`);
        const videoInput = document.getElementById(`videoInput${stepId}`);
        const audioButton = document.getElementById(`audioButton${stepId}`);

        submitButton.addEventListener('click', function() {
            let dataType, dataContent;

            if (textInput.value) {
                dataType = 'text';
                dataContent = textInput.value;
            } else if (imageInput.files.length > 0) {
                dataType = 'image';
                dataContent = imageInput.files[0];
            } else if (videoInput.files.length > 0) {
                dataType = 'video';
                dataContent = videoInput.files[0];
            }

            if (dataType && dataContent) {
                socket.emit('submit_inspection_data', {
                    inspection_id: inspectionId,
                    step_id: stepId,
                    data_type: dataType,
                    data_content: dataContent,
                    technician_name: technicianName
                });
                socket.emit('step_completed', {
                    inspection_id: inspectionId,
                    step_id: stepId,
                    technician_name: technicianName
                });
            }
        });

        // Notify others when working on a step
        step.addEventListener('click', function() {
            socket.emit('working_on_step', { inspection_id: inspectionId, technician_name: technicianName, step_id: stepId });
        });
    });

    // Add event listener for submitting SSRA
    const ssraForm = document.getElementById('ssraForm');
    ssraForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const hazard = document.getElementById('hazard').value;
        const riskLevel = document.getElementById('riskLevel').value;
        const controlMeasure = document.getElementById('controlMeasure').value;

        socket.emit('submit_ssra', {
            inspection_id: inspectionId,
            hazard: hazard,
            risk_level: riskLevel,
            control_measure: controlMeasure,
            technician_name: technicianName
        });

        // Clear the form
        ssraForm.reset();
    });

    // Initialize and handle grid map
    const canvas = new fabric.Canvas('gridMap');
    window.canvas = canvas;

    const gridSize = 20;
    const canvasWidth = 600;
    const canvasHeight = 400;

    // Create grid
    for (let i = 0; i < canvasWidth / gridSize; i++) {
        canvas.add(new fabric.Line([i * gridSize, 0, i * gridSize, canvasHeight], { stroke: '#ccc', selectable: false }));
    }
    for (let i = 0; i < canvasHeight / gridSize; i++) {
        canvas.add(new fabric.Line([0, i * gridSize, canvasWidth, i * gridSize], { stroke: '#ccc', selectable: false }));
    }

    canvas.on('mouse:down', function(options) {
        const x = Math.floor(options.e.offsetX / gridSize);
        const y = Math.floor(options.e.offsetY / gridSize);

        const rect = new fabric.Rect({
            left: x * gridSize,
            top: y * gridSize,
            width: gridSize,
            height: gridSize,
            fill: 'rgba(255, 0, 0, 0.5)',
            selectable: false
        });

        canvas.add(rect);
        canvas.renderAll();

        // Emit grid map update
        const gridData = canvas.getObjects('rect').map(obj => ({ x: obj.left / gridSize, y: obj.top / gridSize }));
        socket.emit('update_grid_map', { inspection_id: inspectionId, grid_data: JSON.stringify(gridData), technician_name: technicianName });
    });

    // Clear grid
    const clearGridButton = document.getElementById('clearGrid');
    clearGridButton.addEventListener('click', function() {
        canvas.clear();
        // Recreate the grid lines
        for (let i = 0; i < canvasWidth / gridSize; i++) {
            canvas.add(new fabric.Line([i * gridSize, 0, i * gridSize, canvasHeight], { stroke: '#ccc', selectable: false }));
        }
        for (let i = 0; i < canvasHeight / gridSize; i++) {
            canvas.add(new fabric.Line([0, i * gridSize, canvasWidth, i * gridSize], { stroke: '#ccc', selectable: false }));
        }
        canvas.renderAll();
        socket.emit('update_grid_map', { inspection_id: inspectionId, grid_data: JSON.stringify([]), technician_name: technicianName });
    });
});
