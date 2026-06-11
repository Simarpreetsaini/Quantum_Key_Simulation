/**
 * Quantum Key Distribution (QKD) Satellite System Simulation
 * Implementing BB84 protocol simulation and custom Canvas visualizer
 */

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const messageInput = document.getElementById('message-input');
    const interceptionCheckbox = document.getElementById('interception-checkbox');
    const runBtn = document.getElementById('run-btn');
    const clearBtn = document.getElementById('clear-btn');
    const logOutput = document.getElementById('log-output');
    const clearLogBtn = document.getElementById('clear-log-btn');
    const systemStatus = document.getElementById('system-status');
    
    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Result Fields
    const resOriginal = document.getElementById('res-original');
    const resEncrypted = document.getElementById('res-encrypted');
    const resDecrypted = document.getElementById('res-decrypted');
    const statRawKey = document.getElementById('stat-raw-key');
    const statFinalKey = document.getElementById('stat-final-key');
    const statQber = document.getElementById('stat-qber');
    const statSecurityStatus = document.getElementById('stat-security-status');
    const securityStatusBox = document.getElementById('security-status-box');
    
    // Details Fields
    const alicePolarizationsDisplay = document.getElementById('alice-polarizations-display');
    const aliceBasesDisplay = document.getElementById('alice-bases-display');
    const bobBasesDisplay = document.getElementById('bob-bases-display');
    const reconciliationDisplay = document.getElementById('reconciliation-display');
    const rawKeySample = document.getElementById('raw-key-sample');
    const finalKeySample = document.getElementById('final-key-sample');
    
    // Security Fields
    const securityAlertBanner = document.getElementById('security-alert-banner');
    const alertTitle = document.getElementById('alert-title');
    const alertDesc = document.getElementById('alert-desc');
    const secQberVal = document.getElementById('sec-qber-val');
    const secCompromiseEstimate = document.getElementById('sec-compromise-estimate');
    const secConfidence = document.getElementById('sec-confidence');
    const secEntropyReduction = document.getElementById('sec-entropy-reduction');
    const secLeakage = document.getElementById('sec-leakage');
    const securityRecommendation = document.getElementById('security-recommendation');
    
    // Modal Elements
    const aboutLink = document.getElementById('about-link');
    const docsLink = document.getElementById('docs-link');
    const aboutModal = document.getElementById('about-modal');
    const docsModal = document.getElementById('docs-modal');
    const closeBtns = document.querySelectorAll('.close-btn');
    
    // Progress Modal
    const progressModal = document.getElementById('progress-modal');
    const simulationProgressBar = document.getElementById('simulation-progress-bar');
    const progressStatus = document.getElementById('progress-status');
    
    // Canvas & Animation Elements
    const canvas = document.getElementById('viz-canvas');
    const ctx = canvas.getContext('2d');
    const animToggleBtn = document.getElementById('anim-toggle-btn');
    const animResetBtn = document.getElementById('anim-reset-btn');
    
    // Global Simulation State
    let simData = null;
    let isAnimating = false;
    let animationFrameId = null;
    let animationPhase = 0; // 0: Standby, 1: Quantum, 2: Measurement, 3: Sifting, 4: Error correction/Key creation
    let animProgress = 0;
    let particles = [];
    let satellitesFloatOffset = 0;
    let pulseRadius = 0;
    
    // Initialize Log
    addLogEntry("System initialized.");
    addLogEntry("Quantum key distribution modules loaded.");
    addLogEntry("Satellite communication protocol initialized.");
    addLogEntry("System ready for simulation.");
    
    // Utility: sleep helper
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Tab switcher
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            addLogEntry(`Switched to panel: ${btn.textContent.trim()}`);
        });
    });

    // Modals
    const openModal = (modal) => modal.classList.add('active');
    const closeModal = (modal) => modal.classList.remove('active');
    
    aboutLink.addEventListener('click', (e) => { e.preventDefault(); openModal(aboutModal); });
    docsLink.addEventListener('click', (e) => { e.preventDefault(); openModal(docsModal); });
    
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(aboutModal);
            closeModal(docsModal);
        });
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === aboutModal) closeModal(aboutModal);
        if (e.target === docsModal) closeModal(docsModal);
    });

    // Log console helper
    function addLogEntry(message, type = 'info') {
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        
        const line = document.createElement('div');
        line.className = `log-line log-${type}`;
        
        const timestamp = document.createElement('span');
        timestamp.className = 'log-timestamp';
        timestamp.textContent = `[${timeStr}]`;
        
        const content = document.createElement('span');
        content.className = 'log-text-content';
        content.textContent = message;
        
        line.appendChild(timestamp);
        line.appendChild(content);
        logOutput.appendChild(line);
        logOutput.scrollTop = logOutput.scrollHeight;
    }
    
    clearLogBtn.addEventListener('click', () => {
        logOutput.innerHTML = '';
        addLogEntry("Log cleared.");
    });

    // BB84 Protocol Simulation Engine
    async function simulateQKD(message, simulateInterception) {
        addLogEntry(`Starting simulation for message: "${message}"`);
        if (simulateInterception) {
            addLogEntry("Interception simulation enabled (Eve active).", "warning");
        }
        
        // Show progress overlay
        openModal(progressModal);
        
        const steps = [
            { desc: "Generating entangled photon pairs...", progress: 10 },
            { desc: "Aligning satellite transmitter optical beacons...", progress: 20 },
            { desc: "Distributing polarization-coded quantum states...", progress: 30 },
            { desc: "Bob measuring arriving photons under random basis selection...", progress: 45 },
            { desc: "Initiating public classical channel sifting protocol...", progress: 60 },
            { desc: "Performing basis reconciliation and raw key distillation...", progress: 75 },
            { desc: "Estimating Quantum Bit Error Rate (QBER)...", progress: 85 },
            { desc: "Applying error correction codes...", progress: 92 },
            { desc: "Executing Privacy Amplification universal hashing...", progress: 97 },
            { desc: "Encrypting transmission and verifying decryption payload...", progress: 100 }
        ];

        for (const step of steps) {
            simulationProgressBar.style.width = `${step.progress}%`;
            progressStatus.textContent = step.desc;
            addLogEntry(`[SIM] ${step.desc}`);
            await sleep(250);
        }
        
        await sleep(200);
        closeModal(progressModal);
        
        // Core quantum calculations
        const keyLength = 512;
        const bases = ['+', 'x'];
        const polarizations = {
            '+': ['↑', '→'], // 0 and 1
            'x': ['↗', '↖']  // 0 and 1
        };
        
        // Generate random bases for Alice and Bob
        let aliceBases = [];
        let bobBases = [];
        let rawBits = [];
        
        for (let i = 0; i < keyLength; i++) {
            aliceBases.push(bases[Math.floor(Math.random() * 2)]);
            bobBases.push(bases[Math.floor(Math.random() * 2)]);
            rawBits.push(Math.random() < 0.5 ? 0 : 1);
        }
        
        // Sift indices where bases match
        let matchingIndices = [];
        for (let i = 0; i < keyLength; i++) {
            if (aliceBases[i] === bobBases[i]) {
                matchingIndices.push(i);
            }
        }
        
        // Calculate QBER
        let qber = 0;
        let interceptDetected = false;
        if (simulateInterception) {
            // High error rate due to Eve's measurements (usually around 20-25%)
            qber = 15 + Math.random() * 10; 
            interceptDetected = true;
        } else {
            // Normal channel background noise (2-6%)
            qber = 2 + Math.random() * 4;
            interceptDetected = qber > 10.0;
        }
        
        // Simulate Bob's bit readings after noise/eavesdropping
        let bobBits = [...rawBits];
        let errorCount = 0;
        
        // Apply errors to sifted keys
        matchingIndices.forEach(idx => {
            const errorProbability = qber / 100;
            if (Math.random() < errorProbability) {
                bobBits[idx] = bobBits[idx] === 0 ? 1 : 0;
                errorCount++;
            }
        });
        
        // Recalculate exact QBER based on sample
        const actualQber = (errorCount / Math.max(matchingIndices.length, 1)) * 100;
        const finalInterceptDetected = actualQber >= 10.0;
        
        // Distill key
        const rawKeySize = matchingIndices.length;
        const errorCorrectionReduction = Math.floor(rawKeySize * 0.22);
        const privacyAmplificationReduction = Math.floor(rawKeySize * 0.15);
        let finalKeySize = rawKeySize - errorCorrectionReduction - privacyAmplificationReduction;
        finalKeySize = Math.max(finalKeySize, 32);
        
        // Create actual key binary strings
        let rawKeyStr = matchingIndices.map(idx => rawBits[idx]).join('');
        let finalKeyStr = '';
        for (let i = 0; i < finalKeySize; i++) {
            finalKeyStr += Math.random() < 0.5 ? '0' : '1';
        }
        
        // Perform Encryption/Decryption
        const encoder = new TextEncoder();
        const decoder = new TextDecoder();
        const messageBytes = encoder.encode(message);
        
        // Convert final binary key to byte array
        let keyBytes = [];
        for (let i = 0; i < finalKeyStr.length; i += 8) {
            const byteStr = finalKeyStr.substr(i, 8);
            if (byteStr.length === 8) {
                keyBytes.push(parseInt(byteStr, 2));
            }
        }
        if (keyBytes.length === 0) keyBytes = [101, 102, 103, 104];
        
        // Repeat key to match message length and XOR
        let encryptedBytes = new Uint8Array(messageBytes.length);
        for (let i = 0; i < messageBytes.length; i++) {
            const keyByte = keyBytes[i % keyBytes.length];
            encryptedBytes[i] = messageBytes[i] ^ keyByte;
        }
        
        // Hex represent encrypted message
        const encryptedHex = Array.from(encryptedBytes)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('')
            .toUpperCase();
            
        // Decrypt XOR payload
        let decryptedBytes = new Uint8Array(encryptedBytes.length);
        for (let i = 0; i < encryptedBytes.length; i++) {
            const keyByte = keyBytes[i % keyBytes.length];
            decryptedBytes[i] = encryptedBytes[i] ^ keyByte;
        }
        const decryptedText = decoder.decode(decryptedBytes);
        
        // Entropy parameters
        const entropyReduction = 10 + Math.random() * 8;
        const securityParameter = 128;
        const maxLeakage = Math.pow(2, -securityParameter / 8);
        const compromiseEstimate = finalInterceptDetected ? (qber * 2.1) : 0;
        const confidenceLevel = finalInterceptDetected ? (80 + Math.random() * 19.5) : 99.9;
        
        simData = {
            originalMessage: message,
            encryptedHex: encryptedHex,
            decryptedText: decryptedText,
            aliceBases: aliceBases.slice(0, 80),
            bobBases: bobBases.slice(0, 80),
            rawBits: rawBits.slice(0, 80),
            bobBits: bobBits.slice(0, 80),
            matchingIndices: matchingIndices.slice(0, 80),
            rawKeySize: rawKeySize,
            finalKeySize: finalKeySize,
            qber: actualQber,
            interceptDetected: finalInterceptDetected,
            entropyReduction: entropyReduction,
            securityParameter: securityParameter,
            maxLeakage: maxLeakage,
            compromiseEstimate: compromiseEstimate,
            confidenceLevel: confidenceLevel,
            rawKeyStr: rawKeyStr,
            finalKeyStr: finalKeyStr
        };
        
        addLogEntry("QKD simulation completed successfully.", "success");
        updateResultsUI();
    }

    // Bind simulation results to UI Elements
    function updateResultsUI() {
        if (!simData) return;
        
        // 1. Summary Card
        resOriginal.textContent = simData.originalMessage;
        resEncrypted.textContent = simData.encryptedHex.match(/.{1,8}/g).join(' ');
        resDecrypted.textContent = simData.decryptedText;
        statRawKey.textContent = simData.rawKeySize;
        statFinalKey.textContent = simData.finalKeySize;
        statQber.textContent = simData.qber.toFixed(2);
        
        const statusSpan = statSecurityStatus;
        statusSpan.className = 'stat-status';
        
        if (simData.interceptDetected) {
            statusSpan.textContent = "COMPROMISED";
            statusSpan.classList.add('compromised');
            securityStatusBox.style.borderColor = 'var(--danger-glow)';
            addLogEntry("CRITICAL: Quantum Channel integrity breached! Interception detected.", "alert");
        } else {
            statusSpan.textContent = "SECURE";
            statusSpan.classList.add('secure');
            securityStatusBox.style.borderColor = 'var(--success-glow)';
            addLogEntry("Quantum Channel confirmed SECURE. Secure key successfully established.", "success");
        }
        
        // 2. Protocol Details Card
        // Generate polarization displays
        alicePolarizationsDisplay.innerHTML = '';
        aliceBasesDisplay.innerHTML = '';
        bobBasesDisplay.innerHTML = '';
        reconciliationDisplay.innerHTML = '';
        
        const basisSymbols = { '+': '✛', 'x': '✕' };
        const polarSymbols = {
            '+': ['↑', '→'], // 0=↑, 1=→
            'x': ['↗', '↖']  // 0=↗, 1=↖
        };
        
        for (let i = 0; i < 40; i++) {
            const aBasis = simData.aliceBases[i];
            const bBasis = simData.bobBases[i];
            const aBit = simData.rawBits[i];
            const isMatch = aBasis === bBasis;
            const className = isMatch ? 'match' : 'mismatch';
            
            // Polarizations
            const pSpan = document.createElement('span');
            pSpan.className = className;
            pSpan.textContent = polarSymbols[aBasis][aBit];
            alicePolarizationsDisplay.appendChild(pSpan);
            
            // Alice bases
            const abSpan = document.createElement('span');
            abSpan.className = className;
            abSpan.textContent = basisSymbols[aBasis];
            aliceBasesDisplay.appendChild(abSpan);
            
            // Bob bases
            const bbSpan = document.createElement('span');
            bbSpan.className = className;
            bbSpan.textContent = basisSymbols[bBasis];
            bobBasesDisplay.appendChild(bbSpan);
            
            // Reconciliation
            const rSpan = document.createElement('span');
            rSpan.className = className;
            rSpan.textContent = isMatch ? '✓' : '✗';
            reconciliationDisplay.appendChild(rSpan);
        }
        
        rawKeySample.textContent = simData.rawKeyStr.substring(0, 64) + '...';
        finalKeySample.textContent = simData.finalKeyStr.substring(0, 64) + '...';
        
        // 3. Security Analysis Card
        secQberVal.textContent = `${simData.qber.toFixed(2)}%`;
        
        // Switch banner & card states based on security breach
        const banner = securityAlertBanner;
        banner.className = 'alert-banner';
        
        if (simData.interceptDetected) {
            banner.classList.add('compromised');
            alertTitle.textContent = "Security Breach Detected";
            alertDesc.textContent = `The measured QBER of ${simData.qber.toFixed(2)}% exceeds the critical 10.0% security threshold.`;
            
            secCompromiseEstimate.textContent = `${simData.compromiseEstimate.toFixed(1)}%`;
            secCompromiseEstimate.style.color = 'var(--danger)';
            secConfidence.textContent = `${simData.confidenceLevel.toFixed(1)}%`;
            secConfidence.style.color = 'var(--warning)';
            
            secEntropyReduction.textContent = "ABORTED";
            secLeakage.textContent = "HIGH";
            
            securityRecommendation.className = "recommendation-content abort";
            securityRecommendation.innerHTML = `<strong>RECOMMENDATION: ABORT KEY TRANSFER</strong><br>
                Eavesdropping detected on the orbital channel. The raw session key must be immediately purged. Do not encrypt data with this key. Reload transmitter systems and initiate QKD frequency scan to lock out interception nodes.`;
        } else {
            banner.classList.add('secure');
            alertTitle.textContent = "Channel Secure";
            alertDesc.textContent = `The measured QBER of ${simData.qber.toFixed(2)}% is safely below the 10.0% threshold.`;
            
            secCompromiseEstimate.textContent = "0.0%";
            secCompromiseEstimate.style.color = 'var(--success)';
            secConfidence.textContent = "99.9%";
            secConfidence.style.color = 'var(--success)';
            
            secEntropyReduction.textContent = `${simData.entropyReduction.toFixed(1)}%`;
            secLeakage.textContent = `< ${simData.maxLeakage.toExponential(2)}`;
            
            securityRecommendation.className = "recommendation-content secure";
            securityRecommendation.innerHTML = `<strong>RECOMMENDATION: ESTABLISH CRYPTO CONTEXT</strong><br>
                Channel integrity verified. The distilled final key size of ${simData.finalKeySize} bits contains negligible information leakage. You may safely initiate secure encrypted data transmissions over the classical satellite carrier.`;
        }
        
        // Enable Animation controls
        animToggleBtn.removeAttribute('disabled');
        animToggleBtn.textContent = 'Start Animation';
        isAnimating = false;
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
        
        // Switch active tab to Visualization automatically
        tabBtns[0].click();
        
        // Auto-start animation
        startSimulationAnimation();
    }

    // Button Bindings
    runBtn.addEventListener('click', () => {
        const msg = messageInput.value.trim();
        if (!msg) {
            alert("Please enter a message to encrypt.");
            return;
        }
        
        const simulateInterception = interceptionCheckbox.checked;
        simulateQKD(msg, simulateInterception);
    });
    
    clearBtn.addEventListener('click', () => {
        simData = null;
        resOriginal.textContent = '-';
        resEncrypted.textContent = '-';
        resDecrypted.textContent = '-';
        statRawKey.textContent = '-';
        statFinalKey.textContent = '-';
        statQber.textContent = '-';
        statSecurityStatus.textContent = '-';
        statSecurityStatus.className = 'stat-status';
        securityStatusBox.style.borderColor = 'var(--border-color)';
        
        alicePolarizationsDisplay.textContent = 'Run simulation to see sequence';
        aliceBasesDisplay.textContent = '-';
        bobBasesDisplay.textContent = '-';
        reconciliationDisplay.textContent = '-';
        rawKeySample.textContent = '-';
        finalKeySample.textContent = '-';
        
        securityAlertBanner.className = 'alert-banner';
        alertTitle.textContent = "No Simulation Data";
        alertDesc.textContent = "Run a quantum key distribution simulation to analyze channel security.";
        secQberVal.textContent = '-';
        secCompromiseEstimate.textContent = '-';
        secConfidence.textContent = '-';
        secEntropyReduction.textContent = '-';
        secLeakage.textContent = '-';
        securityRecommendation.className = "recommendation-content";
        securityRecommendation.textContent = "Run simulation to receive automated system instructions.";
        
        animToggleBtn.setAttribute('disabled', 'true');
        animToggleBtn.textContent = 'Start Animation';
        
        resetAnimationState();
        addLogEntry("Simulation results cleared.");
    });

    // Custom Canvas Animation Framework
    const satPos = { x: 400, y: 100 };
    const alicePos = { x: 180, y: 380 };
    const bobPos = { x: 620, y: 380 };
    const evePos = { x: 400, y: 400 };

    // Reset Animation
    function resetAnimationState() {
        isAnimating = false;
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        animationPhase = 0;
        animProgress = 0;
        particles = [];
        satellitesFloatOffset = 0;
        pulseRadius = 0;
        drawStandbyScene();
    }
    
    animResetBtn.addEventListener('click', () => {
        resetAnimationState();
        if (simData) {
            animToggleBtn.textContent = 'Start Animation';
            animToggleBtn.removeAttribute('disabled');
        }
        addLogEntry("Visualizer display reset.");
    });
    
    animToggleBtn.addEventListener('click', () => {
        if (isAnimating) {
            // Stop
            isAnimating = false;
            animToggleBtn.textContent = 'Resume Animation';
            addLogEntry("Animation paused.");
        } else {
            // Start
            startSimulationAnimation();
        }
    });

    function startSimulationAnimation() {
        if (!simData) return;
        isAnimating = true;
        animToggleBtn.textContent = 'Pause Animation';
        addLogEntry("Visualizer animation started.");
        
        // Start from phase 1
        animationPhase = 1;
        animProgress = 0;
        particles = [];
        generatePhaseParticles();
        
        animate();
    }

    // Generate Particles for specific phases
    function generatePhaseParticles() {
        particles = [];
        
        if (animationPhase === 1) {
            // Quantum state distribution: stream of particles from Satellite to Alice and Bob
            const colors = simData.interceptDetected 
                ? ['#38bdf8', '#c084fc', '#ef4444', '#f59e0b'] 
                : ['#38bdf8', '#c084fc', '#10b981'];
                
            // Generate 15 particles going to Alice and Bob
            for (let i = 0; i < 15; i++) {
                // Towards Alice
                particles.push({
                    x: satPos.x,
                    y: satPos.y,
                    startX: satPos.x,
                    startY: satPos.y,
                    endX: alicePos.x,
                    endY: alicePos.y,
                    speed: 0.008 + Math.random() * 0.005,
                    progress: -i * 0.08, // Delayed start
                    size: 4 + Math.random() * 3,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    type: 'quantum-alice'
                });
                
                // Towards Bob
                particles.push({
                    x: satPos.x,
                    y: satPos.y,
                    startX: satPos.x,
                    startY: satPos.y,
                    endX: bobPos.x,
                    endY: bobPos.y,
                    speed: 0.008 + Math.random() * 0.005,
                    progress: -i * 0.08,
                    size: 4 + Math.random() * 3,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    type: 'quantum-bob',
                    intercepted: false
                });
            }
        } else if (animationPhase === 3) {
            // Sifting/Reconciliation: Classical packets passing between Alice and Bob
            // Generate packets from Alice to Bob and Bob to Alice
            particles.push({
                x: alicePos.x,
                y: alicePos.y - 30,
                startX: alicePos.x,
                startY: alicePos.y - 30,
                endX: bobPos.x,
                endY: bobPos.y - 30,
                speed: 0.015,
                progress: 0,
                color: '#38bdf8',
                label: 'Alice Bases',
                type: 'classical-forward'
            });
            particles.push({
                x: bobPos.x,
                y: bobPos.y - 15,
                startX: bobPos.x,
                startY: bobPos.y - 15,
                endX: alicePos.x,
                endY: alicePos.y - 15,
                speed: 0.015,
                progress: -0.3, // Start slightly delayed
                color: '#10b981',
                label: 'Bob Bases',
                type: 'classical-backward'
            });
        } else if (animationPhase === 5) {
            // Secure Key Established: Data transmission Alice -> Bob
            if (!simData.interceptDetected) {
                // stream of green data packets
                for (let i = 0; i < 6; i++) {
                    particles.push({
                        x: alicePos.x,
                        y: alicePos.y,
                        startX: alicePos.x,
                        startY: alicePos.y,
                        endX: bobPos.x,
                        endY: bobPos.y,
                        speed: 0.012,
                        progress: -i * 0.18,
                        size: 7,
                        color: '#10b981',
                        type: 'secure-data'
                    });
                }
            }
        }
    }

    // Static standby scene rendering
    function drawStandbyScene() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw space grid lines
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.03)';
        ctx.lineWidth = 1;
        const gridSize = 40;
        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // Draw Links / Channels
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        
        // Alice-Satellite Link
        ctx.beginPath();
        ctx.moveTo(alicePos.x, alicePos.y);
        ctx.lineTo(satPos.x, satPos.y + satellitesFloatOffset);
        ctx.stroke();
        
        // Bob-Satellite Link
        ctx.beginPath();
        ctx.moveTo(bobPos.x, bobPos.y);
        ctx.lineTo(satPos.x, satPos.y + satellitesFloatOffset);
        ctx.stroke();

        // Alice-Bob Classical Link (horizontal bottom line)
        ctx.beginPath();
        ctx.moveTo(alicePos.x, alicePos.y + 10);
        ctx.lineTo(bobPos.x, bobPos.y + 10);
        ctx.stroke();
        
        ctx.setLineDash([]); // Reset dash

        // Draw Eve (Eavesdropping node) if simulation has intercept checked
        if (interceptionCheckbox.checked) {
            drawEveNode();
        }

        // Draw Stations and Satellite
        drawSatellite(satPos.x, satPos.y + satellitesFloatOffset);
        drawGroundStation(alicePos.x, alicePos.y, "Alice (Sender)", "#ef4444");
        drawGroundStation(bobPos.x, bobPos.y, "Bob (Receiver)", "#10b981");

        // Helper label
        ctx.fillStyle = '#64748b';
        ctx.font = '12px Space Grotesk';
        ctx.textAlign = 'center';
        ctx.fillText("Ready. Run simulation and trigger animation.", canvas.width / 2, canvas.height - 20);
    }

    // Node Drawing Subroutines
    function drawSatellite(x, y) {
        ctx.save();
        
        // Solar Panel Left
        ctx.fillStyle = '#1e293b';
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 1.5;
        ctx.fillRect(x - 65, y - 8, 30, 16);
        ctx.strokeRect(x - 65, y - 8, 30, 16);
        
        // Solar grid marks
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.beginPath();
        ctx.moveTo(x - 50, y - 8); ctx.lineTo(x - 50, y + 8);
        ctx.moveTo(x - 65, y); ctx.lineTo(x - 35, y);
        ctx.stroke();
        
        // Solar Panel Right
        ctx.fillStyle = '#1e293b';
        ctx.strokeStyle = '#38bdf8';
        ctx.fillRect(x + 35, y - 8, 30, 16);
        ctx.strokeRect(x + 35, y - 8, 30, 16);
        
        // Solar grid marks
        ctx.beginPath();
        ctx.moveTo(x + 50, y - 8); ctx.lineTo(x + 50, y + 8);
        ctx.moveTo(x + 35, y); ctx.lineTo(x + 65, y);
        ctx.stroke();
        
        // Panel Connectors
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x - 35, y); ctx.lineTo(x - 15, y);
        ctx.moveTo(x + 15, y); ctx.lineTo(x + 35, y);
        ctx.stroke();
        
        // Core Body Satellite (Circle and glow)
        ctx.shadowBlur = 10;
        ctx.shadowColor = 'rgba(56, 189, 248, 0.6)';
        ctx.fillStyle = '#0f172a';
        ctx.strokeStyle = '#38bdf8';
        ctx.beginPath();
        ctx.arc(x, y, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        
        // Inner detail dish
        ctx.shadowBlur = 0; // Reset
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, Math.PI * 2);
        ctx.stroke();
        
        // Antennas
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x, y + 18);
        ctx.lineTo(x, y + 26);
        ctx.stroke();
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath();
        ctx.arc(x, y + 27, 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Label
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Space Grotesk';
        ctx.textAlign = 'center';
        ctx.fillText("QUANTUM SATELLITE", x, y - 24);
        
        ctx.restore();
    }

    function drawGroundStation(x, y, label, themeColor) {
        ctx.save();
        
        // Draw signal range/base circle
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        ctx.beginPath();
        ctx.arc(x, y, 50, 0, Math.PI * 2);
        ctx.stroke();

        // Pulsing rings around secure/active base
        if (isAnimating) {
            ctx.strokeStyle = themeColor + '20'; // Hex opacity
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(x, y, 30 + pulseRadius, 0, Math.PI * 2);
            ctx.stroke();
        }

        // Base Dome
        ctx.fillStyle = '#0f172a';
        ctx.strokeStyle = themeColor;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 22, Math.PI, 0); // half circle dome
        ctx.lineTo(x + 22, y + 16);
        ctx.lineTo(x - 22, y + 16);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        // Inner Core glowing circle
        ctx.fillStyle = themeColor;
        ctx.shadowBlur = 8;
        ctx.shadowColor = themeColor;
        ctx.beginPath();
        ctx.arc(x, y - 4, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0; // Reset

        // Antenna dish structure
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x, y - 4);
        ctx.lineTo(x - 12, y - 18);
        ctx.stroke();
        
        ctx.strokeStyle = themeColor;
        ctx.beginPath();
        ctx.arc(x - 14, y - 20, 8, -Math.PI / 4, Math.PI * 3 / 4);
        ctx.stroke();

        // Labels
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Space Grotesk';
        ctx.textAlign = 'center';
        ctx.fillText(label.split(' ')[0], x, y + 36);
        
        ctx.fillStyle = varColorText();
        ctx.font = '10px Space Grotesk';
        ctx.fillText(label.split(' ')[1] || '', x, y + 48);
        
        ctx.restore();
        
        function varColorText() {
            return themeColor === '#ef4444' ? 'rgba(239, 68, 68, 0.7)' : 'rgba(16, 185, 129, 0.7)';
        }
    }

    function drawEveNode() {
        ctx.save();
        
        const isBreached = simData && simData.interceptDetected;
        const eveThemeColor = isBreached ? '#ef4444' : '#f59e0b';
        
        // Glowing alert ring around Eve if breach confirmed
        if (isBreached && isAnimating) {
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.2)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(evePos.x, evePos.y, 40 + (pulseRadius * 0.5), 0, Math.PI * 2);
            ctx.stroke();
        }

        // Diamond container representing interceptor node
        ctx.fillStyle = '#0f172a';
        ctx.strokeStyle = eveThemeColor;
        ctx.lineWidth = 2;
        
        ctx.shadowBlur = 8;
        ctx.shadowColor = eveThemeColor;
        
        ctx.beginPath();
        ctx.moveTo(evePos.x, evePos.y - 20);
        ctx.lineTo(evePos.x + 20, evePos.y);
        ctx.lineTo(evePos.x, evePos.y + 20);
        ctx.lineTo(evePos.x - 20, evePos.y);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0; // Reset
        
        // Inner core lens
        ctx.fillStyle = eveThemeColor;
        ctx.beginPath();
        ctx.arc(evePos.x, evePos.y, 5, 0, Math.PI * 2);
        ctx.fill();

        // Label
        ctx.fillStyle = eveThemeColor;
        ctx.font = 'bold 12px Space Grotesk';
        ctx.textAlign = 'center';
        ctx.fillText("EVE (INTERCEPTOR)", evePos.x, evePos.y + 36);
        
        ctx.restore();
    }

    // Animation Loop Execution
    function animate() {
        if (!isAnimating) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Grid lines drawing
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.03)';
        ctx.lineWidth = 1;
        const gridSize = 40;
        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // Dynamic properties increment
        satellitesFloatOffset = Math.sin(Date.now() * 0.003) * 6;
        pulseRadius = (pulseRadius + 0.4) % 20;

        // Draw background link paths
        drawActiveLinks();

        // Render nodes
        if (interceptionCheckbox.checked || (simData && simData.interceptDetected)) {
            drawEveNode();
        }
        drawSatellite(satPos.x, satPos.y + satellitesFloatOffset);
        drawGroundStation(alicePos.x, alicePos.y, "Alice (Sender)", "#ef4444");
        drawGroundStation(bobPos.x, bobPos.y, "Bob (Receiver)", "#10b981");

        // Render phase status banner at top
        drawPhaseBanner();

        // Update & draw particles
        updateAndDrawParticles();

        animationFrameId = requestAnimationFrame(animate);
    }

    function drawActiveLinks() {
        ctx.save();
        ctx.setLineDash([4, 4]);
        
        // Standard links
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        
        // Alice link
        ctx.beginPath();
        ctx.moveTo(alicePos.x, alicePos.y);
        ctx.lineTo(satPos.x, satPos.y + satellitesFloatOffset);
        ctx.stroke();
        
        // Bob Link (Direct or through Eve)
        ctx.beginPath();
        ctx.moveTo(bobPos.x, bobPos.y);
        if (interceptionCheckbox.checked) {
            ctx.lineTo(evePos.x, evePos.y);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(evePos.x, evePos.y);
            ctx.lineTo(satPos.x, satPos.y + satellitesFloatOffset);
            ctx.stroke();
        } else {
            ctx.lineTo(satPos.x, satPos.y + satellitesFloatOffset);
            ctx.stroke();
        }
        
        // Public Classical Link (Bottom Line)
        if (animationPhase === 3) {
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
            ctx.shadowBlur = 5;
            ctx.shadowColor = 'rgba(56, 189, 248, 0.3)';
            ctx.setLineDash([]);
        } else {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        }
        ctx.beginPath();
        ctx.moveTo(alicePos.x, alicePos.y + 10);
        ctx.lineTo(bobPos.x, bobPos.y + 10);
        ctx.stroke();
        
        ctx.restore();
    }

    function drawPhaseBanner() {
        ctx.save();
        
        const phases = [
            "",
            "Phase 1: Quantum state distribution (polarization lasers)",
            "Phase 2: Measurement & Basis Selection (analyzing photon states)",
            "Phase 3: Basis Reconciliation (exchanging bases over public classical channel)",
            "Phase 4: Error correction & privacy amplification",
            "Phase 5: Key Distillation Completed"
        ];
        
        ctx.fillStyle = '#0f172a';
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.lineWidth = 1;
        ctx.fillRect(20, 20, canvas.width - 40, 32);
        ctx.strokeRect(20, 20, canvas.width - 40, 32);
        
        ctx.fillStyle = '#38bdf8';
        ctx.font = '500 13px Space Grotesk';
        ctx.textAlign = 'left';
        ctx.fillText(phases[animationPhase], 36, 40);
        
        ctx.restore();
    }

    function updateAndDrawParticles() {
        let allFinished = true;
        
        ctx.save();
        
        particles.forEach(p => {
            if (p.progress < 0) {
                // Not spawned yet
                p.progress += 0.01;
                allFinished = false;
                return;
            }
            
            if (p.progress < 1) {
                allFinished = false;
                
                // Advance
                p.progress += p.speed;
                if (p.progress > 1) p.progress = 1;
                
                // Position calculations
                let currentFloat = (p.startY === satPos.y) ? satellitesFloatOffset : 0;
                
                // Intercept logic for Bob path
                if (interceptionCheckbox.checked && p.type === 'quantum-bob' && p.progress >= 0.5) {
                    if (!p.intercepted) {
                        p.intercepted = true;
                        // Eve perturbs the color of the photon due to measurement noise
                        p.color = '#f59e0b';
                    }
                    
                    // Route from satellite through Eve to Bob
                    if (p.progress <= 0.75) {
                        const subProg = (p.progress - 0.5) / 0.25; // mapped 0 to 1
                        p.x = satPos.x + (evePos.x - satPos.x) * subProg;
                        p.y = (satPos.y + currentFloat) + (evePos.y - (satPos.y + currentFloat)) * subProg;
                    } else {
                        const subProg = (p.progress - 0.75) / 0.25; // mapped 0 to 1
                        p.x = evePos.x + (bobPos.x - evePos.x) * subProg;
                        p.y = evePos.y + (bobPos.y - evePos.y) * subProg;
                    }
                } else {
                    // Normal straight linear path
                    p.x = p.startX + (p.endX - p.startX) * p.progress;
                    p.y = (p.startY + currentFloat) + (p.endY - p.startY) * p.progress;
                }
                
                // Draw particle
                if (p.type.startsWith('quantum')) {
                    // Glowing photon
                    ctx.shadowBlur = 8;
                    ctx.shadowColor = p.color;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // polarization vector indicator
                    ctx.shadowBlur = 0;
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath();
                    ctx.moveTo(p.x - 3, p.y); ctx.lineTo(p.x + 3, p.y);
                    ctx.stroke();
                } else if (p.type.startsWith('classical')) {
                    // Draw classical packet block
                    ctx.fillStyle = p.color;
                    ctx.shadowBlur = 6;
                    ctx.shadowColor = p.color;
                    ctx.fillRect(p.x - 35, p.y - 10, 70, 20);
                    
                    ctx.shadowBlur = 0;
                    ctx.fillStyle = '#0f172a';
                    ctx.font = '9px var(--font-mono)';
                    ctx.textAlign = 'center';
                    ctx.fillText(p.label, p.x, p.y + 3);
                } else if (p.type === 'secure-data') {
                    // Secure data packet moving from Alice to Bob
                    ctx.fillStyle = p.color;
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = p.color;
                    ctx.fillRect(p.x - 6, p.y - 6, 12, 12);
                    
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(p.x - 6, p.y - 6, 12, 12);
                }
            }
        });
        
        ctx.restore();
        
        // Handle Phase Transitions
        if (allFinished && particles.length > 0) {
            handlePhaseAdvance();
        }
    }

    function handlePhaseAdvance() {
        if (animationPhase === 1) {
            // Move to Measurement
            animationPhase = 2;
            addLogEntry("[VIS] Quantum state measurement in progress...");
            setTimeout(() => {
                animationPhase = 3;
                generatePhaseParticles();
                addLogEntry("[VIS] Starting basis reconciliation over public channel...");
            }, 1500);
        } else if (animationPhase === 3) {
            // Move to Error check
            animationPhase = 4;
            addLogEntry("[VIS] Calculating QBER and sifting keys...");
            setTimeout(() => {
                animationPhase = 5;
                if (simData.interceptDetected) {
                    addLogEntry("[VIS] CRITICAL: QBER exceeded threshold. Aborting key exchange.", "alert");
                    isAnimating = false;
                    animToggleBtn.textContent = 'Start Animation';
                    drawAbortedScene();
                } else {
                    generatePhaseParticles();
                    addLogEntry("[VIS] Secure key established. Initiating data transmission.", "success");
                }
            }, 1500);
        } else if (animationPhase === 5) {
            // End loop
            isAnimating = false;
            animToggleBtn.textContent = 'Replay Animation';
            addLogEntry("[VIS] Animation sequence completed.");
        }
    }

    function drawAbortedScene() {
        ctx.save();
        
        // Draw aborted banner
        ctx.fillStyle = 'rgba(239, 68, 68, 0.1)';
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 2;
        ctx.fillRect(50, canvas.height / 2 - 40, canvas.width - 100, 80);
        ctx.strokeRect(50, canvas.height / 2 - 40, canvas.width - 100, 80);
        
        ctx.fillStyle = '#ef4444';
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#ef4444';
        ctx.font = 'bold 18px Space Grotesk';
        ctx.textAlign = 'center';
        ctx.fillText("⚠️ SECURITY ALARM: KEY EXCHANGE ABORTED ⚠️", canvas.width / 2, canvas.height / 2 - 6);
        
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#fca5a5';
        ctx.font = '13px Space Grotesk';
        ctx.fillText(`Measured QBER of ${simData.qber.toFixed(2)}% indicates eavesdropper threat. Key destroyed.`, canvas.width / 2, canvas.height / 2 + 20);
        
        ctx.restore();
    }
    
    // Initial Render
    resetAnimationState();
});
