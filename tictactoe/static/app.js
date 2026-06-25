const WIN_LINES = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6]
];

let board = Array(9).fill(null);
let currentPlayer = "X";
let gameOver = false;
let locked = false;

const cells = document.querySelectorAll(".cell");
const status = document.getElementById("status");
const resetBtn = document.getElementById("reset-btn");
const modeToggle = document.getElementById("mode-toggle");
const difficultySelect = document.getElementById("difficulty");
const difficultyWrap = document.getElementById("difficulty-wrap");

function getWinnerCells(board, winner) {
  for (const [a, b, c] of WIN_LINES) {
    if (board[a] === winner && board[b] === winner && board[c] === winner) {
      return [a, b, c];
    }
  }
  return [];
}

function render(state) {
  board = state.board;
  currentPlayer = state.next_player;
  gameOver = state.winner !== null;

  const winCells = state.winner && state.winner !== "draw"
    ? getWinnerCells(state.board, state.winner)
    : [];

  cells.forEach((cell, i) => {
    const val = board[i];
    cell.textContent = val === "X" ? "✕" : val === "O" ? "○" : "";
    cell.className = "cell";
    if (val) cell.classList.add("taken", val.toLowerCase());
    if (winCells.includes(i)) cell.classList.add("winner");
  });

  if (state.winner === "X") status.textContent = "✕ wins!";
  else if (state.winner === "O") status.textContent = "○ wins!";
  else if (state.winner === "draw") status.textContent = "It's a draw!";
  else status.textContent = `${state.next_player === "X" ? "✕" : "○"}'s turn`;

  resetBtn.classList.toggle("pulse", gameOver);
  locked = false;
}

async function handleCellClick(index) {
  if (locked || gameOver || board[index] !== null) return;
  locked = true;

  try {
    const resp = await fetch("/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        board,
        cell: index,
        player: currentPlayer,
        mode: modeToggle.value,
        difficulty: difficultySelect.value
      })
    });

    if (!resp.ok) { locked = false; return; }

    const state = await resp.json();

    if (modeToggle.value === "ai" && !state.winner) {
      await new Promise(r => setTimeout(r, 300));
    }

    render(state);
  } catch {
    status.textContent = "Connection error — try again.";
    locked = false;
  }
}

async function handleReset() {
  locked = true;
  gameOver = false;
  const resp = await fetch("/reset", { method: "POST" });
  const state = await resp.json();
  render(state);
}

cells.forEach(cell => {
  cell.addEventListener("click", () => handleCellClick(Number(cell.dataset.index)));
});

resetBtn.addEventListener("click", handleReset);

modeToggle.addEventListener("change", () => {
  difficultyWrap.classList.toggle("hidden", modeToggle.value !== "ai");
  handleReset();
});

difficultySelect.addEventListener("change", handleReset);
