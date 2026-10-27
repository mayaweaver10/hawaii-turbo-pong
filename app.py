# ============================================================
# 🌺 HAWAII TURBO PONG — YOU VS. COMPUTER
# Run with: streamlit run app.py
#
# Python displays the game.
# JavaScript runs the game inside the Streamlit page.
# You control the left paddle; the computer controls the right.
# ============================================================

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hawaii Turbo Pong", page_icon="🌺", layout="wide")

components.html(r"""
<style>
  body { margin: 0; }
  *, *::before, *::after { box-sizing: border-box; }
  #ha-court:focus-visible { outline: 3px solid #ffe18a; outline-offset: 3px; }
</style>
<div id="hawaii-auto-pong"
     style="max-width:850px;margin:auto;padding:14px;
            background:#124e60;color:white;border-radius:16px;
            font-family:Arial,sans-serif;">

  <!-- Game title -->
  <div style="display:flex;justify-content:space-between;
              align-items:center;flex-wrap:wrap;gap:10px;">
    <div>
      <div style="font-size:25px;font-weight:900;color:#ffe18a">
        🌺 HAWAII TURBO PONG
      </div>
      <div style="font-size:13px;color:#b9f4e9">
        YOU VS. COMPUTER
      </div>
    </div>

    <!-- Live scores -->
    <div style="background:#0b3948;padding:10px;border-radius:8px">
      🌴 You: <b id="ha-left-score">0</b>
      &nbsp;|&nbsp;
      🤖 Computer: <b id="ha-right-score">0</b>
    </div>

    <!-- Start a match, or restart once it is underway. -->
    <button id="ha-restart"
      style="padding:10px 14px;border:0;border-radius:8px;
             background:#ffbd59;color:#533018;font-weight:bold;
             cursor:pointer">
      ▶ Start game
    </button>
  </div>

  <!-- Canvas is the playing field -->
  <canvas id="ha-court" width="820" height="470"
    tabindex="0" aria-label="Pong court. Control the left paddle with W and S or the up and down arrow keys."
    aria-describedby="ha-instructions"
    style="width:100%;height:auto;display:block;margin-top:12px;
           border:3px solid #e6bb75;border-radius:12px;
           touch-action:none;cursor:ns-resize">
  </canvas>

  <p id="ha-instructions" style="font-size:14px;color:#e0fff5">
    You control the left paddle. Move your mouse over the court or drag your
    finger on it. For keyboard controls, click the court and use W/S or ↑/↓.
  </p>

  <!-- Game status and controls -->
  <div style="display:flex;align-items:center;gap:10px;
              flex-wrap:wrap;margin-top:10px;">
    <label for="ha-speed" style="font-size:14px">
      ⚡ Ball speed:
    </label>
    <select id="ha-speed"
      style="padding:7px;border-radius:6px;border:0">
      <option value="12">Fast</option>
      <option value="20" selected>Turbo</option>
      <option value="28">Insane</option>
      <option value="36">Ludicrous</option>
    </select>

    <label for="ha-skill" style="font-size:14px">
      🤖 Computer skill:
    </label>
    <select id="ha-skill"
      style="padding:7px;border-radius:6px;border:0">
      <option value="4">Relaxed</option>
      <option value="7" selected>Competitive</option>
      <option value="12">Expert</option>
    </select>
  </div>

  <p id="ha-status" style="font-size:14px;color:#e0fff5">
    🌴 Ready? Select Start game to play against the computer.
  </p>
</div>

<script>
(() => {
  // Find the game container.
  const root = document.getElementById("hawaii-auto-pong");

  // Prevent duplicate animation loops if the component is rerun.
  if (!root || root.dataset.started) return;
  root.dataset.started = "yes";

  // Get the canvas and drawing tools.
  const canvas = root.querySelector("#ha-court");
  const ctx = canvas.getContext("2d");

  // Store the playing field's internal dimensions.
  const W = canvas.width;
  const H = canvas.height;

  // Find the score labels, controls, and status message.
  const leftScoreText = root.querySelector("#ha-left-score");
  const rightScoreText = root.querySelector("#ha-right-score");
  const restartButton = root.querySelector("#ha-restart");
  const speedSelect = root.querySelector("#ha-speed");
  const skillSelect = root.querySelector("#ha-skill");
  const status = root.querySelector("#ha-status");

  // Set the dimensions of the paddles and ball.
  const PW = 15;
  const PH = 88;
  const BR = 8;

  // Create your paddle on the left.
  const left = {
    x: 28,
    y: H / 2 - PH / 2,
    score: 0
  };

  // Create the right computer-controlled paddle.
  const right = {
    x: W - 28 - PW,
    y: H / 2 - PH / 2,
    score: 0
  };

  // Create the ball in the middle of the court.
  const ball = {
    x: W / 2,
    y: H / 2,
    vx: 12,
    vy: 5
  };

  // Track animation timing and game state.
  let lastTime = 0;
  let playing = false;
  let serveTimer = null;
  const pressedKeys = new Set();
  const movementKeys = new Set(["w", "s", "arrowup", "arrowdown"]);

  // Handle keys only while the court has focus, leaving menus usable.
  canvas.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    if (!movementKeys.has(key)) return;
    event.preventDefault();
    pressedKeys.add(key);
  });
  window.addEventListener("keyup", (event) => {
    pressedKeys.delete(event.key.toLowerCase());
  });
  canvas.addEventListener("blur", () => pressedKeys.clear());
  window.addEventListener("blur", () => pressedKeys.clear());
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pressedKeys.clear();
  });

  // Convert mouse/touch coordinates to the canvas's internal playing field.
  function movePointer(event) {
    const rect = canvas.getBoundingClientRect();
    left.y = (event.clientY - rect.top - canvas.clientTop) * H /
      canvas.clientHeight - PH / 2;
    clamp(left);
  }
  canvas.addEventListener("pointerdown", (event) => {
    if (!event.isPrimary || event.button !== 0) return;
    event.preventDefault();
    pressedKeys.clear();
    canvas.focus({preventScroll: true});
    canvas.setPointerCapture(event.pointerId);
    movePointer(event);
  });
  canvas.addEventListener("pointermove", (event) => {
    if (!event.isPrimary) return;
    if (event.pointerType === "mouse" || canvas.hasPointerCapture(event.pointerId)) {
      movePointer(event);
    }
  });

  // Read the selected starting speed.
  function selectedSpeed() {
    return Number(speedSelect.value);
  }

  // Read the selected computer movement speed.
  function selectedSkill() {
    return Number(skillSelect.value);
  }

  // Keep a paddle between the top and bottom edges.
  function clamp(paddle) {
    paddle.y = Math.max(0, Math.min(H - PH, paddle.y));
  }

  function movePlayer(dt) {
    const up = pressedKeys.has("w") || pressedKeys.has("arrowup");
    const down = pressedKeys.has("s") || pressedKeys.has("arrowdown");
    left.y += (Number(down) - Number(up)) * 14 * dt;
    clamp(left);
  }

  // Start a new point after a brief pause.
  function serve(direction) {
    // Center the ball.
    ball.x = W / 2;
    ball.y = H / 2;

    // Set the horizontal speed in the chosen direction.
    ball.vx = direction * selectedSpeed();

    // Give the ball a random vertical direction.
    ball.vy = (Math.random() * 2 - 1) * selectedSpeed() * 0.45;

    // Pause the ball briefly so the score can be seen.
    playing = false;

    // Clear any previous restart timer.
    if (serveTimer !== null) clearTimeout(serveTimer);

    // Resume the rally after 600 milliseconds.
    serveTimer = setTimeout(() => {
      playing = true;
      serveTimer = null;
    }, 600);
  }

  // Draw a tropical sunset, ocean, and distant island.
  function drawBeach() {
    // Paint the sunset sky with a gradient.
    const sky = ctx.createLinearGradient(0, 0, 0, H * 0.6);
    sky.addColorStop(0, "#f78c72");
    sky.addColorStop(0.5, "#ffc36b");
    sky.addColorStop(1, "#f9df9b");
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // Draw the sun.
    ctx.fillStyle = "#fff1a5";
    ctx.beginPath();
    ctx.arc(W / 2, H * 0.29, 38, 0, Math.PI * 2);
    ctx.fill();

    // Draw a dark volcanic island silhouette.
    ctx.fillStyle = "#436b60";
    ctx.beginPath();
    ctx.moveTo(0, H * 0.39);
    ctx.lineTo(100, H * 0.32);
    ctx.lineTo(190, H * 0.36);
    ctx.lineTo(290, H * 0.25);
    ctx.lineTo(390, H * 0.37);
    ctx.lineTo(510, H * 0.29);
    ctx.lineTo(620, H * 0.36);
    ctx.lineTo(720, H * 0.30);
    ctx.lineTo(W, H * 0.36);
    ctx.lineTo(W, H * 0.46);
    ctx.lineTo(0, H * 0.46);
    ctx.closePath();
    ctx.fill();

    // Draw the turquoise ocean.
    const ocean = ctx.createLinearGradient(0, H * 0.4, 0, H);
    ocean.addColorStop(0, "#168a9b");
    ocean.addColorStop(0.55, "#12b7b5");
    ocean.addColorStop(1, "#f5ce91");
    ctx.fillStyle = ocean;
    ctx.fillRect(0, H * 0.4, W, H * 0.6);

    // Draw decorative wave marks across the ocean.
    for (let i = 0; i < 30; i++) {
      const x = (i * 137 + 20) % W;
      const y = H * 0.44 + ((i * 47) % 230);

      ctx.strokeStyle = i % 2 ? "#b8fff0" : "#fff2cc";
      ctx.globalAlpha = 0.4;
      ctx.lineWidth = 2;

      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.quadraticCurveTo(x + 12, y - 4, x + 24, y);
      ctx.stroke();
    }

    // Restore normal opacity for the remaining drawings.
    ctx.globalAlpha = 1;

    // Draw the sandy beach at the bottom.
    ctx.fillStyle = "#f6d6a1";
    ctx.fillRect(0, H - 12, W, 12);

    // Draw the center line of the Pong court.
    ctx.strokeStyle = "#fff8df";
    ctx.lineWidth = 3;
    ctx.setLineDash([9, 12]);
    ctx.beginPath();
    ctx.moveTo(W / 2, 12);
    ctx.lineTo(W / 2, H - 12);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw a simple palm tree.
    function palm(x, y, size) {
      // Draw the trunk.
      ctx.strokeStyle = "#70452c";
      ctx.lineWidth = 6 * size;
      ctx.beginPath();
      ctx.moveTo(x, y + 55 * size);
      ctx.quadraticCurveTo(x - 5 * size, y + 25 * size,
                           x + 4 * size, y);
      ctx.stroke();

      // Draw seven green palm leaves.
      for (let i = 0; i < 7; i++) {
        const angle = (i / 6) * Math.PI - Math.PI * 0.92;
        ctx.strokeStyle = i % 2 ? "#328451" : "#56a85e";
        ctx.lineWidth = 5 * size;

        ctx.beginPath();
        ctx.moveTo(x + 4 * size, y);
        ctx.quadraticCurveTo(
          x + Math.cos(angle) * 27 * size,
          y + Math.sin(angle) * 23 * size - 5 * size,
          x + Math.cos(angle) * 49 * size,
          y + Math.sin(angle) * 40 * size
        );
        ctx.stroke();
      }
    }

    // Put palm trees in the top corners.
    palm(25, 32, 0.8);
    palm(W - 25, 32, 0.8);
  }

  // Draw the complete court, both paddles, and the ball.
  function draw() {
    drawBeach();

    // Draw your surfboard paddle.
    ctx.fillStyle = "#078ca0";
    ctx.beginPath();
    ctx.roundRect(left.x, left.y, PW, PH, 8);
    ctx.fill();
    ctx.strokeStyle = "#fff1c9";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Add a small flower to the left paddle.
    ctx.fillStyle = "#fff1c9";
    ctx.beginPath();
    ctx.arc(left.x + PW / 2, left.y + PH / 2, 5,
            0, Math.PI * 2);
    ctx.fill();

    // Draw the right computer's coral surfboard paddle.
    ctx.fillStyle = "#e96855";
    ctx.beginPath();
    ctx.roundRect(right.x, right.y, PW, PH, 8);
    ctx.fill();
    ctx.strokeStyle = "#fff1c9";
    ctx.stroke();

    // Add a small flower to the right paddle.
    ctx.fillStyle = "#ffe3a2";
    ctx.beginPath();
    ctx.arc(right.x + PW / 2, right.y + PH / 2, 5,
            0, Math.PI * 2);
    ctx.fill();

    // Draw a glowing golden ball.
    ctx.shadowColor = "#fff4a0";
    ctx.shadowBlur = 16;
    ctx.fillStyle = "#fff7b2";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, BR, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Label the human and computer players.
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 13px Arial";
    ctx.textAlign = "center";
    ctx.fillText("YOU", 75, 22);
    ctx.fillText("COMPUTER", W - 75, 22);
  }

  // Make a computer paddle follow the ball automatically.
  function moveAI(paddle, dt) {
    // Aim slightly ahead of the ball when it is approaching this paddle.
    // This simple prediction helps the computers return fast shots.
    let targetY = ball.y;

    // Add a small amount of imperfect aim to make rallies more varied.
    targetY += Math.sin(Date.now() / 250 + paddle.x) * 10;

    // Calculate the paddle's center and distance from its target.
    const center = paddle.y + PH / 2;
    const difference = targetY - center;

    // Use the selected AI skill as the paddle's maximum movement speed.
    const maxMove = selectedSkill() * dt;

    // Move toward the target, without exceeding the speed limit.
    paddle.y += Math.max(-maxMove, Math.min(maxMove, difference));

    // Keep the paddle inside the playing area.
    clamp(paddle);
  }

  // Check whether the ball overlaps a paddle and bounce it away.
  function collide(paddle, direction) {
    // Check the ball's horizontal and vertical overlap with the paddle.
    const overlaps =
      ball.x + BR >= paddle.x &&
      ball.x - BR <= paddle.x + PW &&
      ball.y + BR >= paddle.y &&
      ball.y - BR <= paddle.y + PH;

    // Only bounce if the ball is traveling toward this paddle.
    const movingTowardPaddle =
      direction === 1 ? ball.vx < 0 : ball.vx > 0;

    if (!overlaps || !movingTowardPaddle) return;

    // Put the ball just outside the paddle to avoid repeated collisions.
    if (direction === 1) {
      ball.x = paddle.x + PW + BR;
    } else {
      ball.x = paddle.x - BR;
    }

    // Calculate how far from the paddle's center the ball hit.
    const hit = (ball.y - (paddle.y + PH / 2)) / (PH / 2);

    // Increase the horizontal speed by 8%, but cap it to avoid
    // the ball becoming impossible to track.
    const speed = Math.min(40, Math.abs(ball.vx) * 1.08);

    // Reverse the horizontal direction.
    ball.vx = direction === 1 ? speed : -speed;

    // Send the ball up or down based on the impact position.
    ball.vy = hit * Math.min(18, selectedSpeed() * 0.65);
  }

  // Update ball motion, paddle motion, wall bounces, and scoring.
  function update(dt) {
    // You can position your paddle even before starting or between points.
    movePlayer(dt);

    // Freeze gameplay during the pause between points.
    if (!playing) return;

    // Only the right paddle follows the ball automatically.
    moveAI(right, dt);

    // Move the ball using its horizontal and vertical velocity.
    ball.x += ball.vx * dt;
    ball.y += ball.vy * dt;

    // Bounce off the top wall.
    if (ball.y - BR <= 0 && ball.vy < 0) {
      ball.y = BR;
      ball.vy = Math.abs(ball.vy);
    }

    // Bounce off the bottom wall.
    if (ball.y + BR >= H && ball.vy > 0) {
      ball.y = H - BR;
      ball.vy = -Math.abs(ball.vy);
    }

    // Check for collisions with both paddles.
    collide(left, 1);
    collide(right, -1);

    // If the ball escapes the left edge, the right player scores.
    if (ball.x + BR < 0) {
      right.score++;
      rightScoreText.textContent = right.score;
      status.textContent = "🤖 The computer scores! Get ready for the next serve.";
      serve(1);
    }

    // If the ball escapes the right edge, the left player scores.
    if (ball.x - BR > W) {
      left.score++;
      leftScoreText.textContent = left.score;
      status.textContent = "🌺 You score! Keep it up!";
      serve(-1);
    }
  }

  // Reset the score, paddles, ball, and serve timer.
  function restart() {
    // Cancel a pending serve if Restart is clicked during a pause.
    if (serveTimer !== null) {
      clearTimeout(serveTimer);
      serveTimer = null;
    }

    // Reset both scores.
    left.score = 0;
    right.score = 0;
    leftScoreText.textContent = "0";
    rightScoreText.textContent = "0";

    // Put both paddles in the center.
    pressedKeys.clear();
    left.y = H / 2 - PH / 2;
    right.y = H / 2 - PH / 2;

    // Put the ball in the middle and choose a random direction.
    ball.x = W / 2;
    ball.y = H / 2;
    ball.vx = (Math.random() < 0.5 ? -1 : 1) * selectedSpeed();
    ball.vy = (Math.random() * 2 - 1) * selectedSpeed() * 0.45;

    // Resume play and display a message.
    playing = true;
    restartButton.textContent = "🔄 Restart";
    status.textContent = "🌴 New match! You are on the left. Good luck!";
    canvas.focus({preventScroll: true});
  }

  // Connect the Restart button to the restart function.
  restartButton.addEventListener("click", restart);

  // Update the starting ball speed when the speed menu changes.
  speedSelect.addEventListener("change", () => {
    // Keep the current direction while changing horizontal speed.
    ball.vx = Math.sign(ball.vx || 1) * selectedSpeed();

    // Scale vertical speed to suit the newly selected speed.
    ball.vy = Math.sign(ball.vy || 1) * selectedSpeed() * 0.35;

    status.textContent = "⚡ Ball speed changed!";
  });

  // Start a fresh animation frame repeatedly.
  function frame(now) {
    // Calculate elapsed time so motion is consistent across displays.
    // The cap limits large jumps if the browser pauses briefly.
    const dt = lastTime
      ? Math.min(1.5, (now - lastTime) / 16.67)
      : 1;

    // Remember the current time.
    lastTime = now;

    // Update positions and collisions.
    update(dt);

    // Redraw the entire tropical court.
    draw();

    // Ask the browser to draw the next frame.
    requestAnimationFrame(frame);
  }

  // Draw the court; the ball waits until Start game is selected.
  draw();
  requestAnimationFrame(frame);

})();
</script>
""", height=760, scrolling=True)
