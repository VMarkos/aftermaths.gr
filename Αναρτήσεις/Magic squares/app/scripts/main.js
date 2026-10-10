const N = 4;
let gameBoard, magicNumber = 34;
let movingNum;

const init = {
    gameSquare: () => {
        const gs = document.getElementById("game-square");
        let cell;
        for (let i = 0; i < N * N; i++) {
            cell = document.createElement("div");
            cell.id = "game-square-" + i;
            cell.classList.add("square-cell", "game", "empty");
            gs.append(cell);
        }
        gameBoard = new MagicSquare(N, magicNumber);
    },
    numSquare: () => {
        const gs = document.getElementById("number-square");
        let cell, row, col;
        for (let i = 0; i < N * N; i++) {
            row = Math.floor(i / N) + 1;
            col = i % N + 1;
            cell = document.createElement("div");
            cell.id = "num-square-" + i;
            cell.classList.add("square-cell", "number");
            cell.innerText = i + 1;
            cell.style.gridArea = [row, col, row, col].join("/");
            cell.addEventListener("mousedown", listeners.grabNum, false);
            cell.addEventListener("mouseup", listeners.dropNum, false);
            gs.append(cell);
        }
    },
    sums: () => {
        let rowSum, colSum, dSum, rowEl, colEl, dEl;
        for (let i = 0; i < N; i++) {
            rowSum = document.createElement("div");
            rowSum.classList.add("square-cell", "sum");
            rowSum.id = "row-sum-" + i;
            rowSum.style.left = "70px";
            rowSum.innerText = "0";
            rowEl = document.getElementById("game-square-" + (i * N + N - 1));
            rowEl.append(rowSum);
            colSum = document.createElement("div");
            colSum.classList.add("square-cell", "sum");
            colSum.id = "col-sum-" + i;
            colSum.style.top = "70px";
            colSum.innerText = "0";
            colEl = document.getElementById("game-square-" + (N * (N - 1) + i));
            colEl.append(colSum);
        }
        dSum = document.createElement("div");
        dSum.classList.add("square-cell", "sum");
        dSum.id = "diag-sum-1";
        dSum.style.top = "70px";
        dSum.style.left = "70px";
        dSum.innerText = "0";
        dEl = document.getElementById("game-square-" + (N * N - 1));
        dEl.append(dSum);
        dSum = document.createElement("div");
        dSum.classList.add("square-cell", "sum");
        dSum.id = "diag-sum--1";
        dSum.style.top = "70px";
        dSum.style.left = "-70px";
        dSum.innerText = "0";
        dEl = document.getElementById("game-square-" + (N * (N - 1)));
        dEl.append(dSum);
    },
};

const utils = {
    updateSum: (type, i) => {
        const sum = document.getElementById(type + "-sum-" + i);
        let sumValue;
        if (type === "row") {
            sumValue = gameBoard.sumOfRow(i);
        } else if (type === "col") {
            sumValue = gameBoard.sumOfCol(i);
        } else if (type === "diag") {
            sumValue = gameBoard.sumOfDiag(i);
        }
        if (sumValue === gameBoard.magicNumber) {
            if (!sum.classList.contains("valid")) {
                sum.classList.add("valid");
            }
            if (sum.classList.contains("invalid")) {
                sum.classList.remove("invalid");
            }
        } else if (sumValue > gameBoard.magicNumber) {
            if (!sum.classList.contains("invalid")) {
                sum.classList.add("invalid");
            }
            if (sum.classList.contains("valid")) {
                sum.classList.remove("valid");
            }
        } else {
            if (sum.classList.contains("valid")) {
                sum.classList.remove("valid");
            }
            if (sum.classList.contains("invalid")) {
                sum.classList.remove("invalid");
            }
        }
        sum.innerText = sumValue;
    },
    updateSums: (i, val, remove = false) => {
        const row = Math.floor(i / N);
        const col = i % N;
        gameBoard.setValue(row, col, remove ? 0 : val);
        utils.updateSum("row", row);
        utils.updateSum("col", col);
        if (row === col) {
            utils.updateSum("diag", 1);
        } else if (row + col === N - 1) {
            utils.updateSum("diag", -1);
        }
        if (gameBoard.isSolved()) {
            console.log("Solved"); // TODO Continue from here, adding a modal and a reset option etc.
        }
    }
}

const listeners = {
    grabNum: (event) => {
        movingNum = event.target;
        document.body.addEventListener("mousemove", listeners.moveNum, false);
        movingNum.style.position = "absolute";
        movingNum.style.top = event.clientY - 25 + "px";
        movingNum.style.left = event.clientX - 25 + "px";
    },
    moveNum: (event) => {
        movingNum.style.top = event.clientY - 25 + "px";
        movingNum.style.left = event.clientX - 25 + "px";
    },
    dropNum: (event) => {
        const numTop = event.clientY;
        const numLeft = event.clientX;
        const over = document.elementsFromPoint(numLeft, numTop)[1];
        movingNum.style.removeProperty("top");
        movingNum.style.removeProperty("left");
        movingNum.style.position = "static";
        if (over.classList.contains("game")) {
            over.classList.remove("empty");
            over.append(movingNum);
            movingNum.removeEventListener("mousedown", listeners.grabNum, false);
            movingNum.classList.remove("number");
            movingNum.removeEventListener("mouseup", listeners.dropNum, false);
            setTimeout(() => {
                movingNum.addEventListener("click", listeners.sendBack, false);
                movingNum = undefined;
            }, 0);
            const i = parseInt(over.id.substring(12));
            const val = parseInt(movingNum.id.substring(11)) + 1;
            utils.updateSums(i, val);
        }
        document.body.removeEventListener("mousemove", listeners.moveNum, false);
    },
    sendBack: (event) => {
        const num = event.target;
        const numRect = num.getBoundingClientRect();
        const numParent = num.parentElement;
        num.removeEventListener("click", listeners.sendBack, false);
        numParent.classList.add("empty");
        num.classList.add("number");
        const nums = document.getElementById("number-square");
        nums.append(num);
        const parRect = num.getBoundingClientRect();
        numParent.append(num);
        const dx = parRect.left - numRect.left + "px";
        const dy = parRect.top - numRect.top + "px";
        num.style.setProperty("--dx", dx);
        num.style.setProperty("--dy", dy);
        num.addEventListener("animationend", () => {
            nums.append(num);
            num.removeEventListener("animationend", this.callee, false);
            num.addEventListener("mousedown", listeners.grabNum, false);
            num.addEventListener("mouseup", listeners.dropNum, false);
            num.classList.remove("move");
            const val = parseInt(num.id.substring(11)) + 1;
            utils.updateSums(parseInt(numParent.id.substring(12)), val, true);
        }, false);
        num.classList.add("move");
    },
}

function initialize() {
    magicNumber = parseInt(document.getElementById("magic-number").value);
    init.gameSquare();
    init.numSquare();
    init.sums();
}

window.addEventListener("load", initialize, false);