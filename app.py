import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 설정 ---
st.set_page_config(page_title="잔혹동화: 빨간 모자의 역습", page_icon="🌲", layout="centered")

st.title("🌲 잔혹동화: 빨간 모자와 숲속의 늑대들 🪓")
st.markdown("""
**🎮 플레이 가이드:**
1. **1단계 숲속:** 미로 안의 황금 별(⭐)을 먹으면 무적 상태가 됩니다! 도망치는 늑대를 **3마리** 사냥하세요. 성공하면 중앙에 **수영 장비(🤿)**가 나타납니다. 장비를 먹고 파란색 물웅덩이 블록으로 들어가세요!
2. **2단계 심해:** 물속에 숨겨진 **사냥꾼의 총(🔫)**을 찾으세요! 총을 얻으면 영구 무적이 됩니다. 수중 괴물들을 사냥해 **열쇠(🔑)**를 얻고 다시 지상으로 복귀하세요!
3. **3단계 최종전:** 지상으로 돌아와 총의 강력한 위력으로 남은 늑대들을 **완전히 소탕**한 뒤, 최상단의 **할머니 집🏡**으로 들어가면 대망의 트루 엔딩!
""")

# --- 시각 보정 및 이동 패치 완료 HTML5 컴포넌트 ---
game_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <div id="p-stage" style="padding: 6px 10px; background: #14532d; color: #a7f3d0; border-radius: 6px; font-weight: bold; font-size: 13px;">🗺️ 구역: 1단계 숲속 미로</div>
            <div id="p-kill" style="padding: 6px 10px; background: #7f1d1d; color: #fca5a5; border-radius: 6px; font-weight: bold; font-size: 13px;">🐺 숲 늑대 사냥: 0/3</div>
            <div id="p-item" style="padding: 6px 10px; background: #374151; color: #9ca3af; border-radius: 6px; font-weight: bold; font-size: 13px;">🎒 장비: 없음</div>
        </div>
        <button id="p-reset" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px;">🔄 리셋</button>
    </div>
    
    <canvas id="pacmanCanvas" width="440" height="440" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); background: #a7f3d0; border: 4px solid #78350f; outline: none;" tabindex="0"></canvas>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const stageUI = document.getElementById('p-stage'); const killUI = document.getElementById('p-kill');
    const itemUI = document.getElementById('p-item'); const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;

    // 💡 스크린샷 구조 원본 복사 데이터
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
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], // 스타팅 라인 완전 개방
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

    // 캐릭터 이동 속도를 2로 주어 타일 연산 버그 원천 차단
    let redHat = { x: 9 * TILE_SIZE, y: 18 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 2 };
    let wolves = [];
    let scaredTimer = 0;

    function initForestGrid() {
        grid = JSON.parse(JSON.stringify(forestMap));
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (grid[r][c] === 0) grid[r][c] = 2; // 빈 바닥에 🍄 배치
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

    // 💡 정교한 벽 충돌 알고리즘 개선
    function isColliding(x, y) {
        if (x < 0 || x + TILE_SIZE > canvas.width || y < 0 || y + TILE_SIZE > canvas.height) return true;

        let left = Math.floor(x / TILE_SIZE);
        let right = Math.floor((x + TILE_SIZE - 1) / TILE_SIZE);
        let top = Math.floor(y / TILE_SIZE);
        let bottom = Math.floor((y + TILE_SIZE - 1) / TILE_SIZE);

        let checkPoints = [{r: top, c: left}, {r: top, c: right}, {r: bottom, c: left}, {r: bottom, c: right}];

        for (let pt of checkPoints) {
            let tile = grid[pt.r][pt.c];
            if (tile === 1) return true; // 숲속 나무벽
            if (tile === 6) return true; // 심해 돌벽
            if (tile === 4 && !hasAquaGear && currentStage === 1) return true; // 장비 없이 물웅덩이 이동불가
            if (tile === 5) {
                if (currentStage === 3 && wolves.every(w => w.dead)) return false; 
                return true;
            }
        }
        return false;
    }

    function update() {
        if (gameOver || gameWin) return;

        if (scaredTimer > 0 && !hasGun && currentStage !== 3) {
            scaredTimer--;
            if (scaredTimer === 0) wolves.forEach(w => w.scared = false);
        }

        // 정확히 22단위 타일에 들어왔을 때 유저가 누른 새 방향으로 변경
        if (redHat.x % TILE_SIZE === 0 && redHat.y % TILE_SIZE === 0) {
            if (!isColliding(redHat.x + redHat.nextDirX * TILE_SIZE, redHat.y + redHat.nextDirY * TILE_SIZE)) {
                redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
            }
        }

        let nextX = redHat.x + redHat.dirX * redHat.speed;
        let nextY = redHat.y + redHat.dirY * redHat.speed;

        if (!isColliding(nextX, nextY)) {
            redHat.x = nextX; redHat.y = nextY;
        } else {
            redHat.x = Math.round(redHat.x / TILE_SIZE) * TILE_SIZE;
            redHat.y = Math.round(redHat.y / TILE_SIZE) * TILE_SIZE;
        }

        let currCol = Math.floor((redHat.x + TILE_SIZE/2) / TILE_SIZE);
        let currRow = Math.floor((redHat.y + TILE_SIZE/2) / TILE_SIZE);

        if (currCol >= 0 && currCol < COLS && currRow >= 0 && currRow < ROWS) {
            if (grid[currRow][currCol] === 2 || grid[currRow][currCol] === 7) grid[currRow][currCol] = 0;
            
            if (grid[currRow][currCol] === 3) {
                grid[currRow][currCol] = 0;
                if (!hasGun && currentStage === 1) { scaredTimer = 350; wolves.forEach(w => w.scared = true); }
            }
            
            if (currentStage === 1 && gearSpawned && !hasAquaGear && currRow === gearPos.row && currCol === gearPos.col) {
                hasAquaGear = true;
                itemUI.innerHTML = "🎒 장비: 🤿 수영장비 장착!"; itemUI.style.background = "#2563eb";
            }

            if (currentStage === 1 && hasAquaGear && forestMap[currRow][currCol] === 4) {
                currentStage = 2; grid = JSON.parse(JSON.stringify(aquaMap));
                canvas.style.background = "#1e3a8a"; canvas.style.border = "4px solid #0ea5e9"; // 심해 바닥은 파란색
                stageUI.innerHTML = "🗺️ 구역: 2단계 푸른 심해 바다"; stageUI.style.background = "#0284c7";
                killUI.innerHTML = "🦈 수중 처치: 0/3"; killUI.style.background = "#7f1d1d";
                resetPositions(); wolves.forEach(w => { w.dead = false; w.scared = false; });
                return;
            }

            if (currentStage === 2 && !hasGun && currRow === gunPos.row && currCol === gunPos.col) {
                hasGun = true; wolves.forEach(w => w.scared = true);
                itemUI.innerHTML = "🎒 장비: 🤿 + 🔫 사냥꾼의 총!"; itemUI.style.background = "#dc2626";
            }

            if (currentStage === 2 && keySpawned && !hasKey && currRow === keyPos.row && currCol === keyPos.col) {
                hasKey = true; currentStage = 3; grid = JSON.parse(JSON.stringify(forestMap)); 
                canvas.style.background = "#a7f3d0"; canvas.style.border = "4px solid #f59e0b";
                stageUI.innerHTML = "🗺️ 구역: 3단계 최종 소탕전"; stageUI.style.background = "#b45309";
                killUI.innerHTML = "🐺 남은 늑대 제거!"; killUI.style.background = "#b91c1c";
                itemUI.innerHTML = "🎒 장비: 👑 완전 무적 복수 상태";
                resetPositions(); wolves.forEach(w => { w.dead = false; w.scared = true; }); 
                return;
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
                        let nC = Math.floor((w.x + d.x * TILE_SIZE)/TILE_SIZE);
                        let nR = Math.floor((w.y + d.y * TILE_SIZE)/TILE_SIZE);
                        if (grid[nR][nC] !== 5 && (d.x !== -w.dirX || d.y !== -w.dirY)) validDirs.push(d);
                    }
                });
                if (validDirs.length === 0) {
                    dirs.forEach(d => { if (!isColliding(w.x+d.x*TILE_SIZE, w.y+d.y*TILE_SIZE)) validDirs.push(d); });
                }
                if (validDirs.length > 0) {
                    w.dirX = validDirs[0].x; w.dirY = validDirs[0].y;
                    if(Math.random() > 0.4) {
                        let chosen = validDirs[Math.floor(Math.random() * validDirs.length)];
                        w.dirX = chosen.x; w.dirY = chosen.y;
                    }
                } else {
                    w.dirX = -w.dirX; w.dirY = -w.dirY;
                }
            }

            let spd = 1.0;
            let nWpX = w.x + w.dirX * spd; let nWpY = w.y + w.dirY * spd;
            if (!isColliding(nWpX, nWpY)) { w.x = nWpX; w.y = nWpY; }
            else { w.x = Math.round(w.x/TILE_SIZE)*TILE_SIZE; w.y = Math.round(w.y/TILE_SIZE)*TILE_SIZE; w.dirX = -w.dirX; w.dirY = -w.dirY; }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared || hasGun || currentStage === 3) {
                    w.dead = true; w.x = -999; w.y = -999; 
                    
                    if (currentStage === 1) {
                        forestKills++; killUI.innerHTML = `🐺 숲 늑대 사냥: ${forestKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 8*TILE_SIZE; 
                        if (forestKills === 3) {
                            gearSpawned = true;
                            itemUI.innerHTML = "🎒 장비: 🤿 수영장비 출현!"; itemUI.style.background = "#f59e0b";
                        }
                    } else if (currentStage === 2) {
                        waterKills++; killUI.innerHTML = `🦈 수중 처치: ${waterKills}/3`;
                        w.dead = false; w.x = 9*TILE_SIZE; w.y = 10*TILE_SIZE; 
                        if (waterKills === 3) {
                            keySpawned = true;
                            itemUI.innerHTML = "🎒 장비: 🔑 탈출 열쇠 출현!"; itemUI.style.background = "#a855f7";
                        }
                    } else if (currentStage === 3) {
                        let remaining = wolves.filter(wolf => !wolf.dead).length;
                        if (remaining === 0) {
                            killUI.innerHTML = "🏡 집 오픈! 할머니 집으로 복귀하세요!"; killUI.style.background = "#16a34a";
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
        redHat.x = 9 * TILE_SIZE; redHat.y = 18 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves = [
            { x: 2 * TILE_SIZE, y: 3 * TILE_SIZE, dirX: 1, dirY: 0, scared: (currentStage===3||hasGun), dead: false },
            { x: 17 * TILE_SIZE, y: 3 * TILE_SIZE, dirX: -1, dirY: 0, scared: (currentStage===3||hasGun), dead: false },
            { x: 9 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: 0, dirY: -1, scared: (currentStage===3||hasGun), dead: false }
        ];
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (currentStage === 1 || currentStage === 3) {
                    if (forestMap[r][c] === 1) {
                        // 🌲 벽 색상: 어둡고 중후한 진청록색
                        ctx.fillStyle = '#064e3b'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE); 
                    } else if (forestMap[r][c] === 4) {
                        // 🟦 물웅덩이 색상: 파란색 블록
                        ctx.fillStyle = '#2563eb'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE); 
                    } else if (forestMap[r][c] === 5) {
                        ctx.font = '15px Arial'; ctx.fillText('🏡', x+3, y+16); 
                    } else if (forestMap[r][c] === 3 && grid[r][c] === 3) {
                        ctx.font = '14px Arial'; ctx.fillText('⭐', x+3, y+17);
                    }
                    if (grid[r][c] === 2) {
                        ctx.font = '12px Arial'; ctx.fillText('🍄', x+4, y+16);
                    }
                } else if (currentStage === 2) {
                    if (grid[r][c] === 6) {
                        // ⬛ 심해의 벽 색상: 아주 어두운 차콜 블랙
                        ctx.fillStyle = '#0f172a'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
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
        ctx.fillStyle = (hasGun || currentStage === 3) ? '#facc15' : (scaredTimer > 0 ? '#fb923c' : '#dc2626');
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
                if (currentStage === 1 || currentStage === 3) {
                    ctx.font = '16px Arial'; ctx.fillText('🐺', wx-8, wy+6); 
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
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 26px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('👑 TRUE HAPPY ENDING 👑', canvas.width/2, canvas.height/2 - 25);
            ctx.fillStyle = '#fff'; ctx.font = '14px sans-serif'; ctx.fillText('사냥꾼의 총으로 물속 괴물과 숲속의 늑대들을', canvas.width/2, canvas.height/2 + 15);
            ctx.fillStyle = '#34d399'; ctx.font = 'bold 15px sans-serif'; ctx.fillText('완벽하게 소탕하고 할머니 집으로 복귀했습니다!', canvas.width/2, canvas.height/2 + 40);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        currentStage = 1; gameOver = false; gameWin = false; forestKills = 0; waterKills = 0;
        hasAquaGear = false; gearSpawned = false; hasGun = false; hasKey = false; keySpawned = false; scaredTimer = 0;
        canvas.style.background = "#a7f3d0"; canvas.style.border = "4px solid #78350f";
        stageUI.innerHTML = "🗺️ 구역: 1단계 숲속 미로"; stageUI.style.background = "#14532d";
        killUI.innerHTML = "🐺 숲 늑대 사냥: 0/3"; killUI.style.background = "#7f1d1d";
        itemUI.innerHTML = "🎒 장비: 없음"; itemUI.style.background = "#374151";
        initForestGrid(); resetPositions(); canvas.focus();
    });

    initForestGrid(); resetPositions();
    setTimeout(() => { canvas.focus(); }, 300);
    loop();
</script>
"""

components.html(game_js, height=520)
