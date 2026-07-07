import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="빨간 모자의 숲속 모험", page_icon="🌲", layout="centered")

st.title("🌲 빨간 모자의 미로 대모험 (무한 리스폰 패치) 🪓")
st.markdown("""
**🚨 경고: 늑대 무한 증식 중!**
* 이제 늑대와 상어를 처치해도 완전히 사라지지 않고 **끝없이 부활**합니다!
* 끊임없이 밀려오는 늑대들을 피해 버섯을 모으고 탈출하세요!
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
