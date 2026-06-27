import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="빨간 모자의 숲속 모험", page_icon="🌲", layout="centered")

st.title("🌲 빨간 모자의 미로 대모험 (늑대 해방 패치) 🪓")
st.markdown("""
**📢 늑대 무죄 판결 및 석방:**
* 늑대들이 벽 속에 갇히지 않도록 초기 소환 위치(Coordinate)를 벽이 없는 **넓은 평지 길 위로 변경**했습니다.
* 이제 게임이 시작되자마자 자유를 얻은 늑대들이 활기차게 돌아다닙니다!
""")

game_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white; width: 570px; margin: 0 auto;">
    <div style="display: flex; flex-direction: column; gap: 8px; width: 560px; margin: 0 auto 12px auto; background: #1e293b; padding: 10px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); box-sizing: border-box;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px;">
            <div id="p-stage" style="padding: 5px 8px; background: #0f172a; color: #f1f5f9; border-radius: 6px; font-weight: bold; font-size: 11px;">🗺️ 1단계 숲속</div>
            <div id="p-mush" style="padding: 5px 8px; background: #d97706; color: white; border-radius: 6px; font-weight: bold; font-size: 11px;">🍄 보유 버섯: 0개</div>
            <div id="p-inventory" style="padding: 5px 8px; background: #059669; color: white; border-radius: 6px; font-weight: bold; font-size: 11px;">🎒 인벤토리: 비어있음</div>
            <div id="p-kill" style="padding: 5px 8px; background: #7f1d1d; color: #fca5a5; border-radius: 6px; font-weight: bold; font-size: 11px;">🐺 사냥: 0/3</div>
        </div>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 4px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 6px; background: #0f172a; padding: 4px 8px; border-radius: 6px;">
                <span style="font-size: 11px; font-weight: bold; color: #cbd5e1;">🏃 속도:</span>
                <input type="range" id="p-speed" min="2" max="6" step="1" value="4" style="width: 80px; cursor: pointer;">
                <span id="p-speed-val" style="font-size: 11px; font-weight: bold; color: #facc15;">4</span>
            </div>
            <div style="display: flex; gap: 4px;">
                <button id="p-god" style="padding: 6px 10px; background: #475569; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 11px;">⚔️ 일반 모드</button>
                <button id="p-reset" style="padding: 6px 10px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 11px;">🔄 리셋</button>
            </div>
        </div>
    </div>
    
    <canvas id="pacmanCanvas" width="560" height="440" style="border-radius: 16px; box-shadow: 0 12px 30px rgba(0,0,0,0.7); background: #143a29; border: 4px solid #451a03; outline: none; display: block; margin: 0 auto;" tabindex="0"></canvas>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const stageUI = document.getElementById('p-stage'); const killUI = document.getElementById('p-kill');
    const mushUI = document.getElementById('p-mush'); const invUI = document.getElementById('p-inventory');
    const godBtn = document.getElementById('p-god'); const resetBtn = document.getElementById('p-reset');
    const speedInput = document.getElementById('p-speed'); const speedVal = document.getElementById('p-speed-val');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20; 
    
    let isGodMode = false; 
    let myMushrooms = 0;
    let currentStage = 1; 
    let gameOver = false; let gameWin = false;

    let forestKills = 0; let waterKills = 0;
    let hasGun = false; let hasKey = false; let keySpawned = false;

    let invAquaGear = false; 
    let invAxeCount = 0;      
    let equipAquaGear = false;
    let equipAxe = false;

    const forestMap = [
        [1,1,1,1,1,1,1,1,1,5,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,4,4,4,0,0,0,0,4,4,4,0,0,0,0,1], 
        [1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,0,4,4,4,1,1,4,4,4,0,0,1,1,0,1],
        [1,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,1],
        [1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
        [1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1],
        [1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1],
        [1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1],
        [4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4], 
        [1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
        [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,1], 
        [1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    const aquaMap = [
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
        [6,7,7,7,0,0,0,0,7,6,6,7,0,0,0,0,7,7,7,6],
        [6,7,6,7,0,0,0,0,7,6,6,7,0,0,0,0,7,6,7,6],
        [6,7,6,7,7,7,7,7,7,0,0,7,7,7,7,7,7,6,7,6],
        [6,7,6,6,0,0,0,0,0,6,6,0,0,0,0,0,6,6,7,6],
        [6,7,7,7,7,6,6,6,7,6,6,7,6,6,6,7,7,7,7,6],
        [6,6,0,6,7,6,7,7,7,7,7,7,7,7,6,7,6,0,6,6],
        [6,6,0,6,7,6,7,6,6,6,6,6,6,7,6,7,6,0,6,6],
        [6,6,0,0,7,0,7,6,6,9,9,6,6,7,0,7,0,0,6,6], 
        [6,6,0,6,7,6,7,6,6,9,9,6,6,7,6,7,6,0,6,6],
        [0,0,0,0,7,0,7,0,0,0,0,0,0,7,0,7,0,0,0,0], 
        [6,6,0,6,7,6,7,6,6,6,6,6,6,7,6,7,6,0,6,6],
        [6,6,0,0,0,0,7,7,7,7,7,7,7,7,0,0,0,0,6,6],
        [6,7,7,7,7,6,6,6,6,6,6,6,6,6,6,7,7,7,7,6],
        [6,7,6,6,7,7,7,7,7,7,7,7,7,7,7,7,6,6,7,6],
        [6,7,6,6,0,0,7,6,6,6,6,6,6,7,0,0,6,6,7,6],
        [6,7,7,7,0,0,0,7,7,0,0,7,7,0,0,0,7,7,7,6],
        [6,7,6,7,0,0,0,0,7,6,6,7,0,0,0,0,7,6,7,6],
        [6,7,7,7,7,7,7,7,7,6,6,7,7,7,7,7,7,7,7,6],
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
    ];

    let grid = [];
    let gunPos = {row: 10, col: 12}; let keyPos = {row: 13, col: 10};

    let redHat = { x: 1 * TILE_SIZE, y: 18 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: parseInt(speedInput.value) };
    let wolves = [];

    function initGrid() {
        grid = JSON.parse(JSON.stringify(currentStage === 2 ? aquaMap : forestMap));
        if (currentStage === 1 || currentStage === 3) {
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) { if (grid[r][c] === 0) grid[r][c] = 2; }
            }
        }
        updateUI();
    }

    function updateUI() {
        mushUI.innerHTML = `🍄 보유 버섯: ${myMushrooms}개`;
        let items = [];
        if (invAquaGear) items.push(equipAquaGear ? "▶🤿수영(ON)◀" : "🤿수영장비");
        if (invAxeCount > 0) items.push(equipAxe ? `▶🪓도끼x${invAxeCount}(ON)◀` : `🪓도끼x${invAxeCount}`);
        if (hasGun) items.push("🔫총");
        if (hasKey) items.push("🔑열쇠");
        
        invUI.innerHTML = `🎒 인벤: ${items.length > 0 ? items.join(", ") : "비어있음"} [1:도끼 2:수영]`;

        if (currentStage === 1) { stageUI.innerHTML = "🗺️ 1단계 숲속"; stageUI.style.background = "#1e293b"; killUI.innerHTML = `🐺 늑대 사냥: ${forestKills}/3`; }
        else if (currentStage === 2) { stageUI.innerHTML = "🗺️ 2단계 푸른 심해"; stageUI.style.background = "#0284c7"; killUI.innerHTML = `🦈 수중 처치: ${waterKills}/3`; }
        else if (currentStage === 3) { stageUI.innerHTML = "🗺️ 3단계 최종전"; stageUI.style.background = "#b45309"; killUI.innerHTML = "🐺 남은 늑대 소탕!"; }
    }

    function spawnMushroomLater(r, c) {
        setTimeout(() => {
            if ((currentStage === 1 || currentStage === 3) && grid[r][c] === 0) { grid[r][c] = 2; }
        }, 1000);
    }

    window.addEventListener('keydown', e => { if([37, 38, 39, 40, 49, 50].indexOf(e.keyCode) > -1) { e.preventDefault(); canvas.focus(); } }, {passive: false});
    
    canvas.addEventListener('keydown', e => {
        if(e.keyCode === 37) { redHat.nextDirX = -1; redHat.nextDirY = 0; }
        if(e.keyCode === 39) { redHat.nextDirX = 1; redHat.nextDirY = 0; }
        if(e.keyCode === 38) { redHat.nextDirX = 0; redHat.nextDirY = -1; }
        if(e.keyCode === 40) { redHat.nextDirX = 0; redHat.nextDirY = 1; }
        
        if(e.keyCode === 49) { if (invAxeCount > 0) { equipAxe = !equipAxe; updateUI(); } }
        if(e.keyCode === 50) { if (invAquaGear) { equipAquaGear = !equipAquaGear; updateUI(); } }
    });

    function checkWall(x, y) {
        if (x < 0 || x + TILE_SIZE > TILE_SIZE * COLS || y < 0 || y + TILE_SIZE > canvas.height) return true;
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

        let remX = redHat.x % TILE_SIZE; let remY = redHat.y % TILE_SIZE;
        if (redHat.nextDirX !== 0 || redHat.nextDirY !== 0) {
            if (redHat.nextDirX !== redHat.dirX || redHat.nextDirY !== redHat.dirY) {
                if ((redHat.nextDirX !== 0 && (remY <= redHat.speed || TILE_SIZE - remY <= redHat.speed)) || 
                    (redHat.nextDirY !== 0 && (remX <= redHat.speed || TILE_SIZE - remX <= redHat.speed))) {
                    let checkX = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE; let checkY = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE;
                    if (!checkWall(checkX + redHat.nextDirX * TILE_SIZE, checkY + redHat.nextDirY * TILE_SIZE)) {
                        redHat.x = checkX; redHat.y = checkY; redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
                    }
                }
            }
        }

        let nextX = redHat.x + redHat.dirX * redHat.speed; let nextY = redHat.y + redHat.dirY * redHat.speed;
        if (!checkWall(nextX, nextY)) { redHat.x = nextX; redHat.y = nextY; } 
        else { redHat.x = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE; redHat.y = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; }

        let pC = Math.floor((redHat.x + TILE_SIZE / 2) / TILE_SIZE);
        let pR = Math.floor((redHat.y + TILE_SIZE / 2) / TILE_SIZE);

        if (pR >= 0 && pR < ROWS && pC >= 0 && pC < COLS) {
            if (grid[pR][pC] === 2) { grid[pR][pC] = 0; myMushrooms++; updateUI(); spawnMushroomLater(pR, pC); }
            if (grid[pR][pC] === 7) { grid[pR][pC] = 0; }

            if (currentStage === 1 && grid[pR][pC] === 4) {
                if (equipAquaGear || isGodMode) {
                    currentStage = 2; canvas.style.background = "#112d42"; 
                    initGrid(); resetPositions(); return;
                }
            }

            if (currentStage === 2 && grid[pR][pC] === 9) {
                currentStage = 1; canvas.style.background = "#143a29"; 
                initGrid(); resetPositions(); return;
            }

            if (currentStage === 2 && !hasGun && pR === gunPos.row && pC === gunPos.col) { hasGun = true; updateUI(); }

            if (currentStage === 2 && keySpawned && !hasKey && pR === keyPos.row && pC === keyPos.col) {
                hasKey = true; currentStage = 3; canvas.style.background = "#143a29";
                initGrid(); resetPositions(); return;
            }

            if (currentStage === 3 && grid[pR][pC] === 5 && wolves.every(w => w.dead)) { gameWin = true; }
        }

        wolves.forEach(w => {
            if (w.dead) return;

            let monsterSpeed = 2;
            let nextWx = w.x + w.dirX * monsterSpeed;
            let nextWy = w.y + w.dirY * monsterSpeed;

            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0 || checkWall(nextWx, nextWy)) {
                w.x = Math.round(w.x / TILE_SIZE) * TILE_SIZE;
                w.y = Math.round(w.y / TILE_SIZE) * TILE_SIZE;

                let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                let validDirs = dirs.filter(d => !checkWall(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE));

                if (validDirs.length > 0) {
                    let bestDir = validDirs[0];
                    let minD = 9999999;
                    let isPlayerStrong = hasGun || (currentStage === 1 && equipAxe && invAxeCount > 0) || currentStage === 3;

                    validDirs.forEach(d => {
                        let nX = w.x + d.x * TILE_SIZE; let nY = w.y + d.y * TILE_SIZE;
                        let dist = Math.pow(nX - redHat.x, 2) + Math.pow(nY - redHat.y, 2);
                        if (isPlayerStrong) { if (dist > minD || minD === 9999999) { minD = dist; bestDir = d; } } 
                        else { if (dist < minD) { minD = dist; bestDir = d; } }
                    });

                    if (checkWall(w.x + bestDir.x * TILE_SIZE, w.y + bestDir.y * TILE_SIZE)) {
                        bestDir = validDirs[Math.floor(Math.random() * validDirs.length)];
                    }

                    w.dirX = bestDir.x; w.dirY = bestDir.y;
                } else {
                    w.dirX = -w.dirX; w.dirY = -w.dirY;
                }
            }

            let finalX = w.x + w.dirX * monsterSpeed;
            let finalY = w.y + w.dirY * monsterSpeed;
            if (!checkWall(finalX, finalY)) { 
                w.x = finalX; w.y = finalY; 
            } else { 
                w.dirX = -w.dirX; w.dirY = -w.dirY; 
            }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                let canKill = isGodMode || hasGun || (currentStage === 1 && equipAxe && invAxeCount > 0) || currentStage === 3;
                
                if (canKill) {
                    if (!isGodMode && !hasGun && currentStage === 1 && equipAxe) {
                        invAxeCount--;
                        if (invAxeCount <= 0) equipAxe = false; 
                    }
                    w.dead = true; w.x = -999; w.y = -999;
                    if (currentStage === 1) {
                        forestKills++; updateUI();
                        if (forestKills < 3) { w.dead = false; w.x = 1*TILE_SIZE; w.y = 1*TILE_SIZE; w.dirX = 1; w.dirY = 0; } // 안전 구역 리스폰
                    } else if (currentStage === 2) {
                        waterKills++; updateUI();
                        if (waterKills < 3) { w.dead = false; w.x = 4*TILE_SIZE; w.y = 1*TILE_SIZE; w.dirX = -1; w.dirY = 0; } // 수중 안전 구역 리스폰
                    } else if (currentStage === 3) {
                        if (wolves.every(wolf => wolf.dead)) updateUI();
                    }
                } else {
                    gameOver = true;
                }
            }
        });
    }

    // 🗺️ [좌표 전면 수정] 벽(1, 6번 타일)이 절대 없는 안전 구역 바닥(0번)으로 스폰 위치 재배치
    function resetPositions() {
        redHat.x = 1 * TILE_SIZE; redHat.y = 18 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves = [
            { x: 1 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: 1, dirY: 0, dead: false },  // 좌측 상단 빈 길목
            { x: 18 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: -1, dirY: 0, dead: false }, // 우측 상단 빈 길목
            { x: 10 * TILE_SIZE, y: 18 * TILE_SIZE, dirX: 0, dirY: -1, dead: false } // 하단 중앙 빈 길목
        ];
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (currentStage === 1 || currentStage === 3) {
                    if (grid[r][c] === 1) {
                        ctx.fillStyle = '#01241a'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE); 
                        ctx.fillStyle = '#065f46'; ctx.fillRect(x, y, TILE_SIZE, 2); 
                    } else {
                        ctx.fillStyle = '#143a29'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        if (grid[r][c] === 4) {
                            ctx.fillStyle = '#1d4ed8'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                            ctx.fillStyle = 'white'; ctx.font = 'bold 9px sans-serif'; ctx.fillText('우물', x+2, y+14);
                        } else if (grid[r][c] === 5) {
                            ctx.font = '15px Arial'; ctx.fillText('🏡', x+3, y+16);
                        }
                        if (grid[r][c] === 2) { ctx.font = '12px Arial'; ctx.fillText('🍄', x+4, y+16); }
                    }
                } else if (currentStage === 2) {
                    if (grid[r][c] === 6) {
                        ctx.fillStyle = '#090d16'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    } else {
                        ctx.fillStyle = '#112d42'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        if (grid[r][c] === 7) {
                            ctx.font = '12px Arial'; ctx.fillText('🌿', x+4, y+16);
                        } else if (grid[r][c] === 9) {
                            ctx.font = '16px Arial'; ctx.fillText('🌀', x+2, y+17);
                        }
                    }
                }
            }
        }

        if (currentStage === 2) {
            if (!hasGun) { ctx.font = '16px Arial'; ctx.fillText('🔫', gunPos.col*TILE_SIZE+3, gunPos.row*TILE_SIZE+18); }
            if (keySpawned && !hasKey) { ctx.font = '16px Arial'; ctx.fillText('🔑', keyPos.col*TILE_SIZE+3, keyPos.row*TILE_SIZE+18); }
        }

        let px = redHat.x + TILE_SIZE/2; let py = redHat.y + TILE_SIZE/2;
        ctx.beginPath(); ctx.arc(px, py, 8, 0, Math.PI*2); ctx.fillStyle = '#facc15'; ctx.fill();
        ctx.beginPath(); ctx.arc(px, py+2, 5, 0, Math.PI*2); ctx.fillStyle = '#ef4444'; ctx.fill();

        if (equipAxe) { ctx.font = '10px Arial'; ctx.fillText('🪓', redHat.x-4, redHat.y+4); }
        if (equipAquaGear) { ctx.font = '10px Arial'; ctx.fillText('🤿', redHat.x+14, redHat.y+4); }

        wolves.forEach(w => {
            if (w.dead) return;
            ctx.font = '16px Arial'; ctx.fillText(currentStage === 2 ? '🦈' : '🐺', w.x+3, w.y+17);
        });

        ctx.fillStyle = '#1e293b'; ctx.fillRect(440, 0, 120, 440);
        ctx.fillStyle = '#334155'; ctx.fillRect(440, 0, 4, 440);

        ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 13px sans-serif'; ctx.fillText('🛒 버섯 상점', 455, 30);
        
        ctx.fillStyle = invAquaGear ? '#475569' : '#0284c7'; ctx.fillRect(450, 60, 100, 45);
        ctx.fillStyle = '#ffffff'; ctx.font = '11px sans-serif'; ctx.fillText('🤿 수영장비', 462, 78);
        ctx.fillStyle = '#facc15'; ctx.fillText('🍄 40개 필요', 466, 95);

        ctx.fillStyle = '#b45309'; ctx.fillRect(450, 120, 100, 45);
        ctx.fillStyle = '#ffffff'; ctx.font = '11px sans-serif'; ctx.fillText('🪓 무기도끼', 462, 138);
        ctx.fillStyle = '#facc15'; ctx.fillText('🍄 20개 필요', 469, 155);

        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('GAME OVER (늑대 충돌)', 280, 220);
            ctx.textAlign = 'start'; 
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(15,23,42,0.95)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 26px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('👑 미션 대성공! 👑', 280, 220);
            ctx.textAlign = 'start';
        }
    }

    if (!canvas.onclick_bound) {
        canvas.addEventListener('click', (e) => {
            let rect = canvas.getBoundingClientRect();
            let clickX = e.clientX - rect.left; let clickY = e.clientY - rect.top;
            
            if (clickX >= 450 && clickX <= 550) {
                if (clickY >= 60 && clickY <= 105 && !invAquaGear && myMushrooms >= 40) {
                    myMushrooms -= 40; invAquaGear = true; updateUI();
                }
                if (clickY >= 120 && clickY <= 165 && myMushrooms >= 20) {
                    myMushrooms -= 20; invAxeCount++; updateUI();
                }
            }
        });
        canvas.onclick_bound = true;
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    speedInput.addEventListener('input', (e) => { let val = parseInt(e.target.value); redHat.speed = val; speedVal.innerHTML = val; });
    godBtn.addEventListener('click', () => { isGodMode = !isGodMode; godBtn.innerHTML = isGodMode ? "🛡️ 무적 ON" : "⚔️ 일반 모드"; godBtn.style.background = isGodMode ? "#2563eb" : "#475569"; canvas.focus(); });
    resetBtn.addEventListener('click', () => {
        currentStage = 1; gameOver = false; gameWin = false; forestKills = 0; waterKills = 0; myMushrooms = 0;
        invAquaGear = false; invAxeCount = 0; equipAquaGear = false; equipAxe = false; hasGun = false; hasKey = false; keySpawned = false;
        canvas.style.background = "#143a29"; initGrid(); resetPositions(); canvas.focus();
    });

    initGrid(); resetPositions();
    setTimeout(() => { canvas.style.background = "#143a29"; canvas.focus(); }, 300);
    loop();
</script>
"""

components.html(game_js, height=580, width=600)
