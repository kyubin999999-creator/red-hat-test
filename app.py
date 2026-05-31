import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="잔혹동화: 빨간 모자의 역습", page_icon="🪓", layout="centered")

st.title("🌲 잔혹동화: 빨간 모자와 숲속의 늑대들 🪓")
st.markdown("""
**🩸 잔혹동화의 본질에 눈을 뜨다:**
* 숲속의 **버섯(🍄)**을 삼킬 때마다 빨간 모자의 증오가 심해지며 화면이 피로 물들고 진동합니다.
* **복수의 도끼(🪓)**를 쥐는 순간, 공포의 추격전은 피의 숙청으로 뒤바뀝니다.
""")

game_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <div id="p-stage" style="padding: 6px 10px; background: #111827; color: #f3f4f6; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #374151;">🗺️ 잔혹한 잔영: 1단계 숲속</div>
            <div id="p-kill" style="padding: 6px 10px; background: #7f1d1d; color: #fca5a5; border-radius: 6px; font-weight: bold; font-size: 13px;">🪓 처단한 늑대: 0/3</div>
            <div id="p-item" style="padding: 6px 10px; background: #374151; color: #9ca3af; border-radius: 6px; font-weight: bold; font-size: 13px;">🎒 유품: 없음</div>
        </div>
        <button id="p-reset" style="padding: 6px 12px; background: #b91c1c; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; box-shadow: 0 2px 8px rgba(0,0,0,0.4);">🔄 회귀</button>
    </div>
    
    <div id="canvasContainer" style="position: relative; width: 440px; height: 440px; margin: 0 auto; overflow: hidden; border-radius: 16px;">
        <canvas id="pacmanCanvas" width="440" height="440" style="background: #14532d; border: 4px solid #451a03; outline: none;" tabindex="0"></canvas>
    </div>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const container = document.getElementById('canvasContainer');
    const stageUI = document.getElementById('p-stage'); const killUI = document.getElementById('p-kill');
    const itemUI = document.getElementById('p-item'); const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;

    // 1: 어두운 깊은 숲 벽, 0: 이끼 낀 길
    const forestMap = [
        [1,1,1,1,1,1,1,1,1,5,1,1,1,1,1,1,1,1,1,1],
        [1,3,0,0,1,4,4,4,0,0,0,0,4,4,4,1,0,0,3,1],
        [1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,4,4,4,1,1,4,4,4,1,1,1,1,0,1],
        [1,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,1],
        [1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1],
        [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
        [1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1],
        [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
        [4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4], 
        [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
        [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
        [1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1],
        [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,3,0,0,1,4,4,0,0,0,0,0,0,4,4,1,0,0,3,1], 
        [1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    const aquaMap = [
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
        [6,7,7,7,6,0,0,0,7,6,6,7,0,0,0,6,7,7,7,6],
        [6,7,6,7,6,6,6,6,7,6,6,7,6,6,6,6,7,6,7,6],
        [6,7,6,7,7,7,7,7,7,0,0,7,7,7,7,7,7,6,7,6],
        [6,7,6,6,6,6,0,0,0,6,6,0,0,0,6,6,6,6,7,6],
        [6,7,7,7,7,6,6,6,7,6,6,7,6,6,6,7,7,7,7,6],
        [6,6,6,6,7,6,7,7,7,7,7,7,7,7,6,7,6,6,6,6],
        [6,6,6,6,7,6,7,6,6,6,6,6,6,7,6,7,6,6,6,6],
        [6,6,6,6,7,0,7,6,6,6,6,6,6,7,0,7,6,6,6,6],
        [6,6,6,6,7,6,7,6,6,6,6,6,6,7,6,7,6,6,6,6],
        [0,0,0,0,7,0,7,0,0,0,0,0,0,7,0,7,0,0,0,0], 
        [6,6,6,6,7,6,7,6,6,6,6,6,6,7,6,7,6,6,6,6],
        [6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6],
        [6,7,7,7,7,6,6,6,6,6,6,6,6,6,6,7,7,7,7,6],
        [6,7,6,6,7,7,7,7,7,7,7,7,7,7,7,7,6,6,7,6],
        [6,7,6,6,6,6,7,6,6,6,6,6,6,7,6,6,6,6,7,6],
        [6,7,7,7,6,0,0,7,7,0,0,7,7,0,0,6,7,7,7,6],
        [6,7,6,7,6,6,6,6,7,6,6,7,6,6,6,6,7,6,7,6],
        [6,7,7,7,7,7,7,7,7,6,6,7,7,7,7,7,7,7,7,6],
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
    ];

    let currentStage = 1; let grid = [];
    let gameOver = false; let gameWin = false;

    let forestKills = 0; let waterKills = 0;
    let hasAquaGear = false; let gearSpawned = false;
    let hasGun = false; let hasKey = false; let keySpawned = false;

    let gearPos = {row: 12, col: 9}; let gunPos = {row: 10, col: 10}; let keyPos = {row: 10, col: 9};

    let redHat = { x: 1 * TILE_SIZE, y: 18 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 2 };
    let wolves = [];
    
    // 이펙트 연출용 변수
    let scaredTimer = 0;
    let flashTimer = 0;      // 독버섯 섭취 시 화면 붉은 플래시 타임
    let shakeTimer = 0;      // 화면 진동 타임
    let particles = [];      // 늑대 처치 파편 이펙트

    function initForestGrid() {
        grid = JSON.parse(JSON.stringify(forestMap));
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (grid[r][c] === 0) grid[r][c] = 2; 
            }
        }
    }

    window.addEventListener('keydown', e => {
        if([37, 38, 39, 40].indexOf(e.keyCode) > -1) { e.preventDefault(); canvas.focus(); }
    }, {passive: false});

    canvas.addEventListener('keydown', e => {
        if(e.keyCode === 37) { redHat.nextDirX = -1; redHat.nextDirY = 0; }
        if(e.keyCode === 39) { redHat.nextDirX = 1; redHat.nextDirY = 0; }
        if(e.keyCode === 38) { redHat.nextDirX = 0; redHat.nextDirY = -1; }
        if(e.keyCode === 40) { redHat.nextDirX = 0; redHat.nextDirY = 1; }
    });

    function isColliding(x, y) {
        if (x < 0 || x + TILE_SIZE > canvas.width || y < 0 || y + TILE_SIZE > canvas.height) return true;
        let left = Math.floor(x / TILE_SIZE); let right = Math.floor((x + TILE_SIZE - 1) / TILE_SIZE);
        let top = Math.floor(y / TILE_SIZE); let bottom = Math.floor((y + TILE_SIZE - 1) / TILE_SIZE);
        let checkPoints = [{r: top, c: left}, {r: top, c: right}, {r: bottom, c: left}, {r: bottom, c: right}];
        for (let pt of checkPoints) {
            let tile = grid[pt.r][pt.c];
            if (tile === 1 || tile === 6) return true; 
            if (tile === 4 && !hasAquaGear && currentStage === 1) return true; 
            if (tile === 5) { if (currentStage === 3 && wolves.every(w => w.dead)) return false; return true; }
        }
        return false;
    }

    // 🩸 처치 파편 생성 함수
    function spawnParticles(x, y, color) {
        for(let i=0; i<15; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4,
                radius: Math.random() * 3 + 1,
                alpha: 1,
                color: color
            });
        }
    }

    function update() {
        if (gameOver || gameWin) return;

        // 이펙트 타이머 업데이트
        if (scaredTimer > 0 && !hasGun && currentStage !== 3) {
            scaredTimer--; if (scaredTimer === 0) wolves.forEach(w => w.scared = false);
        }
        if (flashTimer > 0) flashTimer--;
        if (shakeTimer > 0) shakeTimer--;

        // 파편 업데이트
        particles.forEach((p, index) => {
            p.x += p.vx; p.y += p.vy; p.alpha -= 0.04;
            if(p.alpha <= 0) particles.splice(index, 1);
        });

        if (redHat.x % TILE_SIZE === 0 && redHat.y % TILE_SIZE === 0) {
            if (!isColliding(redHat.x + redHat.nextDirX * TILE_SIZE, redHat.y + redHat.nextDirY * TILE_SIZE)) {
                redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
            }
        }

        let nextX = redHat.x + redHat.dirX * redHat.speed; let nextY = redHat.y + redHat.dirY * redHat.speed;
        if (!isColliding(nextX, nextY)) { redHat.x = nextX; redHat.y = nextY; }
        else { redHat.x = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE; redHat.y = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE; }

        let currCol = Math.floor((redHat.x + TILE_SIZE/2) / TILE_SIZE);
        let currRow = Math.floor((redHat.y + TILE_SIZE/2) / TILE_SIZE);

        if (currCol >= 0 && currCol < COLS && currRow >= 0 && currRow < ROWS) {
            // 🩸 버섯 획득 시: 환각/진동 연출 발동!
            if (grid[currRow][currCol] === 2 || grid[currRow][currCol] === 7) {
                grid[currRow][currCol] = 0;
                flashTimer = 6; shakeTimer = 8; // 환각 연출 트리거
            }
            
            // 🪓 도끼 대용 (원래 3번 블록) 얻었을 때
            if (grid[currRow][currCol] === 3) {
                grid[currRow][currCol] = 0;
                flashTimer = 15; shakeTimer = 15;
                if (!hasGun && currentStage === 1) { scaredTimer = 260; wolves.forEach(w => w.scared = true); }
            }
            
            if (currentStage === 1 && gearSpawned && !hasAquaGear && currRow === gearPos.row && currCol === gearPos.col) {
                hasAquaGear = true; itemUI.innerHTML = "🎒 유품: 🤿 수영장비"; itemUI.style.background = "#1d4ed8";
            }

            if (currentStage === 1 && hasAquaGear && forestMap[currRow][currCol] === 4) {
                currentStage = 2; grid = JSON.parse(JSON.stringify(aquaMap));
                canvas.style.background = "#0c4a6e"; 
                stageUI.innerHTML = "🗺️ 잔혹한 잔영: 2단계 심해"; stageUI.style.background = "#0369a1";
                killUI.innerHTML = "🦈 심해 수축: 0/3"; resetPositions(); return;
            }

            if (currentStage === 2 && !hasGun && currRow === gunPos.row && currCol === gunPos.col) {
                hasGun = true; wolves.forEach(w => w.scared = true);
                itemUI.innerHTML = "🎒 유품: 🤿 + 🔫 사냥꾼의 총"; itemUI.style.background = "#991b1b";
            }

            if (currentStage === 2 && keySpawned && !hasKey && currRow === keyPos.row && currCol === keyPos.col) {
                hasKey = true; currentStage = 3; grid = JSON.parse(JSON.stringify(forestMap)); 
                canvas.style.background = "#14532d";
                stageUI.innerHTML = "🗺️ 잔혹한 잔영: 3단계 도살장"; stageUI.style.background = "#7f1d1d";
                killUI.innerHTML = "🐺 남은 늑대 도살!"; resetPositions();
                wolves.forEach(w => { w.dead = false; w.scared = true; }); return;
            }

            if (currentStage === 3 && forestMap[currRow][currCol] === 5) {
                if (wolves.every(w => w.dead)) gameWin = true;
            }
        }

        wolves.forEach(w => {
            if (w.dead) return;
            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0) {
                let validDirs = []; let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                dirs.forEach(d => {
                    if (!isColliding(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) {
                        let nC = Math.floor((w.x + d.x * TILE_SIZE)/TILE_SIZE); let nR = Math.floor((w.y + d.y * TILE_SIZE)/TILE_SIZE);
                        if (grid[nR][nC] !== 5 && (d.x !== -w.dirX || d.y !== -w.dirY)) validDirs.push(d);
                    }
                });
                if (validDirs.length === 0) { dirs.forEach(d => { if (!isColliding(w.x+d.x*TILE_SIZE, w.y+d.y*TILE_SIZE)) validDirs.push(d); }); }

                if (validDirs.length > 0) {
                    let bestDir = validDirs[0]; let minTargetDist = 999999;
                    validDirs.forEach(d => {
                        let nextWcX = w.x + d.x * TILE_SIZE; let nextWcY = w.y + d.y * TILE_SIZE;
                        let dist = Math.pow(nextWcX - redHat.x, 2) + Math.pow(nextWcY - redHat.y, 2);
                        if (w.scared || hasGun || currentStage === 3) { if (dist > minTargetDist || minTargetDist === 999999) { minTargetDist = dist; bestDir = d; } }
                        else { if (dist < minTargetDist) { minTargetDist = dist; bestDir = d; } }
                    });
                    w.dirX = bestDir.x; w.dirY = bestDir.y;
                    if(Math.random() < 0.15) { let chosen = validDirs[Math.floor(Math.random() * validDirs.length)]; w.dirX = chosen.x; w.dirY = chosen.y; }
                } else { w.dirX = -w.dirX; w.dirY = -w.dirY; }
            }

            let spd = 2.0; let nWpX = w.x + w.dirX * spd; let nWpY = w.y + w.dirY * spd;
            if (!isColliding(nWpX, nWpY)) { w.x = nWpX; w.y = nWpY; }
            else { w.x = Math.round(w.x/TILE_SIZE)*TILE_SIZE; w.y = Math.round(w.y/TILE_SIZE)*TILE_SIZE; w.dirX = -w.dirX; w.dirY = -w.dirY; }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared || hasGun || currentStage === 3) {
                    // 🩸 처벌 완료: 선혈 이펙트 유발
                    spawnParticles(w.x + TILE_SIZE/2, w.y + TILE_SIZE/2, '#dc2626');
                    shakeTimer = 12;
                    w.dead = true; w.x = -999; w.y = -999; 
                    
                    if (currentStage === 1) {
                        forestKills++; killUI.innerHTML = `🪓 처단한 늑대: ${forestKills}/3`;
                        w.dead = false; w.x = 2*TILE_SIZE; w.y = 1*TILE_SIZE; 
                        if (forestKills === 3) { gearSpawned = true; itemUI.innerHTML = "🎒 유품: 🤿 발견됨"; }
                    } else if (currentStage === 2) {
                        waterKills++; killUI.innerHTML = `🦈 심해 수축: ${waterKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 10*TILE_SIZE; 
                        if (waterKills === 3) { keySpawned = true; itemUI.innerHTML = "🎒 유품: 🔑 발견됨"; }
                    } else if (currentStage === 3) {
                        let remaining = wolves.filter(wolf => !wolf.dead).length;
                        if (remaining === 0) killUI.innerHTML = "🏡 문이 열렸다. 할머니 집으로.";
                        else killUI.innerHTML = `🐺 남은 해충: ${remaining}마리`;
                    }
                } else { gameOver = true; }
            }
        });
    }

    function resetPositions() {
        redHat.x = 1 * TILE_SIZE; redHat.y = 18 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves = [
            { x: 2 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: 1, dirY: 0, scared: (currentStage===3||hasGun), dead: false },
            { x: 17 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: -1, dirY: 0, scared: (currentStage===3||hasGun), dead: false },
            { x: 8 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: 1, dirY: 0, scared: (currentStage===3||hasGun), dead: false }
        ];
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.save();
        // 💡 화면 진동 연출 반영
        if (shakeTimer > 0) {
            let dx = (Math.random() - 0.5) * 5; let dy = (Math.random() - 0.5) * 5;
            ctx.translate(dx, dy);
        }

        // 🗺️ 맵 입체 그래픽 드로잉
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (currentStage === 1 || currentStage === 3) {
                    if (forestMap[r][c] === 1) {
                        // 🌲 벽 3D 입체화: 어두운 그림자 베이스에 상단 테두리 드로잉
                        ctx.fillStyle = '#022c22'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#065f46'; ctx.fillRect(x, y, TILE_SIZE, 3); // 상단 라이팅
                        ctx.fillStyle = '#044e3a'; ctx.fillRect(x, y+TILE_SIZE-3, TILE_SIZE, 3); // 하단 섀도우
                    } else if (forestMap[r][c] === 4) {
                        ctx.fillStyle = '#1e3a8a'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE); 
                    } else if (forestMap[r][c] === 5) {
                        ctx.font = '15px Arial'; ctx.fillText('🏡', x+3, y+16); 
                    } else if (forestMap[r][c] === 3 && grid[r][c] === 3) {
                        ctx.font = '15px Arial'; ctx.fillText('🪓', x+2, y+17); // 별 대신 도끼 배치
                    }
                    if (grid[r][c] === 2) {
                        // 독버섯 디테일 강조
                        ctx.font = '13px Arial'; ctx.fillText('🍄', x+4, y+16);
                    }
                } else if (currentStage === 2) {
                    if (grid[r][c] === 6) {
                        ctx.fillStyle = '#020617'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#1e293b'; ctx.fillRect(x, y, TILE_SIZE, 2);
                    } else if (grid[r][c] === 7) {
                        ctx.font = '12px Arial'; ctx.fillText('🌿', x+4, y+16);
                    }
                }
            }
        }

        if (currentStage === 1 && gearSpawned && !hasAquaGear) { ctx.font = '16px Arial'; ctx.fillText('🤿', gearPos.col*TILE_SIZE+3, gearPos.row*TILE_SIZE+18); }
        if (currentStage === 2 && !hasGun) { ctx.font = '16px Arial'; ctx.fillText('🔫', gunPos.col*TILE_SIZE+3, gunPos.row*TILE_SIZE+18); }
        if (currentStage === 2 && keySpawned && !hasKey) { ctx.font = '16px Arial'; ctx.fillText('🔑', keyPos.col*TILE_SIZE+3, keyPos.row*TILE_SIZE+18); }

        // 👥 캐릭터 밑 그림자 연출
        let drawShadow = (cx, cy) => {
            ctx.beginPath(); ctx.ellipse(cx, cy + 8, 7, 3, 0, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0, 0, 0, 0.4)'; ctx.fill();
        };

        // 빨간 모자 렌더링
        let px = redHat.x + TILE_SIZE/2; let py = redHat.y + TILE_SIZE/2;
        drawShadow(px, py);
        
        // 도끼 버프 상태일 때 광기 오라 연출
        if (scaredTimer > 0 || hasGun || currentStage === 3) {
            ctx.beginPath(); ctx.arc(px, py, 11, 0, Math.PI*2);
            ctx.fillStyle = 'rgba(220, 38, 38, 0.35)'; ctx.fill();
        }

        ctx.save();
        ctx.beginPath(); ctx.arc(px, py, 8, 0, Math.PI*2);
        ctx.fillStyle = (hasGun || currentStage === 3) ? '#b91c1c' : (scaredTimer > 0 ? '#ea580c' : '#dc2626');
        ctx.fill();
        ctx.beginPath(); ctx.arc(px, py+2, 5, 0, Math.PI*2); ctx.fillStyle = '#fed7aa'; ctx.fill();
        if(hasAquaGear) { ctx.font = '10px Arial'; ctx.fillText('🤿', px+3, py-3); }
        if(hasGun) { ctx.font = '10px Arial'; ctx.fillText('🔫', px-9, py+5); }
        ctx.restore();

        // 늑대들 렌더링
        wolves.forEach(w => {
            if (w.dead) return;
            let wx = w.x + TILE_SIZE/2; let wy = w.y + TILE_SIZE/2;
            drawShadow(wx, wy);
            ctx.save();
            if (w.scared || hasGun || currentStage === 3) {
                ctx.font = '17px Arial'; ctx.fillText('😭', wx-8, wy+6); // 공포에 질려 우는 연출
            } else {
                ctx.font = '16px Arial'; ctx.fillText(currentStage === 2 ? '🦈' : '🐺', wx-8, wy+6);
            }
            ctx.restore();
        });

        // 💥 선혈/처단 파편 이펙트 드로잉
        particles.forEach(p => {
            ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
        });

        ctx.restore(); // 진동 트랜스레이트 해제

        // 🩸 독버섯 섭취 시 화면 환각 플래시 렌더링
        if (flashTimer > 0) {
            ctx.fillStyle = `rgba(220, 38, 38, ${flashTimer * 0.06})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.9)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 28px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('포식당했습니다.', canvas.width/2, canvas.height/2);
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(10, 10, 10, 0.96)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 24px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('🩸 잔혹동화: 복수의 종결 🩸', canvas.width/2, canvas.height/2 - 20);
            ctx.fillStyle = '#9ca3af'; ctx.font = '13px sans-serif'; ctx.fillText('늑대들의 가죽을 벗기고 할머니의 안식을 찾았습니다.', canvas.width/2, canvas.height/2 + 20);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        currentStage = 1; gameOver = false; gameWin = false; forestKills = 0; waterKills = 0;
        hasAquaGear = false; gearSpawned = false; hasGun = false; hasKey = false; keySpawned = false; scaredTimer = 0;
        flashTimer = 0; shakeTimer = 0; particles = [];
        canvas.style.background = "#14532d";
        stageUI.innerHTML = "🗺️ 구역: 1단계 숲속"; stageUI.style.background = "#111827";
        killUI.innerHTML = "🪓 처단한 늑대: 0/3";
        itemUI.innerHTML = "🎒 유품: 없음"; itemUI.style.background = "#374151";
        initForestGrid(); resetPositions(); canvas.focus();
    });

    initForestGrid(); resetPositions();
    setTimeout(() => { canvas.focus(); }, 300);
    loop();
</script>
"""

components.html(game_js, height=520)
