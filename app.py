import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="빨간 모자의 숲속 모험", page_icon="🌲", layout="centered")

st.title("🌲 빨간 모자와 숲속의 미로 대모험 🪓")
st.markdown("""
**🎮 광속 스피드런 벨런스 패치 완로:**
* **폭풍 스피드 (Speed 5.5):** 플레이어의 속도가 극대화되었습니다! 맵 전체를 초고속으로 누비세요.
* **스마트 코너링 보정:** 속도가 너무 빨라 벽에 걸리지 않도록 코너 부근에서 부드럽게 미끄러져 들어가는 자석 시스템을 강화했습니다.
""")

game_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 4px; flex-wrap: wrap;">
            <div id="p-stage" style="padding: 5px 8px; background: #1e293b; color: #f1f5f9; border-radius: 6px; font-weight: bold; font-size: 12px;">🗺️ 1단계 숲속</div>
            <div id="p-mush" style="padding: 5px 8px; background: #065f46; color: #a7f3d0; border-radius: 6px; font-weight: bold; font-size: 12px;">🍄 남은 버섯: 계산중</div>
            <div id="p-kill" style="padding: 5px 8px; background: #7f1d1d; color: #fca5a5; border-radius: 6px; font-weight: bold; font-size: 12px;">🐺 사냥: 0/3</div>
            <div id="p-item" style="padding: 5px 8px; background: #334155; color: #cbd5e1; border-radius: 6px; font-weight: bold; font-size: 12px;">🎒 장비: 없음</div>
        </div>
        <button id="p-reset" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 12px;">🔄 리셋</button>
    </div>
    
    <canvas id="pacmanCanvas" width="440" height="440" style="border-radius: 16px; box-shadow: 0 12px 30px rgba(0,0,0,0.7); background: #0f291e; border: 4px solid #451a03; outline: none;" tabindex="0"></canvas>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const stageUI = document.getElementById('p-stage'); const killUI = document.getElementById('p-kill');
    const mushUI = document.getElementById('p-mush'); const itemUI = document.getElementById('p-item'); 
    const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;

    const forestMap = [
        [1,1,1,1,1,1,1,1,1,5,1,1,1,1,1,1,1,1,1,1],
        [1,8,0,0,1,4,4,4,0,0,0,0,4,4,4,1,0,0,8,1], 
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
        [1,0,0,0,1,4,4,0,0,0,0,0,0,4,4,1,0,0,0,1], 
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
    let hasAxe = false;

    let gearPos = {row: 12, col: 9}; let gunPos = {row: 10, col: 10}; let keyPos = {row: 10, col: 9};

    // ⚡ 플레이어 속도를 초고속 5.5로 상향!
    let redHat = { x: 1 * TILE_SIZE, y: 18 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 5.5 };
    let wolves = [];
    let scaredTimer = 0;

    let axeSpawnTimer = 0;
    const AXE_RESPAWN_DELAY = 260; 
    let activeAxes = []; 

    function initForestGrid() {
        grid = JSON.parse(JSON.stringify(forestMap));
        activeAxes = [];
        activeAxes.push({r: 1, c: 1}, {r: 1, c: 18});
        
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (grid[r][c] === 0) grid[r][c] = 2; 
            }
        }
        updateMushCount();
    }

    function updateMushCount() {
        if (currentStage === 2) { mushUI.innerHTML = "🌊 심해 탐사중"; return 0; }
        let count = 0;
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) { if (grid[r][c] === 2) count++; }
        }
        if (count === 0) {
            mushUI.innerHTML = "🍄 버섯 완판! 우물 개방"; mushUI.style.background = "#2563eb";
        } else {
            mushUI.innerHTML = `🍄 남은 버섯: ${count}개`; mushUI.style.background = "#065f46";
        }
        return count;
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

    function checkWall(x, y) {
        if (x < 0 || x + TILE_SIZE > canvas.width || y < 0 || y + TILE_SIZE > canvas.height) return true;
        let left = Math.floor(x / TILE_SIZE); let right = Math.floor((x + TILE_SIZE - 0.1) / TILE_SIZE);
        let top = Math.floor(y / TILE_SIZE); let bottom = Math.floor((y + TILE_SIZE - 0.1) / TILE_SIZE);
        
        let tiles = [grid[top][left], grid[top][right], grid[bottom][left], grid[bottom][right]];
        for(let t of tiles) {
            if (t === 1 || t === 6) return true;
            if (t === 5 && !(currentStage === 3 && wolves.every(w => w.dead))) return true;
        }
        return false;
    }

    function update() {
        if (gameOver || gameWin) return;

        if (scaredTimer > 0 && !hasGun && currentStage !== 3) {
            scaredTimer--; 
            if (scaredTimer === 0) { wolves.forEach(w => w.scared = false); hasAxe = false; }
        }

        if (currentStage === 1) {
            axeSpawnTimer++;
            if (axeSpawnTimer >= AXE_RESPAWN_DELAY) {
                axeSpawnTimer = 0;
                if (!activeAxes.some(a => a.r === 1 && a.c === 1)) activeAxes.push({r: 1, c: 1});
                if (!activeAxes.some(a => a.r === 1 && a.c === 18)) activeAxes.push({r: 1, c: 18});
            }
        }

        // 고속 이동 시 벽에 박히지 않도록 허용 오차(Magnet 범위)를 대폭 완화
        let remX = redHat.x % TILE_SIZE;
        let remY = redHat.y % TILE_SIZE;

        if (redHat.nextDirX !== 0 || redHat.nextDirY !== 0) {
            if (redHat.nextDirX !== redHat.dirX || redHat.nextDirY !== redHat.dirY) {
                // 초고속 이동 중에도 반격자(rem) 오차가 속도 이내라면 강제로 축을 맞춰서 부드럽게 흡입 처리
                if ((redHat.nextDirX !== 0 && (remY <= redHat.speed || TILE_SIZE - remY <= redHat.speed)) || 
                    (redHat.nextDirY !== 0 && (remX <= redHat.speed || TILE_SIZE - remX <= redHat.speed))) {
                    let checkX = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE;
                    let checkY = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE;
                    if (!checkWall(checkX + redHat.nextDirX * TILE_SIZE, checkY + redHat.nextDirY * TILE_SIZE)) {
                        redHat.x = checkX; redHat.y = checkY;
                        redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
                    }
                }
            }
        }

        let nextX = redHat.x + redHat.dirX * redHat.speed;
        let nextY = redHat.y + redHat.dirY * redHat.speed;
        
        if (!checkWall(nextX, nextY)) {
            redHat.x = nextX; redHat.y = nextY;
        } else {
            redHat.x = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE;
            redHat.y = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE;
            redHat.dirX = 0; redHat.dirY = 0;
        }

        let leftCol = Math.floor(redHat.x / TILE_SIZE);
        let rightCol = Math.floor((redHat.x + TILE_SIZE - 1) / TILE_SIZE);
        let topRow = Math.floor(redHat.y / TILE_SIZE);
        let botRow = Math.floor((redHat.y + TILE_SIZE - 1) / TILE_SIZE);

        let activeTiles = [
            {r: topRow, c: leftCol}, {r: topRow, c: rightCol},
            {r: botRow, c: leftCol}, {r: botRow, c: rightCol}
        ];

        activeTiles.forEach(pt => {
            if (pt.r >= 0 && pt.r < ROWS && pt.c >= 0 && pt.c < COLS) {
                if (grid[pt.r][pt.c] === 2 || grid[pt.r][pt.c] === 7) {
                    grid[pt.r][pt.c] = 0; updateMushCount();
                }
                
                let axeIndex = activeAxes.findIndex(a => a.r === pt.r && a.c === pt.c);
                if (axeIndex !== -1) {
                    activeAxes.splice(axeIndex, 1);
                    if (!hasGun && currentStage === 1) { 
                        scaredTimer = 240; 
                        hasAxe = true; 
                        wolves.forEach(w => w.scared = true); 
                    }
                }
                
                if (currentStage === 1 && gearSpawned && !hasAquaGear && pt.r === gearPos.row && pt.c === gearPos.col) {
                    hasAquaGear = true; itemUI.innerHTML = "🎒 장비: 🤿 수영장비"; itemUI.style.background = "#2563eb";
                }

                if (currentStage === 1 && hasAquaGear && updateMushCount() === 0) {
                    if (forestMap[pt.r][pt.c] === 4) {
                        currentStage = 2; grid = JSON.parse(JSON.stringify(aquaMap));
                        canvas.style.background = "#07243a";
                        stageUI.innerHTML = "🗺️ 2단계 푸른 심해"; stageUI.style.background = "#0284c7";
                        killUI.innerHTML = "🦈 수중 처치: 0/3"; updateMushCount(); resetPositions(); return;
                    }
                }

                if (currentStage === 2 && !hasGun && pt.r === gunPos.row && pt.c === gunPos.col) {
                    hasGun = true; wolves.forEach(w => w.scared = true);
                    itemUI.innerHTML = "🎒 장비: 🤿 + 🔫 사냥꾼의 총"; itemUI.style.background = "#dc2626";
                }

                if (currentStage === 2 && keySpawned && !hasKey && pt.r === keyPos.row && pt.c === keyPos.col) {
                    hasKey = true; currentStage = 3; grid = JSON.parse(JSON.stringify(forestMap)); 
                    canvas.style.background = "#0f291e";
                    stageUI.innerHTML = "🗺️ 3단계 최종전"; stageUI.style.background = "#b45309";
                    killUI.innerHTML = "🐺 남은 늑대 소탕!"; resetPositions();
                    wolves.forEach(w => { w.dead = false; w.scared = true; }); return;
                }
                if (currentStage === 3 && forestMap[pt.r][pt.c] === 5) { if (wolves.every(w => w.dead)) gameWin = true; }
            }
        });

        wolves.forEach(w => {
            if (w.dead) return;
            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0) {
                let validDirs = []; let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                dirs.forEach(d => {
                    if (!checkWall(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) {
                        let nC = Math.floor((w.x + d.x * TILE_SIZE)/TILE_SIZE); let nR = Math.floor((w.y + d.y * TILE_SIZE)/TILE_SIZE);
                        if (grid[nR][nC] !== 5 && (d.x !== -w.dirX || d.y !== -w.dirY)) validDirs.push(d);
                    }
                });
                if (validDirs.length === 0) { dirs.forEach(d => { if (!checkWall(w.x+d.x*TILE_SIZE, w.y+d.y*TILE_SIZE)) validDirs.push(d); }); }

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

            // 플레이어 속도가 압도적이므로 추격 난이도를 위해 늑대 속도도 살짝 상향 (2.5)
            let spd = 2.5; 
            let nWpX = w.x + w.dirX * spd; let nWpY = w.y + w.dirY * spd;
            if (!checkWall(nWpX, nWpY)) { w.x = nWpX; w.y = nWpY; }
            else { w.x = Math.round(w.x/TILE_SIZE)*TILE_SIZE; w.y = Math.round(w.y/TILE_SIZE)*TILE_SIZE; w.dirX = -w.dirX; w.dirY = -w.dirY; }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared || hasGun || currentStage === 3) {
                    w.dead = true; w.x = -999; w.y = -999; 
                    if (currentStage === 1) {
                        forestKills++; killUI.innerHTML = `🐺 늑대 사냥: ${forestKills}/3`;
                        w.dead = false; w.x = 2*TILE_SIZE; w.y = 1*TILE_SIZE; 
                        if (forestKills === 3) { gearSpawned = true; itemUI.innerHTML = "🎒 장비: 🤿 수영장비 출현!"; }
                    } else if (currentStage === 2) {
                        waterKills++; killUI.innerHTML = `🦈 수중 처치: ${waterKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 10*TILE_SIZE; 
                        if (waterKills === 3) { keySpawned = true; itemUI.innerHTML = "🎒 장비: 🔑 탈출 열쇠 출현!"; }
                    } else if (currentStage === 3) {
                        let remaining = wolves.filter(wolf => !wolf.dead).length;
                        if (remaining === 0) killUI.innerHTML = "🏡 할머니 집으로 복귀 가능!";
                        else killUI.innerHTML = `🐺 남은 늑대 수: ${remaining}마리`;
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
        ctx.shadowBlur = 6; ctx.shadowOffsetX = 3; ctx.shadowOffsetY = 3;

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (currentStage === 1 || currentStage === 3) {
                    if (forestMap[r][c] === 1) {
                        ctx.shadowColor = 'rgba(0,0,0,0.5)';
                        let wallGrad = ctx.createLinearGradient(x, y, x, y + TILE_SIZE);
                        wallGrad.addColorStop(0, '#065f46'); wallGrad.addColorStop(1, '#022c22');
                        ctx.fillStyle = wallGrad; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#10b981'; ctx.fillRect(x, y, TILE_SIZE, 2); 
                    } else if (forestMap[r][c] === 8) {
                        ctx.shadowColor = 'rgba(0,0,0,0.4)';
                        ctx.fillStyle = '#475569'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#94a3b8'; ctx.fillRect(x+1, y+1, TILE_SIZE-2, 2); 
                    } else if (forestMap[r][c] === 4) {
                        ctx.shadowColor = 'rgba(0,0,0,0.3)';
                        ctx.fillStyle = '#1d4ed8'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#3b82f6'; ctx.fillRect(x+2, y+2, TILE_SIZE-4, TILE_SIZE-4);
                    } else if (forestMap[r][c] === 5) {
                        ctx.shadowColor = 'transparent'; ctx.font = '15px Arial'; ctx.fillText('🏡', x+3, y+16); 
                    }
                    
                    if (grid[r][c] === 2) {
                        ctx.shadowColor = 'transparent'; ctx.font = '12px Arial'; ctx.fillText('🍄', x+4, y+16);
                    }
                    if (activeAxes.some(a => a.r === r && a.c === c)) {
                        ctx.shadowColor = 'transparent'; ctx.font = '15px Arial'; ctx.fillText('🪓', x+2, y+17);
                    }
                } else if (currentStage === 2) {
                    if (grid[r][c] === 6) {
                        ctx.shadowColor = 'rgba(0,0,0,0.6)';
                        ctx.fillStyle = '#0f172a'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.fillStyle = '#334155'; ctx.fillRect(x, y, TILE_SIZE, 2);
                    } else if (grid[r][c] === 7) {
                        ctx.shadowColor = 'transparent'; ctx.font = '12px Arial'; ctx.fillText('🌿', x+4, y+16);
                    }
                }
            }
        }

        ctx.shadowColor = 'transparent'; 
        if (currentStage === 1 && gearSpawned && !hasAquaGear) { ctx.font = '16px Arial'; ctx.fillText('🤿', gearPos.col*TILE_SIZE+3, gearPos.row*TILE_SIZE+18); }
        if (currentStage === 2 && !hasGun) { ctx.font = '16px Arial'; ctx.fillText('🔫', gunPos.col*TILE_SIZE+3, gunPos.row*TILE_SIZE+18); }
        if (currentStage === 2 && keySpawned && !hasKey) { ctx.font = '16px Arial'; ctx.fillText('🔑', keyPos.col*TILE_SIZE+3, keyPos.row*TILE_SIZE+18); }

        ctx.shadowBlur = 4; ctx.shadowColor = 'rgba(0,0,0,0.4)';
        let px = redHat.x + TILE_SIZE/2; let py = redHat.y + TILE_SIZE/2;
        ctx.save();
        ctx.beginPath(); ctx.arc(px, py, 8, 0, Math.PI*2);
        ctx.fillStyle = (hasGun || currentStage === 3) ? '#facc15' : (scaredTimer > 0 ? '#fb923c' : '#dc2626');
        ctx.fill();
        ctx.beginPath(); ctx.arc(px, py+2, 5, 0, Math.PI*2); ctx.fillStyle = '#fed7aa'; ctx.fill();
        
        if (hasAxe && currentStage === 1) { 
            ctx.font = '12px Arial'; ctx.fillText('🪓', px - 11, py - 3); 
        } else if (hasAquaGear) { 
            ctx.font = '10px Arial'; ctx.fillText('🤿', px + 3, py - 3); 
        }
        if (hasGun) { ctx.font = '10px Arial'; ctx.fillText('🔫', px - 9, py + 5); }
        ctx.restore();

        wolves.forEach(w => {
            if (w.dead) return;
            let wx = w.x + TILE_SIZE/2; let wy = w.y + TILE_SIZE/2;
            ctx.save();
            if (w.scared || hasGun || currentStage === 3) { ctx.font = '17px Arial'; ctx.fillText('🥶', wx-8, wy+6); } 
            else { ctx.font = '16px Arial'; ctx.fillText(currentStage === 2 ? '🦈' : '🐺', wx-8, wy+6); }
            ctx.restore();
        });

        ctx.shadowBlur = 0; 
        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 30px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2);
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(15,23,42,0.95)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 26px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('👑 HAPPY ENDING 👑', canvas.width/2, canvas.height/2 - 25);
            ctx.fillStyle = '#fff'; ctx.font = '14px sans-serif'; ctx.fillText('초고속 스피드런 성공!', canvas.width/2, canvas.height/2 + 20);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        currentStage = 1; gameOver = false; gameWin = false; forestKills = 0; waterKills = 0;
        hasAquaGear = false; gearSpawned = false; hasGun = false; hasKey = false; keySpawned = false; hasAxe = false; scaredTimer = 0; axeSpawnTimer = 0;
        canvas.style.background = "#0f291e";
        stageUI.innerHTML = "🗺️ 1단계 숲속 미로"; stageUI.style.background = "#1e293b";
        killUI.innerHTML = "🐺 늑대 사냥: 0/3";
        itemUI.innerHTML = "🎒 장비: 없음"; itemUI.style.background = "#334155";
        initForestGrid(); resetPositions(); canvas.focus();
    });

    initForestGrid(); resetPositions();
    setTimeout(() => { canvas.focus(); }, 300);
    loop();
</script>
"""

components.html(game_js, height=520)
