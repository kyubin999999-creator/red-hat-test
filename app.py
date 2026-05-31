import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 설정 ---
st.set_page_config(page_title="빨간 모자의 역습", page_icon="🔫", layout="centered")

st.title("🌲 빨간 모자의 역습: 사냥꾼의 총과 늑대 소탕 작전 🔫")
st.markdown("""
**🎮 게임 미션:**
1. **숲속 (Stage 1):** 별(⭐)을 먹고 늑대를 **3마리** 잡아 **수영 장비(🤿)**를 얻은 후 물웅덩이(파란 블록)로 돌진하세요!
2. **물속 (Stage 2):** 깊은 곳에 숨겨진 **사냥꾼의 총(🔫)**을 찾으세요. 총을 얻으면 상시 무적이 됩니다! 물속 괴물을 **3마리** 잡고 **열쇠(🔑)**를 얻어 지상으로 복귀하세요!
3. **최종전 (Stage 3):** 지상으로 돌아와 총의 힘으로 늑대들을 **완전히 소탕**하고 할머니 집🏡으로 당당하게 걸어가세요!
""")

# --- 자바스크립트 기반 3단계 완전체 게임 코드 ---
pacman_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <div id="p-stage" style="padding: 6px 10px; background: #14532d; color: #a7f3d0; border-radius: 6px; font-weight: bold; font-size: 13px;">🗺️ 구역: 1단계 숲속 미로</div>
            <div id="p-kill" style="padding: 6px 10px; background: #7f1d1d; color: #fca5a5; border-radius: 6px; font-weight: bold; font-size: 13px;">🐺 숲 늑대 사냥: 0/3</div>
            <div id="p-item" style="padding: 6px 10px; background: #374151; color: #9ca3af; border-radius: 6px; font-weight: bold; font-size: 13px;">🎒 장비: 없음</div>
        </div>
        <button id="p-reset" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px;">🔄 리셋</button>
    </div>
    
    <canvas id="pacmanCanvas" width="440" height="440" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); background: #14532d; border: 4px solid #78350f; outline: none;" tabindex="0"></canvas>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const stageUI = document.getElementById('p-stage'); const killUI = document.getElementById('p-kill');
    const itemUI = document.getElementById('p-item'); const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;
    
    // ⭐ 캐릭터 시작 위치(길)가 벽(1)으로 막히지 않도록 완전히 뚫어놓은 정밀한 안전 맵
    const forestMap = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,3,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,2,1,1,2,2,2,2,2,1,1,2,2,2,2,2,1,1,2,1],
        [1,2,2,2,2,1,1,1,2,2,2,2,1,1,1,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
        [1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,0,0,1,1,0,1,2,1,1,1,1],
        [4,4,4,4,2,0,0,1,0,0,0,0,1,0,0,2,4,4,4,4], 
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [1,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,3,2,1,2,2,2,2,2,0,0,2,2,2,2,2,1,2,3,1], // ◀ 하단 통로와 시작 위치 스폰 지역 안전 확보 완료
        [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
        [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    const aquaMap = [
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
        [6,7,7,7,7,7,7,7,7,0,0,7,7,7,7,7,7,7,7,6],
        [6,7,6,6,7,6,6,6,7,6,6,7,6,6,6,7,6,6,7,6],
        [6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6],
        [6,7,6,6,7,6,7,6,6,6,6,6,6,7,6,7,6,6,7,6],
        [6,7,7,7,7,6,7,7,7,6,6,7,7,7,6,7,7,7,7,6],
        [6,6,6,6,7,6,6,6,0,6,6,0,6,6,6,7,6,6,6,6],
        [0,0,0,6,7,6,0,0,0,0,0,0,0,0,6,7,6,0,0,0],
        [6,6,6,6,7,6,0,6,6,0,0,6,6,0,6,7,6,6,6,6],
        [0,0,0,0,7,0,0,6,0,0,0,0,6,0,0,7,0,0,0,0], 
        [6,6,6,6,7,6,0,6,6,6,6,6,6,0,6,7,6,6,6,6],
        [0,0,0,6,7,6,0,0,0,0,0,0,0,0,6,7,6,0,0,0],
        [6,6,6,6,7,6,0,6,6,6,6,6,6,0,6,7,6,6,6,6],
        [6,7,7,7,7,7,7,7,7,6,6,7,7,7,7,7,7,7,7,6],
        [6,7,6,6,7,6,6,6,7,6,6,7,6,6,6,7,6,6,7,6],
        [6,7,7,6,7,7,7,7,7,0,0,7,7,7,7,7,6,7,7,6],
        [6,6,7,6,7,6,7,6,6,6,6,6,6,7,6,7,6,7,6,6],
        [6,7,7,7,7,6,7,7,7,6,6,7,7,7,6,7,7,7,7,6],
        [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
    ];

    const finalForestMap = JSON.parse(JSON.stringify(forestMap));
    finalForestMap[0][9] = 5; finalForestMap[0][10] = 5; 

    let currentStage = 1; 
    let grid = JSON.parse(JSON.stringify(forestMap));
    let gameOver = false; let gameWin = false;

    let forestKills = 0; let waterKills = 0;
    let hasAquaGear = false; let gearSpawned = false;
    let hasGun = false;
    let hasKey = false; let keySpawned = false;

    let gearPos = {row: 14, col: 9}; 
    let gunPos = {row: 9, col: 10};
    let keyPos = {row: 9, col: 9};

    let redHat = { x: 9 * TILE_SIZE, y: 16 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 2 };
    let wolves = [
        { x: 1 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: 1, dirY: 0, scared: false, dead: false },
        { x: 18 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: -1, dirY: 0, scared: false, dead: false },
        { x: 9 * TILE_SIZE, y: 14 * TILE_SIZE, dirX: 0, dirY: -1, scared: false, dead: false }
    ];

    let scaredTimer = 0;

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
        let left = Math.floor(x / TILE_SIZE); let right = Math.floor((x + TILE_SIZE - 1) / TILE_SIZE);
        let top = Math.floor(y / TILE_SIZE); let bottom = Math.floor((y + TILE_SIZE - 1) / TILE_SIZE);
        
        if(left < 0 || right >= COLS || top < 0 || bottom >= ROWS) return true;

        let blockedTypes = (currentStage === 2) ? [6] : [1];
        if(currentStage === 1 && !hasAquaGear) blockedTypes.push(4); 

        if (blockedTypes.includes(grid[top][left]) || blockedTypes.includes(grid[top][right]) || 
            blockedTypes.includes(grid[bottom][left]) || blockedTypes.includes(grid[bottom][right])) {
            return true;
        }
        return false;
    }

    function update() {
        if (gameOver || gameWin) return;

        if (scaredTimer > 0 && !hasGun) {
            scaredTimer--;
            if (scaredTimer === 0) wolves.forEach(w => w.scared = false);
        }

        if (redHat.x % TILE_SIZE === 0 && redHat.y % TILE_SIZE === 0) {
            if (!isColliding(redHat.x + redHat.nextDirX * TILE_SIZE, redHat.y + redHat.nextDirY * TILE_SIZE)) {
                redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
            }
        }
        if (!isColliding(redHat.x + redHat.dirX * redHat.speed, redHat.y + redHat.dirY * redHat.speed)) {
            redHat.x += redHat.dirX * redHat.speed; redHat.y += redHat.dirY * redHat.speed;
        }

        if (redHat.x < -TILE_SIZE/2) redHat.x = COLS * TILE_SIZE - TILE_SIZE/2;
        if (redHat.x > COLS * TILE_SIZE - TILE_SIZE/2) redHat.x = -TILE_SIZE/2;

        let currCol = Math.floor((redHat.x + TILE_SIZE/2) / TILE_SIZE);
        let currRow = Math.floor((redHat.y + TILE_SIZE/2) / TILE_SIZE);

        if (currCol >= 0 && currCol < COLS && currRow >= 0 && currRow < ROWS) {
            if (grid[currRow][currCol] === 2 || grid[currRow][currCol] === 7) grid[currRow][currCol] = 0;
            
            if (grid[currRow][currCol] === 3) {
                grid[currRow][currCol] = 0;
                if (!hasGun) { scaredTimer = 300; wolves.forEach(w => w.scared = true); }
            }
            
            if (currentStage === 1 && gearSpawned && !hasAquaGear && currRow === gearPos.row && currCol === gearPos.col) {
                hasAquaGear = true;
                itemUI.innerHTML = "🎒 장비: 🤿 수영장비"; itemUI.style.background = "#2563eb";
            }

            if (currentStage === 1 && hasAquaGear && grid[currRow][currCol] === 4) {
                currentStage = 2;
                grid = JSON.parse(JSON.stringify(aquaMap));
                canvas.style.background = "#1e3a8a"; canvas.style.border = "4px solid #3b82f6";
                stageUI.innerHTML = "🗺️ 구역: 2단계 푸른 심해 바다"; stageUI.style.background = "#1d4ed8";
                killUI.innerHTML = "🦈 수중 처치: 0/3"; killUI.style.background = "#7f1d1d";
                resetPositions(); wolves.forEach(w => { w.dead = false; w.scared = false; });
                return;
            }

            if (currentStage === 2 && !hasGun && currRow === gunPos.row && currCol === gunPos.col) {
                hasGun = true; wolves.forEach(w => w.scared = true);
                itemUI.innerHTML = "🎒 장비: 🤿 + 🔫 사냥꾼의 총!"; itemUI.style.background = "#dc2626";
            }

            if (currentStage === 2 && keySpawned && !hasKey && currRow === keyPos.row && currCol === keyPos.col) {
                hasKey = true; currentStage = 3; 
                grid = JSON.parse(JSON.stringify(finalForestMap));
                canvas.style.background = "#14532d"; canvas.style.border = "4px solid #f59e0b";
                stageUI.innerHTML = "🗺️ 구역: 3단계 최종 복수전 (지상)"; stageUI.style.background = "#b45309";
                killUI.innerHTML = "🐺 남은 늑대 제거!"; killUI.style.background = "#b91c1c";
                itemUI.innerHTML = "🎒 장비: 👑 완전 무적 상태";
                resetPositions(); wolves.forEach(w => { w.dead = false; w.scared = true; }); 
                return;
            }

            if (currentStage === 3 && grid[currRow][currCol] === 5) {
                if (wolves.every(w => w.dead)) gameWin = true;
            }
        }

        wolves.forEach(w => {
            if (w.dead) return;

            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0) {
                let validDirs = []; let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                dirs.forEach(d => {
                    if (!isColliding(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) {
                        let nC = Math.floor((w.x + d.x * TILE_SIZE)/TILE_SIZE);
                        let nR = Math.floor((w.y + d.y * TILE_SIZE)/TILE_SIZE);
                        if (grid[nR][nC] !== 5 && (d.x !== -w.dirX || d.y !== -w.dirY)) validDirs.push(d);
                    }
                });
                if (validDirs.length === 0) {
                    dirs.forEach(d => { if (!isColliding(w.x+d.x*TILE_SIZE, w.y+d.y*TILE_SIZE)) validDirs.push(d); });
                }
                if (validDirs.length > 0) {
                    let chosen = validDirs[Math.floor(Math.random() * validDirs.length)];
                    w.dirX = chosen.x; w.dirY = chosen.y;
                } else {
                    w.dirX = -w.dirX; w.dirY = -w.dirY;
                }
            }

            let spd = (w.scared || hasGun || currentStage === 3) ? 1 : 1.5;
            let nWpX = w.x + w.dirX * spd; let nWpY = w.y + w.dirY * spd;
            if (!isColliding(nWpX, nWpY)) { w.x = nWpX; w.y = nWpY; }
            else { w.x = Math.round(w.x/TILE_SIZE)*TILE_SIZE; w.y = Math.round(w.y/TILE_SIZE)*TILE_SIZE; w.dirX = -w.dirX; w.dirY = -w.dirY; }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared || hasGun || currentStage === 3) {
                    w.dead = true; w.x = -999; w.y = -999; 
                    
                    if (currentStage === 1) {
                        forestKills++; killUI.innerHTML = `🐺 숲 늑대 사냥: ${forestKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 1*TILE_SIZE; 
                        if (forestKills === 3) {
                            gearSpawned = true;
                            itemUI.innerHTML = "🎒 장비: 🤿 수영장비 출현!"; itemUI.style.background = "#f59e0b";
                        }
                    } else if (currentStage === 2) {
                        waterKills++; killUI.innerHTML = `🦈 수중 처치: ${waterKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 1*TILE_SIZE; 
                        if (waterKills === 3) {
                            keySpawned = true;
                            itemUI.innerHTML = "🎒 장비: 🔑 탈출 열쇠 출현!"; itemUI.style.background = "#a855f7";
                        }
                    } else if (currentStage === 3) {
                        let remaining = wolves.filter(wolf => !wolf.dead).length;
                        if (remaining === 0) {
                            killUI.innerHTML = "🏡 문이 열렸습니다! 들어가세요!"; killUI.style.background = "#16a34a";
                        } else {
                            killUI.innerHTML = `🐺 남은 늑대 수: ${remaining}마리`;
                        }
                    }
                } else {
                    gameOver = true;
                }
            }
        });
    }

    function resetPositions() {
        redHat.x = 9 * TILE_SIZE; redHat.y = 16 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves[0] = { x: 1 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: 1, dirY: 0, scared: (currentStage===3||hasGun), dead: false };
        wolves[1] = { x: 18 * TILE_SIZE, y: 1 * TILE_SIZE, dirX: -1, dirY: 0, scared: (currentStage===3||hasGun), dead: false };
        wolves[2] = { x: 9 * TILE_SIZE, y: 14 * TILE_SIZE, dirX: 0, dirY: -1, scared: (currentStage===3||hasGun), dead: false };
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (currentStage === 1 || currentStage === 3) {
                    if (grid[r][c] === 1) {
                        ctx.fillStyle = '#064e3b'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    } else if (grid[r][c] === 4) {
                        ctx.fillStyle = '#1d4ed8'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    } else if (grid[r][c] === 2) {
                        ctx.font = '12px Arial'; ctx.fillText('🍄', x+4, y+16);
                    } else if (grid[r][c] === 3) {
                        ctx.font = '14px Arial'; ctx.fillText('⭐', x+3, y+17);
                    } else if (grid[r][c] === 5) {
                        ctx.fillStyle = '#d97706'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                        ctx.font = '14px Arial'; ctx.fillText('🏡', x+3, y+16);
                    }
                } else if (currentStage === 2) {
                    if (grid[r][c] === 6) {
                        ctx.fillStyle = '#1e3a8a'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    } else if (grid[r][c] === 7) {
                        ctx.font = '12px Arial'; ctx.fillText('🌿', x+4, y+16);
                    }
                }
            }
        }

        if (currentStage === 1 && gearSpawned && !hasAquaGear) {
            ctx.font = '16px Arial'; ctx.fillText('🤿', gearPos.col*TILE_SIZE+3, gearPos.row*TILE_SIZE+18);
        }
        if (currentStage === 2 && !hasGun) {
            ctx.font = '16px Arial'; ctx.fillText('🔫', gunPos.col*TILE_SIZE+3, gunPos.row*TILE_SIZE+18);
        }
        if (currentStage === 2 && keySpawned && !hasKey) {
            ctx.font = '16px Arial'; ctx.fillText('🔑', keyPos.col*TILE_SIZE+3, keyPos.row*TILE_SIZE+18);
        }

        let px = redHat.x + TILE_SIZE/2; let py = redHat.y + TILE_SIZE/2;
        ctx.save();
        ctx.beginPath(); ctx.arc(px, py, 8, 0, Math.PI*2);
        ctx.fillStyle = (hasGun || currentStage === 3) ? '#facc15' : ((currentStage === 2) ? '#06b6d4' : '#dc2626');
        ctx.fill();
        ctx.beginPath(); ctx.arc(px, py+2, 5, 0, Math.PI*2); ctx.fillStyle = '#fed7aa'; ctx.fill();
        if(hasAquaGear) { ctx.font = '10px Arial'; ctx.fillText('🤿', px+3, py-3); }
        if(hasGun) { ctx.font = '10px Arial'; ctx.fillText('🔫', px-9, py+5); }
        ctx.restore();

        wolves.forEach(w => {
            if (w.dead) return;
            let wx = w.x + TILE_SIZE/2; let wy = w.y + TILE_SIZE/2;
            ctx.save();
            if (w.scared || hasGun || currentStage === 3) {
                ctx.font = '17px Arial'; ctx.fillText('🥶', wx-8, wy+6);
            } else {
                if (currentStage === 1) {
                    ctx.beginPath(); ctx.arc(wx, wy, 7, 0, Math.PI*2); ctx.fillStyle = '#4b5563'; ctx.fill();
                } else {
                    ctx.font = '16px Arial'; ctx.fillText('🦈', wx-8, wy+6);
                }
            }
            ctx.restore();
        });

        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 30px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2);
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(15,23,42,0.95)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 28px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('👑 TRUE HAPPY ENDING 👑', canvas.width/2, canvas.height/2 - 25);
            ctx.fillStyle = '#fff'; ctx.font = '14px sans-serif'; ctx.fillText('사냥꾼의 총으로 물속 괴물과 숲속의 늑대들을', canvas.width/2, canvas.height/2 + 15);
            ctx.fillStyle = '#34d399'; ctx.font = 'bold 15px sans-serif'; ctx.fillText('완벽하게 처단하고 무사히 탈출했습니다! 사냥 성공!', canvas.width/2, canvas.height/2 + 40);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        currentStage = 1; grid = JSON.parse(JSON.stringify(forestMap));
        gameOver = false; gameWin = false; forestKills = 0; waterKills = 0;
        hasAquaGear = false; gearSpawned = false; hasGun = false; hasKey = false; keySpawned = false; scaredTimer = 0;
        canvas.style.background = "#14532d"; canvas.style.border = "4px solid #78350f";
        stageUI.innerHTML = "🗺️ 구역: 1단계 숲속 미로"; stageUI.style.background = "#14532d";
        killUI.innerHTML = "🐺 숲 늑대 사냥: 0/3"; killUI.style.background = "#7f1d1d";
        itemUI.innerHTML = "🎒 장비: 없음"; itemUI.style.background = "#374151";
        resetPositions(); wolves.forEach(w => { w.dead = false; w.scared = false; }); canvas.focus();
    });

    setTimeout(() => { canvas.focus(); }, 300);
    resetPositions(); loop();
</script>
"""

components.html(pacman_js, height=520)
