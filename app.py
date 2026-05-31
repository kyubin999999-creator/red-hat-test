import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 설정 ---
st.set_page_config(page_title="동화 속으로: 빨간 모자의 여정", page_icon="🍄", layout="centered")

st.title("🌲 잔혹동화: 빨간 모자와 숲속의 늑대들 🐺")
st.markdown("무시무시한 늑대들을 피해 숲속의 **버섯**을 모두 따고, 미로 위쪽에 있는 **할머니의 안전한 오두막집🏡**으로 탈출하세요!")

# --- 자바스크립트 기반 게임 코드 ---
pacman_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 8px;">
            <div id="p-score" style="padding: 8px 12px; background: #fef2f2; color: #991b1b; border-radius: 6px; font-weight: bold; font-size: 14px; border: 1px solid #fee2e2;">🍄 바구니 속 버섯: 0</div>
            <div id="p-lives" style="padding: 8px 12px; background: #fffbeb; color: #b45309; border-radius: 6px; font-weight: bold; font-size: 14px; border: 1px solid #fde68a;">❤️ 목숨: ❤️❤️❤️</div>
        </div>
        <button id="p-reset" style="padding: 8px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px;">🔄 처음부터</button>
    </div>
    
    <canvas id="pacmanCanvas" width="440" height="440" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); background: #14532d; border: 4px solid #78350f; outline: none;" tabindex="0"></canvas>
    
    <div style="font-size: 13px; color: #a8a29e; margin-top: 10px;">
        🎮 <b>조작법:</b> 키보드 방향키(`←` `→` `↑` `↓`)를 누르면 빨간 모자가 바로 움직입니다!
    </div>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const scoreUI = document.getElementById('p-score'); const livesUI = document.getElementById('p-lives');
    const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;
    
    // ⭐ [맵 리디자인] 물웅덩이(4)가 길을 완전히 막지 않고, 우회로를 통해 모든 버섯(2,3)을 먹을 수 있도록 수정 완료
    const map = [
        [1,1,1,1,1,1,1,1,1,5,5,1,1,1,1,1,1,1,1,1],
        [1,3,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,3,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,2,1,1,2,4,4,2,2,1,1,2,2,4,4,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,4,2,2,4,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
        [1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,0,0,1,1,0,1,2,1,1,1,1],
        [4,4,4,4,2,0,0,1,0,0,0,0,1,0,0,2,4,4,4,4],
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,3,2,1,2,2,2,2,2,0,0,2,2,2,2,2,1,2,3,1],
        [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
        [1,2,2,2,2,1,4,4,2,1,1,2,4,4,1,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    let grid = JSON.parse(JSON.stringify(map));
    let score = 0; let lives = 3; let gameOver = false; let gameWin = false;
    let totalMushrooms = 0;

    for(let r=0; r<ROWS; r++) {
        for(let c=0; c<COLS; c++) {
            if(grid[r][c] === 2 || grid[r][c] === 3) totalMushrooms++;
        }
    }

    let redHat = { x: 9 * TILE_SIZE, y: 16 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 2 };
    let wolves = [
        { x: 9 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: 1, dirY: 0, scared: false },
        { x: 10 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: -1, dirY: 0, scared: false },
        { x: 9 * TILE_SIZE, y: 12 * TILE_SIZE, dirX: 0, dirY: -1, scared: false }
    ];

    let scaredTimer = 0;

    window.addEventListener('keydown', function(e) {
        if([37, 38, 39, 40].indexOf(e.keyCode) > -1) { 
            e.preventDefault(); 
            canvas.focus();
        }
    }, {passive: false});

    canvas.addEventListener('keydown', e => {
        if(e.keyCode === 37) { redHat.nextDirX = -1; redHat.nextDirY = 0; }
        if(e.keyCode === 39) { redHat.nextDirX = 1; redHat.nextDirY = 0; }
        if(e.keyCode === 38) { redHat.nextDirX = 0; redHat.nextDirY = -1; }
        if(e.keyCode === 40) { redHat.nextDirX = 0; redHat.nextDirY = 1; }
    });

    function isColliding(x, y) {
        let left = Math.floor(x / TILE_SIZE);
        let right = Math.floor((x + TILE_SIZE - 1) / TILE_SIZE);
        let top = Math.floor(y / TILE_SIZE);
        let bottom = Math.floor((y + TILE_SIZE - 1) / TILE_SIZE);
        
        if(left < 0 || right >= COLS || top < 0 || bottom >= ROWS) return true;

        let blockedTypes = [1, 4];
        if (blockedTypes.includes(grid[top][left]) || blockedTypes.includes(grid[top][right]) || 
            blockedTypes.includes(grid[bottom][left]) || blockedTypes.includes(grid[bottom][right])) {
            return true;
        }
        return false;
    }

    function update() {
        if (gameOver || gameWin) return;

        if (scaredTimer > 0) {
            scaredTimer--;
            if (scaredTimer === 0) wolves.forEach(w => w.scared = false);
        }

        if (redHat.x % TILE_SIZE === 0 && redHat.y % TILE_SIZE === 0) {
            if (!isColliding(redHat.x + redHat.nextDirX * TILE_SIZE, redHat.y + redHat.nextDirY * TILE_SIZE)) {
                redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
            }
        }

        if (!isColliding(redHat.x + redHat.dirX * redHat.speed, redHat.y + redHat.dirY * redHat.speed)) {
            redHat.x += redHat.dirX * redHat.speed;
            redHat.y += redHat.dirY * redHat.speed;
        }

        if (redHat.x < -TILE_SIZE/2) redHat.x = COLS * TILE_SIZE - TILE_SIZE/2;
        if (redHat.x > COLS * TILE_SIZE - TILE_SIZE/2) redHat.x = -TILE_SIZE/2;

        let currCol = Math.floor((redHat.x + TILE_SIZE/2) / TILE_SIZE);
        let currRow = Math.floor((redHat.y + TILE_SIZE/2) / TILE_SIZE);

        if (currCol >= 0 && currCol < COLS && currRow >= 0 && currRow < ROWS) {
            if (grid[currRow][currCol] === 2) {
                grid[currRow][currCol] = 0; score++; totalMushrooms--;
            } else if (grid[currRow][currCol] === 3) {
                grid[currRow][currCol] = 0; score += 10; totalMushrooms--;
                scaredTimer = 350;
                wolves.forEach(w => w.scared = true);
            }
            
            if (totalMushrooms <= 0 && grid[currRow][currCol] === 5) {
                gameWin = true;
            }
            scoreUI.innerHTML = `🍄 바구니 속 버섯: ${score} ${totalMushrooms > 0 ? `(남은 버섯: ${totalMushrooms})` : '◀ 🏡할머니 집으로 가세요!'}`;
        }

        wolves.forEach(w => {
            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0) {
                let validDirs = [];
                let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                
                dirs.forEach(d => {
                    let nextX = w.x + d.x * TILE_SIZE;
                    let nextY = w.y + d.y * TILE_SIZE;
                    
                    if (!isColliding(nextX, nextY)) {
                        let nextCol = Math.floor(nextX / TILE_SIZE);
                        let nextRow = Math.floor(nextY / TILE_SIZE);
                        
                        if (nextRow >= 0 && nextRow < ROWS && nextCol >= 0 && nextCol < COLS && grid[nextRow][nextCol] !== 5) {
                            if (d.x !== -w.dirX || d.y !== -w.dirY) {
                                validDirs.push(d);
                            }
                        }
                    }
                });

                if (validDirs.length === 0) {
                    dirs.forEach(d => {
                        if (!isColliding(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) {
                            validDirs.push(d);
                        }
                    });
                }

                if (validDirs.length > 0) {
                    let chosen = validDirs[Math.floor(Math.random() * validDirs.length)];
                    w.dirX = chosen.x; 
                    w.dirY = chosen.y;
                } else {
                    w.dirX = -w.dirX;
                    w.dirY = -w.dirY;
                }
            }

            let nextWpX = w.x + w.dirX * (w.scared ? 1 : 1.5);
            let nextWpY = w.y + w.dirY * (w.scared ? 1 : 1.5);
            
            if (!isColliding(nextWpX, nextWpY)) {
                w.x = nextWpX;
                w.y = nextWpY;
            } else {
                w.x = Math.round(w.x / TILE_SIZE) * TILE_SIZE;
                w.y = Math.round(w.y / TILE_SIZE) * TILE_SIZE;
                w.dirX = -w.dirX; w.dirY = -w.dirY;
            }

            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared) {
                    w.x = 9 * TILE_SIZE; w.y = 9 * TILE_SIZE; w.scared = false; score += 30;
                } else {
                    lives--;
                    livesUI.innerHTML = `❤️ 목숨: ${'❤️'.repeat(lives)}`;
                    if (lives <= 0) gameOver = true; else resetPositions();
                }
            }
        });
    }

    function resetPositions() {
        redHat.x = 9 * TILE_SIZE; redHat.y = 16 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves[0] = { x: 9 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: 1, dirY: 0, scared: wolves[0].scared };
        wolves[1] = { x: 10 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: -1, dirY: 0, scared: wolves[1].scared };
        wolves[2] = { x: 9 * TILE_SIZE, y: 12 * TILE_SIZE, dirX: 0, dirY: -1, scared: wolves[2].scared };
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                
                if (grid[r][c] === 1) { 
                    ctx.fillStyle = '#064e3b'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    ctx.fillStyle = '#047857'; ctx.fillRect(x+4, y+4, TILE_SIZE-8, TILE_SIZE-8);
                } else if (grid[r][c] === 4) { 
                    ctx.fillStyle = '#1d4ed8'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    ctx.fillStyle = '#3b82f6'; ctx.fillRect(x+2, y+2, TILE_SIZE-4, TILE_SIZE-4);
                } else if (grid[r][c] === 5) { 
                    ctx.fillStyle = '#b45309'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    ctx.font = '14px Arial'; ctx.fillText('🏡', x + TILE_SIZE/2, y + TILE_SIZE/2 + 2);
                } else if (grid[r][c] === 2) { 
                    ctx.font = '13px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                    ctx.fillText('🍄', x + TILE_SIZE/2, y + TILE_SIZE/2);
                } else if (grid[r][c] === 3) { 
                    ctx.font = '15px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                    ctx.fillText('⭐', x + TILE_SIZE/2, y + TILE_SIZE/2);
                }
            }
        }

        // 빨간 망토 소녀 그리기
        let px = redHat.x + TILE_SIZE/2; let py = redHat.y + TILE_SIZE/2;
        ctx.save();
        ctx.beginPath(); ctx.arc(px, py - 1, 8, 0, Math.PI * 2); ctx.fillStyle = '#dc2626'; ctx.fill();
        ctx.beginPath(); ctx.arc(px, py + 2, 5, 0, Math.PI * 2); ctx.fillStyle = '#fed7aa'; ctx.fill();
        ctx.fillStyle = '#000'; ctx.fillRect(px - 3, py + 1, 1.5, 1.5); ctx.fillRect(px + 1, py + 1, 1.5, 1.5);
        ctx.beginPath(); ctx.arc(px, py + 5, 2, 0, Math.PI*2); ctx.fillStyle = '#b91c1c'; ctx.fill();
        ctx.restore();

        // 야수 늑대 그리기
        wolves.forEach(w => {
            let wx = w.x + TILE_SIZE/2; let wy = w.y + TILE_SIZE/2;
            ctx.save();
            if (w.scared) {
                ctx.font = '17px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText('🥶', wx, wy);
            } else {
                ctx.beginPath(); ctx.arc(wx, wy, 7, 0, Math.PI*2); ctx.fillStyle = '#4b5563'; ctx.fill();
                ctx.fillStyle = '#1f2937';
                ctx.beginPath(); ctx.moveTo(wx - 6, wy - 4); ctx.lineTo(wx - 3, wy - 10); ctx.lineTo(wx, wy - 4); ctx.fill();
                ctx.beginPath(); ctx.moveTo(wx + 6, wy - 4); ctx.lineTo(wx + 3, wy - 10); ctx.lineTo(wx, wy - 4); ctx.fill();
                ctx.fillStyle = '#facc15'; ctx.fillRect(wx - 3, wy - 2, 2, 2); ctx.fillRect(wx + 1, wy - 2, 2, 2);
            }
            ctx.restore();
        });

        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 34px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2 - 15);
            ctx.fillStyle = '#fff'; ctx.font = '15px sans-serif'; ctx.fillText('늑대에게 잡혀 할머니집에 가지 못했습니다...', canvas.width/2, canvas.height/2 + 25);
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(15,23,42,0.9)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#34d399'; ctx.font = 'bold 32px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('🎉 HAPPY ENDING 🎉', canvas.width/2, canvas.height/2 - 20);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 16px sans-serif'; ctx.fillText('해냈습니다! 버섯을 전부 가득 채운 채', canvas.width/2, canvas.height/2 + 20);
            ctx.fillStyle = '#fef08a'; ctx.font = '15px sans-serif'; ctx.fillText('안전한 할머니 오두막집🏡에 무사히 도착했습니다!', canvas.width/2, canvas.height/2 + 45);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        grid = JSON.parse(JSON.stringify(map)); score = 0; lives = 3; gameOver = false; gameWin = false; scaredTimer = 0;
        totalMushrooms = 0; for(let r=0; r<ROWS; r++) for(let c=0; c<COLS; c++) if(grid[r][c]===2 || grid[r][c]===3) totalMushrooms++;
        scoreUI.innerHTML = `🍄 바구니 속 버섯: 0 (남은 버섯: ${totalMushrooms})`; livesUI.innerHTML = "❤️ 목숨: ❤️❤️❤️"; resetPositions(); canvas.focus();
    });

    setTimeout(() => { canvas.focus(); }, 300);
    resetPositions(); loop();
</script>
"""

components.html(pacman_js, height=520)
