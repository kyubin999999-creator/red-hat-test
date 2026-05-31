import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="잔혹동화: 빨간 모자와 늑대", page_icon="🍄", layout="centered")

st.title("🍄 잔혹동화: 빨간 모자와 늑대 (팩맨 버전) 🐺")
st.markdown("숲속 미로를 탐험하며 **늑대들**을 피해 **버섯**을 모두 바구니에 담으세요! 반짝이는 **황금 버섯**을 먹으면 전세가 역전되어 늑대를 사냥할 수 있습니다.")

pacman_js = """
<div style="text-align: center; font-family: 'Malgun Gothic', sans-serif; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 440px; margin: 0 auto 12px auto;">
        <div style="display: flex; gap: 8px;">
            <div id="p-score" style="padding: 8px 12px; background: #fef2f2; color: #991b1b; border-radius: 6px; font-weight: bold; font-size: 14px; border: 1px solid #fee2e2;">🍄 버섯 바구니: 0</div>
            <div id="p-lives" style="padding: 8px 12px; background: #fffbeb; color: #b45309; border-radius: 6px; font-weight: bold; font-size: 14px; border: 1px solid #fde68a;">❤️ 목숨: ❤️❤️❤️</div>
        </div>
        <button id="p-reset" style="padding: 8px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px;">🔄 처음부터</button>
    </div>
    
    <canvas id="pacmanCanvas" width="440" height="440" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.6); background: #0c0a09; border: 3px solid #78350f;" tabindex="0"></canvas>
    
    <div style="font-size: 13px; color: #a8a29e; margin-top: 10px;">
        🎯 <b>플레이 방법:</b> 게임 화면을 <b>마우스로 한 번 클릭</b>한 후, 키보드 방향키(`←` `→` `↑` `↓`)로 움직이세요!
    </div>
</div>

<script>
    const canvas = document.getElementById('pacmanCanvas'); const ctx = canvas.getContext('2d');
    const scoreUI = document.getElementById('p-score'); const livesUI = document.getElementById('p-lives');
    const resetBtn = document.getElementById('p-reset');

    const TILE_SIZE = 22; const COLS = 20; const ROWS = 20;
    
    // 0: 빈 공간, 1: 숲속 벽(나무), 2: 일반 버섯, 3: 황금 버섯(파워 펠렛)
    const map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
        [1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,0,0,1,1,0,1,2,1,1,1,1],
        [0,0,0,0,2,0,0,1,0,0,0,0,1,0,0,2,0,0,0,0],
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
        [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
        [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
        [1,3,2,1,2,2,2,2,2,0,0,2,2,2,2,2,1,2,3,1],
        [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
        [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    let grid = JSON.parse(JSON.stringify(map));
    let score = 0; let lives = 3; let gameOver = false; let gameWin = false;
    let totalMushrooms = 0;

    // 맵 내 버섯 총 개수 세기
    for(let r=0; r<ROWS; r++) {
        for(let c=0; c<COLS; c++) {
            if(grid[r][c] === 2 || grid[r][c] === 3) totalMushrooms++;
        }
    }

    // 캐릭터 정의
    let redHat = { x: 9 * TILE_SIZE, y: 16 * TILE_SIZE, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, speed: 2 };
    
    let wolves = [
        { x: 9 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: 1, dirY: 0, color: '#ef4444', scared: false },
        { x: 10 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: -1, dirY: 0, color: '#a855f7', scared: false },
        { x: 9 * TILE_SIZE, y: 9 * TILE_SIZE, dirX: 0, dirY: -1, color: '#06b6d4', scared: false }
    ];

    let scaredTimer = 0;

    // 키보드 입력 스크롤 방지
    window.addEventListener('keydown', function(e) {
        if([37, 38, 39, 40].indexOf(e.keyCode) > -1) { e.preventDefault(); }
    }, false);

    window.addEventListener('keydown', e => {
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
        
        // 포탈 터널 예외 처리
        if(left < 0 || right >= COLS) return false;

        if (grid[top][left] === 1 || grid[top][right] === 1 || grid[bottom][left] === 1 || grid[bottom][right] === 1) {
            return true;
        }
        return false;
    }

    function update() {
        if (gameOver || gameWin) return;

        // 사냥 상태 타이머 제어
        if (scaredTimer > 0) {
            scaredTimer--;
            if (scaredTimer === 0) {
                wolves.forEach(w => w.scared = false);
            }
        }

        // 1. 빨간 모자 이동 및 방향 전환 시스템
        if (redHat.x % TILE_SIZE === 0 && redHat.y % TILE_SIZE === 0) {
            if (!isColliding(redHat.x + redHat.nextDirX * TILE_SIZE, redHat.y + redHat.nextDirY * TILE_SIZE)) {
                redHat.dirX = redHat.nextDirX; redHat.dirY = redHat.nextDirY;
            }
        }

        if (!isColliding(redHat.x + redHat.dirX * redHat.speed, redHat.y + redHat.dirY * redHat.speed)) {
            redHat.x += redHat.dirX * redHat.speed;
            redHat.y += redHat.dirY * redHat.speed;
        }

        // 좌우 끝 포탈 기능
        if (redHat.x < -TILE_SIZE/2) redHat.x = COLS * TILE_SIZE - TILE_SIZE/2;
        if (redHat.x > COLS * TILE_SIZE - TILE_SIZE/2) redHat.x = -TILE_SIZE/2;

        // 2. 아이템 획득 판정
        let currCol = Math.floor((redHat.x + TILE_SIZE/2) / TILE_SIZE);
        let currRow = Math.floor((redHat.y + TILE_SIZE/2) / TILE_SIZE);

        if (currCol >= 0 && currCol < COLS && currRow >= 0 && currRow < ROWS) {
            if (grid[currRow][currCol] === 2) { // 일반 버섯
                grid[currRow][currCol] = 0; score++; totalMushrooms--;
            } else if (grid[currRow][currCol] === 3) { // 황금 버섯 (늑대가 도망감)
                grid[currRow][currCol] = 0; score += 10; totalMushrooms--;
                scaredTimer = 400; // 약 7초간 유지
                wolves.forEach(w => w.scared = true);
            }
            scoreUI.innerHTML = `🍄 버섯 바구니: ${score}`;
            if (totalMushrooms <= 0) gameWin = true;
        }

        // 3. 늑대 인공지능 및 충돌 판정
        wolves.forEach(w => {
            if (w.x % TILE_SIZE === 0 && w.y % TILE_SIZE === 0) {
                let validDirs = [];
                let dirs = [{x:1, y:0}, {x:-1, y:0}, {x:0, y:1}, {x:0, y:-1}];
                dirs.forEach(d => {
                    if (!isColliding(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) {
                        // 왔던 길로 바로 되돌아가는 것 차단 (자연스러운 전진)
                        if (d.x !== -w.dirX || d.y !== -w.dirY) validDirs.push(d);
                    }
                });
                if (validDirs.length === 0) {
                    dirs.forEach(d => { if (!isColliding(w.x + d.x * TILE_SIZE, w.y + d.y * TILE_SIZE)) validDirs.push(d); });
                }
                let chosen = validDirs[Math.floor(Math.random() * validDirs.length)];
                if (chosen) { w.dirX = chosen.x; w.dirY = chosen.y; }
            }

            w.x += w.dirX * (w.scared ? 1 : 2); // 무서워할 때는 느려짐
            w.y += w.dirY * (w.scared ? 1 : 2);

            // 좌우 끝 포탈 (늑대용)
            if (w.x < -TILE_SIZE/2) w.x = COLS * TILE_SIZE - TILE_SIZE/2;
            if (w.x > COLS * TILE_SIZE - TILE_SIZE/2) w.x = -TILE_SIZE/2;

            // 충돌 이벤트 발생
            if (Math.abs(redHat.x - w.x) < TILE_SIZE * 0.7 && Math.abs(redHat.y - w.y) < TILE_SIZE * 0.7) {
                if (w.scared) {
                    // 사냥 성공: 늑대는 소굴로 리젠
                    w.x = 9 * TILE_SIZE; w.y = 9 * TILE_SIZE; w.scared = false; score += 50;
                } else {
                    // 피해를 입음
                    lives--;
                    livesUI.innerHTML = `❤️ 목숨: ${'❤️'.repeat(lives)}`;
                    if (lives <= 0) { gameOver = true; } else { resetPositions(); }
                }
            }
        });
    }

    function resetPositions() {
        redHat.x = 9 * TILE_SIZE; redHat.y = 16 * TILE_SIZE; redHat.dirX = 0; redHat.dirY = 0; redHat.nextDirX = 0; redHat.nextDirY = 0;
        wolves[0] = { x: 9 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: 1, dirY: 0, color: '#ef4444', scared: wolves[0].scared };
        wolves[1] = { x: 10 * TILE_SIZE, y: 8 * TILE_SIZE, dirX: -1, dirY: 0, color: '#a855f7', scared: wolves[1].scared };
        wolves[2] = { x: 9 * TILE_SIZE, y: 9 * TILE_SIZE, dirX: 0, dirY: -1, color: '#06b6d4', scared: wolves[2].scared };
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. 지형물 그리기
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let x = c * TILE_SIZE; let y = r * TILE_SIZE;
                if (grid[r][c] === 1) { // 숲속 나무 벽
                    ctx.fillStyle = '#1c1917'; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
                    ctx.strokeStyle = '#451a03'; ctx.lineWidth = 1.5; ctx.strokeRect(x+1, y+1, TILE_SIZE-2, TILE_SIZE-2);
                } else if (grid[r][c] === 2) { // 버섯
                    ctx.font = '13px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                    ctx.fillText('🍄', x + TILE_SIZE/2, y + TILE_SIZE/2);
                } else if (grid[r][c] === 3) { // 반짝이는 황금버섯
                    ctx.font = '16px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                    let pulse = Math.sin(Date.now() / 150) * 2;
                    ctx.save(); ctx.shadowBlur = 10; ctx.shadowColor = '#fbbf24';
                    ctx.fillText('⭐', x + TILE_SIZE/2, y + TILE_SIZE/2 + pulse); ctx.restore();
                }
            }
        }

        // 2. 주인공: 빨간 모자 (👧)
        ctx.font = '18px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('👧', redHat.x + TILE_SIZE/2, redHat.y + TILE_SIZE/2);

        // 3. 악당: 늑대들 (🐺)
        wolves.forEach(w => {
            ctx.font = '18px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            if (w.scared) {
                ctx.save(); ctx.shadowBlur = 6; ctx.shadowColor = '#3b82f6';
                ctx.fillText('🥶', w.x + TILE_SIZE/2, w.y + TILE_SIZE/2); ctx.restore(); // 겁먹은 상태
            } else {
                ctx.fillText('🐺', w.x + TILE_SIZE/2, w.y + TILE_SIZE/2);
            }
        });

        // 4. 게임 종료 오버레이
        if (gameOver) {
            ctx.fillStyle = 'rgba(0,0,0,0.8)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 36px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2 - 15);
            ctx.fillStyle = '#fff'; ctx.font = '16px sans-serif'; ctx.fillText('늑대에게 잡히고 말았습니다...', canvas.width/2, canvas.height/2 + 25);
        }
        if (gameWin) {
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#34d399'; ctx.font = 'bold 36px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('HAPPY ENDING 👑', canvas.width/2, canvas.height/2 - 15);
            ctx.fillStyle = '#fff'; ctx.font = '16px sans-serif'; ctx.fillText('버섯을 모두 모아 무사히 집으로 돌아갔습니다!', canvas.width/2, canvas.height/2 + 25);
        }
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    resetBtn.addEventListener('click', () => {
        grid = JSON.parse(JSON.stringify(map)); score = 0; lives = 3; gameOver = false; gameWin = false; scaredTimer = 0;
        totalMushrooms = 0; for(let r=0; r<ROWS; r++) for(let c=0; c<COLS; c++) if(grid[r][c]===2 || grid[r][c]===3) totalMushrooms++;
        scoreUI.innerHTML = "🍄 버섯 바구니: 0"; livesUI.innerHTML = "❤️ 목숨: ❤️❤️❤️"; resetPositions(); canvas.focus();
    });

    canvas.focus(); resetPositions(); loop();
</script>
"""
    components.html(pacman_js, height=520)
